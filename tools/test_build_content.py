#!/usr/bin/env python3
"""build_content.py のリンク変換とエスケープの回帰テスト。

実行: python3 tools/test_build_content.py
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(__file__))
import build_content as bc  # noqa: E402


class InlineLinkTest(unittest.TestCase):
    def test_https_link_is_preserved(self):
        out = bc.inline("[SQS](https://docs.aws.amazon.com/sqs/)")
        self.assertEqual(
            out,
            '<a href="https://docs.aws.amazon.com/sqs/" target="_blank" '
            'rel="noopener noreferrer">SQS</a>',
        )

    def test_query_and_quote_in_url_are_escaped(self):
        out = bc.inline('[a](https://e.com/?a=1&b="2")')
        self.assertIn('href="https://e.com/?a=1&amp;b=&quot;2&quot;"', out)
        self.assertNotIn('b="2"', out)

    def test_javascript_scheme_is_dropped(self):
        self.assertEqual(bc.inline("[x](javascript:alert%281%29)"), "x")
        self.assertNotIn("<a", bc.inline("[x](javascript:alert(1))"))
        self.assertNotIn("<a", bc.inline("[x](JAVASCRIPT:void(0))"))

    def test_data_and_http_schemes_are_dropped(self):
        self.assertEqual(bc.inline("[x](data:text/html,hi)"), "x")
        self.assertEqual(bc.inline("[x](http://example.com/)"), "x")

    def test_internal_chapter_link_becomes_data_go(self):
        out = bc.inline("[第3章](./03-network.md)")
        self.assertEqual(out, '<a href="#network" data-go="network">第3章</a>')

    def test_internal_link_with_anchor_and_readme(self):
        self.assertEqual(
            bc.inline("[DB](./04-database.md#41)"),
            '<a href="#database" data-go="database">DB</a>',
        )
        self.assertEqual(
            bc.inline("[目次](./README.md)"),
            '<a href="#home" data-go="home">目次</a>',
        )

    def test_unknown_relative_file_is_dropped(self):
        self.assertEqual(bc.inline("[x](./99-none.md)"), "x")
        self.assertEqual(bc.inline("[x](#anchor-only)"), "x")

    def test_label_html_is_escaped_and_bold_kept(self):
        out = bc.inline("**<b>太字</b>** と [<i>x</i>](https://e.com/)")
        self.assertIn("<b>&lt;b&gt;太字&lt;/b&gt;</b>", out)
        self.assertIn(">&lt;i&gt;x&lt;/i&gt;</a>", out)


class BuildTest(unittest.TestCase):
    def test_all_chapters_have_group_and_unique_id(self):
        out = bc.build()
        ids = [c["id"] for c in out]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertTrue(all(c.get("group") for c in out))
        self.assertEqual(out[0]["id"], "foundations")
        self.assertEqual(out[0]["num"], "第0章")



class FigureTest(unittest.TestCase):
    """図の参照行が figure ブロックになり、GitHub 表示用の複製が書き出されること。"""

    def _parse(self, md):
        import tempfile
        with tempfile.NamedTemporaryFile("w", suffix=".md", encoding="utf-8", delete=False) as f:
            f.write(md)
            path = f.name
        try:
            return bc.parse(path)
        finally:
            os.unlink(path)

    def test_figure_line_becomes_figure_block(self):
        ch = self._parse(
            "# 第3章 テスト\n\n## 3.1 節\n\n"
            "![図：VPCの基本構成](./figures/vpc-overview.svg)\n\n"
            "**図：** 受信は**IGW**経由。\n\n本文が続く。\n"
        )
        blocks = ch["sections"][0]["blocks"]
        fig = blocks[0]
        self.assertEqual(fig["t"], "figure")
        self.assertEqual(fig["id"], "vpc-overview")
        self.assertEqual(fig["alt"], "図：VPCの基本構成")
        self.assertIn("<svg", fig["svg"])
        self.assertEqual(fig["caption"], "受信は<b>IGW</b>経由。")
        # キャプション行は本文として二重に出力されない
        self.assertEqual([b["t"] for b in blocks], ["figure", "p"])
        self.assertEqual(blocks[1]["html"], "本文が続く。")

    def test_standalone_copy_has_plate_and_fixed_color(self):
        self._parse(
            "# 第3章 テスト\n\n## 3.1 節\n\n"
            "![図](./figures/vpc-overview.svg)\n"
        )
        out = os.path.join(bc.FIG_OUT, "vpc-overview.svg")
        self.assertTrue(os.path.exists(out))
        svg = open(out, encoding="utf-8").read()
        self.assertIn('color="#1B212E"', svg)
        self.assertIn('fill="#FFFFFF"', svg)
        self.assertNotIn("<style", svg)


class CalloutAndTableTest(unittest.TestCase):
    """GitHub の注記記法とセル数のずれた表を正しく扱うこと。"""
    _parse = FigureTest._parse

    def test_note_marker_becomes_kind_not_text(self):
        ch = self._parse("# 第1章 テスト\n\n## 1.1 節\n\n> [!WARNING]\n> **注意**：本文。\n")
        note = ch["sections"][0]["blocks"][0]
        self.assertEqual(note["t"], "note")
        self.assertEqual(note["kind"], "warn")
        self.assertNotIn("[!", note["html"])
        self.assertTrue(note["html"].startswith("<b>注意</b>"))

    def test_plain_quote_has_no_kind(self):
        ch = self._parse("# 第1章 テスト\n\n## 1.1 節\n\n> ただの引用。\n")
        self.assertEqual(ch["sections"][0]["blocks"][0]["kind"], "")

    def test_row_with_extra_cell_is_rejected(self):
        with self.assertRaises(ValueError):
            self._parse("# 第1章 テスト\n\n## 1.1 節\n\n| a | b |\n|---|---|\n| 1 | 2 | 3 |\n")

    def test_repository_docs_have_no_callout_markers_left(self):
        for ch in bc.build():
            for s in ch["sections"]:
                for b in s["blocks"]:
                    self.assertNotIn("[!", b.get("html", ""), (ch["id"], s["title"]))


if __name__ == "__main__":
    unittest.main()
