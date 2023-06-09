import time

from FaceDetection.Monster import Monster
from FaceDetection.Player import Player
from FaceDetection.Game import GameMap

class Controller:

    def __init__(self):
        pass

    def iniciar(self):

        print("BIENVENIDO AL JUEGO")
        size = int(input("Ingrese el tamaño deseado para el tablero:"))
        tablero = GameMap(size)
        player = Player()
        monster = Monster()
        tablero.place_player(player)
        tablero.place_monster(monster)
        tablero.print_map()
        while monster.life >10:
            print("============PLAYER TURN============")
            move= input("Escriba hacia a donde se quiere mover: ")
            player.move_player(move, tablero)
            player.print_inventory()
            player.show_life_player()
            monster.show_life_monster()
            tablero.print_map()
            time.sleep(3)
            print("============MONSTER TURN============")
            monster.move_monster(tablero, player)
            player.show_life_player()
            monster.show_life_monster()
            tablero.print_map()
            player.attack(monster)

controller = Controller()
controller.iniciar()


