from enum import Enum
from pydantic import BaseModel, Field, field_validator


class NivelCriticidad(str, Enum):
    baja = "baja"
    media = "media"
    alta = "alta"


class ExtraccionTecnica(BaseModel):
    tecnologias: list[str] = Field(
        description="Lista de tecnologias, frameworks, bases de datos o herramientas detectadas"
    )
    nivel_de_criticidad: NivelCriticidad = Field(
        description="Nivel de criticidad del evento o arquitectura analizada (baja, media, alta)"
    )
    resumen_tecnico: str = Field(
        description="Resumen breve y tecnico del problema o arquitectura detectada"
    )

    @field_validator("tecnologias")
    @classmethod
    def validar_tecnologias(cls, lista_tecnologias: list[str]) -> list[str]:
        limpias = [tec.strip() for tec in lista_tecnologias if tec.strip()]
        if not limpias:
            raise ValueError("La lista de tecnologias no puede estar vacia")
        return limpias

    @field_validator("resumen_tecnico")
    @classmethod
    def validar_resumen(cls, texto_resumen: str) -> str:
        limpio = texto_resumen.strip()
        if not limpio:
            raise ValueError("El resumen tecnico no puede estar vacio")
        return limpio
