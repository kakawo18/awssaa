#!/usr/bin/env python3
"""docs/*.md を Artifact ページ用の構造化 JSON (web/content.js) に変換する。"""
import json, os, re, html

DOCS = os.path.join(os.path.dirname(__file__), "..", "docs")
OUT = os.path.join(os.path.dirname(__file__), "..", "web", "content.js")
# 図は web/figures/<id>.svg が原本（currentColor で描き、ページのテーマ色を継承する）。
# GitHub の Markdown ビューア用には、白い下地と固定色を与えた複製を docs/figures/ に書き出す。
FIG_SRC = os.path.join(os.path.dirname(__file__), "..", "web", "figures")
FIG_OUT = os.path.join(DOCS, "figures")
FIG_RE = re.compile(r"^!\[([^\]]*)\]\(\./figures/([A-Za-z0-9_-]+)\.svg\)$")

# (ファイル名, 章ID, 章グループ)。グループは目次とホームの見出しになる。
# 章IDは Web の読了状態（localStorage）のキーなので、既存の ID は変えない。
FILES = [
    ("00-foundations.md", "foundations", "第0章 設計の基礎"),
    ("01-compute.md", "compute", "第1部 サービス別"), ("02-storage.md", "storage", "第1部 サービス別"),
    ("03-network.md", "network", "第1部 サービス別"), ("04-database.md", "database", "第1部 サービス別"),
    ("05-security.md", "security", "第1部 サービス別"), ("06-integration.md", "integration", "第1部 サービス別"),
    ("07-analytics.md", "analytics", "第1部 サービス別"), ("08-management.md", "management", "第1部 サービス別"),
    ("09-container.md", "container", "第1部 サービス別"), ("10-others.md", "others", "第1部 サービス別"),
    ("11-secure.md", "d1", "第2部 分野別"), ("12-resilient.md", "d2", "第2部 分野別"),
    ("13-performance.md", "d3", "第2部 分野別"), ("14-cost.md", "d4", "第2部 分野別"),
    ("90-comparison.md", "cmp", "付録"), ("91-keywords.md", "kw", "付録"),
]
CHAPTER_ID = {fname: cid for fname, cid, _ in FILES}
CHAPTER_ID["README.md"] = "home"

def link(label, url):
    """Markdown リンクを安全な a 要素にする。

    - https:// だけを外部リンクとして保持する。http:, javascript:, data: などは
      無効化してラベルだけ残す
    - ./03-network.md のような教材内リンクは章IDへの遷移（data-go）にする
    - それ以外（#anchor だけ、未知のファイル）はラベルだけ残す
    label は呼び出し側で既にエスケープ済み。url はここで属性用にエスケープする。
    """
    # inline() で quote=False のエスケープ済み（& が &amp;）なので、一度戻してから属性用に再エスケープする
    url = html.unescape(url.strip())
    if re.match(r"^https://[^\s]+$", url, re.I):
        return '<a href="%s" target="_blank" rel="noopener noreferrer">%s</a>' % (
            html.escape(url, quote=True), label)
    m = re.match(r"^(?:\./)?([0-9A-Za-z_-]+\.md)(?:#.*)?$", url)
    if m and m.group(1) in CHAPTER_ID:
        cid = CHAPTER_ID[m.group(1)]
        return '<a href="#%s" data-go="%s">%s</a>' % (cid, cid, label)
    return label

def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", lambda m: link(m.group(1), m.group(2)), s)
    return s

def figure_svg(fig_id):
    """図の原本を読む。呼び出し側で content.js にそのまま埋め込む。"""
    with open(os.path.join(FIG_SRC, fig_id + ".svg"), encoding="utf-8") as f:
        return f.read().strip()

def write_standalone_figure(fig_id, svg):
    """GitHub 表示用に、白い下地と固定の文字色を与えた SVG を docs/figures/ へ書き出す。

    currentColor のままだと GitHub のダークテーマで黒い線が沈むため、
    ルート要素に color を与え、どのテーマでも読める白い下地を最初に敷く。
    """
    os.makedirs(FIG_OUT, exist_ok=True)
    m = re.match(r"^<svg[^>]*>", svg)
    if not m:
        raise ValueError("figure %s: <svg> 要素が見つからない" % fig_id)
    head = m.group(0)
    if " color=" not in head:
        head = head[:-1] + ' color="#1B212E">'
    body = head + '\n  <rect width="100%" height="100%" rx="10" fill="#FFFFFF"/>' + svg[m.end():]
    path = os.path.join(FIG_OUT, fig_id + ".svg")
    old = open(path, encoding="utf-8").read() if os.path.exists(path) else None
    if old != body:
        with open(path, "w", encoding="utf-8") as f:
            f.write(body)

