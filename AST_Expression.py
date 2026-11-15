# Los Nodos de Expression
from __future__ import annotations
from abc import ABC, abstractmethod
from Errors import Location
from AST_Nodes import Node, Context
from Maps_Object_Terrains import Map
from Errors import SemanticError

class Expression(Node):
    def __init__(self, location: Location):
        self.location = location
    
    @abstractmethod
    def evaluate(self, context: Context):
        pass

class Number(Expression): #Un Literal
    def __init__(self, location: Location, value: int):
        super().__init__(location)
        self.value = value
    
    def check(self, context: Context) -> str:
        return 'int'
    
    def evaluate(self):
        pass # Implementar
    
    def draw(self, indent=0):
        prefix = "  " * indent
        print(f"{prefix}└─ Number({self.value})")

class Text(Expression):
    def __init__(self, location: Location, label: str):
        super().__init__(location)
        self.label = label
    
    def check(self, context: Context) -> str:
        return 'str'
    
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

    @abstractmethod
    def check(self, context: Context) -> str:
        pass
    
    def evaluate(self):
        pass # Nunca se van a emplear, esta clase no se instancia
    
    @abstractmethod
    def assign(self):## que sea para asignar el valor a una variable
        pass

    def draw(self, indent=0):
        prefix = "  " * indent
        print(f"{prefix}└─ {self.__class__.__name__}({self.name})")

class Constant(Ident):

    def __init__(self, location: Location, name: str):
        super().__init__(location, name, None)
        self.value = self.assign(name) # Como es una constante, tiene un valor segun el npombre
    
    def check(self, context: Context) -> str:
        return 'int'
    
    def evaluate(self):
        pass # Implementar

    def assign(self, name):
        pass # Implementar, constatar contra diccionario de constantes

class Variable(Ident): # Variable

    # No se implementara __init__ porque es el mismo que el del padre
    
    def check(self, context: Context) -> str:
        
        if self.name not in context.variables_created: # Vrificamos si en algun momento ha sido creada
            raise SemanticError(self.location, f"Variable '{self.name}' is used but never assigned in the program.")
        return 'variable'
    
    def evaluate(self):
        pass # Implementar
    
    def assign(self):
        pass # Implementar

class Perception(Ident):
    
    # No se implementara __init__ porque es el mismo que el del padre

    def check(self, context: Context) -> str:
        PERCEPCIONES_TEXTO = {'species', 'faction', 'terrain_here', 'last_roar'}
        return 'str' if self.name in PERCEPCIONES_TEXTO else 'int'
    
    def evaluate(self):
        pass # Implementar
    
    def assign(self):
        pass # Implementar

class BinaryExpression(Expression): # Clase Abstracta, no se Instancia
    symbol = ''
    def __init__(self, location: Location, left: Expression, right: Expression): #left y right puede ser
        super().__init__(location)  # Number, Ident, Binary expresin, etc
        self.left = left
        self.right = right
    
    def evaluate(self):
        pass # No se implementa aca

    def draw(self, indent=0):
        prefix = "  " * indent
        print(f"{prefix}└─ {self.__class__.__name__} ({self.symbol})")
        self.left.draw(indent + 1)
        self.right.draw(indent + 1)

class Arithmetic(BinaryExpression): # Clase abstracta, no se instancia

    def check(self, context: Context) -> str:

        left_type = self.left.check(context) # Verifica los tipos y si estan correctos sus operandos
        right_type = self.right.check(context)

        if left_type not in ('int', 'variable'): # Si no es entero, o any, que se emplea para cuando una variable fue aginada con dos valores distintos
            raise SemanticError(self.location,f"Operator '{self.symbol}' expects a number on the left, but got '{left_type}'.")
        
        if right_type not in ('int', 'variable'):
            raise SemanticError(self.location, f"Operator '{self.symbol}' expects a number on the right, but got '{right_type}'.")

        return 'int'

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
    
    def check(self, context: Context) -> str:
        
        left_type = self.left.check(context)
        right_type = self.right.check(context)

        if self.symbol in ('<', '<=', '>', '>='): # Esto es por si hay un texto en una operacion de numeros
            if left_type == 'str' or right_type == 'str':
                raise SemanticError(self.location, f"Operator '{self.symbol}' only accepts numbers, not text.")

        if {left_type, right_type} == {'int', 'str'}: # Si existe una mezcla de tipos conocidos, lanza error, si es alguno o ambos variables, entonces dejalo pasar
            raise SemanticError(self.location, f"Cannot compare '{left_type}' with '{right_type}'.")

        # Si llego a aca entonces o hay variables involucradas, o es el mismo tipo
        return 'int'
    
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
    
    def check(self, context: Context) -> str:
        self.left.check(context)
        self.right.check(context)

        return 'int' # Siempre devuelve el mismo tipo
    
    def evaluate(self):
        pass # Implementar la de todas las op logicas aqui, vaya, pa que sirva pa algo esta clase

class Or(Logical):
    symbol = 'or'

    # El check lo implementa Binary Expression y el evaluate Logical

class And(Logical):
    symbol = 'and'

    # El check lo implementa Binary Expression y el evaluate Logical

class UnaryExpression(Expression): #Clase abstracta, no se instancia
    symbol = ''
    def __init__(self, location: Location, value: Expression):
        super().__init__(location)
        self.value = value
    
    def evaluate(self):
        pass # Implementar aqui la de sus hijos, con un dict y unos if, devuelven 0 o 1

    def draw(self, indent=0):
        prefix = "  " * indent
        print(f"{prefix}└─ {self.__class__.__name__} ({self.symbol})")
        self.value.draw(indent + 1)

class Not(UnaryExpression): # Negador logico Not
    symbol = 'not'

    def check(self, context: Context) -> str:
        self.value.check(context) # Solo verificamos que el hijo no tenga errores
        return 'int' # Devuelve 1 o 0

    # el evaluate lo implementa Unary Expression 

class Neg(UnaryExpression): # Entero negativo
    symbol = '-'

    def check(self, context: Context) -> str:
        tipo_operando = self.value.check(context)
        if tipo_operando == 'str':
            raise SemanticError(self.location, "Unary operator '-' only accepts numbers.")
        return 'int'
    
    # el evaluate lo implementa Unary Expression 

class FuncCall(Expression): # Clase Abstracta, no Instanciar 
    def __init__(self, location: Location, x_value: Expression, y_value: Expression):
        super().__init__(location)
        self.x_value = x_value
        self.y_value = y_value
    
    def check(self, context: Context) -> str:

        x_type = self.x_value.check(context) # Vemos para las coordenadas
        y_type = self.y_value.check(context)
        
        if x_type == 'str' or y_type == 'str':
            raise SemanticError( self.location, f"{self.__class__.__name__} requires the Location to be a tuple of numbers.")
        
        if self.__class__.__name__ == 'See':
            return 'int'
        return 'str'
        
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
