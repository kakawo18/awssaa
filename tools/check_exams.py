#!/usr/bin/env python3
"""exams/set-*.md の構造を検証する。

問題集は手で書き足していくため、形式のゆらぎ（選択肢の抜け、正解記号の誤り、
参照リンク切れ、外す理由の書き漏れ）を機械的に止める。

実行: python3 tools/check_exams.py
"""
import os
import re
import sys

ROOT = os.path.join(os.path.dirname(__file__), "..")
EXAMS = os.path.join(ROOT, "exams")

Q_RE = re.compile(r"^### Q(\d+)\s*｜\s*(.+?)\s*｜\s*(★{1,3})\s*$")
OPT_RE = re.compile(r"^- \*\*([A-F])\.\*\*\s+(\S.*)$")
# 単一選択は「**正解：B**」、複数選択は「**正解：A・D**」
ANSWER_RE = re.compile(r"^\*\*正解：([A-F](?:・[A-F])*)\*\*\s*$")
REASON_RE = re.compile(r"^- \*\*([A-F])\*\*：\s*(\S.*)$")
LINK_RE = re.compile(r"\]\((\.\./[^)#\s]+)")
LETTERS = ["A", "B", "C", "D", "E", "F"]


def check_file(path):
    """1ファイルを検証し、(行番号, メッセージ) のリストを返す。"""
    errors = []
    with open(path, encoding="utf-8") as f:
        lines = f.read().split("\n")

    def err(i, msg):
        errors.append((i + 1, msg))

    if not lines or not lines[0].startswith("# 問題セット"):
        err(0, "1行目が「# 問題セット」で始まっていない")

    # 問題ごとに切り出す
    starts = [i for i, ln in enumerate(lines) if ln.startswith("### Q")]
    if not starts:
        err(0, "問題（### Q…）が1つもない")
    for n, start in enumerate(starts):
        end = starts[n + 1] if n + 1 < len(starts) else len(lines)
        block = lines[start:end]
        m = Q_RE.match(block[0])
        if not m:
            err(start, "見出しの形式が違う（### Q1 ｜ トピック ｜ ★★ の形にする）")
            continue
        if int(m.group(1)) != n + 1:
            err(start, "問題番号が連番でない（Q%s → Q%d が期待値）" % (m.group(1), n + 1))

        opts = [(i, OPT_RE.match(ln)) for i, ln in enumerate(block) if OPT_RE.match(ln)]
        got = [mm.group(1) for _, mm in opts]
        if len(got) < 4 or got != LETTERS[:len(got)]:
            err(start, "選択肢がAから連続していない、または4つ未満（検出: %s）" % ("".join(got) or "なし"))

        if block.count("<details>") != 1 or block.count("</details>") != 1:
            err(start, "<details> と </details> が1組になっていない")

        answer_lines = [mm.group(1) for ln in block for mm in [ANSWER_RE.match(ln.strip())] if mm]
        if len(answer_lines) != 1:
            err(start, "「**正解：X**」の行が1つでない（検出: %d）" % len(answer_lines))
            continue
        answer = answer_lines[0].split("・")
        if len(set(answer)) != len(answer):
            err(start, "正解の記号が重複している（%s）" % "・".join(answer))
        if any(a not in got for a in answer):
            err(start, "正解に存在しない選択肢が含まれる（正解: %s／選択肢: %s）"
                % ("・".join(answer), "".join(got)))
        if len(answer) > 1 and len(got) < 5:
            err(start, "複数選択は選択肢を5つ以上にする（検出: %d）" % len(got))
        if len(answer) > 1 and ("つ選択" not in "".join(block[:12])):
            err(start, "複数選択の設問文に「2つ選択してください」等の指示がない")

        if not any(ln.startswith("**決め手**") for ln in block):
            err(start, "「**決め手**」の記述がない")

        try:
            r_at = next(i for i, ln in enumerate(block) if ln.startswith("**他の選択肢を外す理由**"))
        except StopIteration:
            err(start, "「**他の選択肢を外す理由**」の節がない")
            r_at = None
        if r_at is not None:
            reasons = []
            for ln in block[r_at + 1:]:
                mm = REASON_RE.match(ln)
                if mm:
                    reasons.append(mm.group(1))
                elif ln.strip() == "":
                    if reasons:
                        break
                    continue
                elif reasons:
                    break
            expected = [c for c in got if c not in answer]
            if reasons != expected:
                err(start + r_at, "外す理由が正解以外の3つと一致しない（期待: %s／検出: %s）"
                    % ("".join(expected), "".join(reasons) or "なし"))

        if not any(ln.startswith("**参照**") for ln in block):
            err(start, "「**参照**」の行がない（根拠の章を必ず示す）")

    # 教材へのリンク切れ
    for i, ln in enumerate(lines):
        for rel in LINK_RE.findall(ln):
            if not os.path.exists(os.path.normpath(os.path.join(os.path.dirname(path), rel))):
                err(i, "リンク先が存在しない: %s" % rel)

    return errors


def check_all():
    """exams/ 配下すべてを検証し、(相対パス, 行, メッセージ) のリストを返す。"""
    out = []
    if not os.path.isdir(EXAMS):
        return [("exams/", 0, "ディレクトリがない")]
    for name in sorted(os.listdir(EXAMS)):
        if not (name.startswith("set-") and name.endswith(".md")):
            continue
        path = os.path.join(EXAMS, name)
        for line, msg in check_file(path):
            out.append((os.path.join("exams", name), line, msg))
    return out


def count_questions():
    """セットごとの問題数を返す（索引の記載と突き合わせる用）。"""
    counts = {}
    for name in sorted(os.listdir(EXAMS)):
        if name.startswith("set-") and name.endswith(".md"):
            with open(os.path.join(EXAMS, name), encoding="utf-8") as f:
                text = f.read()
            counts[name] = len(re.findall(r"^### Q", text, re.M))
    return counts


if __name__ == "__main__":
    problems = check_all()
    counts = count_questions()
    for name, n in counts.items():
        print("%s: %d問" % (name, n))
    if problems:
        print("\n%d件の問題があります:" % len(problems), file=sys.stderr)
        for path, line, msg in problems:
            print("  %s:%d  %s" % (path, line, msg), file=sys.stderr)
        sys.exit(1)
    print("\n合計 %d問 / 形式チェックはすべて通過" % sum(counts.values()))
