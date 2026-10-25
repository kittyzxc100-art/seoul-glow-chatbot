"""
intenciones.py

Base de conocimiento del asistente virtual de Seoul Glow (boutique en linea
de skincare coreano). Aqui viven las intenciones, las entidades y los datos
de negocio (precios, rutinas, ingredientes) que el chatbot usa para
responder. Separar esto de la logica (chatbot.py) permite agregar nuevas
intenciones o productos sin tocar el motor de deteccion.
"""

# ---------------------------------------------------------------------------
# 1. Intenciones: cada una tiene frases de ejemplo (como habla el usuario)
#    y, cuando la respuesta no depende de una entidad, una lista de
#    respuestas posibles.
# ---------------------------------------------------------------------------

INTENCIONES = {
    "saludo": {
        "ejemplos": [
            "hola", "buenas", "buenos dias", "buenas tardes", "buenas noches",
            "que tal", "hola buen dia", "hey", "oli",
        ],
        "respuestas": [
            "Hola, soy el asistente virtual de Seoul Glow. Puedo ayudarte "
            "con rutinas, ingredientes, precios, envios y cambios. "
            "En que te ayudo?"
        ],
    },
    "consultar_rutina": {
        "ejemplos": [
            "que rutina me recomiendan", "que rutina es buena para mi piel",
            "como armo mi rutina de skincare", "que productos debo usar",
            "rutina para piel grasa", "rutina para piel seca",
            "rutina para piel sensible", "que pasos debo seguir en mi rutina",
            "recomiendame una rutina", "cual es el orden correcto de mis productos",
        ],
    },
    "consultar_ingredientes": {
        "ejemplos": [
            "que hace la niacinamida", "para que sirve el acido hialuronico",
            "que es la centella asiatica", "sirve la mucina de caracol",
            "que beneficios tiene el retinol", "la vitamina c mancha la piel",
            "puedo usar retinol y vitamina c juntos", "que ingrediente ayuda con las manchas",
            "el acido hialuronico reseca la piel",
        ],
    },
    "consultar_precio": {
        "ejemplos": [
            "cuanto cuesta el limpiador", "precio del serum",
            "cuanto sale la mascarilla", "que precio tiene el protector solar",
            "cuanto cuesta el tonico", "precio de la crema",
            "cuanto vale el kit completo",
        ],
    },
    "consultar_envio": {
        "ejemplos": [
            "cuanto tarda el envio", "cuando llega mi pedido",
            "hacen envios a todo mexico", "cuanto cuesta el envio",
            "puedo rastrear mi pedido", "hacen envios internacionales",
            "tienen envio gratis",
        ],
    },
    "soporte_posventa": {
        "ejemplos": [
            "quiero cambiar un producto", "como hago una devolucion",
            "mi pedido llego incompleto", "quiero cancelar mi pedido",
            "mi pedido nunca llego", "llego daniado el empaque",
            "cual es su politica de cambios",
        ],
    },
    "despedida": {
        "ejemplos": [
            "gracias hasta luego", "adios", "nos vemos",
            "muchas gracias eso es todo", "listo gracias", "bye",
        ],
        "respuestas": [
            "Gracias por escribir a Seoul Glow. Que tengas un dia con mucho glow."
        ],
    },
}

# Mensaje cuando ninguna intencion supera el umbral de coincidencia.
FALLBACK = (
    "No estoy segura de haber entendido bien. Puedo ayudarte con rutinas, "
    "ingredientes, precios, envios o cambios/devoluciones. Sobre cual "
    "quieres que te ayude?"
)

# Palabras que activan una alerta de seguridad (reaccion en la piel). Esto
# NO se trata como una intencion mas: se revisa antes de clasificar, porque
# una reaccion adversa debe canalizarse a una persona y nunca recibir una
# recomendacion automatica de producto.
PALABRAS_ALERTA = [
    "reaccion", "irrit", "ardor", "alergi", "rojez", "hinchaz",
    "comezon", "picazon", "me quemo", "se me quemo",
]

