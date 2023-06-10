import time
from FaceDetection.Monster import Monster
from FaceDetection.Player import Player
from FaceDetection.Game import GameMap
import Mediapipe
class Controller:

    def __init__(self):
        pass
    def iniciar(self):
        print("BIENVENIDO AL JUEGO")
        size = int(input("Ingrese el tamaño para el tablero:"))
        tablero = GameMap(size)
        player = Player()
        monster = Monster()
        tablero.place_player(player)
        tablero.place_monster(monster)
        tablero.print_map()
        perder = True
        while perder:
            print("============PLAYER TURN============")
            print("Mueva su cabeza hacia donde se desea mover y presione la tecla m")
            move, mouth, arms = Mediapipe.capture_look()  # Asignar la dirección capturada a la variable 'move'
            if move is not None and move != "forward":
                player.move_player(move, tablero)
            else:
                print("No puedes moverte hacia el frente! intenta de nuevo..")
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
            if player.check_attack(monster):
                print("Si quiere atacar al monstruo abra la boca y presione m")
                player.attack(monster)
            else:
                print("Aun no puedes atacar al monstruo")

            if monster.life <= 0:
                print("el jugador gano!!!!")
                perder = False
            elif player.life <= 0:
                print("el mounstro gano :(")
                perder = False





controller = Controller()
controller.iniciar()


