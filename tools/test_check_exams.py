#!/usr/bin/env python3
"""check_exams.py が実際に不備を検出できることの回帰テスト。

実行: python3 tools/test_check_exams.py
"""
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(__file__))
import check_exams as ce  # noqa: E402

GOOD = """# 問題セット99 ｜ テスト

### Q1 ｜ トピック ｜ ★★

設問文。

- **A.** 選択肢A
- **B.** 選択肢B
- **C.** 選択肢C
- **D.** 選択肢D

<details>
<summary>解答と解説</summary>

**正解：B**

**決め手**：理由。

**他の選択肢を外す理由**
- **A**：理由A
- **C**：理由C
- **D**：理由D

**参照**：[第1章](../docs/01-compute.md)

</details>
"""


class CheckExamsTest(unittest.TestCase):
    def check(self, text):
        with tempfile.NamedTemporaryFile(
            "w", suffix=".md", encoding="utf-8", delete=False,
            dir=os.path.join(os.path.dirname(__file__), "..", "exams"),
        ) as f:
            f.write(text)
            path = f.name
        try:
            return [msg for _, msg in ce.check_file(path)]
        finally:
            os.unlink(path)

    def test_valid_question_passes(self):
        self.assertEqual(self.check(GOOD), [])

    def test_missing_option_is_reported(self):
        msgs = self.check(GOOD.replace("- **D.** 選択肢D\n", ""))
        self.assertTrue(any("選択肢がAから連続していない" in m for m in msgs), msgs)

    def test_reason_for_correct_answer_is_reported(self):
        # 正解Bの理由を書いてしまい、Cの理由が抜けている状態
        msgs = self.check(GOOD.replace("- **C**：理由C", "- **B**：理由B"))
        self.assertTrue(any("外す理由が正解以外の3つと一致しない" in m for m in msgs), msgs)

    def test_missing_answer_is_reported(self):
        msgs = self.check(GOOD.replace("**正解：B**", "正解はB"))
        self.assertTrue(any("正解" in m for m in msgs), msgs)

    def test_missing_reference_is_reported(self):
        msgs = self.check(GOOD.replace("**参照**：[第1章](../docs/01-compute.md)", "おわり"))
        self.assertTrue(any("参照" in m for m in msgs), msgs)

    def test_broken_link_is_reported(self):
        msgs = self.check(GOOD.replace("01-compute.md", "99-nonexistent.md"))
        self.assertTrue(any("リンク先が存在しない" in m for m in msgs), msgs)

    def test_question_numbering_is_checked(self):
        msgs = self.check(GOOD.replace("### Q1 ｜", "### Q3 ｜"))
        self.assertTrue(any("連番" in m for m in msgs), msgs)

    def test_repository_exam_sets_are_valid(self):
        self.assertEqual(ce.check_all(), [])


MULTI = """# 問題セット98 ｜ テスト

### Q1 ｜ トピック ｜ ★★

設問文。**2つ選択してください。**

- **A.** 選択肢A
- **B.** 選択肢B
- **C.** 選択肢C
- **D.** 選択肢D
- **E.** 選択肢E

<details>
<summary>解答と解説</summary>

**正解：B・E**

**決め手**：理由。

**他の選択肢を外す理由**
- **A**：理由A
- **C**：理由C
- **D**：理由D

**参照**：[第1章](../docs/01-compute.md)

</details>
"""


class MultipleResponseTest(unittest.TestCase):
    check = CheckExamsTest.check

    def test_valid_multiple_response_passes(self):
        self.assertEqual(self.check(MULTI), [])

    def test_four_options_for_multiple_response_is_reported(self):
        msgs = self.check(MULTI.replace("- **E.** 選択肢E\n", "").replace("**正解：B・E**", "**正解：B・D**")
                          .replace("- **D**：理由D\n", ""))
        self.assertTrue(any("複数選択は選択肢を5つ以上" in m for m in msgs), msgs)

    def test_missing_select_two_instruction_is_reported(self):
        msgs = self.check(MULTI.replace("**2つ選択してください。**", ""))
        self.assertTrue(any("2つ選択してください" in m for m in msgs), msgs)

    def test_unknown_answer_letter_is_reported(self):
        msgs = self.check(MULTI.replace("**正解：B・E**", "**正解：B・F**"))
        self.assertTrue(any("正解に存在しない選択肢" in m for m in msgs), msgs)

    def test_reasons_must_cover_every_wrong_option(self):
        msgs = self.check(MULTI.replace("- **D**：理由D\n", ""))
        self.assertTrue(any("外す理由が正解以外" in m for m in msgs), msgs)


if __name__ == "__main__":
    unittest.main()
