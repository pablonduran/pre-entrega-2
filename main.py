import asyncio
import json
from chain import process_text


async def main():
    casos_de_prueba = [
        (
            "Caso 1: Arquitectura con cuello de botella",
            "Nuestra arquitectura actual utiliza una API desarrollada en FastAPI conectada a Redis para cache y a PostgreSQL para persistencia. Durante las horas pico detectamos una saturacion severa en el pool de conexiones a la base de datos que provoca demoras criticas en las respuestas."
        ),
        (
            "Caso 2: Log de error en microservicio",
            "CRITICAL 2026-10-06 14:32:00 [payment-service] ConnectionRefusedError: Failed to connect to Kafka broker at kafka:9092. Fallback to RabbitMQ also failed. Database MySQL timed out after 30000ms. Service unreachable."
        ),
        (
            "Caso 3: Texto breve / mantenimiento",
            "Se realizo una actualizacion de dependencias en un script de Python usando Docker para correr tareas en segundo plano sin novedades ni incidentes."
        ),
    ]

    for titulo, texto in casos_de_prueba:
        print(f"\n{titulo}")
        print(f"Entrada: {texto}\n")

        try:
            resultado = await process_text(texto)
            print("Salida validada (Pydantic):")
            print(json.dumps(resultado.model_dump(), indent=2, ensure_ascii=False))
        except Exception as error:
            print(f"Ocurrio un fallo al procesar: {error}")


if __name__ == "__main__":
    asyncio.run(main())