MENSAJE_ALERTA = (
    "Lamento escuchar eso. Por tu seguridad suspende el uso del producto "
    "de inmediato, enjuaga la zona con agua tibia y evita el sol directo. "
    "Te voy a canalizar con una persona del equipo para dar seguimiento a "
    "tu caso; esto no sustituye una valoracion con un dermatologo."
)

# ---------------------------------------------------------------------------
# 2. Entidades: diccionarios de sinonimos (igual que SERVICIOS en el
#    ejemplo del profesor) para mapear como escribe la gente a una
#    categoria interna que el negocio reconoce.
# ---------------------------------------------------------------------------

TIPO_PIEL = {
    "grasa": ["grasa", "oleosa", "aceitosa", "con brillo"],
    "seca": ["seca", "deshidratada", "resecada"],
    "mixta": ["mixta", "combinada"],
    "sensible": ["sensible", "reactiva", "que se irrita facil"],
    "con_acne": ["acne", "granos", "espinillas", "barros"],
}

PRODUCTOS = {
    "limpiador": ["limpiador", "cleanser", "gel limpiador", "jabon facial"],
    "tonico": ["tonico", "toner"],
    "serum": ["serum", "serums"],
    "mascarilla": ["mascarilla", "mask", "sheet mask"],
    "protector_solar": ["protector solar", "bloqueador", "spf", "filtro solar"],
    "crema": ["crema", "moisturizer", "hidratante"],
}

INGREDIENTES = {
    "niacinamida": ["niacinamida", "niacinamide"],
    "acido_hialuronico": ["acido hialuronico", "hialuronico"],
    "centella_asiatica": ["centella asiatica", "centella", "cica"],
    "mucina_caracol": ["mucina de caracol", "baba de caracol", "snail mucin", "caracol"],
    "retinol": ["retinol", "retinoide"],
    "vitamina_c": ["vitamina c", "vit c"],
}

# ---------------------------------------------------------------------------
# 3. Datos de negocio: lo que el chatbot necesita para responder con datos
#    reales (no solo texto generico) una vez identificada la entidad.
# ---------------------------------------------------------------------------

PRECIOS = {
    "limpiador": 320,
    "tonico": 380,
    "serum": 590,
    "mascarilla": 45,
    "protector_solar": 420,
    "crema": 480,
}

RUTINAS = {
    "grasa": (
        "Dia: limpiador en gel, tonico, serum con niacinamida y protector "
        "solar. Noche: doble limpieza, exfoliante suave 2-3 veces por "
        "semana y crema ligera en gel."
    ),
    "seca": (
        "Dia: limpiador cremoso, tonico hidratante, serum de acido "
        "hialuronico, crema rica y protector solar. Noche: doble limpieza, "
        "serum y crema nutritiva."
    ),
    "mixta": (
        "Dia: limpiador suave, tonico, serum con niacinamida, crema ligera "
        "y protector solar. Noche: doble limpieza, serum hidratante y "
        "crema."
    ),
    "sensible": (
        "Dia: limpiador sin fragancia, tonico calmante con centella "
        "asiatica, crema y protector solar mineral. Noche: limpieza suave, "
        "serum calmante y crema reparadora."
    ),
    "con_acne": (
        "Dia: limpiador con acido salicilico, tonico, serum con "
        "niacinamida y protector solar oil-free. Noche: doble limpieza, "
        "tratamiento puntual y crema ligera."
    ),
}

INFO_INGREDIENTES = {
    "niacinamida": "Controla la grasa, minimiza poros y pareja el tono de la piel.",
    "acido_hialuronico": "Hidrata profundamente atrayendo agua a la piel; va bien en piel seca o deshidratada.",
    "centella_asiatica": "Calma la irritacion y fortalece la barrera de la piel; muy usada en piel sensible.",
    "mucina_caracol": "Repara, hidrata y da elasticidad; ayuda con marcas leves de acne.",
    "retinol": "Renueva la piel y suaviza lineas finas; se usa de noche y siempre con protector solar al dia siguiente.",
    "vitamina_c": "Ilumina el tono y ayuda con manchas; conviene usarla junto con protector solar porque puede sensibilizar la piel al sol.",
}
