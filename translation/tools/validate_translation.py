#!/usr/bin/env python3
"""Compare protected LaTeX structure and report translation QA.

Uses only the Python standard library.  Structural mismatches are errors;
English residue and layout-warning deltas are review warnings.  Explicitly
declared target-only supplements are validated independently without weakening
the source/translation comparison for paired files.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

MATH_ENVS = (
    "equation", "equation*", "align", "align*", "aligned", "gather",
    "gather*", "multline", "multline*", "split", "cases", "matrix",
    "pmatrix", "bmatrix", "vmatrix", "array", "eqnarray", "eqnarray*",
)
COUNT_ENVS = (
    "theorem", "definition", "lemma", "proposition", "corollary", "proof",
    "remark", "example", "consequence", "figure", "figure*", "table",
    "table*", "algorithm", "algorithm*", "equation", "equation*", "align",
    "align*", "itemize", "enumerate",
)
VERBATIM_ENVS = ("verbatim", "Verbatim", "lstlisting", "minted", "alltt", "filecontents", "filecontents*")
INACTIVE_PROSE_ENVS = ("comment",)


def read_text(path: Path) -> str:
    # TeX source is UTF-8.  TeX Live logs on Windows may additionally contain
    # bytes in the active console code page, so tolerate only those diagnostic
    # decoding defects; all structural comparisons still operate on UTF-8 source.
    return path.read_text(encoding="utf-8", errors="replace").replace("\r\n", "\n").replace("\r", "\n")


def strip_comments(text: str) -> str:
    out = []
    for line in text.splitlines(keepends=True):
        cut = len(line)
        for i, ch in enumerate(line):
            if ch == "%":
                backslashes = 0
                j = i - 1
                while j >= 0 and line[j] == "\\":
                    backslashes += 1
                    j -= 1
                if backslashes % 2 == 0:
                    cut = i
                    break
        body = line[:cut]
        if line.endswith("\n") and not body.endswith("\n"):
            body += "\n"
        out.append(body)
    return "".join(out)


def blank_verbatim(text: str) -> str:
    for env in VERBATIM_ENVS:
        pat = re.compile(r"\\begin\{" + re.escape(env) + r"\}.*?\\end\{" + re.escape(env) + r"\}", re.S)
        text = pat.sub(lambda m: "\n" * m.group(0).count("\n"), text)
    return text


def is_escaped(text: str, pos: int) -> bool:
    n = 0
    pos -= 1
    while pos >= 0 and text[pos] == "\\":
        n += 1
        pos -= 1
    return n % 2 == 1


def math_regions(text: str):
    """Return ordered (kind, inner, start, end) active math regions."""
    text = blank_verbatim(strip_comments(text))
    env_alt = "|".join(re.escape(e) for e in sorted(MATH_ENVS, key=len, reverse=True))
    opener = re.compile(r"\\begin\{(" + env_alt + r")\}|\\\(|\\\[|\$\$|\$")
    regions = []
    pos = 0
    while True:
        match = opener.search(text, pos)
        if not match:
            break
        start = match.start()
        token = match.group(0)
        if token.startswith("$") and is_escaped(text, start):
            pos = match.end()
            continue
        if token.startswith("\\begin"):
            env = match.group(1)
            close = "\\end{" + env + "}"
            end_at = text.find(close, match.end())
            if end_at < 0:
                regions.append(("unclosed:" + env, text[match.end():], start, len(text)))
                break
            end = end_at + len(close)
            regions.append((env, text[match.end():end_at], start, end))
        elif token == "\\(":
            end_at = text.find("\\)", match.end())
            if end_at < 0:
                regions.append(("unclosed:inline-paren", text[match.end():], start, len(text)))
                break
            end = end_at + 2
            regions.append(("inline-paren", text[match.end():end_at], start, end))
        elif token == "\\[":
            end_at = text.find("\\]", match.end())
            if end_at < 0:
                regions.append(("unclosed:display-bracket", text[match.end():], start, len(text)))
                break
            end = end_at + 2
            regions.append(("display-bracket", text[match.end():end_at], start, end))
        else:
            delim = token
            search = match.end()
            end_at = -1
            while True:
                end_at = text.find(delim, search)
                if end_at < 0 or not is_escaped(text, end_at):
                    break
                search = end_at + len(delim)
            if end_at < 0:
                regions.append(("unclosed:dollar", text[match.end():], start, len(text)))
                break
            end = end_at + len(delim)
            regions.append(("display-dollar" if delim == "$$" else "inline-dollar", text[match.end():end_at], start, end))
        pos = end
    return text, regions


def math_signature(text: str):
    _, regions = math_regions(text)
    return [
        {
            "kind": kind,
            "sha256": hashlib.sha256(inner.encode("utf-8")).hexdigest(),
            "content": inner,
        }
        for kind, inner, _, _ in regions
    ]


def combined_math_hash(signature):
    payload = json.dumps(
        [(item["kind"], item["content"]) for item in signature],
        ensure_ascii=False,
        separators=(",", ":"),
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def command_counter(text: str, command: str) -> Counter:
    active = strip_comments(text)
    pattern = re.compile(r"\\" + command + r"\s*(?:\[[^\]]*\]\s*){0,2}\{([^{}]*)\}")
    return Counter(m.group(1).strip() for m in pattern.finditer(active))


def citation_counter(text: str) -> Counter:
    active = strip_comments(text)
    pattern = re.compile(r"\\cite[a-zA-Z]*\s*(?:\[[^\]]*\]\s*){0,2}\{([^{}]*)\}")
    keys = []
    for match in pattern.finditer(active):
        keys.extend(k.strip() for k in match.group(1).split(",") if k.strip())
    return Counter(keys)


def protected_signature(text: str):
    commands = (
        "label", "ref", "eqref", "pageref", "autoref", "cref", "Cref",
        "figref", "Figref", "secref", "Secref", "Eqref", "plaineqref",
        "input", "include", "includegraphics", "bibliography", "addbibresource",
        "lstinputlisting", "inputminted", "url",
    )
    result = {name: command_counter(text, name) for name in commands}
    result["citations"] = citation_counter(text)
    active = strip_comments(text)
    result["href_url"] = Counter(re.findall(r"\\href\s*\{([^{}]*)\}\s*\{", active))
    return result


def structure_signature(text: str):
    active = blank_verbatim(strip_comments(text))
    tokens = [(m.group(1), m.group(2), m.start()) for m in re.finditer(r"\\(begin|end)\{([^{}]+)\}", active)]
    stack = []
    problems = []
    counts = Counter()
    for kind, env, pos in tokens:
        if kind == "begin":
            stack.append((env, pos))
            counts[env] += 1
        elif not stack or stack[-1][0] != env:
            problems.append(f"unexpected end {env} at offset {pos}")
        else:
            stack.pop()
    problems.extend(f"unclosed begin {env} at offset {pos}" for env, pos in stack)
    depth = 0
    min_depth = 0
    for i, ch in enumerate(active):
        if ch in "{}" and not is_escaped(active, i):
            depth += 1 if ch == "{" else -1
            min_depth = min(min_depth, depth)
    if depth or min_depth < 0:
        problems.append(f"brace balance depth={depth}, minimum={min_depth}")
    return {"sequence": [(k, e) for k, e, _ in tokens], "counts": counts, "problems": problems}


def mask_protected_prose(text: str) -> str:
    active, regions = math_regions(text)
    chars = list(active)
    for _, _, start, end in regions:
        for i in range(start, min(end, len(chars))):
            if chars[i] != "\n":
                chars[i] = " "
    masked = "".join(chars)
    # LaTeX's comment environment is inactive source, not untranslated prose.
    # Keep it in structural/math comparisons, but suppress it for residue and
    # terminology scans so dormant drafts do not become false positives.
    for env in INACTIVE_PROSE_ENVS:
        pat = re.compile(r"\\begin\{" + re.escape(env) + r"\}.*?\\end\{" + re.escape(env) + r"\}", re.S)
        masked = pat.sub(lambda m: "\n" * m.group(0).count("\n"), masked)
    masked = re.sub(r"\\(?:documentclass|usepackage|RequirePackage)\s*(?:\[[^\]]*\]\s*)?\{[^{}]*\}", " ", masked)
    masked = re.sub(r"\\(?:cite[a-zA-Z]*|label|ref|eqref|pageref|autoref|cref|Cref|figref|Figref|secref|Secref|Eqref|plaineqref|input|include|includegraphics|bibliography|addbibresource|url)\s*(?:\[[^\]]*\]\s*){0,2}\{[^{}]*\}", " ", masked)
    masked = re.sub(r"\\(?:verb|lstinline)(.)(.*?)\1", " ", masked)
    # Environment names and optional layout keys are LaTeX structure, not
    # untranslated prose (for example, tcolorbox's colback/colframe options).
    masked = re.sub(r"\\(?:begin|end)\{[^{}]+\}(?:\[[^\]]*\])?", " ", masked)
    masked = re.sub(r"\\[A-Za-z@]+\*?", " ", masked)
    masked = re.sub(r"[{}\[\]~_^&]", " ", masked)
    return masked


def english_residue(text: str, keep: set[str]):
    masked = mask_protected_prose(text)
    # Remove complete protected names before tokenising so multi-word names
    # such as "Tensor Field Networks" are not misreported word by word.
    for term in sorted(keep, key=len, reverse=True):
        if len(term) >= 3:
            masked = re.sub(r"(?<![A-Za-z])" + re.escape(term) + r"(?![A-Za-z])", " ", masked, flags=re.I)
    findings = []
    for lineno, line in enumerate(masked.splitlines(), 1):
        words = re.findall(r"[A-Za-z][A-Za-z-]{2,}", line)
        review = [w for w in words if w not in keep and w.upper() not in keep]
        if len(review) >= 3:
            findings.append({"line": lineno, "words": review[:12], "text": " ".join(line.split())[:200]})
    return findings


def log_summary(text: str):
    patterns = {
        "fatal": r"Fatal error|Emergency stop",
        "undefined_references": r"Reference .* undefined|There were undefined references",
        "undefined_citations": r"Citation .* undefined|There were undefined citations",
        "missing_files": r"File .* not found",
        "fancyhdr": r"Package fancyhdr Warning:",
        "overfull_hbox": r"Overfull \\hbox",
        "underfull_hbox": r"Underfull \\hbox",
        "overfull_vbox": r"Overfull \\vbox",
        "underfull_vbox": r"Underfull \\vbox",
        "latex_warnings": r"LaTeX Warning:",
        "font_warnings": r"LaTeX Font Warning:",
        "fontspec_warnings": r"Package fontspec Warning:",
        "missing_characters": r"Missing character:",
    }
    return {name: len(re.findall(pattern, text)) for name, pattern in patterns.items()}


def compare_counter(name, source, target, errors):
    if source != target:
        errors.append({"check": name, "source_only": dict(source - target), "target_only": dict(target - source)})


def normalized_tex_resource(value: str) -> str:
    normalized = value.strip().replace("\\", "/")
    return normalized[:-4] if normalized.lower().endswith(".tex") else normalized


def load_keep(path: Path) -> set[str]:
    return {line.strip() for line in read_text(path).splitlines() if line.strip() and not line.startswith("#")}


def term_checks(source_text: str, target_text: str, glossary: Path, keep_original: set[str] | None = None):
    src_prose = mask_protected_prose(source_text).lower()
    tgt_prose = mask_protected_prose(target_text)
    with glossary.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    approved_targets = [row["target_term"].strip() for row in rows if row["target_term"].strip()]
    # Proper model, dataset, software, and project names may legitimately
    # contain a glossary source term (for example, "Graph Isomorphism
    # Network"). Mask complete keep-original entries before checking for
    # untranslated glossary terms so those names do not create false alarms.
    for term in sorted(keep_original or set(), key=len, reverse=True):
        if len(term) < 3:
            continue
        # Single-name entries such as Riemann or Fourier may be part of an
        # approved target term (for example, "Riemann 度量") and must remain
        # visible there.  Other single-token proper names can be masked safely.
        if " " not in term and any(re.search(r"(?<![A-Za-z])" + re.escape(term) + r"(?![A-Za-z])", target, re.I) for target in approved_targets):
            continue
        pattern = r"(?<![A-Za-z])" + re.escape(term) + r"(?![A-Za-z])"
        src_prose = re.sub(pattern, " ", src_prose, flags=re.I)
        tgt_prose = re.sub(pattern, " ", tgt_prose, flags=re.I)
    warnings = []
    # Check compound terms before their components ("geodesic distance"
    # before "geodesic"), then consume matched spans.  This avoids demanding
    # the standalone translation for a word that occurs only as part of an
    # already-approved compound term.
    for row in sorted(rows, key=lambda item: len(item["source_term"].strip()), reverse=True):
        source = row["source_term"].strip()
        target = row["target_term"].strip()
        keep = row["keep_original"].strip().lower() == "true"
        plural = r"s?" if source and not source.lower().endswith("s") else ""
        source_pattern = r"(?<![A-Za-z])" + re.escape(source) + plural + r"(?![A-Za-z])"
        if not source or not re.search(source_pattern, src_prose, re.I):
            continue
        if not keep and target and target not in tgt_prose:
            warnings.append(f"术语缺少目标译名：{source} -> {target}")
        if not keep and re.search(source_pattern, tgt_prose, re.I):
            warnings.append(f"术语仍残留英文：{source}")
        src_prose = re.sub(source_pattern, " ", src_prose, flags=re.I)
        if target:
            tgt_prose = tgt_prose.replace(target, " ")
    return warnings


def main() -> int:
    parser = argparse.ArgumentParser()
    repo = Path(__file__).resolve().parents[2]
    parser.add_argument("--source-root", type=Path, default=repo)
    parser.add_argument("--target-root", type=Path, default=repo / "zh-cn")
    parser.add_argument("--files", nargs="+", default=["main.tex", "math_commands.tex", "introduction.tex", "geometricpriors.tex", "geometricdomains.tex", "geometricmodels.tex", "geometricapplications.tex", "historic.tex", "geometricstability.tex"])
    parser.add_argument(
        "--target-only-files",
        nargs="*",
        default=[],
        help="Chinese supplements with no English counterpart; their input entries are allowed only on the target side",
    )
    parser.add_argument("--sample", default="geometricmodels.tex")
    parser.add_argument("--baseline-log", type=Path, default=repo / "translation" / "baseline-build" / "main.log")
    parser.add_argument("--target-log", type=Path, default=repo / "zh-cn" / "build" / "main.log")
    parser.add_argument("--glossary", type=Path, default=repo / "translation" / "glossary.csv")
    parser.add_argument("--keep-original", type=Path, default=repo / "translation" / "keep-original.txt")
    parser.add_argument("--json-out", type=Path)
    parser.add_argument("--quiet", action="store_true", help="write JSON without printing the full report")
    args = parser.parse_args()

    errors = []
    warnings = []
    files_report = {}
    keep = load_keep(args.keep_original)
    allowed_target_inputs = {normalized_tex_resource(rel) for rel in args.target_only_files}
    for rel in args.files:
        src_path = args.source_root / rel
        tgt_path = args.target_root / rel
        if not src_path.exists() or not tgt_path.exists():
            errors.append({"check": "file_exists", "file": rel, "source": src_path.exists(), "target": tgt_path.exists()})
            continue
        source = read_text(src_path)
        target = read_text(tgt_path)
        src_math = math_signature(source)
        tgt_math = math_signature(target)
        math_equal = src_math == tgt_math
        if not math_equal:
            mismatch = next((i for i, pair in enumerate(zip(src_math, tgt_math)) if pair[0] != pair[1]), min(len(src_math), len(tgt_math)))
            errors.append({"check": "math", "file": rel, "source_count": len(src_math), "target_count": len(tgt_math), "first_mismatch": mismatch})

        src_protected = protected_signature(source)
        tgt_protected = protected_signature(target)
        for key in src_protected:
            target_counter = tgt_protected[key]
            if key == "input" and allowed_target_inputs:
                target_counter = Counter(
                    {
                        value: count
                        for value, count in target_counter.items()
                        if normalized_tex_resource(value) not in allowed_target_inputs
                    }
                )
            compare_counter(f"{rel}:{key}", src_protected[key], target_counter, errors)

        src_struct = structure_signature(source)
        tgt_struct = structure_signature(target)
        if src_struct["problems"]:
            warnings.append({"file": rel, "source_structure_problems": src_struct["problems"]})
        if tgt_struct["problems"]:
            errors.append({"check": "target_structure", "file": rel, "problems": tgt_struct["problems"]})
        if src_struct["sequence"] != tgt_struct["sequence"]:
            errors.append({"check": "environment_sequence", "file": rel})
        for env in COUNT_ENVS:
            if src_struct["counts"][env] != tgt_struct["counts"][env]:
                errors.append({"check": "environment_count", "file": rel, "environment": env, "source": src_struct["counts"][env], "target": tgt_struct["counts"][env]})

        files_report[rel] = {
            "math_regions": len(src_math),
            "math_kinds": dict(Counter(m["kind"] for m in src_math)),
            "math_equal": math_equal,
            "source_math_sha256": combined_math_hash(src_math),
            "target_math_sha256": combined_math_hash(tgt_math),
            "labels": sum(src_protected["label"].values()),
            "refs": sum(sum(src_protected[k].values()) for k in ("ref", "eqref", "pageref", "autoref", "cref", "Cref", "figref", "Figref", "secref", "Secref", "Eqref", "plaineqref")),
            "citations": sum(src_protected["citations"].values()),
            "environments": {env: src_struct["counts"][env] for env in COUNT_ENVS if src_struct["counts"][env]},
        }

    for rel in args.target_only_files:
        tgt_path = args.target_root / rel
        if not tgt_path.exists():
            errors.append({"check": "target_only_file_exists", "file": rel, "target": False})
            continue
        target = read_text(tgt_path)
        tgt_math = math_signature(target)
        tgt_protected = protected_signature(target)
        tgt_struct = structure_signature(target)
        if tgt_struct["problems"]:
            errors.append({"check": "target_only_structure", "file": rel, "problems": tgt_struct["problems"]})
        residue = english_residue(target, keep)
        if residue:
            warnings.append({"file": rel, "english_residue": residue})
        files_report[rel] = {
            "target_only": True,
            "math_regions": len(tgt_math),
            "math_kinds": dict(Counter(m["kind"] for m in tgt_math)),
            "target_math_sha256": combined_math_hash(tgt_math),
            "labels": sum(tgt_protected["label"].values()),
            "refs": sum(sum(tgt_protected[k].values()) for k in ("ref", "eqref", "pageref", "autoref", "cref", "Cref", "figref", "Figref", "secref", "Secref", "Eqref", "plaineqref")),
            "citations": sum(tgt_protected["citations"].values()),
            "inputs": dict(tgt_protected["input"]),
            "environments": {env: tgt_struct["counts"][env] for env in COUNT_ENVS if tgt_struct["counts"][env]},
        }

    sample_source = read_text(args.source_root / args.sample)
    sample_target = read_text(args.target_root / args.sample)
    residue = english_residue(sample_target, keep)
    if residue:
        warnings.append({"english_residue": residue})
    warnings.extend(term_checks(sample_source, sample_target, args.glossary, keep))

    logs = {}
    if args.baseline_log.exists():
        logs["baseline"] = log_summary(read_text(args.baseline_log))
    else:
        warnings.append(f"缺少英文基线日志：{args.baseline_log}")
    if args.target_log.exists():
        logs["target"] = log_summary(read_text(args.target_log))
        if logs["target"]["fatal"] or logs["target"]["undefined_references"] or logs["target"]["undefined_citations"] or logs["target"]["missing_files"]:
            errors.append({"check": "target_build_log", "summary": logs["target"]})
        if "baseline" in logs:
            logs["delta"] = {key: logs["target"][key] - logs["baseline"][key] for key in logs["target"]}
    else:
        warnings.append(f"缺少中文构建日志：{args.target_log}")

    report = {"ok": not errors, "errors": errors, "warnings": warnings, "files": files_report, "logs": logs}
    output = json.dumps(report, ensure_ascii=False, indent=2)
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(output + "\n", encoding="utf-8")
    if not args.quiet:
        print(output)
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
