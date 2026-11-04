import json, html, sys, os
from playwright.sync_api import sync_playwright

BASE = os.path.dirname(os.path.abspath(__file__))
A = "file://" + os.path.join(BASE, "assets") + "/"
CARDS_PATH = sys.argv[1] if len(sys.argv) > 1 else os.path.join(BASE, "cards.json")
cards = json.load(open(CARDS_PATH, encoding="utf-8"))
TOTAL = len(cards)
e = html.escape

CSS = """
@font-face{font-family:'Prompt';font-weight:400;src:url('%(A)sPrompt-Regular.ttf')}
@font-face{font-family:'Prompt';font-weight:500;src:url('%(A)sPrompt-Medium.ttf')}
@font-face{font-family:'Prompt';font-weight:600;src:url('%(A)sPrompt-SemiBold.ttf')}
@font-face{font-family:'Prompt';font-weight:800;src:url('%(A)sPrompt-ExtraBold.ttf')}
*{box-sizing:border-box;margin:0;padding:0}
body{background:#FFFFFF;font-family:'Prompt',sans-serif;color:#1A1A1A}
.card{width:1200px;background:#FFFFFF;display:flex;flex-direction:column;min-height:%(H)spx}
.hero{position:relative;background:#070F40;height:600px;overflow:hidden;flex:none}
.hero .glow{position:absolute;left:0;bottom:0;width:640px}
.hero .outline{position:absolute;right:-170px;top:215px;width:530px}
.hero .dots{position:absolute;right:80px;top:70px;width:230px}
.hero .logo{position:absolute;left:80px;top:72px;width:330px}
.hero .tag{position:absolute;left:80px;top:218px;display:flex;gap:16px;align-items:center}
.chip{background:#4C67FF;color:#FFFFFF;font-weight:800;font-size:22px;letter-spacing:2px;text-transform:uppercase;padding:10px 20px}
.eixo{color:#8698FF;font-weight:800;font-size:22px;letter-spacing:2px;text-transform:uppercase}
.hero h1{position:absolute;left:80px;top:290px;width:740px;color:#FFFFFF;font-weight:800;font-size:56px;line-height:1.12;text-transform:uppercase}
.meta{display:flex;background:#F0F0F0;flex:none}
.meta>div{flex:1;padding:28px 40px 26px 80px}
.meta>div+div{border-left:2px solid #FFFFFF;padding-left:48px}
.meta .k{color:#2A3BA0;font-weight:800;font-size:18px;letter-spacing:2px;text-transform:uppercase}
.meta .v{color:#070F40;font-weight:800;font-size:34px;margin-top:4px}
.body{padding:56px 80px 24px 80px;display:flex;flex-direction:column;gap:40px;flex:1}
.sec h3{color:#2A3BA0;font-weight:800;font-size:20px;letter-spacing:2.5px;text-transform:uppercase;margin-bottom:12px}
.sec p{font-size:27px;line-height:1.55;color:#1A1A1A;font-weight:400}
.sec p+p{margin-top:14px}
.sec .src{font-size:21px;color:#2A3BA0;font-weight:600;margin-top:12px}
.gancho{border-left:8px solid #4C67FF;padding:6px 0 6px 32px}
.gancho p{font-size:38px;line-height:1.22;color:#070F40;font-weight:800}
ol{list-style:none;counter-reset:s}
ol li{counter-increment:s;position:relative;padding-left:64px;font-size:27px;line-height:1.5;margin-bottom:12px}
ol li::before{content:counter(s);position:absolute;left:0;top:2px;width:42px;height:42px;background:#2A3BA0;color:#FFFFFF;font-weight:800;font-size:22px;display:flex;align-items:center;justify-content:center}
.cta{background:#070F40;padding:34px 40px}
.cta h3{color:#8698FF;font-weight:800;font-size:20px;letter-spacing:2.5px;text-transform:uppercase;margin-bottom:10px}
.cta p{color:#FFFFFF;font-size:29px;line-height:1.4;font-weight:600}
.aviso{border:3px solid #2A3BA0;padding:22px 30px}
.aviso h3{margin-bottom:6px}
.aviso p{font-size:23px;line-height:1.45;color:#070F40;font-weight:500}
.foot{position:relative;background:#070F40;height:240px;overflow:hidden;flex:none;margin-top:24px}
.foot .logo{position:absolute;left:80px;top:46px;width:300px}
.foot .pat{position:absolute;right:-80px;top:-260px;width:740px}
.foot .h{position:absolute;left:80px;bottom:36px;color:#FFFFFF;font-weight:800;font-size:26px;letter-spacing:1px}
"""


