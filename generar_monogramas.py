"""
Generador de Monogramas — Carlos Dueñas (CD)
Varios estilos inspirados en el monograma de @clinicaholguera
Fondo transparente para usar como sello en cualquier post
"""

from PIL import Image, ImageDraw, ImageFont
import os, math

FONTS_DIR  = "/home/user/clinica-estetica/fonts"
OUTPUT_DIR = "/home/user/clinica-estetica/monogramas"
os.makedirs(OUTPUT_DIR, exist_ok=True)

S = 400  # Tamaño del canvas (cuadrado)

CREMA  = (245, 240, 232)
MARRON = (58,  31,  13)
DORADO = (201, 169, 110)
TRANS  = (0, 0, 0, 0)

def font(size, style="serif"):
    try:
        path = f"{FONTS_DIR}/PlayfairDisplay-Bold.ttf" if style == "serif" \
               else f"{FONTS_DIR}/Montserrat-Light.ttf"
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()

def new_canvas():
    return Image.new("RGBA", (S, S), TRANS)

def cx(draw, text, fnt):
    bb = draw.textbbox((0,0), text, font=fnt)
    return (S - (bb[2]-bb[0])) // 2

def cy_text(draw, text, fnt):
    bb = draw.textbbox((0,0), text, font=fnt)
    return (S - (bb[3]-bb[1])) // 2

def save_preview(img_rgba, filename, bg=MARRON):
    """Guarda versión previa sobre fondo oscuro y claro para ver cómo queda."""
    # Sobre fondo marrón
    bg_img = Image.new("RGB", (S, S), bg)
    bg_img.paste(img_rgba, mask=img_rgba.split()[3])
    bg_img.save(f"{OUTPUT_DIR}/{filename}_preview_oscuro.png")
    # Sobre fondo crema
    bg_img2 = Image.new("RGB", (S, S), CREMA)
    bg_img2.paste(img_rgba, mask=img_rgba.split()[3])
    bg_img2.save(f"{OUTPUT_DIR}/{filename}_preview_claro.png")
    # PNG transparente (para usar en posts)
    img_rgba.save(f"{OUTPUT_DIR}/{filename}.png")
    print(f"OK  {filename}")

