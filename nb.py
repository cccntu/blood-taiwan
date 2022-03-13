# %%
# use gitpython to get all the versions of a file

import argparse
import datetime
import glob
import json
import logging
import os
import re
import shutil
import subprocess
import sys
import time

import git

git.__version__

# %%

# use gitpython to get all the versions of a file

repo = git.Repo(os.getcwd())
for commit in repo.iter_commits():
    print(commit.hexsha)
    print(commit.message)
    print(commit.author)
    print(commit.committed_datetime)
    print("\n")
# %%
print(len(list(repo.iter_commits())))

# %%
commits = list(repo.iter_commits())

# %%
commit = commits[100]

# %%
from rich import inspect

# %%
# %%
inspect(commit)
# %%
inspect(commit.stats)

# %%
inspect(commit.tree.blobs)
# %%
tree = commit.tree
# %%
len(tree)

# %%
inspect(tree.trees[0])
# %%
tree.blobs
# %%
inspect(tree.blobs[1])
# %%
(list(tree.traverse()))

# %%
print(commit.tree.blobs[0].data_stream.read().decode("utf-8"))
# %%
from rich import print

for blob in commit.tree.blobs:
    print(blob.path)
    print(blob.data_stream.read().decode("utf-8"))
# %%

# %%
x.decode("utf-8")

# %%
for blob in commits[102].tree.traverse():
    print(blob.path)
# %%
inspect(commit)

# %%
import pandas as pd

# %%
data = []
for commit in repo.iter_commits():
    if "data.csv" not in commit.stats.files:
        continue
    time = commit.committed_datetime
    for blob in commit.tree.traverse():
        if blob.path == "data.csv":
            df = pd.read_csv(blob.data_stream)
            # print(blob.data_stream.read().decode("utf-8"))
    data.append(
        {
            "time": time,
            "data": df,
        }
    )


# %%
df.to_dict(orient="records")

# %%
inspect(df.to_dict)
# %%
# schema: time, location, type, amount

dfs = []
for dic in data:
    time = dic["time"]
    df = dic["data"]
    df = df.melt(df.columns[0], var_name="col", value_name="val")
    df.columns = ["type", "region", "value"]
    df["time"] = time
    dfs.append(df)

# %%
adf = pd.concat(dfs)
# %%
x = df.set_index(df.columns[0])
# %%
df["region"].unique(), df["value"].unique(), df["type"].unique()
# %%
adf["num"] = adf["value"].map({"庫存量4到7日": 4, "庫存量7日以上": 7, "庫存量4日以下": 2})
# %%
from matplotlib import pyplot as plt

for n, g in adf.groupby(["region", "type"]):
    g.plot(x="time", y="num", kind="scatter")
    plt.legend(n)
# %%
adf.query('region == "台北" and type == "A型"').plot(x="time", y="num", kind="scatter")
# %%
adf.query('region == "台北" and type == "A型"').plot(x="time", y="num", kind="scatter")
# %%
x.to_dict(orient="split")

# %%
x

# %%
df.set_index("血型").stack().reset_index(name="Val").rename(columns={"level_1": "X"})
# %%
x
# %%
