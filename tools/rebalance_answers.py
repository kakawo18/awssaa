#!/usr/bin/env python3
"""正解記号の偏りをならす。

作問時に正解をAに置く癖がつくと、記号を見るだけで当てられる問題集になる。
選択肢の中身を入れ替えて、正解が A〜D（複数選択は A〜E の組）へ均等に散るようにする。
入れ替えに合わせて「正解」行と「他の選択肢を外す理由」の記号・並びも書き換える。

  python3 tools/rebalance_answers.py --dry-run          # 変更後の分布だけ表示
  python3 tools/rebalance_answers.py                    # すべて書き換える
  python3 tools/rebalance_answers.py --only set-10.md   # 追加したセットだけ直す

既に解き終えたセットを無用に入れ替えないよう、--only で対象を絞れる。

決定的に動く（同じ入力なら同じ結果）。解説の地の文が選択肢記号を参照していると
意味がずれるため、参照は事前に取り除いておくこと。
"""
import argparse
import collections
import os
import random
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
import check_exams as ce  # noqa: E402

EXAMS = os.path.join(os.path.dirname(__file__), "..", "exams")
SEED = 20260917
MULTI_TARGETS = [("A", "C"), ("B", "D"), ("C", "E"), ("A", "D"),
                 ("B", "E"), ("A", "E"), ("C", "D"), ("B", "C")]


def parse_question(lines, start, end):
    """1問分の行範囲から、選択肢・正解・外す理由の位置と内容を取り出す。"""
    opts, reasons = [], []
    answer_at = reasons_at = None
    for i in range(start, end):
        ln = lines[i]
        m = ce.OPT_RE.match(ln)
        if m:
            opts.append((i, m.group(1), m.group(2)))
            continue
        if ce.ANSWER_RE.match(ln.strip()):
            answer_at = i
            continue
        if ln.startswith("**他の選択肢を外す理由**"):
            reasons_at = i
            continue
        m = ce.REASON_RE.match(ln)
        if m and reasons_at is not None:
            reasons.append((i, m.group(1), m.group(2)))
    return opts, answer_at, reasons


def rebalance_file(path, rng, stats):
    with open(path, encoding="utf-8") as f:
        lines = f.read().split("\n")
    starts = [i for i, ln in enumerate(lines) if ln.startswith("### Q")]
    bounds = [(s, starts[n + 1] if n + 1 < len(starts) else len(lines))
              for n, s in enumerate(starts)]

    questions = []
    for start, end in bounds:
        opts, answer_at, reasons = parse_question(lines, start, end)
        answer = ce.ANSWER_RE.match(lines[answer_at].strip()).group(1).split("・")
        questions.append((start, end, opts, answer_at, answer, reasons))

    # このファイルの単一選択に割り当てる正解記号を、均等かつ3連続しないように決める
    singles = [q for q in questions if len(q[4]) == 1]
    targets = []
    if singles:
        pool = [("ABCD")[i % 4] for i in range(len(singles))]
        for _ in range(200):
            rng.shuffle(pool)
            if all(not (pool[i] == pool[i + 1] == pool[i + 2])
                   for i in range(len(pool) - 2)):
                break
        targets = list(pool)

    for _start, _end, opts, answer_at, answer, reasons in questions:
        contents = [text for _, _, text in opts]          # 現在の並びの中身
        letters = [letter for _, letter, _ in opts]
        reason_by_letter = {letter: text for _, letter, text in reasons}
        cur_idx = [letters.index(a) for a in answer]

        if len(answer) == 1:
            want = targets.pop(0)
            tgt_idx = [letters.index(want)]
        else:
            pair = MULTI_TARGETS[stats["multi_seen"] % len(MULTI_TARGETS)]
            stats["multi_seen"] += 1
            tgt_idx = [letters.index(p) for p in pair]

        # 正解の中身を目的の位置へ入れ替える（他は元の並びを保つ）
        order = list(range(len(contents)))
        for src, dst in zip(cur_idx, tgt_idx):
            i, j = order.index(src), order.index(dst)
            order[i], order[j] = order[j], order[i]

        new_contents = [contents[k] for k in order]
        new_answer = sorted(letters[pos] for pos, k in enumerate(order) if k in cur_idx)

        # 選択肢行を書き直す
        for pos, (line_no, _old_letter, _t) in enumerate(opts):
            lines[line_no] = "- **%s.** %s" % (letters[pos], new_contents[pos])

        lines[answer_at] = "**正解：%s**" % "・".join(new_answer)

        # 外す理由を、新しい記号順に並べ替える
        if reasons:
            wrong_positions = [pos for pos, k in enumerate(order) if k not in cur_idx]
            rewritten = []
            for pos in wrong_positions:
                old_letter = letters[order[pos]]
                rewritten.append("- **%s**：%s" % (letters[pos], reason_by_letter[old_letter]))
            for line_no, new_line in zip([i for i, _, _ in reasons], rewritten):
                lines[line_no] = new_line

        stats["dist"][tuple(new_answer)] += 1

    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--only", nargs="*", metavar="FILE",
                    help="対象のファイル名（省略時は exams/set-*.md すべて）")
    args = ap.parse_args()

    rng = random.Random(SEED)
    stats = {"dist": collections.Counter(), "multi_seen": 0}
    for name in sorted(os.listdir(EXAMS)):
        if not (name.startswith("set-") and name.endswith(".md")):
            continue
        if args.only and name not in args.only:
            continue
        path = os.path.join(EXAMS, name)
        out = rebalance_file(path, rng, stats)
        if not args.dry_run:
            with open(path, "w", encoding="utf-8") as f:
                f.write(out)

    single = collections.Counter()
    multi = collections.Counter()
    for key, n in stats["dist"].items():
        (single if len(key) == 1 else multi)["・".join(key)] += n
    total = sum(single.values())
    label = "対象ファイルの" if args.only else ""
    print("%s単一選択 %d問の正解分布%s" % (label, total, "（変更後の見込み）" if args.dry_run else ""))
    for letter in "ABCD":
        print("  %s: %2d問 (%4.1f%%)" % (letter, single[letter], 100 * single[letter] / total))
    print("複数選択:", dict(multi))


if __name__ == "__main__":
    main()
