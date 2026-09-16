#!/usr/bin/env python3
"""exams/set-*.md を Artifact ページ用の構造化 JSON (web/exams.js) に変換する。

本文の Markdown 変換は build_content.py の inline() を共用する（参照リンクは
章への遷移になる）。問題文・選択肢・解説を分けて持たせ、ページ側で
「選択肢をタップ → 正誤と解説」を実現できる形にする。
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
import build_content as bc  # noqa: E402
import check_exams as ce  # noqa: E402

EXAMS = os.path.join(os.path.dirname(__file__), "..", "exams")
OUT = os.path.join(os.path.dirname(__file__), "..", "web", "exams.js")

TITLE_RE = re.compile(r"^#\s*(問題セット\d+)\s*｜\s*(.+?)\s*$")
KEY_RE = re.compile(r"^\*\*決め手\*\*[：:]\s*(.*)$")
REF_RE = re.compile(r"^\*\*参照\*\*[：:]\s*(.*)$")


def parse_set(path):
    with open(path, encoding="utf-8") as f:
        lines = f.read().split("\n")

    num, title = "", os.path.basename(path)
    for ln in lines:
        m = TITLE_RE.match(ln.strip())
        if m:
            num, title = m.group(1), m.group(2)
            break

    questions = []
    starts = [i for i, ln in enumerate(lines) if ln.startswith("### Q")]
    for n, start in enumerate(starts):
        end = starts[n + 1] if n + 1 < len(starts) else len(lines)
        block = lines[start:end]
        head = ce.Q_RE.match(block[0])
        if not head:
            raise ValueError("%s: Q%d の見出しが不正" % (path, n + 1))

        body, options, reasons = [], [], []
        answer, key, refs = "", "", ""
        in_details = False
        in_reasons = False
        for ln in block[1:]:
            s = ln.strip()
            if s.startswith("<details>"):
                in_details = True
                continue
            if s.startswith("</details>") or s.startswith("<summary>") or s == "---":
                continue

            m = ce.OPT_RE.match(ln)
            if m:
                options.append({"l": m.group(1), "html": bc.inline(m.group(2))})
                continue
            if not in_details:
                if s:
                    body.append(bc.inline(s))
                continue

            m = ce.ANSWER_RE.match(s)
            if m:
                answer = m.group(1)
                continue
            m = KEY_RE.match(s)
            if m:
                key = bc.inline(m.group(1))
                continue
            m = REF_RE.match(s)
            if m:
                refs = bc.inline(m.group(1))
                continue
            if s.startswith("**他の選択肢を外す理由**"):
                in_reasons = True
                continue
            m = ce.REASON_RE.match(ln)
            if m and in_reasons:
                reasons.append({"l": m.group(1), "html": bc.inline(m.group(2))})
                continue
            if s and in_reasons and not s.startswith("- "):
                in_reasons = False

        questions.append({
            "n": int(head.group(1)),
            "topic": head.group(2),
            "level": len(head.group(3)),
            "body": body,
            "options": options,
            "answer": answer,
            "key": key,
            "reasons": reasons,
            "refs": refs,
        })

    return {
        "id": "exam-" + os.path.basename(path)[:-3],   # exam-set-01
        "file": os.path.basename(path),
        "num": num,
        "title": title,
        "questions": questions,
    }


def build():
    sets = []
    for name in sorted(os.listdir(EXAMS)):
        if name.startswith("set-") and name.endswith(".md"):
            sets.append(parse_set(os.path.join(EXAMS, name)))
    return sets


if __name__ == "__main__":
    problems = ce.check_all()
    if problems:
        for path, line, msg in problems:
            print("  %s:%d  %s" % (path, line, msg), file=sys.stderr)
        sys.exit("先に tools/check_exams.py の指摘を直す")

    sets = build()
    for s in sets:
        for q in s["questions"]:
            if not (q["answer"] and q["options"] and q["reasons"] and q["refs"]):
                sys.exit("%s Q%d: 解析結果が欠けている" % (s["file"], q["n"]))
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("window.SAA_EXAMS = ")
        json.dump(sets, f, ensure_ascii=False, separators=(",", ":"))
        f.write(";\n")
    print("wrote", OUT, os.path.getsize(OUT), "bytes,",
          sum(len(s["questions"]) for s in sets), "questions in", len(sets), "sets")
