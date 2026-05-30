#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera el manual de marca de Terra Home en PDF (maquetado)."""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table,
    TableStyle, NextPageTemplate, PageBreak, ListFlowable, ListItem, KeepTogether
)
from reportlab.lib.styles import ParagraphStyle

# ---- Paleta de marca ----
GOLD   = HexColor("#B5946A")
CHOCO  = HexColor("#4A3A2C")
BEIGE  = HexColor("#E7DCCB")
CREMA  = HexColor("#F6F1E8")
SAND   = HexColor("#D8C7AE")
GREYTX = HexColor("#5E5246")

PAGE_W, PAGE_H = A4
SERIF = "Times-Roman"
SERIF_B = "Times-Bold"
SERIF_I = "Times-Italic"
SANS = "Helvetica"
SANS_B = "Helvetica-Bold"

# ---------------- estilos ----------------
def style(name, **kw):
    return ParagraphStyle(name, **kw)

H_SECTION = style("sec", fontName=SERIF_B, fontSize=20, textColor=GOLD,
                  spaceAfter=2, spaceBefore=4, leading=23)
H_KICKER  = style("kick", fontName=SANS_B, fontSize=8, textColor=SAND,
                  spaceAfter=10, leading=10, tracking=2)
H_SUB     = style("sub", fontName=SANS_B, fontSize=10.5, textColor=CHOCO,
                  spaceBefore=10, spaceAfter=4, leading=13)
BODY      = style("body", fontName=SANS, fontSize=9.5, textColor=GREYTX,
                  leading=15, spaceAfter=6, alignment=TA_LEFT)
BODY_C    = style("bodyc", parent=BODY, alignment=TA_CENTER)
QUOTE     = style("quote", fontName=SERIF_I, fontSize=14, textColor=GOLD,
                  leading=19, alignment=TA_CENTER, spaceBefore=4, spaceAfter=12)
BULLET    = style("bullet", fontName=SANS, fontSize=9.5, textColor=GREYTX, leading=14)
CELL      = style("cell", fontName=SANS, fontSize=8.5, textColor=GREYTX, leading=12)
CELL_B    = style("cellb", fontName=SANS_B, fontSize=8.5, textColor=CHOCO, leading=12)
CELL_W    = style("cellw", fontName=SANS_B, fontSize=9, textColor=white, leading=12)
SWATCH_HX = style("hx", fontName="Courier", fontSize=8.5, textColor=GREYTX, leading=12)

def bullets(items, color=GOLD):
    return ListFlowable(
        [ListItem(Paragraph(t, BULLET), value="•", leftIndent=12) for t in items],
        bulletType="bullet", bulletColor=color, bulletFontSize=8,
        leftIndent=10, spaceBefore=2, spaceAfter=6,
    )

