"""
chatbot.py

Motor del asistente virtual de Seoul Glow: un chatbot basado en reglas
construido con NLTK (RegexpTokenizer + SnowballStemmer) sobre la base de
conocimiento definida en intenciones.py.

Nota de implementacion: el patron visto en clase usa nltk.word_tokenize()
y nltk.corpus.stopwords, que requieren descargar los paquetes "punkt_tab"
y "stopwords" la primera vez. En el entorno donde desarrolle y probe este
cuaderno esa descarga no estaba disponible (una politica de red bloquea la
descarga automatica de NLTK), asi que adapte el pipeline con dos piezas de
NLTK que no dependen de un corpus descargado:
  - nltk.tokenize.RegexpTokenizer, para tokenizar por reglas (expresion
    regular), y
  - nltk.stem.SnowballStemmer("spanish"), que es puramente algoritmico.
Para las stopwords uso una lista propia (STOPWORDS_ES) en vez de
nltk.corpus.stopwords. La logica de deteccion (interseccion de raices)
es la misma que se explico en clase.
"""

import re
import unicodedata
import random

import pandas as pd
from nltk.tokenize import RegexpTokenizer
from nltk.stem import SnowballStemmer

from intenciones import (
    INTENCIONES, FALLBACK, PALABRAS_ALERTA, MENSAJE_ALERTA,
    TIPO_PIEL, PRODUCTOS, INGREDIENTES, PRECIOS, RUTINAS, INFO_INGREDIENTES,
)

_tokenizer = RegexpTokenizer(r"[a-zA-Z0-9áéíóúñ]+")
_stemmer = SnowballStemmer("spanish")

STOPWORDS_ES = {
    "a", "al", "algo", "algunas", "algunos", "ante", "antes", "como", "con",
    "contra", "cual", "cuando", "de", "del", "desde", "donde", "durante",
    "e", "el", "ella", "ellas", "ellos", "en", "entre", "era", "erais",
    "eramos", "eran", "eres", "es", "esa", "esas", "ese", "eso", "esos",
    "esta", "estaba", "estado", "estamos", "estan", "estar", "este",
    "esto", "estos", "fue", "fueron", "ha", "hace", "hacia", "han", "hay",
    "la", "las", "le", "les", "lo", "los", "me", "mi", "mis", "mucho",
    "muy", "nos", "nosotros", "o", "os", "otra", "otro", "para", "pero",
    "poco", "por", "porque", "que", "quien", "se", "ser", "si", "sin",
    "sobre", "soy", "su", "sus", "te", "tu", "tus", "un", "una", "uno",
    "unos", "y", "ya", "yo",
}


def normalizar(texto: str) -> str:
    """Minusculas y sin acentos, igual que el normalizar() de clase."""
    texto = texto.lower()
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    return texto


def preprocesar(texto: str) -> list:
    """normaliza -> tokeniza (regex) -> quita stopwords -> raiz (stem)."""
    tokens = _tokenizer.tokenize(normalizar(texto))
    return [_stemmer.stem(t) for t in tokens if t not in STOPWORDS_ES]


# Vocabulario de raices por intencion (se calcula una sola vez a partir de
# los ejemplos de intenciones.py).
VOCAB = {
    nombre: {raiz for ejemplo in datos["ejemplos"] for raiz in preprocesar(ejemplo)}
    for nombre, datos in INTENCIONES.items()
}


def detectar_intencion(mensaje: str, umbral: int = 1) -> str:
    """Compara las raices del mensaje contra el vocabulario de cada
    intencion y se queda con la de mas coincidencias. Si nadie llega al
    umbral, regresa 'fallback'."""
    raices_msg = set(preprocesar(mensaje))
    puntajes = {nombre: len(raices_msg & vocab) for nombre, vocab in VOCAB.items()}
    mejor = max(puntajes, key=puntajes.get)
    return mejor if puntajes[mejor] >= umbral else "fallback"


def _buscar_en_diccionario(texto_normalizado: str, diccionario: dict):
    for clave, sinonimos in diccionario.items():
        if any(re.search(rf"\b{re.escape(s)}\b", texto_normalizado) for s in sinonimos):
            return clave
    return None


