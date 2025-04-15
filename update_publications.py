#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 15 19:57:20 2025

@author: jnz
"""

import os
import json
from scholarly import scholarly

author_id = "UF9ZlroAAAAJ"

def sanitize_filename(title):
    return "".join(c if c.isalnum() else "-" for c in title.lower())[:50]

author = scholarly.fill(scholarly.search_author_id(author_id), sections=["publications"])
print(f"抓取作者：{author['name']}，共 {len(author['publications'])} 篇")

output_dir = "content/publication"
os.makedirs(output_dir, exist_ok=True)

for idx, pub in enumerate(author["publications"]):
    try:
        filled = scholarly.fill(pub)
        bib = filled.get("bib", {})
        title = bib.get("title", "Untitled")
        year = bib.get("pub_year", "2023")
        journal = bib.get("venue", "Unknown Journal")
        authors = bib.get("author", "Unknown").split(" and ")
        url = bib.get("url", "")
        
        filename = sanitize_filename(title)
        pub_dir = os.path.join(output_dir, filename)
        os.makedirs(pub_dir, exist_ok=True)

        with open(os.path.join(pub_dir, "index.md"), "w", encoding="utf-8") as f:
            f.write(f"""---
title: "{title}"
authors: {json.dumps(authors)}
date: {year}-01-01
publication_types: ["2"]
publication: "{journal}"
url_pdf: "{url}"
---

自动导入的出版物（Google Scholar 抓取）
""")
        print(f"✅ 生成: {title}")
    except Exception as e:
        print(f"❌ 跳过: {e}")
