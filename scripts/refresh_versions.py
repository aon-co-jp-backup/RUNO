#!/usr/bin/env python3
"""easy-web.tokyo の紹介ページ(MFastAPI / RMojo / 2FastAPI / 2FastAPI-VSC と各 /demo)を、新版に自動追従させる。

VPS のタイマー(1時間ごと)から実行する。標準ライブラリのみ。やること:
1. 4製品の最新リリース(GitHub)と、上流(Python / Flask / Django / FastAPI / Starlette / Rust / Mojo)の最新版を取得する。
2. 各製品フォルダへ `versions.json` を原子的に書く(変化があれば標準出力に1行ずつ記録)。
3. 各ページ(`index.html` と `demo/index.html`)へ、最新版を表示する小さな表示部を差し込む(目印つきで冪等。ページを
   作り直しても次回の実行で復活する)。ページはダウンロード専用のまま(入力欄・アップロードは作らない)。

使い方: refresh_versions.py <紹介ページのルート(既定 /root/easy-web-intros)> [--dry-run]
API の呼び出し制限に配慮し、環境変数 GITHUB_TOKEN があれば使う。失敗した項目は前回の値を残す。
"""
import datetime
import json
import os
import re
import sys
import urllib.request

PRODUCTS = ["MFastAPI", "RMojo", "2FastAPI", "2FastAPI-VSC", "2Poem", "2MFastAPI"]
ORG = "aon-co-jp"
MARK_BEGIN = "<!-- latest-versions:begin -->"
MARK_END = "<!-- latest-versions:end -->"

SNIPPET = (
    MARK_BEGIN
    + """<section id="latest-versions" class="note" style="margin:1.2em 0;padding:.6em .9em;border:1px solid rgba(128,128,128,.4);border-radius:8px;font-size:.92em">
<b>Latest / 最新版:</b> <span id="lv-self">…</span><br>
<span id="lv-up" style="opacity:.85">…</span></section>
<script>(function(){var p=location.pathname.split('/').filter(Boolean)[0]||'';
fetch('/'+p+'/versions.json',{cache:'no-store'}).then(function(r){return r.json()}).then(function(v){
var s=v.products&&v.products[p]; if(s){document.getElementById('lv-self').textContent=p+' '+s.tag+(s.published?' ('+s.published+')':'');}
var u=v.upstream||{},o=[];['python','flask','django','fastapi','starlette','rust','mojo','poem','node','typescript','react','bootstrap','postgresql','mysql','sqlite'].forEach(function(k){if(u[k])o.push((({python:'Python',flask:'Flask',django:'Django',fastapi:'FastAPI',starlette:'Starlette',rust:'Rust',mojo:'Mojo',poem:'Poem',node:'Node.js',typescript:'TypeScript',react:'React',bootstrap:'Bootstrap',postgresql:'PostgreSQL',mysql:'MySQL',sqlite:'SQLite'})[k])+' '+u[k]);});
document.getElementById('lv-up').textContent=o.join(' · ')+(v.generated?'  — '+v.generated:'');}).catch(function(){var e=document.getElementById('latest-versions');if(e)e.style.display='none';});})();</script>"""
    + MARK_END
)


def get(url, timeout=20):
    headers = {"User-Agent": "easy-web-intros-refresh", "Accept": "application/json"}
    tok = os.environ.get("GITHUB_TOKEN")
    if tok and "api.github.com" in url:
        headers["Authorization"] = "Bearer " + tok
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def safe(fn, *a):
    try:
        return fn(*a)
    except Exception as e:  # noqa: BLE001 - 取得失敗は前回の値を残す
        print("warn: %s%r: %s" % (fn.__name__, a, e), file=sys.stderr)
        return None


def release_of(repo):
    j = get("https://api.github.com/repos/%s/%s/releases/latest" % (ORG, repo))
    return {"tag": j["tag_name"], "published": (j.get("published_at") or "")[:10]}


