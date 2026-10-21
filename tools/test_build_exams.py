#!/usr/bin/env python3
"""build_exams.py の設問文の解析の回帰テスト。

実行: python3 tools/test_build_exams.py
"""
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(__file__))
import build_exams as be  # noqa: E402
from test_check_exams import GOOD  # noqa: E402

POLICY = """設問文。

```json
{
  "Effect": "Deny",
  "Resource": "arn:aws:s3:::a<b>/*"
}
```

この設定内容として正しいものを選択してください。"""


class StemCodeBlockTest(unittest.TestCase):
    def parse(self, text):
        with tempfile.NamedTemporaryFile("w", suffix=".md", encoding="utf-8", delete=False) as f:
            f.write(text)
            path = f.name
        try:
            return be.parse_set(path)["questions"][0]
        finally:
            os.unlink(path)

    def test_fenced_block_becomes_one_pre_with_indent(self):
        q = self.parse(GOOD.replace("設問文。", POLICY))
        self.assertEqual(len(q["body"]), 3, q["body"])
        pre = q["body"][1]
        self.assertTrue(pre.startswith('<pre class="qcode"><code>'), pre)
        self.assertIn('\n  "Effect": "Deny",', pre)       # 字下げと改行を保つ
        self.assertIn("a&lt;b&gt;", pre)                    # HTMLとして解釈させない
        self.assertNotIn("```", "".join(q["body"]))

    def test_plain_stem_is_unchanged(self):
        q = self.parse(GOOD)
        self.assertEqual(q["body"], ["設問文。"])


if __name__ == "__main__":
    unittest.main()
