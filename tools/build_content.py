#!/usr/bin/env python3
"""docs/*.md を Artifact ページ用の構造化 JSON (web/content.js) に変換する。"""
import json, os, re, html

DOCS = os.path.join(os.path.dirname(__file__), "..", "docs")
OUT = os.path.join(os.path.dirname(__file__), "..", "web", "content.js")

FILES = [
    ("01-compute.md", "compute"), ("02-storage.md", "storage"),
    ("03-network.md", "network"), ("04-database.md", "database"),
    ("05-security.md", "security"), ("06-integration.md", "integration"),
    ("07-analytics.md", "analytics"), ("08-management.md", "management"),
    ("09-container.md", "container"), ("10-others.md", "others"),
    ("11-secure.md", "d1"), ("12-resilient.md", "d2"),
    ("13-performance.md", "d3"), ("14-cost.md", "d4"),
    ("90-comparison.md", "cmp"), ("91-keywords.md", "kw"),
]

def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)
    return s

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

out = []
for fname, cid in FILES:
    ch = parse(os.path.join(DOCS, fname))
    ch["id"] = cid
    out.append(ch)

with open(OUT, "w", encoding="utf-8") as f:
    f.write("window.SAA_CONTENT = ")
    json.dump(out, f, ensure_ascii=False, separators=(",", ":"))
    f.write(";\n")
print("wrote", OUT, os.path.getsize(OUT), "bytes,", sum(len(c["sections"]) for c in out), "sections")
