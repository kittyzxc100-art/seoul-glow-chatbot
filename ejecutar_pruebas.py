"""
ejecutar_pruebas.py

Corre el asistente de Seoul Glow contra 12 conversaciones distintas
(mas de las 10 minimas que pide el avance), cubriendo todas las
intenciones, la alerta de seguridad y 2 mensajes fuera de alcance.
Calcula precision de intencion y tasa de fallback, igual que el ejemplo
de evaluacion visto en clase, e imprime evidencia real de ejecucion
(no capturas inventadas: esta es la salida real de correr este script).
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chatbot import responder, historial_df  # noqa: E402

CASOS = [
    ("Hola, buenas tardes!", "saludo"),
    ("Que rutina me recomiendan para piel grasa?", "consultar_rutina"),
    ("Para que sirve la niacinamida?", "consultar_ingredientes"),
    ("Cuanto cuesta el serum?", "consultar_precio"),
    ("Cuanto tarda el envio a Mexico?", "consultar_envio"),
    ("Quiero hacer un cambio de mi pedido 482913", "soporte_posventa"),
    ("Se me irrito la piel con el tonico que compre", "alerta_seguridad"),
    ("Mi piel es sensible, que rutina me recomiendas?", "consultar_rutina"),
    ("El retinol se puede usar de dia?", "consultar_ingredientes"),
    ("Quiero cancelar mi contrato de telefonia", "fallback"),
    ("Cual es la capital de Francia?", "fallback"),
    ("Gracias, hasta luego", "despedida"),
]


def main():
    print("=" * 70)
    print("EJECUCION DE PRUEBAS - Asistente virtual Seoul Glow")
    print("=" * 70)

    for i, (mensaje, _esperada) in enumerate(CASOS, start=1):
        respuesta = responder(mensaje)
        print(f"\n--- Conversacion {i} ---")
        print(f"Tu : {mensaje}")
        print(f"Bot: {respuesta}")

    df = historial_df()
    df["esperada"] = [e for _, e in CASOS]
    df["correcto"] = df["esperada"] == df["intencion"]

    precision = df["correcto"].mean()
    tasa_fallback = (df["intencion"] == "fallback").mean()

    print("\n" + "=" * 70)
    print("TABLA DE RESULTADOS")
    print("=" * 70)
    print(df[["usuario", "intencion", "esperada", "correcto"]].to_string(index=False))

    print("\n" + "=" * 70)
    print("METRICAS")
    print("=" * 70)
    print(f"Precision de intencion: {precision:.0%} ({df['correcto'].sum()}/{len(df)} casos)")
    print(f"Tasa de fallback: {tasa_fallback:.0%}")

    errores = df[~df["correcto"]]
    if len(errores):
        print(f"\nCasos con error ({len(errores)}):")
        print(errores[["usuario", "intencion", "esperada"]].to_string(index=False))
    else:
        print("\nSin errores en este lote de pruebas.")

    out_dir = os.path.dirname(os.path.abspath(__file__))
    df.to_csv(os.path.join(out_dir, "casos.csv"), index=False, encoding="utf-8-sig")
    print(f"\nCasos guardados en {os.path.join(out_dir, 'casos.csv')}")


if __name__ == "__main__":
    main()
