# Los Nodos de Expression
from __future__ import annotations
from abc import ABC, abstractmethod
from Errors import Location
from AST_Nodes import Node
from Maps_Object_Terrains import Map

class Expression(Node):
    def __init__(self, location: Location):
        self.location = location
    
    @abstractmethod
    def evaluate(self):
        pass

class Number(Expression): #Un Literal
    def __init__(self, location: Location, value: int):
        super().__init__(location)
        self.value = value
    
    def check(self):
        pass # Implementar
    
    def evaluate(self):
        pass # Implementar
    
    def draw(self, indent=0):
        prefix = "  " * indent
        print(f"{prefix}└─ Number({self.value})")

class Text(Expression):
    def __init__(self, location: Location, label: str):
        super().__init__(location)
        self.label = label
    
    def check(self):
        pass #Implementar
    
    def evaluate(self):
        pass #Implementar

    def draw(self, indent=0):
        prefix = "  " * indent
        print(f'{prefix}└─ Text("{self.label}")')

class Ident(Expression): #Clase abstracta de las variables, constantes y percepciones
    def __init__(self, location: Location, name: str, value = None): #La variable no tiene por que tener un valor apenas se ve en el parser, eso se le asigna a medida de que el codigo revisa las instrucciones assign
        super().__init__(location)
        self.name = name
        self.value = value

    def check(self):
        pass # Nunca se van a emplear, esta clase no se instancia
    
    def evaluate(self):
        pass # Nunca se van a emplear, esta clase no se instancia
    
    @abstractmethod
    def assign(self):## que sea para asignar el valor a una variable
        pass

    def draw(self, indent=0):
        prefix = "  " * indent
        print(f"{prefix}└─ {self.__class__.__name__}({self.name})")

class Constant(Ident):
    def __init__(self, location: Location, name: str, value = None):
        super().__init__(location, name, value)
        self.value = self.assign(name) # Como es una constante, tiene un valor segun el npombre
    def check(self):
        pass #Implementar
    
    def evaluate(self):
        pass # Implementar

    def assign(self, name):
        pass # Implementar, constatar contra diccionario de constantes

class Variable(Ident): # Variable
    # No se implementara __init__ porque es el mismo que el del padre
    def check(self):
        pass # Implementar
    
    def evaluate(self):
        pass # Implementar
    
    def assign(self):
        pass # Implementar

class Perception(Ident):
    # No se implementara __init__ porque es el mismo que el del padre
    def check(self):
        pass # Implementar, recordar que aqui las percepciones no tienen nada cargado antes de la simulacion, o sea esto no puede saltar en Parser
    
    def evaluate(self):
        pass # Implementar
    
    def assign(self):
        pass # Implementar

class BinaryExpression(Expression): # Clase Abstracta, no se Instancia
    symbol = ''
    def __init__(self, location: Location, left, right): #left y right puede ser
        super().__init__(location)  # Number, Ident, Binary expresin, etc
        self.left = left
        self.right = right
    
    def check(self):
        pass # Implementarlo aca para toda su rama
    
    def evaluate(self):
        pass # No se implementa aca

    def draw(self, indent=0):
        prefix = "  " * indent
        print(f"{prefix}└─ {self.__class__.__name__} ({self.symbol})")
        self.left.draw(indent + 1)
        self.right.draw(indent + 1)

class Arithmetic(BinaryExpression): # Clase abstracta, no se instancia

    # check implementado por el padre

    def evaluate(self):
        pass # Implementar la de todas las aritmeticas aqui, vaya, pa que sirva pa algo esta clase

class Sum(Arithmetic):
    symbol = '+'

    # El check lo implementa Binary Expression y el evaluate Arithmetic

class Sub(Arithmetic):
    symbol = '-'

    # El check lo implementa Binary Expression y el evaluate Arithmetic

class Mul(Arithmetic):
    symbol = '*'

    # El check lo implementa Binary Expression y el evaluate Arithmetic

class Div_Int(Arithmetic):
    symbol = '/'

    # El check lo implementa Binary Expression y el evaluate Arithmetic

class Mod(Arithmetic):
    symbol = '%'

    # El check lo implementa Binary Expression y el evaluate Arithmetic 

class Comparison(BinaryExpression): # Clase abstacta, no se instancia
    
    # check se implementa en su padre binary expression
    
    def evaluate(self):
        pass # Implementar la de todas las comparaciones aqui, vaya, pa que sirva pa algo esta clase

class Less(Comparison):
    symbol = '<'

    # El check lo implementa Binary Expression y el evaluate Comparison

class LessEqual(Comparison):
    symbol = '<='
    
    # El check lo implementa Binary Expression y el evaluate Comparison

class Greater(Comparison):
    symbol = '>'
    
    # El check lo implementa Binary Expression y el evaluate Comparison

class GreaterEqual(Comparison):
    symbol = '>='

    # El check lo implementa Binary Expression y el evaluate Comparison

class Equal(Comparison):
    symbol = '=='

    # El check lo implementa Binary Expression y el evaluate Comparison


class NotEqual(Comparison):
    symbol = '!='

    # El check lo implementa Binary Expression y el evaluate Comparison

class Logical(BinaryExpression): # Clase abstracta, no se instancia
    
    # check se realiza en su padre
    
    def evaluate(self):
        pass # Implementar la de todas las op logicas aqui, vaya, pa que sirva pa algo esta clase

class Or(Logical):
    symbol = 'or'

    # El check lo implementa Binary Expression y el evaluate Logical

class And(Logical):
    symbol = 'and'

    # El check lo implementa Binary Expression y el evaluate Logical

class UnaryExpression(Expression): #Clase abstracta, no se instancia
    simbol = ''
    def __init__(self, location: Location, value: int | Ident):
        super().__init__(location)
        self.value = value

    def check(self):
        pass # Se implementa aca para toda su rama 
    
    def evaluate(self):
        pass # Implementar aqui la de sus hijos, con un dict y unos if, devuelven 0 o 1

    def draw(self, indent=0):
        prefix = "  " * indent
        print(f"{prefix}└─ {self.__class__.__name__} ({self.symbol})")
        self.value.draw(indent + 1)

class Not(UnaryExpression): # Negador logico Not
    symbol = 'not'

    # El check y el evaluate lo implementa Unary Expression 

class Neg(UnaryExpression): # Entero negativo
    symbol = '-'

    # El check y el evaluate lo implementa Unary Expression 

class FuncCall(Expression): # Clase Abstracta, no Instanciar 
    def __init__(self, location: Location, x_value: Number | Ident, y_value: Number | Ident):
        super().__init__(location)
        self.x_value = x_value
        self.y_value = y_value
    
    def check(self):
        pass # Implementar, revisar si son numeros,y si son ident, ver si existen y son numericos
    
    def evaluate(self):
        pass # No Implementar, se hace en los hijos
    
    def draw(self, indent=0):
        prefix = "  " * indent
        print(f"{prefix}└─ {self.__class__.__name__}")
        self.x_value.draw(indent + 1)
        self.y_value.draw(indent + 1)

class See(FuncCall):
    def evaluate(self):
        pass # Implementar, recibir el mapa y ver en la posicion que tiene, segun la vision, que este en rango, etc

class NameOf(FuncCall):
    def evaluate(self):
        pass # Implementar, recibir el mapa y verificar que la posicion no se pase de la vision, del mapa ni de nada
