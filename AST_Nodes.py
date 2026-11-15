#AST Nodess, la estructura de arbol de las clases Nodos
from __future__ import annotations
from typing import TYPE_CHECKING
from abc import ABC, abstractmethod
from Errors import Location, ParseError, SemanticError
from Maps_Object_Terrains import Map, Object

# Esto es para poder importar cosas sin hacer referencia circular
if TYPE_CHECKING:
    from AST_Expression import Text, Number
    from AST_Instruction import Label

#Diccionario de CONSTANTES

CONSTANTS = {
    'NONE': -1,
    'GROUND': 0,
    'OBJECT': 1,
    'ALLY': 2,
    'ENEMY': 3
}

# Set de Percepciones para comparar con las ident que se va encontrando el parser e instanciar una percepcion si el nombre esta aqui adentro
PERCEPTIONS = {'health', 'lifespan', 'vision', 'faction', 'species', 'age',
                'x', 'y', 'terrain_here', 'reserve_here', 'width', 'height', 
                'total_creatures', 'total_allies', 'total_enemies', 'random', 
                'allies_near', 'enemies_near', 'objects_near', 'enemy_dist', 
                'enemy_dx', 'enemy_dy', 'ally_dist', 'ally_dx', 'ally_dy', 'object_dist', 
                'object_dx', 'object_dy', 'roars_near', 'last_roar', 'tick'}


# HACER LOS EVALUATE
# PASARLE A TODOS EL MAP CUANDO HACE EVALUATE, ESPECIFICAMENTE POR FunCall
# HACER LOS EXECUTE
# HACER assign method PARA IDENT


class Program: #Este no pertenece a la estructura del arbol en si, es el programa donde
                # se guardaran todos los datos del programa
    def __init__(self, creatures: list[Creature], maps: list[Map], objects: list[Object]):
        self.creatures = creatures
        self.maps = maps
        self.objects = objects 

class Context: # Guardara todas las variables que existen y su valor si ya fueron asignadas
    def __init__(self):

        self.variables_created = set() # Todas lasa que en algun momento se asignaron
        self.variables_value = {} # Clave(nombre de la variable) : valor(ultima asignacion)
        self.labels = set() # Tendra los labels creados hasta el momento


class Node(ABC): #Clase abstracta
    @abstractmethod
    def check(self, context: Context):
        pass
    
    def draw(self, indent=0):
        prefix = "  " * indent
        print(f"{prefix}└─ {self.__class__.__name__}")

class Heather(Node):
    '''OJOOOO, la cabecera debes pasarla como Text o Number, no como Ident, Variable, Constant o Perception OJOO'''
    def __init__(self, name: Text, faction: Text, health: Number, lifespan: Number, vision: Number):
        self.name = name
        self.faction = faction
        self.health = health
        self.lifespan = lifespan
        self.vision = vision
        self.heather_dict = self.heather_dict_func(name, faction, health, lifespan, vision) # Para que sea mas facil acceder a la cabecera

    def check(self, context: Context):
        if not self.name.label.strip(): # Verifica que no sean str vacios
            raise SemanticError(self.name.location, "Header error: 'creature' name cannot be empty.")
            
        if not self.faction.label.strip():
            raise SemanticError(self.faction.location, "Header error: 'faction' cannot be empty.")
        
        if self.health.value <= 0: # Verifica que tengan valores aceptados
            raise SemanticError(self.health.location, "Header error: 'health' must be greater than 0.")
            
        if self.vision.value < 1:
            raise SemanticError(self.vision.location, "Header error: 'vision' must be at least 1.")
            
        if self.lifespan.value <= 0:
            raise SemanticError(self.lifespan.location, "Header error: 'lifespan' must be greater than 0.")
        
    def heather_dict_func(self, name: Text, faction: Text, health: Number, lifespan: Number, vision: Number) -> dict:
        return {
            'name': name.label,
            'faction': faction.label,
            'health': health.value,
            'lifespan': lifespan.value,
            'vision': vision.value
        }

    def draw(self, indent=0):
        prefix = "  " * indent
        print(f"{prefix}└─ Header:")
        self.name.draw(indent + 1)
        self.faction.draw(indent + 1)
        self.health.draw(indent + 1)
        self.lifespan.draw(indent + 1)
        self.vision.draw(indent + 1)

class Creature(Node): 

    '''Esta va a ser la clase que albergue el Ast de una criatura'''

    def __init__(self, heather: Heather, statements: list): # es decir, una instancia por archivo .ins
        self.heather = heather
        self.statements = statements # Lista de Instrucciones desde start en lo adelante
        self.context = Context()
        self.program_counter = 0 # Indicara por donde anda con respecto a los labels

    def check(self):
        
        context = self.context
        self.heather.check(context) #Verifica que las cabeceras esten correctas
        
        for statement in self.statements:    
            if statement.__class__.__name__ == 'Label': # Agrega los nombres de las cabeceras a context.label
                statement.check(context)
            
            elif statement.__class__.__name__ == 'Assign' and statement.variable.__class__.__name__ == 'Variable':
                context.variables_created.add(statement.variable.name)

        for statement in self.statements: #Ahora si checkear todas las instrucciones
            if statement.__class__.__name__ != 'Label':
                statement.check(context) 

    def draw(self): # Esto es para printear todo el arbol AST de la criatura
        self.heather.draw()
        print("\nInstrucciones:")
        for instruction in self.statements:
            instruction.draw(indent=1)
