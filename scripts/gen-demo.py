"""各製品の `/demo` ページ(説明・最新版・Windows版 .exe)を生成してVPSへ置く。
使い方: python scripts/gen-demo.py  (gh と ssh conoha が使える環境で)
CLAUDE.md「製品紹介URLの/demoルール」の実装。静的HTML、JSなし、10言語。
"""
import html, json, subprocess, sys, tempfile, os

PRODUCTS = {  # 製品名: VPSの配信ディレクトリ(webpage)
    "360-speaker": "360-speaker", "aruaru-IME": "aruaru-IME", "aruaru-llm": "aruaru-llm", "maid-cafe-se": "maid-cafe-se",
    "open-backup": "open-backup", "open-cosmo": "open-cosmo", "open-cpu": "open-cpu", "open-cuda": "open-cuda",
    "open-easy-web": "open-easy-web", "open-gitea": "open-gitea", "pdf-r2l-rs": "pdf-r2l-rs", "RPoem": "RPoem",
    "RS-Blog": "RS-Blog", "RS-EC": "RS-EC", "RS-Ops": "RS-Ops", "RS-Red": "RS-Red",
}
L = ["ja", "en", "zh-CN", "zh-TW", "ko", "de", "fr", "es", "pt-BR", "ru"]
NAMES = dict(zip(L, ["日本語", "English", "简体中文", "繁體中文(台灣)", "한국어", "Deutsch", "Français", "Español", "Português (BR)", "Русский"]))
T = {  # latest, dl, none, note, back
    "ja": ("最新版", "Windows 版(.exe)をダウンロード", "Windows 版の .exe はまだありません。最新版のページをご覧ください。", "署名がない場合、Windows が警告します(「詳細情報」→「実行」)。"),
    "en": ("Latest version", "Download for Windows (.exe)", "There is no Windows .exe yet. See the latest release page.", "If it is not signed, Windows may warn you (More info, then Run anyway)."),
    "zh-CN": ("最新版本", "下载 Windows 版(.exe)", "目前还没有 Windows 版 .exe。请查看最新发布页面。", "如果没有签名,Windows 可能会警告(“更多信息”→“仍要运行”)。"),
    "zh-TW": ("最新版本", "下載 Windows 版(.exe)", "目前還沒有 Windows 版 .exe。請查看最新發佈頁面。", "若未簽章,Windows 可能會警告(「其他資訊」→「仍要執行」)。"),
    "ko": ("최신 버전", "Windows용(.exe) 다운로드", "아직 Windows용 .exe가 없습니다. 최신 릴리스 페이지를 확인하세요.", "서명이 없으면 Windows가 경고할 수 있습니다(\"추가 정보\" → \"실행\")."),
    "de": ("Neueste Version", "Für Windows herunterladen (.exe)", "Es gibt noch keine Windows-.exe. Siehe die Seite der neuesten Version.", "Ohne Signatur warnt Windows eventuell („Weitere Informationen“, dann „Trotzdem ausführen“)."),
    "fr": ("Dernière version", "Télécharger pour Windows (.exe)", "Il n'y a pas encore de .exe pour Windows. Voir la page de la dernière version.", "Sans signature, Windows peut afficher un avertissement (« Informations complémentaires », puis « Exécuter quand même »)."),
    "es": ("Última versión", "Descargar para Windows (.exe)", "Todavía no hay un .exe para Windows. Consulta la página de la última versión.", "Si no está firmado, Windows puede avisar («Más información» y «Ejecutar de todas formas»)."),
    "pt-BR": ("Versão mais recente", "Baixar para Windows (.exe)", "Ainda não há um .exe para Windows. Veja a página da versão mais recente.", "Se não for assinado, o Windows pode avisar (\"Mais informações\" e \"Executar assim mesmo\")."),
    "ru": ("Последняя версия", "Скачать для Windows (.exe)", "Версии .exe для Windows пока нет. Смотрите страницу последнего релиза.", "Если программа не подписана, Windows может предупредить («Подробнее», затем «Выполнить в любом случае»)."),
}


