#!/usr/bin/env python3
"""build_site.py が Artifact 用の断片を単体で開けるページにできることの回帰テスト。

実行: python3 tools/test_build_site.py
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(__file__))
import build_site as bs  # noqa: E402


class PageTest(unittest.TestCase):
    FRAGMENT = "<title>T</title>\n<link rel=\"stylesheet\" href=\"x.css\">\n<style>a{}</style>\n\n<header>H</header>\n<script src=\"content.js\"></script>\n"

    def test_fragment_is_wrapped_into_head_and_body(self):
        html = bs.page(self.FRAGMENT)
        self.assertTrue(html.startswith("<!doctype html>"))
        head, body = html.split("</head>")
        self.assertIn("<title>T</title>", head)
        self.assertIn("<style>a{}</style>", head)
        self.assertIn('name="viewport"', head)
        self.assertIn("<header>H</header>", body)
        self.assertIn('<script src="content.js"></script>', body)
        self.assertEqual(html.count("<body>"), 1)

    def test_repository_page_builds_with_all_assets(self):
        html = bs.build()
        self.assertIn('<script src="content.js"></script>', html.split("<body>")[1])
        for name in ("index.html", "content.js", "exams.js", ".nojekyll",
                     "icons/icon.svg", "icons/apple-touch-icon.png"):
            self.assertTrue(os.path.exists(os.path.join(bs.OUT, name)), name)


if __name__ == "__main__":
    unittest.main()
