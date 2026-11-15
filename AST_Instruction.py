from __future__ import annotations
from abc import ABC, abstractmethod
from Errors import Location, SemanticError
from AST_Nodes import Node, Context
from AST_Expression import Ident, Variable, Number, Text, BinaryExpression, UnaryExpression, Expression

# Los Nodos de Instruction
class Instruction(Node): # Clase abstracta, No se instancia
    @abstractmethod
    def execute(self):
        pass # No se implementa

class Assign(Instruction):
    def __init__(self, location: Location, variable: Variable, value: Expression):
        super().__init__(location)
        self.variable = variable
        self.value = value
    
    def check(self, context: Context):

        if not isinstance(self.variable, Variable): # Para verificar que no se le este asignado algo a una Perception o Constant
            raise SemanticError(self.location, f"Cannot assign to read-only identifier '{self.variable.name}'.")

        self.value.check(context) #Revisamos que este semanticamente en orden

    def execute(self):
        pass # Implementar, hacerle a la expression evaluate() 

    def draw(self, indent=0):
        prefix = "  " * indent
        print(f"{prefix}└─ Assign (=)")
        self.variable.draw(indent + 1)
        self.value.draw(indent + 1)

class IfGoto(Instruction):
    def __init__(self, location: Location, condition: BinaryExpression | UnaryExpression, goto: GoTo):
        super().__init__(location)
        self.condition = condition
        self.goto = goto
    
    def check(self, context: Context): # Solo se verifica que sus hijos esten bien
        self.condition.check(context)
        self.goto.check(context)
    
    def execute(self):
        pass # Implementar, necesitas program counter y los "" y 0 son como false, ojo

    def draw(self, indent=0):
        prefix = "  " * indent
        print(f"{prefix}└─ IfGoto (salta a '{self.goto.label}')")
        self.condition.draw(indent + 1)
        self.goto.draw(indent + 1)

class GoTo(Instruction):
    def __init__(self, location: Location, label: str):
        super().__init__(location)
        self.label = label
    
    def check(self, context: Context): 
        if self.label not in context.labels: # Si el label todavia no se ha creado
            raise SemanticError(self.location, f"Label '{self.label}' does not exist.")
    
    def execute(self):
        pass # Implementar, recibe

    def draw(self, indent=0):
        prefix = "  " * indent
        print(f"{prefix}└─ GoTo (salta a '{self.label}')")

class Label(Instruction):
    def __init__(self, location: Location, name: str):
        super().__init__(location)
        self.name = name
    
    def execute(self, program_counter: list):
        pass

    def check(self, context: Context):
        
        if self.name in context.labels: #Verificar si ya existe el label
            raise SemanticError(self.location, f"Duplicate label '{self.name}'.")
        
        context.labels.add(self.name) #Si no existe, lo agrega

    def draw(self, indent=0):
        prefix = "  " * indent
        print(f"{prefix}└─ Label '{self.name}':")

class Action(Instruction): # Clase abstracta, no se instancia
    def __init__(self, location: Location):
        super().__init__(location)
    
class Wait(Action):
    def __init__(self, location: Location, time: Number | Ident):
        super().__init__(location)
        self.time = time
    
    def check(self, context: Context):
        tipo = self.time.check(context) # Veo el tipo que recibio
        if tipo not in ('int', 'variable'): # Si no es un entero o un desconocido, da error
            raise SemanticError(self.location, f"Action 'wait' expects a number, but got '{tipo}'.")
    
    def execute(self):
        pass # Implementar

    def draw(self, indent=0):
        prefix = "  " * indent
        print(f"{prefix}└─ Wait")
        self.time.draw(indent + 1)

class Move(Action):
    def __init__(self, location: Location, dx: Number | Ident, dy: Number | Ident, speed: Number | Ident):
        super().__init__(location)
        self.dx = dx
        self.dy = dy
        self.speed = speed

    def check(self, context: Context): # Verifica que cada uno sea 'int'
        if self.dx.check(context) == 'str':
            raise SemanticError(self.location, f"Action 'move' expects a number for dx.")
        if self.dy.check(context) == 'str':
            raise SemanticError(self.location, f"Action 'move' expects a number for dy.")
        if self.speed.check(context) == 'str':
            raise SemanticError(self.location, f"Action 'move' expects a number for speed.")

    def execute(self):
        pass # Implementar

    def draw(self, indent=0):
        prefix = "  " * indent
        print(f"{prefix}└─ Move")
        self.dx.draw(indent + 1)
        self.dy.draw(indent + 1)
        self.speed.draw(indent + 1)