def card_html(c, H):
    if c["roteiro_lista"]:
        r = "<ol>" + "".join(f"<li>{e(x)}</li>" for x in c["roteiro"]) + "</ol>"
    else:
        r = "".join(f"<p>{e(x)}</p>" for x in c["roteiro"])
    aviso = ""
    if c.get("atencao"):
        aviso = f'<div class="aviso sec"><h3>Conferir antes de gravar</h3><p>{e(c["atencao"])}</p></div>'
    return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>{CSS % {'A': A, 'H': H}}</style></head><body>
<div class="card" id="card">
 <div class="hero">
  <img class="glow" src="{A}glow.png"><img class="outline" src="{A}symbol_outline.png"><img class="dots" src="{A}dots.png">
  <img class="logo" src="{A}logo_dark.png">
  <div class="tag"><span class="chip">Ideia {c['n']} de {TOTAL}</span><span class="eixo">{e(c['eixo'])}</span></div>
  <h1>{e(c['titulo'])}</h1>
 </div>
 <div class="meta"><div><div class="k">Formato</div><div class="v">{e(c['formato'])}</div></div><div><div class="k">{'Tempo sugerido' if c['formato']=='Reel' else 'Extensão'}</div><div class="v">{e(c['duracao'])}</div></div></div>
 <div class="body">
  <div class="sec"><h3>O dado da semana</h3><p>{e(c['dado'])}</p><div class="src">Fonte: {e(c['fonte'])}</div></div>
  <div class="sec"><h3>Gancho de abertura</h3><div class="gancho"><p>{e(c['gancho'])}</p></div></div>
  <div class="sec"><h3>{e(c['roteiro_titulo'])}</h3>{r}</div>
  <div class="sec"><h3>Sugestão de legenda</h3><p>{e(c['legenda'])}</p></div>
  <div class="cta"><h3>Chamada para ação</h3><p>{e(c['cta'])}</p></div>
  {aviso}
 </div>
 <div class="foot"><img class="pat" src="{A}pattern.png"><img class="logo" src="{A}logo_dark.png"><div class="h">@venareinvestimentos</div></div>
</div></body></html>"""


def load(pg, h):
    f = os.path.join(BASE, ".card_tmp.html")
    open(f, "w", encoding="utf-8").write(h)
    pg.goto("file://" + f)
    pg.wait_for_load_state("networkidle")
    pg.evaluate("document.fonts.ready")
    ok = pg.evaluate("[document.fonts.check(\"800 20px Prompt\"), document.fonts.check(\"400 20px Prompt\"), [...document.images].every(i=>i.complete&&i.naturalWidth>0)]")
    assert all(ok), ok


def main(outdir):
    os.makedirs(outdir, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1200, "height": 1000}, device_scale_factor=1)
        heights = []
        for c in cards:
            load(pg, card_html(c, 0))
            heights.append(pg.evaluate("document.getElementById('card').getBoundingClientRect().height"))
        H = int(max(heights)) + 1
        print("heights", heights, "->", H)
        for c in cards:
            load(pg, card_html(c, H))
            el = pg.query_selector("#card")
            path = os.path.join(outdir, f"venare_ideia_{c['n']}.png")
            el.screenshot(path=path)
            print(path)
        b.close()


if __name__ == "__main__":
    main(sys.argv[2] if len(sys.argv) > 2 else os.path.join(BASE, "out"))
