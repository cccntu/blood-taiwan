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
commits = list(repo.iter_commits())

# %%
from rich import inspect

inspect(commits[0].stats)
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
# adf.to_csv("data.csv")
x = df.set_index(df.columns[0])
# %%
df["region"].unique(), df["value"].unique(), df["type"].unique()
# %%
adf["num"] = adf["value"].map({"庫存量4到7日": 5, "庫存量7日以上": 7, "庫存量4日以下": 4})
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

df = adf.query('region == "台北" and type == "A型"').reset_index(drop=True)
# %%
df["next"] = df["num"].shift(1).astype(int)
df["prev"] = df["num"].shift(-1).astype(int)
df["keep"] = df.apply(
    lambda x: x["next"] != x["value"] or x["prev"] != x["value"], axis=1
)
# %%
df[df["keep"] == True].plot(x="time", y="num")
# %%
def get_realval(x):
    if (x["num"], x["next"]) == (5, 7):
        return 6
    if (x["num"], x["prev"]) == (5, 7):
        return 6
    return x["num"]


df["newnum"] = df.apply(get_realval, axis=1)
# %%
df[df["keep"] == True].plot(x="time", y="newnum", kind="scatter")
# %%
def get_realval_df(df):
    df["next"] = df["num"].shift(-1).fillna(0).astype(int)
    df["prev"] = df["num"].shift(1).fillna(0).astype(int)
    df["keep"] = df.apply(
        lambda x: x["next"] != x["num"] or x["prev"] != x["num"], axis=1
    )
    df["newnum"] = df.apply(get_realval, axis=1)
    df = df[df["keep"] == True].reset_index(drop=True)
    return df


# %%
adf2 = adf.groupby(["region", "type"]).apply(get_realval_df)
# %%
df2 = adf2.query('region == "台北" and type == "A型"').reset_index(drop=True)
df2.plot(x="time", y="newnum", kind="scatter")
df2.plot(x="time", y="newnum")
df2

# %%
adf
# %%
adf2["num"] = adf2["newnum"]
adf2[["type", "region", "value", "time", "num"]].reset_index(drop=True)
# %%
adf2.to_csv("aggdata.csv", index=False)
# %%