def extraer_entidades(mensaje: str) -> dict:
    """Entidades por diccionario de sinonimos (tipo de piel, producto,
    ingrediente) + una entidad por regex (numero de pedido, 6 digitos)."""
    texto = normalizar(mensaje)
    entidades = {}

    tipo_piel = _buscar_en_diccionario(texto, TIPO_PIEL)
    if tipo_piel:
        entidades["tipo_piel"] = tipo_piel

    producto = _buscar_en_diccionario(texto, PRODUCTOS)
    if producto:
        entidades["producto"] = producto

    ingrediente = _buscar_en_diccionario(texto, INGREDIENTES)
    if ingrediente:
        entidades["ingrediente"] = ingrediente

    pedido = re.search(r"\b\d{6}\b", texto)
    if pedido:
        entidades["numero_pedido"] = pedido.group()

    return entidades


def detectar_alerta(mensaje: str) -> bool:
    texto = normalizar(mensaje)
    return any(p in texto for p in PALABRAS_ALERTA)


historial = []


def responder(mensaje: str) -> str:
    """Genera la respuesta del bot y registra el turno en el historial
    (igual rol que el historial del ejemplo de clase: sirve de contexto
    y de evidencia de ejecucion)."""
    if detectar_alerta(mensaje):
        intencion = "alerta_seguridad"
        entidades = extraer_entidades(mensaje)
        respuesta = MENSAJE_ALERTA
    else:
        intencion = detectar_intencion(mensaje)
        entidades = extraer_entidades(mensaje)

        if intencion == "fallback":
            respuesta = FALLBACK

        elif intencion == "consultar_rutina":
            tipo = entidades.get("tipo_piel")
            if tipo in RUTINAS:
                respuesta = f"Para piel {tipo.replace('_', ' ')}: {RUTINAS[tipo]}"
            else:
                respuesta = (
                    "Cuentame, tu piel es grasa, seca, mixta, sensible o "
                    "con tendencia a acne? Asi te paso la rutina adecuada."
                )

        elif intencion == "consultar_ingredientes":
            ingr = entidades.get("ingrediente")
            if ingr in INFO_INGREDIENTES:
                respuesta = INFO_INGREDIENTES[ingr]
            else:
                respuesta = (
                    "Sobre que ingrediente quieres saber? Por ejemplo "
                    "niacinamida, acido hialuronico, centella asiatica, "
                    "mucina de caracol, retinol o vitamina C."
                )

        elif intencion == "consultar_precio":
            prod = entidades.get("producto")
            if prod in PRECIOS:
                respuesta = f"El {prod.replace('_', ' ')} cuesta ${PRECIOS[prod]} MXN."
            else:
                respuesta = (
                    "De que producto quieres el precio? limpiador, tonico, "
                    "serum, mascarilla, protector solar o crema."
                )

        elif intencion == "consultar_envio":
            respuesta = (
                "Hacemos envios a todo Mexico: llegan en 3 a 5 dias "
                "habiles con guia rastreable. El envio cuesta $99 MXN y es "
                "gratis en compras mayores a $800 MXN."
            )

        elif intencion == "soporte_posventa":
            pedido = entidades.get("numero_pedido")
            if pedido:
                respuesta = (
                    f"Ya tengo tu pedido {pedido}. Cuentame que paso "
                    "(producto incompleto, cambio o devolucion) y te doy "
                    "los siguientes pasos; tienes 5 dias desde que lo "
                    "recibiste para cambios o devoluciones."
                )
            else:
                respuesta = (
                    "Para ayudarte con tu cambio, devolucion o pedido, "
                    "pasame tu numero de pedido (6 digitos)."
                )

        else:
            respuesta = random.choice(INTENCIONES[intencion]["respuestas"])

    historial.append({
        "usuario": mensaje,
        "intencion": intencion,
        "entidades": entidades,
        "bot": respuesta,
    })
    return respuesta


def historial_df() -> pd.DataFrame:
    return pd.DataFrame(historial)


def chat():
    """Loop interactivo para probar el bot a mano (pensado para Colab)."""
    print("Bot:", responder("hola"))
    while True:
        mensaje = input("Tu: ")
        if mensaje.strip().lower() in ("salir", "exit"):
            break
        print("Bot:", responder(mensaje))
        if historial[-1]["intencion"] == "despedida":
            break


if __name__ == "__main__":
    chat()