class Attack(Action):

    def __init__(self, location: Location, dx: Number | Ident, dy: Number | Ident, damage: Number | Ident):
        super().__init__(location)
        self.dx = dx
        self.dy = dy
        self.damage = damage

    def check(self, context: Context):
        if self.dx.check(context) == 'str': # Verifica que cada uno sea 'int'
            raise SemanticError(self.location, "Action 'attack' expects a number for dx.")
        if self.dy.check(context) == 'str':
            raise SemanticError(self.location, "Action 'attack' expects a number for dy.")
        if self.damage.check(context) == 'str':
            raise SemanticError(self.location, "Action 'attack' expects a number for damage.")
    
    def execute(self):
        pass

    def draw(self, indent=0):
        prefix = "  " * indent
        print(f"{prefix}└─ Attack")
        self.dx.draw(indent + 1)
        self.dy.draw(indent + 1)
        self.damage.draw(indent + 1)
    
class Reproduce(Action):

    def __init__(self, location: Location, dx: Number | Ident, dy: Number | Ident, health: Number | Ident):
        super().__init__(location)
        self.dx = dx
        self.dy = dy
        self.health = health

    def check(self, context: Context): # Verifica que cada uno sea 'int'
        if self.dx.check(context) == 'str':
            raise SemanticError(self.location, "Action 'reproduce' expects a number for dx.")
        if self.dy.check(context) == 'str':
            raise SemanticError(self.location, "Action 'reproduce' expects a number for dy.")
        if self.health.check(context) == 'str':
            raise SemanticError(self.location, "Action 'reproduce' expects a number for health.")
    
    def execute(self):
        pass

    def draw(self, indent=0):
        prefix = "  " * indent
        print(f"{prefix}└─ Reproduce")
        self.dx.draw(indent + 1)
        self.dy.draw(indent + 1)
        self.health.draw(indent + 1)
    
class Consume(Action):
    def __init__(self, location: Location, dx: Number | Ident, dy: Number | Ident, damage :  Number | Ident, heal: Number | Ident):    
        super().__init__(location)
        self.dx = dx
        self.dy = dy
        self.damage = damage
        self.heal = heal
    
    def check(self, context: Context):
        if self.dx.check(context) == 'str': # Verifica que cada uno sea 'int'
            raise SemanticError(self.location, "Action 'consume' expects a number for dx.")
        if self.dy.check(context) == 'str':
            raise SemanticError(self.location, "Action 'consume' expects a number for dy.")
        if self.damage.check(context) == 'str':
            raise SemanticError(self.location, "Action 'consume' expects a number for damage.")  
        if self.heal.check(context) == 'str':
            raise SemanticError(self.location, "Action 'consume' expects a number for heal.")
    
    def execute(self):
        pass # Implementar

    def draw(self, indent=0):
        prefix = "  " * indent
        print(f"{prefix}└─ Consume")
        self.dx.draw(indent + 1)
        self.dy.draw(indent + 1)
        self.damage.draw(indent + 1)
        self.heal.draw(indent + 1)

class Roar(Action):
    def __init__(self, location: Location, text: Expression):
        super().__init__(location)
        self.text = text
    
    def check(self, context: Context): # Basta con verificar que su expression recibida es valida
        self.text.check(context)
    
    def execute(self):
        pass # Implementar

    def draw(self, indent=0):
        prefix = "  " * indent
        print(f"{prefix}└─ Roar")
        self.text.draw(indent + 1)

class Say(Action):
    def __init__(self, location: Location, text: Expression):
        super().__init__(location)
        self.text = text
    
    def check(self, context: Context): # Basta con verificar que su expression recibida es valida
        self.text.check(context)
    
    def execute(self):
        pass # implementar

    def draw(self, indent=0):
        prefix = "  " * indent
        print(f"{prefix}└─ Say")
        self.text.draw(indent + 1)