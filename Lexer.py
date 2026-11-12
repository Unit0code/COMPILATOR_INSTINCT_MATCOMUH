# Lexer, lee el archivo y lo tokeniza
from typing import Callable
from dataclasses import dataclass
from Errors import Location, LexicalError

KEYWORDS = {'if', 'goto', 'and', 'or', 'not'}
SYMBOLS = {'+', '-', '*', '/', '%', '<', '>', '=', '!', '(', ')', ',', ':'}

class TokenType: # Tipos de Tokens
    NUMBER = "number"
    TEXT = "text"
    KEYWORD = "keyword"
    IDENTIFIER = "identifier"
    SYMBOL = "symbol"
    END = "end"

@dataclass(frozen=True) # Clase Inmutable
class Token:
    kind: TokenType
    value: str
    location: Location
    
    def __repr__(self) -> str:
        return f"[{self.kind.upper()} {self.value}]"     

class Lexer: #Un ente Lexer
    def __init__(self, code: str): # defino ubicacion del lexer
        self.code = code
        self.position = 0
        self.line = 1
        self.column = 0
    
    def to_tokenize(self): #################### MANEJAR EXCEPCIONES DE DONDE SE LLAME
        tokens = [] # Se guardan los token, esto es lo que retorna la funcion
        while self.position < len(self.code): # Mientras no se haya analizado todo el codigo
            charc = self.code[self.position]
            if charc.isalpha() or charc == '_': # Tomara todo lo sgte que sea un nombre
                word = self.read_identifier()
                tokens.append(word)
                continue
            elif charc == '"': # Si es un Texto
                word = self.read_text() ################ Manejar excepcion de donde se llame el tokenizar
                tokens.append(word)
                continue
            elif charc.isdigit():
                word = self.read_number()
                tokens.append(word)
                continue
            elif charc in SYMBOLS:
                tokens.append(Token(TokenType.SYMBOL, charc, Location(self.line, self.column)))
                self.column += 1
                self.position += 1
                continue
            elif charc in ' \t\r':
                self.column += 1
                self.position +=1
                continue
            elif charc == '\n':
                self.position += 1
                self.column = 0
                self.line += 1
            elif charc == '#':
                self.read_while(lambda c: c != '\n') # No se empleo lo que retorna, solo necesito que se mueva el position
                continue
            else:
                raise LexicalError(Location(self.line, self.column), f'"{charc}" is not a valid character') # Excepcion a manejar
        
        tokens.append(Token(TokenType.END, 'end', Location(self.line, self.column)))
        return tokens # Si ya llego al final del archivo
            

    
    def read_while(self, condition: Callable ): # condition Para avanzar sobre el codigo mientras se cumpla cierta condicion
        start = self.position
        while self.position < len(self.code) and condition(self.code[self.position]):
            if self.code[self.position] == '\n': # Un Verificador de salto de linea
                self.column = 0
                self.line += 1
            else:
                self.column += 1
            self.position += 1
            
        return (start, self.position)  # Devuelve donde inicio y donde dejo de cumplir la condicion

    def read_identifier(self): #Leera a partir de la posicion del lexer en adelante mientras sea letra, numero o _
        start, end = self.read_while(lambda c: c == "_" or c.isalnum())
        text = self.code[start:end] # Tomo el cacho de texto
        if text in KEYWORDS:
            return Token(TokenType.KEYWORD, text, Location(self.line, self.column - 1)) # Creamos el token tipo Keyword
        return Token(TokenType.IDENTIFIER, text, Location(self.line, self.column - 1)) # Creamos el token tipo Identifier
    
    # OJO se implemento para que un texto pueda tener saltos de linea adentro, no son de una sola linea
    def read_text(self): #Leera a partir de la posicion del lexer en adelante mientras no sea "
        self.position += 1
        self.column += 1
        start , end = self.read_while(lambda c: c != '"')
        if self.position >= len(self.code): # El texto nunca cerro comillas
            raise LexicalError(Location(self.line, self.column - 1), 'Text literals must be closed with "')
        self.position += 1 # Porque se quedo parado en el " de cierre
        self.column += 1
        text = self.code[start:end] # Tomo el cacho de texto
        return Token(TokenType.TEXT, text, Location(self.line, self.column - 1))
    
    def read_number(self):
        start, end = self.read_while(lambda c: c.isdigit())
        if end < len(self.code) and (self.code[end].isalpha() or self.code[end] in '"_'): # Si se pone un _ o una letra a continuacion de un numero 
            raise LexicalError(Location(self.line, self.column), 'Integer literals can only contain digits')
        number = self.code[start: end]
        return Token(TokenType.NUMBER, number, Location(self.line, self.column - 1))