def pypi(name):
    return get("https://pypi.org/pypi/%s/json" % name)["info"]["version"]


def npm(name):
    return get("https://registry.npmjs.org/%s/latest" % name)["version"]


def crates(name):
    return get("https://crates.io/api/v1/crates/%s" % name)["crate"]["max_stable_version"]


def eol(product):
    return get("https://endoflife.date/api/%s.json" % product)[0]["latest"]


def python_latest():
    j = get("https://endoflife.date/api/python.json")
    return j[0]["latest"]


def rust_latest():
    return get("https://api.github.com/repos/rust-lang/rust/releases/latest")["tag_name"].lstrip("v")


def collect(prev):
    out = {"products": dict(prev.get("products", {})), "upstream": dict(prev.get("upstream", {}))}
    for p in PRODUCTS:
        r = safe(release_of, p)
        if r:
            out["products"][p] = r
    for key, fn, arg in [
        ("python", python_latest, ()),
        ("flask", pypi, ("flask",)),
        ("django", pypi, ("django",)),
        ("fastapi", pypi, ("fastapi",)),
        ("starlette", pypi, ("starlette",)),
        ("rust", rust_latest, ()),
        ("mojo", pypi, ("mojo",)),
        ("poem", crates, ("poem",)),
        ("node", eol, ("nodejs",)),
        ("typescript", npm, ("typescript",)),
        ("react", npm, ("react",)),
        ("bootstrap", npm, ("bootstrap",)),
        ("postgresql", eol, ("postgresql",)),
        ("mysql", eol, ("mysql",)),
        ("sqlite", eol, ("sqlite",)),
    ]:
        v = safe(fn, *arg)
        if v:
            out["upstream"][key] = v
    return out


def changes(old, new):
    ch = []
    for k, v in new["products"].items():
        if old.get("products", {}).get(k, {}).get("tag") != v["tag"]:
            ch.append("product %s: %s -> %s" % (k, old.get("products", {}).get(k, {}).get("tag"), v["tag"]))
    for k, v in new["upstream"].items():
        if old.get("upstream", {}).get(k) != v:
            ch.append("upstream %s: %s -> %s" % (k, old.get("upstream", {}).get(k), v))
    return ch


def inject(path):
    """表示部を差し込む(既にあれば置き換え)。変更したら True。"""
    try:
        with open(path, encoding="utf-8") as f:
            html = f.read()
    except OSError:
        return False
    pat = re.compile(re.escape(MARK_BEGIN) + r".*?" + re.escape(MARK_END), re.S)
    new = pat.sub(lambda m: SNIPPET, html) if pat.search(html) else html.replace("</main>", SNIPPET + "</main>", 1)
    if new == html or "</main>" not in html and not pat.search(html):
        return False
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="") as f:
        f.write(new)
    os.replace(tmp, path)
    return True


def main(argv):
    root = next((a for a in argv if not a.startswith("--")), "/root/easy-web-intros")
    dry = "--dry-run" in argv
    prev_path = os.path.join(root, "MFastAPI", "versions.json")
    try:
        with open(prev_path, encoding="utf-8") as f:
            prev = json.load(f)
    except (OSError, ValueError):
        prev = {}
    cur = collect(prev)
    for c in changes(prev, cur):
        print("change:", c)
    cur["generated"] = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    if dry:
        print(json.dumps(cur, ensure_ascii=False, indent=1))
        return 0
    for p in PRODUCTS:
        d = os.path.join(root, p)
        if not os.path.isdir(d):
            continue
        tmp = os.path.join(d, "versions.json.tmp")
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(cur, f, ensure_ascii=False, indent=1)
        os.replace(tmp, os.path.join(d, "versions.json"))
        for page in (os.path.join(d, "index.html"), os.path.join(d, "demo", "index.html")):
            if inject(page):
                print("injected:", page)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
