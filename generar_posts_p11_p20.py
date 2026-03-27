"""
Generador Posts P11-P20 — Carlos Dueñas Estética Médica
Inspirado en @clinicaholguera + @belenmarquez.dermoestetica + @leebrabiotics
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

W, H       = 1080, 1080
OUTPUT_DIR = "/home/user/clinica-estetica/posts"
FONTS_DIR  = "/home/user/clinica-estetica/fonts"
os.makedirs(OUTPUT_DIR, exist_ok=True)

CREMA        = (245, 240, 232)
MARRON       = (58,  31,  13)
OLIVA        = (92, 106,  69)
MALVA        = (74,  32,  64)
DORADO       = (201, 169, 110)
TEXTO_OSCURO = (44,  24,  10)
TEXTO_CLARO  = (245, 240, 232)
GRIS_CALIDO  = (210, 200, 185)

def font(size, style="serif"):
    try:
        path = f"{FONTS_DIR}/PlayfairDisplay-Bold.ttf" if style == "serif" \
               else f"{FONTS_DIR}/Montserrat-Light.ttf"
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()

def cx(draw, text, fnt):
    bb = draw.textbbox((0, 0), text, font=fnt)
    return (W - (bb[2] - bb[0])) // 2

def line(draw, y, color=DORADO, w=140, t=2):
    x1 = (W - w) // 2
    draw.line([(x1, y), (x1 + w, y)], fill=color, width=t)

def shadow_bg(bg=CREMA, shadow=(170, 150, 120), intensity=50):
    img = Image.new("RGB", (W, H), bg)
    ov  = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d   = ImageDraw.Draw(ov)
    d.ellipse([(-220, -220), (480, 480)], fill=(*shadow, intensity))
    ov  = ov.filter(ImageFilter.GaussianBlur(120))
    img.paste(ov, mask=ov.split()[3])
    return img

def texture_dark(color_base, dot_color):
    img  = Image.new("RGB", (W, H), color_base)
    draw = ImageDraw.Draw(img)
    for y in range(0, H, 6):
        for x in range(0, W, 6):
            if (x + y) % 18 == 0:
                draw.point((x, y), fill=dot_color)
    return img

def monogram(draw, y=960, color=DORADO):
    f = font(44, "serif")
    t = "— CD —"
    draw.text((cx(draw, t, f), y), t, font=f, fill=color)

# ══════════════════════════════════════════════════════════════════════════════
# P11 — "TU PIEL TIENE MEMORIA" — statement poético @leebrabiotics style (MARRÓN)
# ══════════════════════════════════════════════════════════════════════════════
def post_11():
    img  = texture_dark(MARRON, (68, 38, 18))
    draw = ImageDraw.Draw(img)

    line(draw, 190, w=100)

    for txt, fnt, col, y in [
        ("TU PIEL",         font(106, "serif"), TEXTO_CLARO,  220),
        ("TIENE",           font( 80, "serif"), DORADO,       348),
        ("MEMORIA.",        font(106, "serif"), TEXTO_CLARO,  440),
    ]:
        draw.text((cx(draw, txt, fnt), y), txt, font=fnt, fill=col)

    line(draw, 590, w=100)

    f_sub = font(44, "sans")
    for txt, y in [
        ("Cada vez que la descuidas,",  625),
        ("lo recuerda.",                673),
        ("Cada vez que la cuidas,",     730),
        ("también.",                    778),
    ]:
        draw.text((cx(draw, txt, f_sub), y), txt, font=f_sub, fill=GRIS_CALIDO)

    line(draw, 860, w=100)
    monogram(draw, 895)

    img.save(f"{OUTPUT_DIR}/post_11_piel_memoria.png")
    print("OK  P11")

# ══════════════════════════════════════════════════════════════════════════════
# P12 — "POV" REEL COVER — @belenmarquez style (CREMA)
# ══════════════════════════════════════════════════════════════════════════════
def post_12():
    img  = shadow_bg()
    draw = ImageDraw.Draw(img)

    # Etiqueta "REEL"
    f_tag = font(34, "sans")
    tag   = "R E E L"
    bbt   = draw.textbbox((0,0), tag, font=f_tag)
    tw    = bbt[2] - bbt[0]
    draw.rectangle([(W//2 - tw//2 - 20, 155), (W//2 + tw//2 + 20, 205)],
                   outline=DORADO, width=2)
    draw.text((W//2 - tw//2, 162), tag, font=f_tag, fill=DORADO)

    line(draw, 240, w=80)

    f_pov = font(58, "sans")
    draw.text((cx(draw, "POV:", f_pov), 275), "POV:", font=f_pov, fill=DORADO)

    f_big = font(88, "serif")
    for txt, y in [
        ("Tu primera",  350),
        ("consulta de", 452),
        ("estética",    554),
        ("médica.",     646),
    ]:
        draw.text((cx(draw, txt, f_big), y), txt, font=f_big, fill=TEXTO_OSCURO)

    line(draw, 780, w=80)

    f_sub = font(38, "sans")
    sub   = "Lo que nadie te cuenta antes de ir"
    draw.text((cx(draw, sub, f_sub), 808), sub, font=f_sub, fill=(120, 88, 55))

    line(draw, 895, w=80)
    monogram(draw, 925, DORADO)

    img.save(f"{OUTPUT_DIR}/post_12_pov_reel.png")
    print("OK  P12")

# ══════════════════════════════════════════════════════════════════════════════
# P13 — "CIENCIA + NATURALEZA" — @leebrabiotics style (OLIVA)
# ══════════════════════════════════════════════════════════════════════════════
def post_13():
    img  = texture_dark(OLIVA, (80, 95, 58))
    draw = ImageDraw.Draw(img)

    line(draw, 170, color=DORADO, w=120)

    f_small = font(38, "sans")
    draw.text((cx(draw, "EL SECRETO DE UNA BUENA PIEL", f_small), 195),
              "EL SECRETO DE UNA BUENA PIEL", font=f_small, fill=GRIS_CALIDO)

    line(draw, 250, color=DORADO, w=120)

    f_big = font(92, "serif")
    for txt, y in [
        ("No está en",  290),
        ("la crema",    395),
        ("más cara.",   490),
    ]:
        draw.text((cx(draw, txt, f_big), y), txt, font=f_big, fill=TEXTO_CLARO)

    line(draw, 620, color=DORADO, w=120)

    f_body = font(46, "sans")
    for txt, y in [
        ("Está en entender qué necesita",  655),
        ("tu piel específicamente.",        703),
        ("Y en tratarla con criterio.",     760),
    ]:
        draw.text((cx(draw, txt, f_body), y), txt, font=f_body, fill=GRIS_CALIDO)

    line(draw, 850, color=DORADO, w=120)

    f_firma = font(40, "sans")
    draw.text((cx(draw, "Ciencia aplicada. Sin tendencias.", f_firma), 878),
              "Ciencia aplicada. Sin tendencias.", font=f_firma, fill=DORADO)

    monogram(draw, 955, DORADO)

    img.save(f"{OUTPUT_DIR}/post_13_ciencia_naturaleza.png")
    print("OK  P13")

# ══════════════════════════════════════════════════════════════════════════════
# P14 — "5 SEÑALES" CAROUSEL COVER — @belenmarquez edu style (CREMA)
# ══════════════════════════════════════════════════════════════════════════════
def post_14():
    img  = shadow_bg()
    draw = ImageDraw.Draw(img)

    # Número grande decorativo
    f_num = font(280, "serif")
    draw.text((cx(draw, "5", f_num) + 10, 60), "5", font=f_num,
              fill=(*DORADO[:3],))

    line(draw, 355, w=160)

    f_big = font(84, "serif")
    for txt, y in [
        ("SEÑALES DE QUE", 378),
        ("TU PIEL NECESITA", 472),
        ("AYUDA PROFESIONAL", 566),
    ]:
        draw.text((cx(draw, txt, f_big), y), txt, font=f_big, fill=TEXTO_OSCURO)

    line(draw, 680, w=160)

    f_sub = font(40, "sans")
    sub   = "Guarda este carrusel"
    draw.text((cx(draw, sub, f_sub), 710), sub, font=f_sub, fill=(120, 88, 55))

    f_sub2 = font(34, "sans")
    sub2   = "Desliza para descubrirlas"
    draw.text((cx(draw, sub2, f_sub2), 758), sub2, font=f_sub2, fill=DORADO)

    line(draw, 840, w=160)
    monogram(draw, 875)

    img.save(f"{OUTPUT_DIR}/post_14_5_senales_cover.png")
    print("OK  P14")

# ══════════════════════════════════════════════════════════════════════════════
# P15 — SLIDE 1 de carrusel "5 señales" — señal #1 (CREMA)
# ══════════════════════════════════════════════════════════════════════════════
def post_14b():
    img  = shadow_bg()
    draw = ImageDraw.Draw(img)

    f_num = font(52, "sans")
    draw.text((cx(draw, "SEÑAL  01 / 05", f_num), 130),
              "SEÑAL  01 / 05", font=f_num, fill=DORADO)

    line(draw, 210, w=180)

    f_big = font(96, "serif")
    for txt, y in [
        ("Tu piel",    260),
        ("siempre",    368),
        ("está",       466),
        ("\"cansada\".", 554),
    ]:
        draw.text((cx(draw, txt, f_big), y), txt, font=f_big, fill=TEXTO_OSCURO)

    line(draw, 680, w=180)

    f_body = font(44, "sans")
    for txt, y in [
        ("Sin brillo, sin tono, sin energía.", 710),
        ("No es normal. Es una señal.", 758),
        ("Tu dermis te está pidiendo ayuda.", 806),
    ]:
        draw.text((cx(draw, txt, f_body), y), txt, font=f_body, fill=(110, 80, 55))

    line(draw, 890, w=180)
    monogram(draw, 925)

    img.save(f"{OUTPUT_DIR}/post_14b_senal_01.png")
    print("OK  P14b")

# ══════════════════════════════════════════════════════════════════════════════
# P16 — "LO QUE EL MARKETING NO TE DICE" — @leebrabiotics edu crítico (MARRÓN)
# ══════════════════════════════════════════════════════════════════════════════
def post_16():
    img  = texture_dark(MARRON, (68, 38, 18))
    draw = ImageDraw.Draw(img)

    line(draw, 155, w=110)

    f_big = font(90, "serif")
    for txt, y in [
        ("Lo que el",   185),
        ("marketing",   285),
        ("no te dice",  385),
        ("sobre tu",    475),
        ("crema.",      565),
    ]:
        draw.text((cx(draw, txt, f_big), y), txt, font=f_big, fill=TEXTO_CLARO)

    line(draw, 660, w=110)

    f_body = font(42, "sans")
    for txt, y in [
        ("Una crema actúa solo en epidermis.", 690),
        ("Los tratamientos médicos",           738),
        ("llegan a la dermis.",                786),
        ("Son cosas distintas.",               842),
    ]:
        draw.text((cx(draw, txt, f_body), y), txt, font=f_body, fill=GRIS_CALIDO)

    line(draw, 910, w=110)
    monogram(draw, 945)

    img.save(f"{OUTPUT_DIR}/post_16_marketing.png")
    print("OK  P16")

# ══════════════════════════════════════════════════════════════════════════════
# P17 — "¿SABES QUÉ ENTRA EN TU PIEL?" ingredient edu (CREMA) @leebrabiotics
# ══════════════════════════════════════════════════════════════════════════════
def post_17():
    img  = shadow_bg()
    draw = ImageDraw.Draw(img)

    f_top = font(40, "sans")
    draw.text((cx(draw, "EDUCACIÓN DE INGREDIENTES", f_top), 120),
              "EDUCACIÓN DE INGREDIENTES", font=f_top, fill=DORADO)

    line(draw, 190, w=200)

    f_big = font(86, "serif")
    for txt, y in [
        ("¿Sabes qué",  225),
        ("entra realmente", 323),
        ("en tu piel?", 421),
    ]:
        draw.text((cx(draw, txt, f_big), y), txt, font=f_big, fill=TEXTO_OSCURO)

    line(draw, 540, w=200)

    ingredientes = [
        ("ÁCIDO HIALURÓNICO",  "Hidratación profunda + estimula colágeno"),
        ("VITAMINA C",         "Antioxidante + unifica tono + luminosidad"),
        ("PRP (plasma propio)", "Regenera desde dentro, 100% biocompatible"),
    ]

    f_ing  = font(40, "serif")
    f_desc = font(32, "sans")
    y = 580
    for ing, desc in ingredientes:
        draw.text((cx(draw, ing, f_ing), y), ing, font=f_ing, fill=TEXTO_OSCURO)
        y += 50
        draw.text((cx(draw, desc, f_desc), y), desc, font=f_desc, fill=(130, 95, 60))
        y += 70
        line(draw, y, w=300, t=1)
        y += 25

    monogram(draw, 955)

    img.save(f"{OUTPUT_DIR}/post_17_ingredientes.png")
    print("OK  P17")

# ══════════════════════════════════════════════════════════════════════════════
# P18 — "¿CARO O BARATO?" PROFESIONAL vs FRANQUICIA (MALVA) @clinicaholguera
# ══════════════════════════════════════════════════════════════════════════════
def post_18():
    img  = texture_dark(MALVA, (85, 40, 75))
    draw = ImageDraw.Draw(img)

    line(draw, 130, color=DORADO, w=120)

    f_title = font(76, "serif")
    draw.text((cx(draw, "¿DÓNDE TE TRATAS?", f_title), 158),
              "¿DÓNDE TE TRATAS?", font=f_title, fill=TEXTO_CLARO)

    line(draw, 270, color=DORADO, w=120)

    col_l, col_r = 270, 810
    f_head = font(46, "serif")
    f_item = font(32, "sans")

    # Cabeceras
    draw.text((col_l - draw.textbbox((0,0),"FRANQUICIA",font=f_head)[2]//2, 300),
              "FRANQUICIA", font=f_head, fill=GRIS_CALIDO)
    draw.text((col_r - draw.textbbox((0,0),"ENFERMERO/A",font=f_head)[2]//2, 300),
              "ENFERMERO/A", font=f_head, fill=DORADO)
    f_sub2 = font(28, "sans")
    draw.text((col_r - draw.textbbox((0,0),"ESPECIALISTA",font=f_sub2)[2]//2, 352),
              "ESPECIALISTA", font=f_sub2, fill=DORADO)

    line(draw, 395, color=DORADO, w=500)

    items_l = ["Protocolo estándar", "Sin valoración previa", "Rotación de personal", "Sin seguimiento"]
    items_r = ["Protocolo personalizado", "Valoración individual", "Siempre el mismo profesional", "Seguimiento continuo"]

    y = 420
    for il, ir in zip(items_l, items_r):
        bbl = draw.textbbox((0,0), f"✗ {il}", font=f_item)
        bbr = draw.textbbox((0,0), f"✓ {ir}", font=f_item)
        draw.text((col_l - (bbl[2]-bbl[0])//2, y), f"✗ {il}", font=f_item, fill=GRIS_CALIDO)
        draw.text((col_r - (bbr[2]-bbr[0])//2, y), f"✓ {ir}", font=f_item, fill=DORADO)
        y += 68

    line(draw, y + 10, color=DORADO, w=500)

    f_fin = font(38, "sans")
    draw.text((cx(draw, "Tu piel merece que te conozcan.", f_fin), y + 35),
              "Tu piel merece que te conozcan.", font=f_fin, fill=TEXTO_CLARO)

    monogram(draw, 970, DORADO)

    img.save(f"{OUTPUT_DIR}/post_18_franquicia_vs_especialista.png")
    print("OK  P18")

# ══════════════════════════════════════════════════════════════════════════════
# P19 — "BIENESTAR ES" poético (CREMA) @leebrabiotics philosophy
# ══════════════════════════════════════════════════════════════════════════════
def post_19():
    img  = shadow_bg(bg=CREMA, shadow=(165, 145, 115))
    draw = ImageDraw.Draw(img)

    line(draw, 185, w=80)

    f_small = font(38, "sans")
    draw.text((cx(draw, "UNA REFLEXIÓN", f_small), 210),
              "UNA REFLEXIÓN", font=f_small, fill=DORADO)

    line(draw, 270, w=80)

    f_big = font(94, "serif")
    for txt, y in [
        ("Bienestar",   305),
        ("no es",       410),
        ("verte igual", 505),
        ("que otra.",   600),
    ]:
        draw.text((cx(draw, txt, f_big), y), txt, font=f_big, fill=TEXTO_OSCURO)

    line(draw, 720, w=80)

    f_body = font(46, "sans")
    for txt, y in [
        ("Es verte como tú,",       752),
        ("pero en tu mejor versión.", 804),
    ]:
        draw.text((cx(draw, txt, f_body), y), txt, font=f_body, fill=(115, 83, 52))

    line(draw, 895, w=80)
    monogram(draw, 928)

    img.save(f"{OUTPUT_DIR}/post_19_bienestar.png")
    print("OK  P19")

# ══════════════════════════════════════════════════════════════════════════════
# P20 — "LA PREGUNTA CORRECTA" engagement hook (OLIVA) @belenmarquez style
# ══════════════════════════════════════════════════════════════════════════════
def post_20():
    img  = texture_dark(OLIVA, (80, 95, 58))
    draw = ImageDraw.Draw(img)

    line(draw, 160, color=DORADO, w=130)

    f_intro = font(40, "sans")
    draw.text((cx(draw, "LA PREGUNTA CORRECTA NO ES...", f_intro), 188),
              "LA PREGUNTA CORRECTA NO ES...", font=f_intro, fill=GRIS_CALIDO)

    line(draw, 252, color=DORADO, w=130)

    f_wrong = font(78, "serif")
    for txt, y in [
        ('"¿Me haré',    285),
        ('algo en',      370),
        ('la cara?"',    455),
    ]:
        draw.text((cx(draw, txt, f_wrong), y), txt, font=f_wrong, fill=TEXTO_CLARO)

    line(draw, 555, color=DORADO, w=300)

    f_label = font(38, "sans")
    draw.text((cx(draw, "La pregunta correcta es:", f_label), 580),
              "La pregunta correcta es:", font=f_label, fill=GRIS_CALIDO)

    f_right = font(78, "serif")
    for txt, y in [
        ('"¿Cómo puedo',   625),
        ('cuidar mejor',   712),
        ('mi piel?"',      799),
    ]:
        draw.text((cx(draw, txt, f_right), y), txt, font=f_right, fill=DORADO)

    line(draw, 905, color=DORADO, w=130)
    monogram(draw, 940, DORADO)

    img.save(f"{OUTPUT_DIR}/post_20_pregunta_correcta.png")
    print("OK  P20")


# ── MAIN ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Generando posts P11-P20...\n")
    post_11()
    post_12()
    post_13()
    post_14()
    post_14b()
    post_16()
    post_17()
    post_18()
    post_19()
    post_20()
    print(f"\nTodos los posts en: {OUTPUT_DIR}/")
