# Tipos de Errores
from dataclasses import dataclass

@dataclass(frozen=True) # Clase Inmutable
class Location:
    line: int
    column: int  

class ElementalError(Exception): # Errores generales que puedan ocurrir
    label = "ElementalError"

    def __init__(self, location: Location, message: str):
        super().__init__(f"{self.label} error at {location}: {message}")
        self.location = location
        self.message = message


class LexicalError(ElementalError): # Creo que estos son bastante intuitivos
    label = "lexical"


class ParseError(ElementalError):
    label = "syntax"


class SemanticError(ElementalError):
    label = "semantic"


class EvaluationError(ElementalError):
    label = "runtime"
