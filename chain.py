import os
import logging
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

from schemas import ExtraccionTecnica

load_dotenv()

logger = logging.getLogger("pipeline_validado")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


def crear_cliente_llm():
    proveedor = os.getenv("LLM_PROVIDER", "openai").lower()
    temperatura = float(os.getenv("LLM_TEMPERATURE", "0.0"))

    if proveedor == "anthropic":
        modelo_nombre = os.getenv("LLM_MODEL", "claude-3-5-haiku-latest")
        clave_api = os.getenv("ANTHROPIC_API_KEY")
        return ChatAnthropic(model=modelo_nombre, api_key=clave_api, temperature=temperatura)

    if proveedor == "gemini":
        modelo_nombre = os.getenv("LLM_MODEL", "gemini-3.5-flash-lite")
        clave_api = os.getenv("GEMINI_API_KEY")
        url_base = "https://generativelanguage.googleapis.com/v1beta/openai/"
        return ChatOpenAI(model=modelo_nombre, api_key=clave_api, base_url=url_base, temperature=temperatura)

    modelo_nombre = os.getenv("LLM_MODEL", "gpt-4o-mini")
    clave_api = os.getenv("OPENAI_API_KEY")
    return ChatOpenAI(model=modelo_nombre, api_key=clave_api, temperature=temperatura)


plantilla_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "Sos un asistente especializado en analisis de arquitectura y logs tecnicos. "
        "Analiza el texto de entrada y extrae con precision las tecnologias utilizadas, "
        "determina el nivel de criticidad (baja, media, alta) y redacta un resumen tecnico conciso en texto plano, sin asteriscos ni negritas."
    ),
    ("human", "Texto a analizar:\n{texto_entrada}")
])

modelo = crear_cliente_llm()
modelo_estructurado = modelo.with_structured_output(ExtraccionTecnica)

cadena = (plantilla_prompt | modelo_estructurado).with_retry(stop_after_attempt=3)


async def process_text(text: str) -> ExtraccionTecnica:
    if not text or not text.strip():
        logger.error("El texto de entrada esta vacio.")
        raise ValueError("El texto de entrada no puede estar vacio.")

    logger.info("Iniciando procesamiento de texto...")
    try:
        resultado = await cadena.ainvoke({"texto_entrada": text})
        logger.info("Validacion completada exitosamente.")
        return resultado
    except Exception as error:
        logger.error(f"Error durante el procesamiento o validacion: {error}")
        raise


procesar_texto = process_text
