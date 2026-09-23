#!/usr/bin/env python3
"""GitHub Pages 用のサイトを site/ に組み立てる。

web/artifact.html は Artifact 用の断片（<html>・<head>・<body> は claude.ai 側が付ける）なので、
単体のページとして開けるよう外枠を付けて site/index.html に書き出す。
データ（content.js / exams.js）とアイコンはそのままコピーする。

実行: python3 tools/build_site.py   （先に build_content.py / build_exams.py を実行しておく）
"""
import os
import shutil

ROOT = os.path.join(os.path.dirname(__file__), "..")
WEB = os.path.join(ROOT, "web")
OUT = os.path.join(ROOT, "site")

HEAD = """<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="description" content="AWS SAA-C03 の要点集と問題解説集。サービス間の違いを「問題文のキーワード → 答え」で引ける。">
<meta name="color-scheme" content="light dark">
<meta name="theme-color" content="#F5F7FA" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0E1218" media="(prefers-color-scheme: dark)">
<meta name="apple-mobile-web-app-title" content="SAA">
<link rel="icon" type="image/svg+xml" href="icons/icon.svg">
<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">
<style>body{margin:0}</style>
"""


def page(fragment):
    """Artifact 用の断片を、<head> と <body> を持つ完全な HTML にする。

    断片は「<title>・<link>・最初の <style>」がページ設定で、その後ろが本文。
    最初の </style> で分けて、前半を <head>、後半を <body> に入れる。
    """
    cut = fragment.index("</style>") + len("</style>")
    return HEAD + fragment[:cut] + "\n</head>\n<body>\n" + fragment[cut:].lstrip("\n") + "\n</body>\n</html>\n"


def build():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(os.path.join(OUT, "icons"))
    with open(os.path.join(WEB, "artifact.html"), encoding="utf-8") as f:
        html = page(f.read())
    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    for name in ("content.js", "exams.js"):
        shutil.copy(os.path.join(WEB, name), os.path.join(OUT, name))
    for name in ("icon.svg", "apple-touch-icon.png"):
        shutil.copy(os.path.join(WEB, "icons", name), os.path.join(OUT, "icons", name))
    # GitHub Pages の Jekyll 処理を止める（そのまま配信させる）
    open(os.path.join(OUT, ".nojekyll"), "w").close()
    return html


if __name__ == "__main__":
    html = build()
    print("wrote", os.path.normpath(OUT), "(index.html", len(html.encode("utf-8")), "bytes)")