# ══════════════════════════════════════════════════════════════════════════════
#  V1 — CD EN CÍRCULO FINO (estilo exacto @clinicaholguera)
#  Las iniciales en serif dentro de un círculo delgado
# ══════════════════════════════════════════════════════════════════════════════
def v1_circulo():
    img  = new_canvas()
    draw = ImageDraw.Draw(img)

    # Círculo fino
    margin = 30
    draw.ellipse([margin, margin, S-margin, S-margin],
                 outline=DORADO, width=3)

    # Letras CD centradas
    f = font(170, "serif")
    txt = "CD"
    bb  = draw.textbbox((0,0), txt, font=f)
    tw, th = bb[2]-bb[0], bb[3]-bb[1]
    draw.text(((S-tw)//2, (S-th)//2 - 10), txt, font=f, fill=DORADO)

    save_preview(img, "v1_CD_circulo")

# ══════════════════════════════════════════════════════════════════════════════
#  V2 — C/D CON BARRA DIAGONAL (estilo firma / monograma tipo lujo)
# ══════════════════════════════════════════════════════════════════════════════
def v2_barra():
    img  = new_canvas()
    draw = ImageDraw.Draw(img)

    f_big  = font(200, "serif")
    f_small = font(110, "serif")

    # "C" a la izquierda
    draw.text((30, 80), "C", font=f_big, fill=DORADO)
    # Barra diagonal
    draw.line([(160, 50), (240, 350)], fill=DORADO, width=4)
    # "D" a la derecha, más abajo
    draw.text((220, 160), "D", font=f_big, fill=DORADO)

    save_preview(img, "v2_C_barra_D")

# ══════════════════════════════════════════════════════════════════════════════
#  V3 — CD APILADO VERTICAL CON LÍNEA SEPARADORA
# ══════════════════════════════════════════════════════════════════════════════
def v3_apilado():
    img  = new_canvas()
    draw = ImageDraw.Draw(img)

    f = font(160, "serif")

    # C arriba
    bb_c = draw.textbbox((0,0), "C", font=f)
    draw.text(((S-(bb_c[2]-bb_c[0]))//2, 50), "C", font=f, fill=DORADO)

    # Línea horizontal
    draw.line([(S//2 - 60, S//2), (S//2 + 60, S//2)], fill=DORADO, width=3)

    # D abajo
    bb_d = draw.textbbox((0,0), "D", font=f)
    draw.text(((S-(bb_d[2]-bb_d[0]))//2, S//2 + 20), "D", font=f, fill=DORADO)

    save_preview(img, "v3_CD_apilado")

# ══════════════════════════════════════════════════════════════════════════════
#  V4 — NOMBRE COMPLETO ABREVIADO EN CÍRCULO: "C.D." con puntos
# ══════════════════════════════════════════════════════════════════════════════
def v4_puntos():
    img  = new_canvas()
    draw = ImageDraw.Draw(img)

    # Círculo
    margin = 25
    draw.ellipse([margin, margin, S-margin, S-margin],
                 outline=DORADO, width=4)
    # Círculo interior decorativo
    margin2 = 40
    draw.ellipse([margin2, margin2, S-margin2, S-margin2],
                 outline=DORADO, width=1)

    # Texto C·D
    f = font(155, "serif")
    txt = "C\u00B7D"  # C·D con punto centrado
    bb  = draw.textbbox((0,0), txt, font=f)
    tw, th = bb[2]-bb[0], bb[3]-bb[1]
    draw.text(((S-tw)//2, (S-th)//2 - 8), txt, font=f, fill=DORADO)

    save_preview(img, "v4_CD_puntos_doble_circulo")

# ══════════════════════════════════════════════════════════════════════════════
#  V5 — SOLO "C" GRANDE CON "D" PEQUEÑA SUPERPUESTA (estilo lujo)
# ══════════════════════════════════════════════════════════════════════════════
def v5_superposicion():
    img  = new_canvas()
    draw = ImageDraw.Draw(img)

    # C grande
    f_big = font(280, "serif")
    bb    = draw.textbbox((0,0), "C", font=f_big)
    draw.text(((S-(bb[2]-bb[0]))//2 - 20, (S-(bb[3]-bb[1]))//2 - 20),
              "C", font=f_big, fill=(*DORADO, 255))

    # D pequeña superpuesta, desplazada
    f_small = font(120, "serif")
    bb2     = draw.textbbox((0,0), "D", font=f_small)
    draw.text(((S-(bb2[2]-bb2[0]))//2 + 55, (S-(bb2[3]-bb2[1]))//2 + 45),
              "D", font=f_small, fill=(*CREMA, 255))

    save_preview(img, "v5_C_grande_D_superpuesta")

# ══════════════════════════════════════════════════════════════════════════════
#  V6 — "carlos dueñas" EN MINÚSCULA ELEGANTE + LÍNEAS (estilo firma)
# ══════════════════════════════════════════════════════════════════════════════
def v6_firma():
    img  = new_canvas()
    draw = ImageDraw.Draw(img)

    # Línea superior
    draw.line([(60, 140), (S-60, 140)], fill=DORADO, width=2)

    # Texto en dos líneas
    f = font(72, "serif")
    for txt, y in [("carlos", 155), ("dueñas", 240)]:
        bb = draw.textbbox((0,0), txt, font=f)
        draw.text(((S-(bb[2]-bb[0]))//2, y), txt, font=f, fill=DORADO)

    # Línea inferior
    draw.line([(60, 330), (S-60, 330)], fill=DORADO, width=2)

    save_preview(img, "v6_nombre_completo_firma")

# ══════════════════════════════════════════════════════════════════════════════
#  V7 — CÍRCULO + "CD" EN SERIF + "ESTÉTICA MÉDICA" PEQUEÑO ALREDEDOR
# ══════════════════════════════════════════════════════════════════════════════
def v7_badge():
    img  = new_canvas()
    draw = ImageDraw.Draw(img)

    # Círculo exterior
    draw.ellipse([20, 20, S-20, S-20], outline=DORADO, width=3)

    # CD grande
    f_big = font(175, "serif")
    txt   = "CD"
    bb    = draw.textbbox((0,0), txt, font=f_big)
    draw.text(((S-(bb[2]-bb[0]))//2, (S-(bb[3]-bb[1]))//2 - 30),
              txt, font=f_big, fill=DORADO)

    # Línea separadora
    draw.line([(S//2 - 70, S//2 + 90), (S//2 + 70, S//2 + 90)],
              fill=DORADO, width=2)

    # Subtexto
    f_sub = font(30, "sans")
    sub   = "ESTÉTICA MÉDICA"
    bb2   = draw.textbbox((0,0), sub, font=f_sub)
    draw.text(((S-(bb2[2]-bb2[0]))//2, S//2 + 104), sub, font=f_sub, fill=DORADO)

    save_preview(img, "v7_badge_estetica_medica")


# ── EJECUTAR TODOS ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Generando monogramas...\n")
    v1_circulo()
    v2_barra()
    v3_apilado()
    v4_puntos()
    v5_superposicion()
    v6_firma()
    v7_badge()
    print(f"\nMonogramas guardados en: {OUTPUT_DIR}/")
    print("Cada variante tiene 3 archivos:")
    print("  *_preview_oscuro.png  → cómo se ve sobre fondo marrón")
    print("  *_preview_claro.png   → cómo se ve sobre fondo crema")
    print("  *.png                 → PNG transparente para usar en posts")
