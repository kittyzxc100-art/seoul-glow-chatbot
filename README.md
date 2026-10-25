# Asistente virtual de Seoul Glow

Chatbot basado en reglas (Python 3 + NLTK) para **Seoul Glow**, una boutique
en linea de skincare coreano. Responde las preguntas repetitivas que antes
saturaban el WhatsApp/Instagram del negocio: rutinas segun tipo de piel,
que hacen ciertos ingredientes, precios, tiempos de envio y cambios o
devoluciones. Si detecta palabras de una posible reaccion en la piel,
no da una recomendacion automatica: canaliza el caso a una persona.

Proyecto academico — Avance de proyecto 1, materia *Desarrollo de
aplicaciones con inteligencia artificial*, Universidad Tecmilenio.
Autora: Iris Bringas (matricula AL07302962).

## Que hace

1. **Preprocesa** el mensaje: minusculas, quita acentos, tokeniza con
   `nltk.tokenize.RegexpTokenizer` y reduce cada palabra a su raiz con
   `nltk.stem.SnowballStemmer("spanish")`.
2. **Detecta la intencion**: compara las raices del mensaje contra un
   vocabulario de raices por intencion (interseccion de conjuntos) y
   se queda con la de mas coincidencias; si ninguna llega al umbral,
   regresa `fallback`.
3. **Extrae entidades** (tipo de piel, producto, ingrediente, numero de
   pedido) con diccionarios de sinonimos y una expresion regular.
4. **Responde** combinando la intencion detectada con las entidades
   encontradas y datos reales del negocio (precios, rutinas,
   informacion de ingredientes).
5. Si el mensaje contiene palabras asociadas a una reaccion en la piel,
   se salta la clasificacion normal y canaliza el caso a una persona.

## Por que NLTK sin descargar corpus

El patron visto en clase usa `nltk.word_tokenize()` y
`nltk.corpus.stopwords`, que requieren descargar `punkt_tab` y
`stopwords` la primera vez. En el entorno donde desarrolle y probe este
proyecto esa descarga automatica no estaba disponible, asi que adapte el
pipeline con dos piezas de NLTK puramente algoritmicas que no dependen de
un corpus descargado (`RegexpTokenizer` y `SnowballStemmer`) y una lista
de stopwords en espaniol definida a mano. La logica de deteccion
(interseccion de raices) es la misma que se explico en clase.

## Estructura del repositorio

```
seoul-glow-chatbot/
├── README.md            este archivo
├── chatbot.ipynb         cuaderno de Colab, ya ejecutado de principio a fin
├── intenciones.py        base de conocimiento (intenciones, entidades, precios, rutinas)
├── chatbot.py             motor del chatbot (preprocesar, detectar_intencion, extraer_entidades, responder)
├── make_diagramas.py      genera los diagramas de arquitectura y de flujo
├── graficas/
│   ├── diagrama_arquitectura.png
│   └── diagrama_flujo.png
└── pruebas/
    ├── ejecutar_pruebas.py     corre 12 conversaciones y calcula metricas
    ├── casos.csv               resultado de esa corrida (mensaje, intencion detectada, esperada, correcto)
    └── evidencia_ejecucion.txt salida real de ejecutar_pruebas.py
```

## Como correrlo

**En Google Colab:** abre `chatbot.ipynb` y corre todas las celdas en
orden (Entorno de ejecucion -> Ejecutar todas). No necesita instalar nada
fuera de lo que ya trae Colab.

**En terminal / VS Code:**

```bash
pip install nltk pandas --break-system-packages
python3 chatbot.py              # chat interactivo
python3 pruebas/ejecutar_pruebas.py   # corre las 12 conversaciones de prueba y muestra metricas
```

## Resultados de la ultima corrida de pruebas

12 conversaciones (las 7 intenciones + alerta de seguridad + 2 mensajes
fuera de alcance):

- **Precision de intencion:** 92% (11/12)
- **Tasa de fallback:** 8%
- Unico error: *"Quiero cancelar mi contrato de telefonia"* se clasifico
  como `soporte_posventa` en vez de `fallback`, porque la raiz de
  "cancelar" tambien aparece en los ejemplos de esa intencion. Ver el
  analisis completo en el documento del Avance 1.

## Limitaciones conocidas y mejoras para el Avance 2

- El bot no entiende negaciones ni contexto entre turnos (cada mensaje se
  clasifica de forma independiente).
- Una palabra compartida entre intenciones puede generar una clasificacion
  incorrecta (ver el error de arriba).
- Para el Avance 2: agregar palabras que excluyan una intencion aunque
  haya coincidencia de raiz, subir el umbral minimo de coincidencias, y
  dar memoria de los ultimos turnos para manejar seguimientos
  ("y en esa misma tienen de seca?").
