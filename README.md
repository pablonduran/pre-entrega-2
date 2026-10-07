# Pre-entrega 2 — Pipeline de Procesamiento Validado

Pipeline de extracción de entidades técnicas a partir de texto sin procesar (logs, descripciones de arquitectura o incidentes), construido con LangChain (LCEL) y validado con Pydantic.

## Requisitos

- Python 3.12 o superior
- API Key de OpenAI, Anthropic o Google Gemini

## Instalación

1. Crear y activar entorno virtual:
```bash
python -m venv .venv
# En Windows:
.venv\Scripts\Activate.ps1
# En Linux / Mac:
# source .venv/bin/activate
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Configurar variables de entorno:
Crear un archivo `.env` basándose en `.env.example`:
```env
LLM_PROVIDER=gemini
GEMINI_API_KEY=tu_clave_de_gemini
# O para OpenAI:
# LLM_PROVIDER=openai
# OPENAI_API_KEY=tu_clave_de_openai
```

## Ejecución

Ejecutar el script de pruebas:
```bash
python main.py
```

## Ejemplo de entrada y salida

### Entrada (Log o texto técnico):
```text
Nuestra arquitectura actual utiliza una API desarrollada en FastAPI conectada a Redis para cache y a PostgreSQL para persistencia. Durante las horas pico detectamos una saturacion severa en el pool de conexiones a la base de datos que provoca demoras criticas en las respuestas.
```

### Salida JSON validada:
```json
{
  "tecnologias": [
    "FastAPI",
    "Redis",
    "PostgreSQL"
  ],
  "nivel_de_criticidad": "alta",
  "resumen_tecnico": "Saturacion severa en el pool de conexiones de PostgreSQL durante horas pico, afectando los tiempos de respuesta de la API en FastAPI."
}
```
