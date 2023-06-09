import random
class Monster:
    def __init__(self):
        self.life = 100
        self.row = None
        self.col = None
        self.monster_emoji = "👽"

    def show_life_monster(self):
        print(f"Monster: {self.life}")

    def move_monster(self, game_map, player):
        directions = ["up", "down", "left", "right"]
        random.shuffle(directions)

        for direction in directions:
            new_row, new_col = self.get_new_position(direction)

            if self.is_valid_move(new_row, new_col, game_map):
                game_map.matrix[self.row][self.col] = "-"
                self.row = new_row
                self.col = new_col

                item = game_map.matrix[self.row][self.col]
                if item in game_map.food:
                    self.life += 20  # Aumentar la vida del monstruo cuando cae en una casilla con comida
                    game_map.matrix[new_row][new_col] = "-"  # Reemplazar la nueva celda por "-"
                elif item in game_map.arms:
                    game_map.matrix[new_row][new_col] = item
                elif self.row == player.row and self.col == player.col:
                    print("El mountro a atacado al jugador y le ha quitado 25 de vida!!!")
                    player.life -= 25  # Restar 25 de vida al jugador cuando el monstruo y el jugador están en la misma celda
                    player.attack(self)  # Llamar al método attack() del jugador
                    self.move_away_from_player(game_map, player)

                game_map.matrix[self.row][self.col] = self.monster_emoji
                break
    #esta funcion sirve para cuando el monster quiere caer a una casilla del player, se le ataque pero se mueva
    #a otro lado para que ambos emojis se conserven en el tablero
    def move_away_from_player(self, game_map, player):
        # Obtener las coordenadas adyacentes válidas
        adjacent_positions = [(self.row - 1, self.col), (self.row + 1, self.col), (self.row, self.col - 1),
                              (self.row, self.col + 1)]
        valid_positions = [(row, col) for row, col in adjacent_positions if self.is_valid_move(row, col, game_map)]
        if valid_positions:
            # Mover el monstruo a una posición adyacente aleatoria
            new_row, new_col = random.choice(valid_positions)
            game_map.matrix[self.row][self.col] = player.player_emoji
            self.row = new_row
            self.col = new_col
            game_map.matrix[self.row][self.col] = self.monster_emoji

    def get_new_position(self, direction):
        if direction == "up":
            return self.row - 1, self.col
        elif direction == "down":
            return self.row + 1, self.col
        elif direction == "left":
            return self.row, self.col - 1
        elif direction == "right":
            return self.row, self.col + 1

    def is_valid_move(self, row, col, game_map):
        size = game_map.size
        return 0 <= row < size and 0 <= col < size
