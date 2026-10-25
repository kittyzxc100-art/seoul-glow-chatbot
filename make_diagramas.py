"""
make_diagramas.py

Genera las dos imagenes de diseno para el documento:
  1. diagrama_arquitectura.png -> Usuario, Chatbot (con su pipeline
     interno), Base de conocimiento y Flujo conversacional, con flechas
     que muestran el intercambio de informacion entre ellos.
  2. diagrama_flujo.png -> las 7 etapas del flujo conversacional, con la
     salida hacia fallback cuando no se reconoce la intencion.

Mismo tema rosa usado en el resto del curso.
"""

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.lines import Line2D

ROSA_OSCURO = "#800f2f"
ROSA_FUERTE = "#c9184a"
ROSA_MEDIO = "#e75480"
ROSA_CLARO = "#f7a1c4"
ROSA_PASTEL = "#ffb3c6"
GRIS_TEXTO = "#4a2733"


def caja(ax, xy, w, h, texto, color, fontsize=10.5, fontweight="bold", text_color="white"):
    box = FancyBboxPatch(
        xy, w, h,
        boxstyle="round,pad=0.02,rounding_size=0.08",
        linewidth=1.4, edgecolor=ROSA_OSCURO, facecolor=color,
    )
    ax.add_patch(box)
    ax.text(
        xy[0] + w / 2, xy[1] + h / 2, texto,
        ha="center", va="center", fontsize=fontsize, fontweight=fontweight,
        color=text_color, wrap=True,
    )
    return box


def flecha(ax, p1, p2, color=ROSA_OSCURO, estilo="-|>", conn="arc3,rad=0.0", lw=1.8, ls="solid"):
    arrow = FancyArrowPatch(
        p1, p2, arrowstyle=estilo, mutation_scale=16,
        linewidth=lw, color=color, connectionstyle=conn, linestyle=ls,
    )
    ax.add_patch(arrow)


# ---------------------------------------------------------------------------
# 1. Arquitectura conceptual
# ---------------------------------------------------------------------------

fig, ax = plt.subplots(figsize=(11, 7.5))
ax.set_xlim(0, 11)
ax.set_ylim(0, 8)
ax.axis("off")
ax.set_title(
    "Arquitectura conceptual del asistente virtual de Seoul Glow",
    fontsize=15, fontweight="bold", color=ROSA_OSCURO, pad=14,
)

# Usuario (arriba a la izquierda)
caja(ax, (0.4, 6.0), 2.6, 1.4, "Usuario\n\nEscribe su pregunta\n(web / WhatsApp)", ROSA_MEDIO, fontsize=10)

# Chatbot (centro, caja grande con el pipeline interno)
caja(ax, (3.6, 4.6), 5.0, 2.9, "", ROSA_FUERTE)
ax.text(6.1, 7.15, "Chatbot (Python + NLTK)", ha="center", fontsize=12,
        fontweight="bold", color="white")

pasos = ["preprocesar()", "detectar_intencion()", "extraer_entidades()", "responder() + fallback"]
for i, paso in enumerate(pasos):
    y = 6.65 - i * 0.55
    caja(ax, (3.9, y), 4.4, 0.42, paso, ROSA_PASTEL, fontsize=9.5,
         fontweight="normal", text_color=GRIS_TEXTO)

# Base de conocimiento (derecha)
caja(ax, (9.0, 4.6), 1.7, 2.9, "Base de\nconocimiento\n\nintenciones,\nentidades,\nprecios,\nrutinas", ROSA_CLARO,
     fontsize=9.5, text_color=GRIS_TEXTO)

# Flujo conversacional (abajo)
caja(ax, (3.1, 1.1), 5.6, 1.5, "Flujo conversacional\n\nSaludo -> Necesidad -> Intencion -> Datos ->\nRespuesta/Accion -> Confirmacion -> Cierre",
     ROSA_OSCURO, fontsize=9.5)

# Flechas: Usuario <-> Chatbot
flecha(ax, (1.7, 6.0), (3.6, 6.3), color=ROSA_OSCURO, conn="arc3,rad=-0.15")
ax.text(2.55, 6.55, "mensaje de texto", fontsize=8.5, color=GRIS_TEXTO, rotation=8)
flecha(ax, (3.6, 5.6), (1.7, 5.75), color=ROSA_OSCURO, conn="arc3,rad=-0.15")
ax.text(2.4, 5.2, "respuesta generada", fontsize=8.5, color=GRIS_TEXTO)

# Flechas: Chatbot <-> Base de conocimiento
flecha(ax, (8.6, 6.3), (9.0, 6.3), color=ROSA_OSCURO)
ax.text(8.55, 6.55, "consulta", fontsize=8.5, color=GRIS_TEXTO)
flecha(ax, (9.0, 5.7), (8.6, 5.7), color=ROSA_OSCURO)
ax.text(8.5, 5.4, "datos reales", fontsize=8.5, color=GRIS_TEXTO)

# Flechas: Chatbot <-> Flujo conversacional
flecha(ax, (5.3, 4.6), (5.3, 2.6), color=ROSA_OSCURO, conn="arc3,rad=-0.1")
ax.text(5.4, 3.6, "consulta etapa actual", fontsize=8.5, color=GRIS_TEXTO)
flecha(ax, (6.8, 2.6), (6.8, 4.6), color=ROSA_OSCURO, conn="arc3,rad=-0.1")
ax.text(6.9, 3.6, "actualiza estado", fontsize=8.5, color=GRIS_TEXTO)

plt.tight_layout()
plt.savefig("graficas/diagrama_arquitectura.png", dpi=150)
plt.close()


# ---------------------------------------------------------------------------
# 2. Flujo conversacional de 7 etapas
# ---------------------------------------------------------------------------

fig, ax = plt.subplots(figsize=(13, 4.2))
ax.set_xlim(0, 13.2)
ax.set_ylim(0, 4.2)
ax.axis("off")
ax.set_title("Flujo conversacional del asistente (7 etapas)", fontsize=14.5,
             fontweight="bold", color=ROSA_OSCURO, pad=10)

etapas = ["Saludo", "Necesidad", "Intencion", "Datos", "Respuesta\no accion", "Confirmacion", "Cierre"]
colores = [ROSA_MEDIO, ROSA_FUERTE, ROSA_OSCURO, ROSA_FUERTE, ROSA_MEDIO, ROSA_FUERTE, ROSA_OSCURO]
w, h, gap = 1.5, 1.2, 0.25
x0 = 0.3
for i, (etapa, color) in enumerate(zip(etapas, colores)):
    x = x0 + i * (w + gap)
    caja(ax, (x, 2.4), w, h, f"{i+1}. {etapa}", color, fontsize=9.3)
    if i < len(etapas) - 1:
        flecha(ax, (x + w, 3.0), (x + w + gap, 3.0))

# Rama de fallback desde "Intencion"
idx_intencion = 2
x_int = x0 + idx_intencion * (w + gap)
caja(ax, (x_int - 0.1, 0.25), w + 0.3, 1.0, "No se reconoce ->\nfallback que orienta", ROSA_PASTEL,
     fontsize=9, text_color=GRIS_TEXTO)
flecha(ax, (x_int + w / 2, 2.4), (x_int + w / 2 + 0.05, 1.25), color=ROSA_OSCURO,
       conn="arc3,rad=0.25", ls="dashed")

plt.tight_layout()
plt.savefig("graficas/diagrama_flujo.png", dpi=150)
plt.close()

print("Diagramas generados: graficas/diagrama_arquitectura.png, graficas/diagrama_flujo.png")
