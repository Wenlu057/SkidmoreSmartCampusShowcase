from __future__ import annotations
import importlib
import pkgutil
from pathlib import Path
import streamlit as st

ROOT = Path(__file__).parent
MOD_ROOT = ROOT / "modules"

st.set_page_config(page_title="S³ Smart Campus Showcase", layout="wide")
st.title("S³ Smart Campus Showcase")
st.caption("Data-structures-first campus projects")

@st.cache_data(show_spinner=False)
def discover_pages():
    pages = []
    for finder, name, ispkg in pkgutil.iter_modules([str(MOD_ROOT)]):
        ui_page = MOD_ROOT / name / "ui" / "page.py"
        if ui_page.exists():
            modname = f"modules.{name}.ui.page"
            try:
                mod = importlib.import_module(modname)
                meta = getattr(mod, "meta", lambda: {"title": name, "description": ""})()
                render = getattr(mod, "render", None)
                if callable(render):
                    pages.append({
                        "key": name,
                        "title": meta.get("title", name),
                        "desc": meta.get("description", ""),
                        "render": render,
                    })
            except Exception as e:
                pages.append({
                    "key": name,
                    "title": f"{name} (import error)",
                    "desc": str(e),
                    "render": lambda: st.error(f"Failed to load {modname}: {e}")
                })
    pages.sort(key=lambda p: p["title"].lower())
    return pages

pages = discover_pages()
if pages:
    labels = [p["title"] for p in pages]
    choice = st.sidebar.radio("Modules", options=list(range(len(pages))), format_func=lambda i: labels[i])
    sel = pages[choice]
    st.subheader(sel["title"])
    if sel["desc"]:
        st.write(sel["desc"])
    sel["render"]()
else:
    st.info("No modules found yet. Add one under modules/<name>/ui/page.py")
