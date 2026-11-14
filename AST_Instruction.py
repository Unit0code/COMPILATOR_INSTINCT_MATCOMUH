from __future__ import annotations
from abc import ABC, abstractmethod
from Errors import Location
from AST_Nodes import Node
from AST_Expression import Ident, Variable, Number, Text, BinaryExpression, UnaryExpression

# Los Nodos de Instruction
class Instruction(Node): # Clase abstracta, No se instancia
    @abstractmethod
    def execute(self):
        pass # No se implementa

class Assign(Instruction):
    def __init__(self, location: Location, variable: Variable, value: Number | Text | Variable):
        super().__init__(location)
        self.variable = variable
        self.value = value
    
    def check(self):
        pass # Implementar, me parece que no debe de hacer bada

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
    
    def check(self):
        pass # Implementar
    
    def execute(self):
        pass # Implementar, necesitas program counter

    def draw(self, indent=0):
        prefix = "  " * indent
        print(f"{prefix}└─ IfGoto (salta a '{self.goto}')")
        self.condition.draw(indent + 1)

class GoTo(Instruction):
    def __init__(self, location: Location, label: str): # Ojo, el parser no detecta si label existe hasta no haber recorrido todo el archivo, por tanto mejor pasarle un str al goto, y kuego semanticamente revisar si el label existe
        super().__init__(location)
        self.label = label
    
    def check(self):
        pass # Implementar, verificar que lo sigte a el es un label de verdad
    
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

    def check(self):
        pass

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
    
    def check(self):
        pass # Implementar
    
    def execute(self):
        pass # Implementar

    def draw(self, indent=0):
        prefix = "  " * indent
        print(f"{prefix}└─ Wait")
        self.time.draw(indent + 1)

class Move(Action):
    def __init__(self, location: Location, dx: Number | Ident, dy: Number | Ident, howmuch: Number | Ident):
        super().__init__(location)
        self.dx = dx
        self.dy = dy
        self.howmuch = howmuch

    def check(self):
        pass # Implementar, hara falta?

    def execute(self):
        pass # Implementar

    def draw(self, indent=0):
        prefix = "  " * indent
        print(f"{prefix}└─ Move")
        self.dx.draw(indent + 1)
        self.dy.draw(indent + 1)
        self.howmuch.draw(indent + 1)

class Attack(Action):

    def __init__(self, location: Location, dx: Number | Ident, dy: Number | Ident, damage: Number | Ident):
        super().__init__(location)
        self.dx = dx
        self.dy = dy
        self.damage = damage

    def check(self):
        pass # Implementar, no se si sea necesario
    
    def execute(self):
        pass

    def draw(self, indent=0):
        prefix = "  " * indent
        print(f"{prefix}└─ Attack")
        self.dx.draw(indent + 1)
        self.dy.draw(indent + 1)
        self.damage.draw(indent + 1)
    
class Reproduce(Action):

    def __init__(self, location: Location, dx: Number | Ident, dy: Number | Ident, heal: Number | Ident):
        super().__init__(location)
        self.dx = dx
        self.dy = dy
        self.heal = heal

    def check(self):
        pass # Implementar, nose
    
    def execute(self):
        pass

    def draw(self, indent=0):
        prefix = "  " * indent
        print(f"{prefix}└─ Reproduce")
        self.dx.draw(indent + 1)
        self.dy.draw(indent + 1)
        self.heal.draw(indent + 1)
    
class Consume(Action):
    def __init__(self, location: Location, dx: Number | Ident, dy: Number | Ident, damage :  Number | Ident, heal: Number | Ident):    
        super().__init__(location)
        self.dx = dx
        self.dy = dy
        self.damage = damage
        self.heal = heal
    
    def check(self):
        pass # Implementar
    
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
    def __init__(self, location: Location, Text: Text | Ident):
        super().__init__(location)
        self.text = Text
    
    def check(self):
        pass # Implementar
    
    def execute(self):
        pass # Implementar

    def draw(self, indent=0):
        prefix = "  " * indent
        print(f"{prefix}└─ Roar")
        self.text.draw(indent + 1)

class Say(Action):
    def __init__(self, location: Location, text: Text):
        super().__init__(location)
        self.text = text
    
    def check(self):
        pass # Implementar
    
    def execute(self):
        pass # implementar

    def draw(self, indent=0):
        prefix = "  " * indent
        print(f"{prefix}└─ Say")
        self.text.draw(indent + 1)