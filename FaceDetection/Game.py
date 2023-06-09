import random
from FaceDetection.Player import Player
from FaceDetection.Monster import Monster
class GameMap:
    def __init__(self, size: int):
        self.arms: list = ["⛏","🔫", "💣", "🗡", "🏹", "🛠"]
        self.food: list = ["🍎", "🍉", "🍕", "🥗"]
        self.size = size
        self.matrix = [[None] * size for _ in range(size)]
        self.place_items()

    def place_items(self):
        available_positions = [(row, col) for row in range(self.size) for col in range(self.size)]
        random.shuffle(available_positions)

        for item in self.arms + self.food:
            row, col = available_positions.pop()
            self.matrix[row][col] = item

        for row, col in available_positions:
            self.matrix[row][col] = "-"

    def place_player(self, player):
        available_positions = [(row, col) for row in range(self.size) for col in range(self.size) if
                               self.matrix[row][col] == "-"]
        position = random.choice(available_positions)
        player.row, player.col = position
        self.matrix[player.row][player.col] = "🥷"

    def place_monster(self, monster):
        available_positions = [(row, col) for row in range(self.size) for col in range(self.size) if
                               self.matrix[row][col] == "-"]
        position = random.choice(available_positions)
        monster.row, monster.col = position
        self.matrix[monster.row][monster.col] = "👽"

    def print_map(self):
        for row in self.matrix:
         print(row)






#player.print_inventory()