# ---------------- páginas con fondo ----------------
def bg(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(white)
    canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    # franja superior fina dorada
    canvas.setFillColor(CREMA)
    canvas.rect(0, PAGE_H-18*mm, PAGE_W, 18*mm, fill=1, stroke=0)
    canvas.setStrokeColor(GOLD)
    canvas.setLineWidth(0.6)
    canvas.line(20*mm, PAGE_H-18*mm, PAGE_W-20*mm, PAGE_H-18*mm)
    # encabezado
    canvas.setFont(SERIF, 9)
    canvas.setFillColor(GOLD)
    canvas.drawString(20*mm, PAGE_H-12*mm, "TERRA HOME")
    canvas.setFont(SANS, 7.5)
    canvas.setFillColor(SAND)
    canvas.drawRightString(PAGE_W-20*mm, PAGE_H-12*mm, "Manual de Marca")
    # pie
    canvas.setStrokeColor(BEIGE)
    canvas.setLineWidth(0.5)
    canvas.line(20*mm, 14*mm, PAGE_W-20*mm, 14*mm)
    canvas.setFont(SANS, 7.5)
    canvas.setFillColor(SAND)
    canvas.drawString(20*mm, 10*mm, "Aromas para tus espacios")
    canvas.drawRightString(PAGE_W-20*mm, 10*mm, str(canvas.getPageNumber()-1))
    canvas.restoreState()

def draw_monogram(canvas, cx, cy, h, color):
    """Monograma estilizado LH (dos astas + travesaño con curva)."""
    canvas.saveState()
    canvas.setStrokeColor(color); canvas.setFillColor(color)
    bw = h*0.16
    gap = h*0.42
    # asta izquierda (L) con base
    canvas.rect(cx-gap-bw/2, cy, bw, h, fill=1, stroke=0)
    canvas.rect(cx-gap-bw/2, cy, gap*0.9, bw*0.9, fill=1, stroke=0)
    # asta derecha (H)
    canvas.rect(cx+gap-bw/2, cy, bw, h, fill=1, stroke=0)
    # travesaño curvo uniendo ambas
    canvas.setLineWidth(bw*0.55)
    p = canvas.beginPath()
    p.moveTo(cx-gap+bw/2, cy+h*0.46)
    p.curveTo(cx-h*0.04, cy+h*0.40, cx+h*0.02, cy+h*0.52, cx+gap-bw/2, cy+h*0.46)
    canvas.drawPath(p, stroke=1, fill=0)
    canvas.restoreState()

def cover(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(CREMA)
    canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    # marco doble fino dorado
    canvas.setStrokeColor(GOLD); canvas.setLineWidth(0.8)
    canvas.rect(16*mm, 16*mm, PAGE_W-32*mm, PAGE_H-32*mm, fill=0, stroke=1)
    canvas.setLineWidth(0.4)
    canvas.rect(18*mm, 18*mm, PAGE_W-36*mm, PAGE_H-36*mm, fill=0, stroke=1)

    draw_monogram(canvas, PAGE_W/2, PAGE_H/2+18*mm, 42*mm, GOLD)

    def spaced(text, font, size, color, y, tracking):
        w = canvas.stringWidth(text, font, size) + tracking*(len(text)-1)
        t = canvas.beginText(PAGE_W/2 - w/2, y)
        t.setFont(font, size); t.setFillColor(color); t.setCharSpace(tracking)
        t.textOut(text)
        canvas.drawText(t)

    spaced("TERRA HOME", SERIF, 30, CHOCO, PAGE_H/2-12*mm, 8)
    canvas.setStrokeColor(GOLD); canvas.setLineWidth(0.7)
    canvas.line(PAGE_W/2-30*mm, PAGE_H/2-20*mm, PAGE_W/2+30*mm, PAGE_H/2-20*mm)
    spaced("AROMAS PARA TUS ESPACIOS", SANS, 9, GOLD, PAGE_H/2-28*mm, 4)

    spaced("MANUAL DE MARCA", SANS_B, 8, SAND, 40*mm, 3)
    canvas.setFont(SERIF_I, 12); canvas.setFillColor(GOLD)
    canvas.drawCentredString(PAGE_W/2, 30*mm, "“La primera sensación al entrar a casa importa.”")
    canvas.restoreState()

# ---------------- helpers de contenido ----------------
def section(title, kicker):
    return [Paragraph(kicker.upper(), H_KICKER), Paragraph(title, H_SECTION),
            Spacer(1, 4)]

def palette_table():
    rows = [
        ("Terra Gold", "#B5946A", "181 · 148 · 106", "Acento principal, logo, detalles", GOLD, white),
        ("Chocolate",  "#4A3A2C", "74 · 58 · 44",    "Texto de contraste, packaging",  CHOCO, white),
        ("Beige / Arena","#E7DCCB","231 · 220 · 203", "Base cálida, fondos",            BEIGE, CHOCO),
        ("Crema / Lino","#F6F1E8", "246 · 241 · 232", "Fondos suaves, aire",            CREMA, CHOCO),
        ("Blanco",     "#FFFFFF", "255 · 255 · 255",  "Fondo principal, limpieza",      white, CHOCO),
    ]
    data = []
    styles = [
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("LINEBELOW",(1,0),(-1,-2),0.4,BEIGE),
        ("TOPPADDING",(0,0),(-1,-1),7),
        ("BOTTOMPADDING",(0,0),(-1,-1),7),
        ("LEFTPADDING",(1,0),(-1,-1),8),
        ("BOX",(0,0),(0,-1),0.5,white),
    ]
    for i,(name,hx,rgb,use,col,txt) in enumerate(rows):
        data.append([
            Paragraph(name, CELL_W if txt==white else style("sw",fontName=SANS_B,fontSize=9,textColor=CHOCO)),
            Paragraph(name, CELL_B), Paragraph(hx, SWATCH_HX),
            Paragraph(rgb, CELL), Paragraph(use, CELL),
        ])
        styles.append(("BACKGROUND",(0,i),(0,i),col))
        if col==white or col==CREMA:
            styles.append(("BOX",(0,i),(0,i),0.5,BEIGE))
    t = Table(data, colWidths=[34*mm, 28*mm, 24*mm, 28*mm, 56*mm])
    t.setStyle(TableStyle(styles))
    return t

def type_table():
    data = [
        [Paragraph("Tipografía", CELL_B), Paragraph("Rol", CELL_B), Paragraph("Uso", CELL_B)],
        [Paragraph("<b>Symphony</b><br/><font size=7 color='#B5946A'>script · caligráfica</font>", CELL),
         Paragraph("Nombres de aromas y titulares emotivos", CELL),
         Paragraph("“Salón de Rosas”, “Jardines Blancos”. Con moderación, para momentos especiales.", CELL)],
        [Paragraph("<b>The Seasons</b><br/><font size=7 color='#B5946A'>serif elegante</font>", CELL),
         Paragraph("Títulos y nombre de marca", CELL),
         Paragraph("Encabezados, “TERRA HOME”. Mayúsculas con buen espaciado.", CELL)],
        [Paragraph("<b>Glacial Indifference</b><br/><font size=7 color='#B5946A'>sans serif</font>", CELL),
         Paragraph("Cuerpo de texto", CELL),
         Paragraph("Descripciones, precios, datos. Limpia y legible. La más usada.", CELL)],
    ]
    t = Table(data, colWidths=[44*mm, 44*mm, 82*mm])
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),BEIGE),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("TOPPADDING",(0,0),(-1,-1),8),("BOTTOMPADDING",(0,0),(-1,-1),8),
        ("LEFTPADDING",(0,0),(-1,-1),8),
        ("LINEBELOW",(0,0),(-1,-1),0.4,BEIGE),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[white, CREMA]),
    ]))
    return t

