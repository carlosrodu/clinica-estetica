"""
Generador de Posts de Instagram - Medicina Estética
Genera los posts gráficos (no los antes/después clínicos)
Formato: 1080x1080px (cuadrado Instagram)
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

W, H       = 1080, 1080
OUTPUT_DIR = "/home/user/clinica-estetica/posts"
FONTS_DIR  = "/home/user/clinica-estetica/fonts"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── PALETA ────────────────────────────────────────────────────────────────────
CREMA        = (245, 240, 232)
MARRON       = (58,  31,  13)
OLIVA        = (92, 106,  69)
DORADO       = (201, 169, 110)
TEXTO_OSCURO = (44,  24,  10)
TEXTO_CLARO  = (245, 240, 232)

# ── FUENTES ───────────────────────────────────────────────────────────────────
def font(size, style="serif"):
    try:
        path = f"{FONTS_DIR}/PlayfairDisplay-Bold.ttf" if style == "serif" \
               else f"{FONTS_DIR}/Montserrat-Light.ttf"
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

# ── HELPERS ───────────────────────────────────────────────────────────────────
def center_x(draw, text, fnt):
    """Retorna x para centrar texto."""
    bb = draw.textbbox((0, 0), text, font=fnt)
    return (W - (bb[2] - bb[0])) // 2

def text_h(draw, text, fnt):
    bb = draw.textbbox((0, 0), text, font=fnt)
    return bb[3] - bb[1]

def draw_line(draw, y, color=DORADO, width=140, thickness=2):
    x1 = (W - width) // 2
    draw.line([(x1, y), (x1 + width, y)], fill=color, width=thickness)

def shadow_bg(bg=CREMA, shadow=(170, 150, 120), intensity=55):
    """Fondo crema con sombra difusa en esquina."""
    img    = Image.new("RGB", (W, H), bg)
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d      = ImageDraw.Draw(overlay)
    d.ellipse([(-220, -220), (480, 480)], fill=(*shadow, intensity))
    overlay = overlay.filter(ImageFilter.GaussianBlur(120))
    img.paste(Image.new("RGB", (W, H), bg), mask=Image.eval(overlay.split()[3], lambda p: 255 - p))
    img.paste(overlay, mask=overlay.split()[3])
    return img

def texture(img, color1, color2):
    """Textura de puntos muy suave sobre fondo oscuro."""
    draw = ImageDraw.Draw(img)
    for y in range(0, H, 6):
        for x in range(0, W, 6):
            if (x + y) % 18 == 0:
                draw.point((x, y), fill=color2)
    return img

# ── ICONOS DIBUJADOS (sin emojis) ─────────────────────────────────────────────
def draw_sad_face(draw, cx, cy, r=90):
    """Cara triste."""
    draw.ellipse([cx-r, cy-r, cx+r, cy+r], outline=TEXTO_OSCURO, width=6)
    eo = r // 3
    draw.ellipse([cx-eo-12, cy-20, cx-eo+12, cy+4],  fill=TEXTO_OSCURO)
    draw.ellipse([cx+eo-12, cy-20, cx+eo+12, cy+4],  fill=TEXTO_OSCURO)
    draw.arc([cx-30, cy+10, cx+30, cy+55], start=200, end=340, fill=TEXTO_OSCURO, width=6)

def draw_happy_face(draw, cx, cy, r=90):
    """Cara feliz con corazones como ojos."""
    draw.ellipse([cx-r, cy-r, cx+r, cy+r], outline=TEXTO_OSCURO, width=6)
    for ox in [-28, 28]:
        hx, hy = cx + ox, cy - 20
        draw.polygon([
            (hx,      hy + 14),
            (hx - 14, hy - 4),
            (hx - 7,  hy - 14),
            (hx,      hy - 6),
            (hx + 7,  hy - 14),
            (hx + 14, hy - 4),
        ], fill=TEXTO_OSCURO)
    draw.arc([cx-30, cy+15, cx+30, cy+50], start=20, end=160, fill=TEXTO_OSCURO, width=6)

def draw_vial(draw, cx, cy, w=44, h=90, color=TEXTO_OSCURO):
    """Ampolla/vial médico."""
    neck_w = w // 2
    draw.rectangle([cx - w//2, cy - h//2 + 20, cx + w//2, cy + h//2], outline=color, width=5)
    draw.rectangle([cx - neck_w//2, cy - h//2 - 14, cx + neck_w//2, cy - h//2 + 20],
                   outline=color, fill=color, width=3)
    draw.line([(cx - w//2 + 8, cy), (cx + w//2 - 8, cy)], fill=color, width=3)
    draw.line([(cx - w//2 + 8, cy + 18), (cx + w//2 - 8, cy + 18)], fill=color, width=3)

def draw_syringe(draw, cx, cy, length=160, color=TEXTO_CLARO):
    """Jeringa simple."""
    draw.rectangle([cx - length//2, cy - 14, cx + length//2 - 30, cy + 14],
                   outline=color, width=4)
    draw.rectangle([cx - length//2 + 6, cy - 8, cx - length//2 + 30, cy + 8],
                   fill=color)
    draw.polygon([
        (cx + length//2 - 30, cy - 14),
        (cx + length//2,       cy),
        (cx + length//2 - 30, cy + 14),
    ], fill=color)
    draw.rectangle([cx - length//2 - 20, cy - 22, cx - length//2, cy + 22],
                   outline=color, width=4)

def draw_coffee_cup(draw, cx, cy, color=TEXTO_CLARO):
    """Taza de café."""
    draw.polygon([
        (cx - 44, cy - 44),
        (cx + 44, cy - 44),
        (cx + 36, cy + 44),
        (cx - 36, cy + 44),
    ], outline=color, width=5)
    draw.arc([cx + 40, cy - 16, cx + 80, cy + 16], start=300, end=60, fill=color, width=5)
    draw.rectangle([cx - 44, cy - 44, cx + 44, cy - 30], fill=color)
    # vapor
    for ox in [-16, 0, 16]:
        draw.arc([cx + ox - 8, cy - 80, cx + ox + 8, cy - 44],
                 start=0, end=180, fill=color, width=3)

# ══════════════════════════════════════════════════════════════════════════════
#  POST 01 — PRESENTACIÓN DEL PERFIL (CREMA)
# ══════════════════════════════════════════════════════════════════════════════
def post_01():
    img  = shadow_bg()
    draw = ImageDraw.Draw(img)

    draw_line(draw, 310, width=100)

    f_sub = font(40, "sans")
    sub   = "MEDICINA ESTÉTICA"
    draw.text((center_x(draw, sub, f_sub), 330), sub, font=f_sub, fill=DORADO)

    f_big = font(120, "serif")
    big   = "BIENVENIDO/A"
    draw.text((center_x(draw, big, f_big), 400), big, font=f_big, fill=TEXTO_OSCURO)

    f_body = font(44, "sans")
    line1  = "Enfermero/a especialista"
    line2  = "en estética médica"
    draw.text((center_x(draw, line1, f_body), 560), line1, font=f_body, fill=(110, 80, 50))
    draw.text((center_x(draw, line2, f_body), 614), line2, font=f_body, fill=(110, 80, 50))

    draw_line(draw, 700, width=100)

    # Monograma: símbolo simple
    f_mono = font(52, "serif")
    mono   = "— AE —"
    draw.text((center_x(draw, mono, f_mono), 740), mono, font=f_mono, fill=DORADO)

    img.save(f"{OUTPUT_DIR}/post_01_presentacion.png")
    print("OK  Post 01")

# ══════════════════════════════════════════════════════════════════════════════
#  POST 02 — CUIDARTE NO ES VANIDAD (MARRÓN)
# ══════════════════════════════════════════════════════════════════════════════
def post_02():
    img  = Image.new("RGB", (W, H), MARRON)
    img  = texture(img, MARRON, (68, 38, 18))
    draw = ImageDraw.Draw(img)

    draw_line(draw, 240, color=DORADO, width=110)

    lines = [
        ("CUIDARTE",  font(118, "serif"), TEXTO_CLARO, 275),
        ("NO ES",     font( 92, "serif"), TEXTO_CLARO, 415),
        ("VANIDAD.",  font(118, "serif"), TEXTO_CLARO, 520),
    ]
    for txt, fnt, col, y in lines:
        draw.text((center_x(draw, txt, fnt), y), txt, font=fnt, fill=col)

    draw_line(draw, 680, color=DORADO, width=110)

    f_sub = font(42, "sans")
    sub   = "Es respeto. Es bienestar. Es salud."
    draw.text((center_x(draw, sub, f_sub), 710), sub, font=f_sub, fill=DORADO)

    f_mono = font(50, "serif")
    mono   = "— AE —"
    draw.text((center_x(draw, mono, f_mono), 900), mono, font=f_mono, fill=DORADO)

    img.save(f"{OUTPUT_DIR}/post_02_vanidad.png")
    print("OK  Post 02")

# ══════════════════════════════════════════════════════════════════════════════
#  POST 06 — NURSE MATH (CREMA)
# ══════════════════════════════════════════════════════════════════════════════
def post_06():
    img  = shadow_bg()
    draw = ImageDraw.Draw(img)

    f_title = font(108, "serif")
    title   = "NURSE MATH:"
    draw.text((center_x(draw, title, f_title), 90), title, font=f_title, fill=TEXTO_OSCURO)

    draw_line(draw, 240, width=120)

    # Ecuación — 5 posiciones centradas
    eq_y   = 500
    gap    = 180
    start  = W // 2 - gap * 2

    draw_sad_face(draw,  start + gap * 0, eq_y)

    f_op = font(100, "sans")
    draw.text((start + gap * 1 - 20, eq_y - 50), "+", font=f_op, fill=TEXTO_OSCURO)

    draw_vial(draw, start + gap * 2, eq_y, w=50, h=100)

    draw.text((start + gap * 3 - 18, eq_y - 50), "=", font=f_op, fill=TEXTO_OSCURO)

    draw_happy_face(draw, start + gap * 4, eq_y)

    draw_line(draw, 650, width=120)

    f_sub  = font(40, "sans")
    line1  = "Piel deshidratada + Ácido hialurónico"
    line2  = "= Piel que brilla"
    draw.text((center_x(draw, line1, f_sub), 675), line1, font=f_sub, fill=(110, 80, 50))
    draw.text((center_x(draw, line2, f_sub), 725), line2, font=f_sub, fill=(110, 80, 50))

    f_mono = font(50, "serif")
    mono   = "— AE —"
    draw.text((center_x(draw, mono, f_mono), 900), mono, font=f_mono, fill=DORADO)

    img.save(f"{OUTPUT_DIR}/post_06_nurse_math.png")
    print("OK  Post 06")

# ══════════════════════════════════════════════════════════════════════════════
#  POST 07 — MESOTERAPIA CARA (VERDE OLIVA)
# ══════════════════════════════════════════════════════════════════════════════
def post_07():
    img  = Image.new("RGB", (W, H), OLIVA)
    img  = texture(img, OLIVA, (80, 95, 58))
    draw = ImageDraw.Draw(img)

    # Headline en 2 líneas
    f_h   = font(82, "serif")
    draw.text((center_x(draw, '"LA MESOTERAPIA', f_h), 80),
              '"LA MESOTERAPIA', font=f_h, fill=TEXTO_CLARO)
    draw.text((center_x(draw, 'ES DEMASIADO CARA..."', f_h), 175),
              'ES DEMASIADO CARA..."', font=f_h, fill=TEXTO_CLARO)

    draw_line(draw, 295, color=DORADO, width=200)

    # Columna izquierda (mesoterapia) y derecha (café)
    col_l, col_r = 270, 810
    icon_y = 430

    draw_syringe(draw, col_l, icon_y, length=150, color=TEXTO_CLARO)
    draw_coffee_cup(draw, col_r, icon_y, color=TEXTO_CLARO)

    f_vs = font(72, "serif")
    draw.text((center_x(draw, "VS.", f_vs), 395), "VS.", font=f_vs, fill=DORADO)

    draw_line(draw, 540, color=DORADO, width=200)

    # Etiquetas
    f_label = font(48, "serif")
    f_price = font(70, "serif")
    f_desc  = font(34, "sans")

    # Izquierda
    t = "Mesoterapia"
    draw.text((col_l - draw.textbbox((0,0), t, font=f_label)[2]//2, 560), t,
              font=f_label, fill=TEXTO_CLARO)
    t2 = "2,50 €/día"
    draw.text((col_l - draw.textbbox((0,0), t2, font=f_price)[2]//2, 618), t2,
              font=f_price, fill=DORADO)
    t3 = "Dura 6-12 meses"
    draw.text((col_l - draw.textbbox((0,0), t3, font=f_desc)[2]//2, 710), t3,
              font=f_desc, fill=TEXTO_CLARO)

    # Derecha
    t = "Café diario"
    draw.text((col_r - draw.textbbox((0,0), t, font=f_label)[2]//2, 560), t,
              font=f_label, fill=TEXTO_CLARO)
    t2 = "2,00 €/día"
    draw.text((col_r - draw.textbbox((0,0), t2, font=f_price)[2]//2, 618), t2,
              font=f_price, fill=DORADO)
    t3 = "Dura 10 minutos"
    draw.text((col_r - draw.textbbox((0,0), t3, font=f_desc)[2]//2, 710), t3,
              font=f_desc, fill=TEXTO_CLARO)

    draw_line(draw, 800, color=DORADO, width=200)

    f_fin = font(38, "sans")
    fin   = "Tú decides."
    draw.text((center_x(draw, fin, f_fin), 825), fin, font=f_fin, fill=TEXTO_CLARO)

    f_mono = font(48, "serif")
    mono   = "— AE —"
    draw.text((center_x(draw, mono, f_mono), 940), mono, font=f_mono, fill=DORADO)

    img.save(f"{OUTPUT_DIR}/post_07_precio.png")
    print("OK  Post 07")

# ══════════════════════════════════════════════════════════════════════════════
#  POST 08 — TESTIMONIO (CREMA)
# ══════════════════════════════════════════════════════════════════════════════
def post_08():
    img  = shadow_bg()
    draw = ImageDraw.Draw(img)

    f_q    = font(200, "serif")
    draw.text((55, 20), "\u201c", font=f_q, fill=DORADO)

    f_body = font(50, "serif")
    lines  = [
        "Vine con muchas dudas y salí",
        "con la piel que quería tener",
        "desde hace años. Me explicaron",
        "todo y solo me recomendaron",
        "lo que necesitaba.",
        "Eso no tiene precio.",
    ]
    y = 250
    for line in lines:
        draw.text((center_x(draw, line, f_body), y), line, font=f_body, fill=TEXTO_OSCURO)
        y += 76

    draw_line(draw, y + 20, width=160)

    f_autor = font(38, "sans")
    autor   = "— M.R., 38 años  ·  Mesoterapia + Peeling"
    draw.text((center_x(draw, autor, f_autor), y + 45), autor, font=f_autor, fill=(130, 95, 60))

    f_q2 = font(160, "serif")
    draw.text((W - 160, y + 10), "\u201d", font=f_q2, fill=DORADO)

    draw_line(draw, 960, width=100)

    f_mono = font(48, "serif")
    mono   = "— AE —"
    draw.text((center_x(draw, mono, f_mono), 985), mono, font=f_mono, fill=DORADO)

    img.save(f"{OUTPUT_DIR}/post_08_testimonio.png")
    print("OK  Post 08")

# ══════════════════════════════════════════════════════════════════════════════
#  POST 10 — EL MOMENTO PERFECTO (MARRÓN)
# ══════════════════════════════════════════════════════════════════════════════
def post_10():
    img  = Image.new("RGB", (W, H), MARRON)
    img  = texture(img, MARRON, (68, 38, 18))
    draw = ImageDraw.Draw(img)

    draw_line(draw, 180, color=DORADO, width=120)

    blocks = [
        ("EL MOMENTO",    font(104, "serif"), TEXTO_CLARO, 210),
        ("PERFECTO",      font(104, "serif"), TEXTO_CLARO, 330),
        ("para empezar",  font( 72, "serif"), DORADO,      460),
        ("no existe.",    font( 90, "serif"), TEXTO_CLARO, 548),
    ]
    for txt, fnt, col, y in blocks:
        draw.text((center_x(draw, txt, fnt), y), txt, font=fnt, fill=col)

    draw_line(draw, 680, color=DORADO, width=120)

    f_sub  = font(46, "sans")
    sub1   = "Pero este es el más cercano"
    sub2   = "que vas a tener."
    draw.text((center_x(draw, sub1, f_sub), 710), sub1, font=f_sub, fill=TEXTO_CLARO)
    draw.text((center_x(draw, sub2, f_sub), 768), sub2, font=f_sub, fill=TEXTO_CLARO)

    f_cta  = font(40, "sans")
    cta    = "Primera valoración gratuita · Plazas limitadas"
    draw.text((center_x(draw, cta, f_cta), 860), cta, font=f_cta, fill=DORADO)

    draw_line(draw, 940, color=DORADO, width=120)

    f_mono = font(48, "serif")
    mono   = "— AE —"
    draw.text((center_x(draw, mono, f_mono), 968), mono, font=f_mono, fill=DORADO)

    img.save(f"{OUTPUT_DIR}/post_10_cta_final.png")
    print("OK  Post 10")

# ── MAIN ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Generando posts...\n")
    post_01()
    post_02()
    post_06()
    post_07()
    post_08()
    post_10()
    print(f"\nTodos los posts en: {OUTPUT_DIR}/")
    print("P3, P5, P9 → usa tus fotos de antes/después")
