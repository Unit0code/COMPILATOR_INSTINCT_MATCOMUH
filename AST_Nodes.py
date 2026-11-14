#AST Nodess, la estructura de arbol de las clases Nodos
from __future__ import annotations
from abc import ABC, abstractmethod
from Errors import Location
from Maps_Object_Terrains import Map, Object

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

# HACER LA FUNCIONALIDAD DRAW
# HACER LOS CHECK
# con respecto a los check, verificar tmb que cuando apliques operaciones, binary y unary y funcioncall, verifique los tipos de datos, no solo si existen
# PASARLE A TODOS LOS CHECK EL CONTEXT
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
    def __init__(self, variables_type: dict, variables_value: dict):
        self.variables_type = variables_type # Clave(nombre de la variable) : valor(tipo de su ultima assign o 'any' en caso de
                                            # haber cambiado de tipo durante la ejecucion del programa
        self.variables_value = variables_value # Clave(nombre de la variable) : valor(ultima asignacion)


class Node(ABC): #Clase abstracta
    @abstractmethod
    def check(self, context: Context):
        pass
    
    def draw(self, indent=0):
        prefix = "  " * indent
        print(f"{prefix}└─ {self.__class__.__name__}")

class Heather(Node):
    def __init__(self, name: str, faction: str, health: int, lifespan: int, vision: int):
        self.heather_dict = {
            'name': name,
            'faction': faction,
            'health': health,
            'lifespan': lifespan,
            'vision': vision
        }
    
    def check(self): # aPLICARLO PARA VERIFICAR VALORES CORRECTOS DE LAS CABECERAS
        pass

    def draw(self, indent=0):
        prefix = "  " * indent
        print(f"{prefix}└─ Header:")
        for key, value in self.heather_dict.items():
            print(f"{prefix}    - {key}: {value}")

class Creature(Node): #Esta va a ser la clase que albergue el Ast de una criatura
    def __init__(self, heather: Heather, statements: list, context: Context): # es decir, una instancia por archivo .ins
        self.heather = heather
        self.statements = statements # Lista de Instrucciones desde start en lo adelante
        self.context = context
        self.program_counter = [0,0] # Indicara por donde anda con respecto a los labels

    def check(self):
        pass    #implementar, verificar que tiene etiqueta start, y los heather, que se verifique el solo si tiene todo bien

    def draw(self): # Esto es para printear todo el arbol AST de la criatura
        self.heather.draw()
        print("\nInstrucciones:")
        for instruction in self.labels:
            instruction.draw(indent=1)



