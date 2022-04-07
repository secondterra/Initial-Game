###
# attr info https://towardsdatascience.com/probably-the-best-practice-of-object-oriented-python-attr-d8c26c0e8a4
# attr página oficial https://www.attrs.org/
###
import attr
import json

import weapons
import ruta

#TODO: Tiene muchos atributos, tal vez se pueda agrupar algunos en caracteristicas
@attr.s
class Player():
    """Atributos necesarios y en orden:
    name, body, hair, outfit, Socket

    Los demás atributos son opcionales y tienen un valor por defecto"""
    name = attr.ib()
    body = attr.ib()
    hair = attr.ib()
    outfit = attr.ib()
    frame = attr.ib(init=False,default=0)
    dir = attr.ib(init=False,default='down')
    action = attr.ib(init=False,default='stop') # Esta action sobra.
    # no se elimina aún porque el front depende de este campo
    #TODO: Eliminar del front, al menos para que se use internamente
    chat = attr.ib(init=False,default='')
    #TODO: Revisar si se puede agrupar en posición
    posX = attr.ib(init=False,default=544)
    posY = attr.ib(init=False,default=800)
    H = attr.ib(init=False,default=48)
    W = attr.ib(init=False,default=32)
    Socket = attr.ib()
    max_health = attr.ib(init=False,default=50) #TODO: tal vez esto va en propiedades del juego?
    health = attr.ib(init=False,default=50)
    speed = attr.ib(init=False,default=3) #TODO: tal vez esto va en propiedades del juego?
    ruta = attr.ib(init=False,factory=dict)
    step = attr.ib(init=False,default=1)
    moves = attr.ib(init=False,default=0)
    weapons = attr.ib(init=False)

    @weapons.default
    def weapons_initialization(self):
        #El nombre del arma se repite como dict key y como valor dentro del dict
        #TODO: Revisar si se puede utilizar un array
        return {
            weapons.clases["normal_gun"]["name"]: weapons.clases["normal_gun"],
            weapons.clases["normal_bomerang"]["name"]: weapons.clases["normal_bomerang"]
        }

    def move(self, direction, step, moves):
        if direction == "up":
            self.posY -= self.speed
        elif direction == "down":
            self.posY += self.speed
        elif direction == "left":
            self.posX -= self.speed
        elif direction == "right":
            self.posX += self.speed

        self.frame += 1
        if self.frame > 3:
            self.frame = 0

        self.dir = direction
        self.step = step
        self.moves = moves

    def stop(self):
        self.ruta = {}
        self.step = 1
        self.moves = 0

    def get_data(self):
        return {
            'dir': self.dir,
            'posX': self.posX,
            'posY': self.posY,
            'ruta': self.ruta,
            'step': self.step,
            'moves': self.moves
        }

    def get_full_data(self):
        return {
            'name': self.name,
            'body': self.body,
            'hair': self.hair,
            'outfit': self.outfit,
            'frame': self.frame,
            'dir': self.dir,
            'action': self.action,
            'chat': self.chat,
            'posX': self.posX,
            'posY': self.posY,
            'H': self.H,
            'W': self.W,
            'Socket': str(self.Socket),
            'max_health': self.max_health,
            'health': self.health,
            'speed': self.speed,
            'ruta': self.ruta,
            'step': self.step,
            'moves': self.moves,
            'weapons': self.weapons
        }

    #TODO: Cambiar a un nombre más descriptivo
    def refresh(self, posX, posY, desX, desY, map_name):
        self.posX = posX
        self.posY = posY
        self.ruta = ruta.calcular_ruta(posX,posY,self.W,self.H,desX,desY,map_name)
        self.step = 1
        self.moves = 0

    async def sendData(self, data):
        message = json.dumps(data)
        await self.Socket.send(message)