def two_col(left_title, left_items, right_title, right_items):
    def cell(title, items, c):
        flow = [Paragraph(title, style("tc",fontName=SANS_B,fontSize=9.5,textColor=c,spaceAfter=4))]
        flow += [Paragraph("• "+i, BULLET) for i in items]
        return flow
    t = Table([[cell(left_title,left_items,GOLD), cell(right_title,right_items,CHOCO)]],
              colWidths=[85*mm, 85*mm])
    t.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"TOP"),
        ("LEFTPADDING",(0,0),(0,0),0),("LEFTPADDING",(1,0),(1,0),10),
        ("BACKGROUND",(0,0),(0,0),CREMA),("BACKGROUND",(1,0),(1,0),CREMA),
        ("TOPPADDING",(0,0),(-1,-1),10),("BOTTOMPADDING",(0,0),(-1,-1),10),
        ("LEFTPADDING",(0,0),(-1,-1),12),("RIGHTPADDING",(0,0),(-1,-1),12)]))
    return t

# ---------------- documento ----------------
def build(path):
    doc = BaseDocTemplate(path, pagesize=A4,
                          leftMargin=20*mm, rightMargin=20*mm,
                          topMargin=24*mm, bottomMargin=20*mm)
    frame = Frame(doc.leftMargin, doc.bottomMargin,
                  doc.width, doc.height, id="main")
    doc.addPageTemplates([
        PageTemplate(id="cover", frames=[frame], onPage=cover),
        PageTemplate(id="content", frames=[frame], onPage=bg),
    ])
    S = []
    S.append(NextPageTemplate("content"))
    S.append(PageBreak())

    # 1. Esencia
    S += section("Esencia de marca", "01 — Quiénes somos")
    S.append(Paragraph("Terra Home", H_SUB))
    S.append(Paragraph("Marca de aromas para el hogar: <b>home sprays, difusores, velas y "
        "complementos</b>. No vendemos perfume de ambiente: vendemos el momento de entrar a un "
        "espacio y sentirse en casa. Bienestar, calma y belleza cotidiana.", BODY))
    S.append(Paragraph("Propósito y promesa", H_SUB))
    S.append(Paragraph("Transformar los espacios y los momentos cotidianos a través del aroma. "
        "Aromas que elevan lo de todos los días: sofisticados, pero cercanos.", BODY))
    S.append(Paragraph("Valores", H_SUB))
    S.append(bullets([
        "<b>Calidez</b> — sensación de hogar, refugio, intimidad.",
        "<b>Elegancia natural</b> — sofisticación sin estridencia; lujo silencioso.",
        "<b>Sensorialidad</b> — todo gira en torno a lo que se huele, se ve y se siente.",
        "<b>Detalle y cuidado</b> — desde la etiqueta hasta la bolsa de entrega.",
    ]))
    S.append(Paragraph("Cliente ideal", H_SUB))
    S.append(bullets([
        "Personas que <b>cuidan la estética de sus espacios</b> y quieren que su casa se vea y se sienta linda.",
        "<b>Negocios</b> (locales, estudios, showrooms) que quieren un aroma de identidad.",
    ]))
    S.append(PageBreak())

    # 2. Personalidad
    S += section("Personalidad y tono de voz", "02 — Cómo nos expresamos")
    S.append(Paragraph("Arquetipo: el Cuidador + el Esteta. Terra Home cuida, embellece y crea atmósfera.", BODY))
    S.append(Spacer(1,4))
    S.append(two_col(
        "La marca SÍ es", ["Cálida y serena","Elegante y delicada","Cercana y amable",
                           "Sensorial y evocadora","Aspiracional pero accesible"],
        "La marca NO es", ["Fría o impersonal","Recargada o estridente","Distante o acartonada",
                           "Técnica o aburrida","Ostentosa o snob"]))
    S.append(Paragraph("Tono de voz", H_SUB))
    S.append(bullets([
        "Tono suave, sensorial y evocador. Describí <b>sensaciones</b>, no ingredientes.",
        "Frases cortas y cuidadas. Invitá a imaginar el aroma.",
        "Trato cercano sin perder elegancia.",
    ]))
    S.append(Paragraph("<font color='#7a9a6a'>✓</font>  “Jardines Blancos. Luminoso y sutil, "
        "como la primera luz de la mañana.”", BODY))
    S.append(Paragraph("<font color='#b56a6a'>✗</font>  “Producto fragancia ambiente 300ml con "
        "esencia importada de alta concentración.”", BODY))
    S.append(PageBreak())

    # 3. Logo
    S += section("Logotipo", "03 — Nuestro símbolo")
    S.append(Paragraph("Monograma <b>“LH”</b> entrelazado acompañado del nombre TERRA HOME en "
        "serif vertical. Es el activo visual más reconocible de la marca.", BODY))
    S.append(Paragraph("Versiones", H_SUB))
    S.append(bullets([
        "<b>Principal:</b> dorado/camel sobre fondo claro (beige, crema o blanco).",
        "<b>Sobre foto / fondo oscuro:</b> versión en blanco.",
        "<b>Monocromo chocolate:</b> cuando no se puede imprimir el dorado.",
        "<b>Isotipo solo:</b> el monograma sin texto, para avatar, sellos, marca de agua y favicon.",
    ]))
    S.append(Paragraph("Área de protección", H_SUB))
    S.append(Paragraph("Dejá un margen libre mínimo equivalente al ancho de la “H” del monograma. "
        "Nada debe invadir ese espacio.", BODY))
    S.append(Paragraph("Usos incorrectos", H_SUB))
    S.append(bullets([
        "No lo estires ni deformes.  ·  No rotes el monograma.",
        "No le cambies el color fuera de la paleta.",
        "No lo pongas sobre fondos cargados o con poco contraste.",
        "No le agregues sombras, contornos ni efectos.",
    ], color=HexColor("#b56a6a")))
    S.append(PageBreak())

    # 4. Paleta
    S += section("Paleta de colores", "04 — Nuestros colores")
    S.append(Paragraph("Paleta neutra, cálida y natural: base beige/crema, acento dorado-tierra y "
        "contraste chocolate.", BODY))
    S.append(Spacer(1,4))
    S.append(palette_table())
    S.append(Spacer(1,10))
    S.append(Paragraph("Proporción 60-30-10", H_SUB))
    S.append(bullets([
        "<b>60%</b> blanco + crema (respiración, fondos).",
        "<b>30%</b> beige / arena (calidez, base).",
        "<b>10%</b> dorado + chocolate (acentos, texto, logo).",
    ]))
    S.append(Paragraph("<i>Los HEX son una aproximación tomada de las imágenes de la marca. "
        "Si existen los valores exactos del diseñador, reemplazarlos.</i>",
        style("note",parent=BODY,fontName=SERIF_I,textColor=SAND,fontSize=8.5)))
    S.append(PageBreak())

    # 5. Tipografía
    S += section("Tipografía", "05 — Nuestras letras")
    S.append(Paragraph("Tres tipografías con roles definidos. No mezclar más de estas tres.", BODY))
    S.append(Spacer(1,4))
    S.append(type_table())
    S.append(Paragraph("Reglas", H_SUB))
    S.append(bullets([
        "Symphony nunca en bloques largos ni en mayúsculas: pierde legibilidad.",
        "The Seasons en mayúsculas con buen espaciado entre letras para titulares.",
        "Glacial Indifference para todo lo funcional. Es la que más se usa.",
    ]))
    S.append(PageBreak())

    # 6. Dirección de arte
    S += section("Dirección de arte y fotografía", "06 — Cómo nos vemos")
    S.append(Paragraph("El estilo visual es el alma de Terra Home: cálido, natural, minimalista y luminoso.", BODY))
    S.append(Paragraph("Principios", H_SUB))
    S.append(bullets([
        "<b>Luz natural</b> suave y abundante. Nada de luz dura ni flashes.",
        "<b>Fondos neutros y limpios:</b> paredes blancas, madera clara, mármol, lino.",
        "<b>Mucho aire:</b> composiciones respiradas, sin saturar.",
        "<b>Naturaleza viva:</b> flores frescas, hojas verdes grandes, ramas, plantas.",
        "<b>Texturas cálidas:</b> madera, mármol, lino, papel kraft, resina ámbar.",
        "<b>El producto protagonista</b>, integrado en escenas reales de hogar.",
    ]))
    S.append(Paragraph("Edición", H_SUB))
    S.append(Paragraph("Tonos tierra, beige, verde follaje y blanco. Cálida y luminosa, con sombras "
        "suaves. Evitar filtros fríos, azulados o muy saturados.", BODY))
    S.append(Paragraph("Firma visual recurrente", H_SUB))
    S.append(bullets([
        "Bandeja de mármol con el producto + tela de lino.",
        "Difusor junto a flores frescas o un libro.",
        "Manos sosteniendo el producto.  ·  Plantas de hoja grande de fondo.",
        "Detalle de la etiqueta dorada.",
    ]))
    S.append(PageBreak())

    # 7. Nomenclatura
    S += section("Nomenclatura de aromas", "07 — Cómo nombramos")
    S.append(Paragraph("Los aromas se nombran como <b>lugares y escenas evocadoras</b>, no de forma "
        "genérica. Es un activo muy fuerte de la marca.", BODY))
    S.append(Paragraph("Ejemplos:", H_SUB))
    S.append(bullets([
        "<i>Salón de Rosas</i> — Maderas preciosas · Rosa · Muguet · Magnolias",
        "<i>Jardines Blancos</i> — “Luminoso y sutil”",
        "<i>Galería de Té</i>   ·   <i>Margarita Dulce</i>   ·   <i>Prosperidad</i> (vela)",
    ]))
    S.append(Paragraph("Fórmula", H_SUB))
    S.append(Paragraph("Nombre poético en <b>Symphony</b> + nota descriptiva breve y sensorial debajo. "
        "Cada aroma puede tener una mini-frase de carácter (“Luminoso y sutil”, “Cálido y envolvente”).", BODY))
    S.append(Paragraph("Categorías", H_SUB))
    S.append(bullets([
        "Home Spray (250/300 ml + Refill 300 ml)",
        "Difusores (con varillas)  ·  Velas  ·  Complementos / sets de regalo",
    ]))
    S.append(PageBreak())

    # 8. Aplicaciones + checklist
    S += section("Aplicaciones", "08 — La marca en acción")
    S.append(Paragraph("Instagram (@terradecco)", H_SUB))
    S.append(bullets([
        "<b>Bio:</b> esencia + categorías + envíos + link a la tienda.",
        "<b>Feed:</b> alternar producto / escena de hogar / persona, cuidando la coherencia del mosaico.",
        "<b>Destacadas:</b> portadas beige con isotipo o ícono fino dorado.",
    ]))
    S.append(Paragraph("Packaging y etiquetas", H_SUB))
    S.append(bullets([
        "Bolsa kraft con el logo en blanco o chocolate (eco).",
        "Etiquetas: fondo claro, marco fino dorado, monograma arriba, nombre en Symphony, "
        "categoría en serif espaciada abajo.",
        "Acabados: dorado mate, papeles de textura natural, sello del isotipo.",
    ]))
    S.append(Paragraph("Tienda online", H_SUB))
    S.append(Paragraph("terrahome4.mitiendanube.com — misma paleta, tipografías y estilo fotográfico "
        "para coherencia total con redes.", BODY))

    S.append(Spacer(1,8))
    chk = [Paragraph("Checklist de coherencia", style("chk",fontName=SANS_B,fontSize=10.5,textColor=CHOCO,spaceAfter=6))]
    for t in ["¿Usa solo los colores de la paleta?",
              "¿Usa solo las 3 tipografías, con sus roles correctos?",
              "¿El logo tiene aire alrededor y buen contraste?",
              "¿La foto es luminosa, cálida y con fondo limpio?",
              "¿El texto suena sensorial, cálido y cercano?",
              "¿Se siente Terra Home: elegante, natural y serena?"]:
        chk.append(Paragraph("<font color='#B5946A'>☐</font>  "+t, BODY))
    box = Table([[chk]], colWidths=[170*mm])
    box.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),CREMA),
        ("BOX",(0,0),(-1,-1),0.6,GOLD),
        ("TOPPADDING",(0,0),(-1,-1),12),("BOTTOMPADDING",(0,0),(-1,-1),12),
        ("LEFTPADDING",(0,0),(-1,-1),14),("RIGHTPADDING",(0,0),(-1,-1),14)]))
    S.append(KeepTogether(box))

    doc.build(S)

if __name__ == "__main__":
    build("/home/user/repositorio-henry/Manual-de-Marca-Terra-Home.pdf")
    print("PDF generado.")