def split_row(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]

def parse(path):
    lines = open(path, encoding="utf-8").read().split("\n")
    ch = {"title": "", "num": "", "lead": "", "sections": []}
    cur = None
    i, n = 0, len(lines)
    buf = []

    def flush():
        nonlocal buf
        if buf and cur is not None:
            text = "".join(buf)
            kind = "p"
            m = re.match(r"^\*\*(一言で|章の一言|この章の使い方)\*\*[：:]\s*(.*)$", text)
            if m:
                cur["blocks"].append({"t": "lede", "label": m.group(1), "html": inline(m.group(2))})
                buf = []
                return
            cur["blocks"].append({"t": kind, "html": inline(text)})
        buf = []

    while i < n:
        line = lines[i].rstrip()
        s = line.strip()
        if s.startswith("# "):
            flush()
            t = s[2:].strip()
            ch["title"] = t
            m = re.match(r"^(第\d+章|付録[A-Z])\s*(.*)$", t)
            if m:
                ch["num"], ch["title"] = m.group(1), m.group(2)
            i += 1
            continue
        if s.startswith("> "):
            flush()
            para = []
            while i < n and lines[i].strip().startswith("> "):
                para.append(lines[i].strip()[2:])
                i += 1
            text = "".join(para)
            text = re.sub(r"^\*\*(章の一言|この章の使い方)\*\*[：:]\s*", "", text)
            if cur is None:
                ch["lead"] = inline(text)
            else:
                cur["blocks"].append({"t": "note", "html": inline(text)})
            continue
        if s.startswith("## "):
            flush()
            title = s[3:].strip()
            m = re.match(r"^([\d.]+(?:〜[\d.]+)?)\s+(.*)$", title)
            num, name = (m.group(1), m.group(2)) if m else ("", title)
            cur = {"id": "s%d" % len(ch["sections"]), "num": num, "title": name, "blocks": []}
            ch["sections"].append(cur)
            i += 1
            continue
        if s.startswith("### "):
            flush()
            if cur is not None:
                cur["blocks"].append({"t": "h3", "html": inline(s[4:].strip())})
            i += 1
            continue
        m = FIG_RE.match(s)
        if m and cur is not None:
            flush()
            alt, fig_id = m.group(1), m.group(2)
            svg = figure_svg(fig_id)
            write_standalone_figure(fig_id, svg)
            i += 1
            caption = ""
            j = i
            while j < n and lines[j].strip() == "":
                j += 1
            if j < n and lines[j].strip().startswith("**図：**"):
                caption = inline(lines[j].strip()[len("**図：**"):].strip())
                i = j + 1
            cur["blocks"].append({"t": "figure", "id": fig_id, "alt": alt, "svg": svg, "caption": caption})
            continue
        if s.startswith("|"):
            flush()
            head = split_row(lines[i]); i += 1
            if i < n and set(lines[i].strip().replace("|", "").replace(":", "").strip()) <= {"-", " "}:
                i += 1
            rows = []
            while i < n and lines[i].strip().startswith("|"):
                rows.append([inline(c) for c in split_row(lines[i])]); i += 1
            if cur is not None:
                cur["blocks"].append({"t": "table", "head": [inline(h) for h in head], "rows": rows})
            continue
        if re.match(r"^[-*] ", s):
            flush()
            items = []
            while i < n and re.match(r"^[-*] ", lines[i].strip()):
                items.append(inline(lines[i].strip()[2:])); i += 1
            if cur is not None:
                cur["blocks"].append({"t": "ul", "items": items})
            continue
        if re.match(r"^\d+\. ", s):
            flush()
            items = []
            while i < n and re.match(r"^\d+\. ", lines[i].strip()):
                items.append(inline(re.sub(r"^\d+\.\s*", "", lines[i].strip()))); i += 1
            if cur is not None:
                cur["blocks"].append({"t": "ol", "items": items})
            continue
        if s.startswith("---") or s == "":
            flush(); i += 1; continue
        if s.startswith("[目次に戻る]"):
            flush(); i += 1; continue
        buf.append(s); i += 1
    flush()
    return ch

def build():
    out = []
    for fname, cid, group in FILES:
        ch = parse(os.path.join(DOCS, fname))
        ch["id"] = cid
        ch["group"] = group
        out.append(ch)
    return out

if __name__ == "__main__":
    out = build()
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("window.SAA_CONTENT = ")
        json.dump(out, f, ensure_ascii=False, separators=(",", ":"))
        f.write(";\n")
    print("wrote", OUT, os.path.getsize(OUT), "bytes,", sum(len(c["sections"]) for c in out), "sections")
