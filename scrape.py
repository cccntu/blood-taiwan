# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.11.4
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass
import dataclasses
import re
import json
import pandas as pd

# +
url = "http://www.blood.org.tw/Internet/main/index.aspx"

html = requests.get(url)

soup = BeautifulSoup(html.text, "lxml")
blood_table = soup.find("div", {"id": "blood-table"})
tables = blood_table.find_all("table")
# -

update_time = tables[0].find("span").text

table = tables[1]
for a in table.find_all("img", alt=True):
    x = a.get("alt", "")
    a.replaceWith(x)
df = pd.read_html(repr(table))[0]
df = df.rename(columns={df.columns[0]: "血型"})
df.to_csv('data.csv', index=False)

with open("README.md", "w") as f:
    f.write("# 台灣血庫爬蟲\n\n")
    f.write(f"{update_time}\n\n")
    f.write(df.to_markdown(index=False))

with open("update_time.txt", "w") as f:
    f.write(update_time)

# cat README.md
