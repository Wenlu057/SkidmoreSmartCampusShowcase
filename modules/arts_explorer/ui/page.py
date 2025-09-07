from __future__ import annotations
import streamlit as st
import pandas as pd
from pathlib import Path
from ..ds import sorting, hashmap

DATA = Path(__file__).parents[1] / "data" / "sample_events.csv"

def meta():
    return {
        "title": "Student Arts & Performance Explorer",
        "description": "Search events by tag/date, show top‑k trending tags, and compare sort stability.",
    }

def render():
    st.write("Browse and analyze events using your own data structures.")
    df = pd.read_csv(DATA)
    st.dataframe(df, hide_index=True)

    st.subheader("Search by tag (HashMap)")
    tag = st.text_input("Tag contains", "jazz").strip().lower()

    # Build tag index with HashMap
    tag_index = hashmap.HashMap()
    for i, row in df.iterrows():
        for t in str(row["tags"]).lower().split(" "):
            lst = tag_index.get(t) or []
            lst.append(i)
            tag_index.put(t, lst)

    if tag and (tag in tag_index):
        hits = df.iloc[tag_index.get(tag)]
        st.success(f"Found {len(hits)} events for tag '{tag}'")
        st.dataframe(hits, hide_index=True)
    else:
        st.info("No matches yet. Try a different tag.")

    st.subheader("Top‑k venues (by event count)")
    counts = df.groupby("venue").size().reset_index(name="count").sort_values("count", ascending=False)
    k = st.slider("k", 1, int(min(10, len(counts))), 5)
    st.table(counts.head(k))

    st.subheader("Sorting demo")
    key = st.selectbox("Sort by", ["date", "title", "venue"])
    alg = st.radio("Algorithm", ["selection", "insertion", "merge"], horizontal=True)
    data = df.to_dict("records")
    if alg == "selection":
        out = sorting.selection_sort(data, key=lambda r: r[key])
    elif alg == "insertion":
        out = sorting.insertion_sort(data, key=lambda r: r[key])
    else:
        out = sorting.merge_sort(data, key=lambda r: r[key])
    st.dataframe(pd.DataFrame(out))