def gh(*a):
    r = subprocess.run(["gh", *a], capture_output=True, text=True, encoding="utf-8")
    return r.stdout.strip() if r.returncode == 0 else ""


def page(name, desc, tag, exe_url, sha):
    E = html.escape
    base = f"https://github.com/aon-co-jp/{name}/releases/latest"
    nav = " · ".join(f'<a href="#{k}">{E(NAMES[k])}</a>' for k in L)
    body = ""
    for k in L:
        lat, dl, none, note = T[k]
        btn = (f'<a class="btn" href="{E(exe_url)}">{E(dl)}</a> ' if exe_url else f"<p>{E(none)}</p>")
        meta = f"<p><small>{E(lat)}: <a href=\"{E(base)}\">{E(tag or '-')}</a>" + (f" · SHA-256: <code>{E(sha)}</code>" if sha else "") + "</small></p>"
        body += f'<section id="{k}" lang="{k}"><h2>{E(NAMES[k])}</h2><p>{E(desc)}</p><p>{btn}</p>{meta}<p>{E(note) if exe_url else ""}</p></section>\n'
    return f"""<!doctype html>
<html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(name)} demo</title>
<style>
body{{font-family:system-ui,sans-serif;max-width:46rem;margin:0 auto;padding:1rem;line-height:1.7;color:#1a1a1a;background:#fff}}
@media(prefers-color-scheme:dark){{body{{color:#e6e6e6;background:#151515}}a{{color:#8ab4f8}}code{{background:#2a2a2a}}}}
nav{{font-size:.95rem;margin:1rem 0}}section{{border-top:1px solid #8884;padding-top:1rem;margin-top:1.5rem}}
code{{background:#eee;padding:0 .25em;border-radius:3px;word-break:break-all}}
.btn{{display:inline-block;background:#2563eb;color:#fff;padding:.5rem 1rem;border-radius:6px;text-decoration:none}}
</style></head><body>
<h1>{E(name)} demo</h1>
<p><a href="../">&larr; {E(name)}</a> · <a href="https://github.com/aon-co-jp/{E(name)}">GitHub</a></p>
<nav>{nav}</nav>
<p><small>説明は GitHub の説明文です。Description from GitHub. 非日本語の定型文は AI 翻訳(ネイティブ未確認)/ Non-Japanese boilerplate is AI-translated, not native-checked.</small></p>
{body}</body></html>
"""


tmp = tempfile.mkdtemp()
for name, d in PRODUCTS.items():
    info = json.loads(gh("repo", "view", f"aon-co-jp/{name}", "--json", "description") or "{}")
    desc = info.get("description") or "説明は準備中です。 / Description coming soon."
    rel = json.loads(gh("release", "view", "-R", f"aon-co-jp/{name}", "--json", "tagName,assets") or "{}")
    names = [a["name"] for a in rel.get("assets", [])]
    exe = next((n for n in names if n.lower().endswith(".exe") and "setup" in n.lower() or "installer" in n.lower() and n.lower().endswith(".exe")), None) \
        or next((n for n in names if n.lower().endswith(".exe")), None)
    url = f"https://github.com/aon-co-jp/{name}/releases/latest/download/{exe}" if exe else ""
    sha = ""
    if exe and exe + ".sha256" in names:
        sha = (gh("release", "download", "-R", f"aon-co-jp/{name}", rel["tagName"], "-p", exe + ".sha256", "-O", "-").split() or [""])[0]
    p = os.path.join(tmp, name + ".html")
    open(p, "w", encoding="utf-8", newline="").write(page(name, desc, rel.get("tagName", ""), url, sha))
    r = subprocess.run(["ssh", "conoha", f"mkdir -p /root/easy-web.tokyo/{d}/webpage/demo"])
    r = subprocess.run(["scp", "-q", p, f"conoha:/root/easy-web.tokyo/{d}/webpage/demo/index.html"])
    print(name, rel.get("tagName"), exe or "no-exe", "uploaded" if r.returncode == 0 else "FAILED")
