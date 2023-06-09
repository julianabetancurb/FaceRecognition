
class Player:
    def __init__(self):
        self.life = 1
        self.arms_inventory = []
        self.row = None
        self.col = None
        self.player_emoji = "🥷"
        self.weapon_damage = {
            "⛏": 40,
            "🔫": 30,
            "💣": 30,
            "🗡": 40,
            "🏹": 30,
            "🛠": 40
        }

    def show_life_player(self):
        print(f"Player: {self.life}")

    def move_player(self, direction, game_map):
        new_row, new_col = self.get_new_position(direction)  # llama al metodo para moverse a la direccion

        if self.is_valid_move(new_row, new_col, game_map):  # luego verifica que el movimiento sea valido
            item = game_map.matrix[new_row][new_col]  # luego asigna como item a el simbolo que haya en la casilla
            if item in game_map.arms:  # si el item es un arma lo guarda al inventario
                self.arms_inventory.append(item)
                game_map.matrix[new_row][new_col] = "-"  # reemplaza lo que habia por un -
            elif item in game_map.food:  # si es una comida, aumenta su vida
                self.life += 20
                game_map.matrix[new_row][new_col] = "-"
            game_map.matrix[self.row][self.col] = "-"
            self.row = new_row
            self.col = new_col
            game_map.matrix[self.row][self.col] = self.player_emoji

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

    def print_inventory(self):
        print("Player Inventory:")
        if len(self.arms_inventory) == 0:
            print("Empty")
        else:
            for item in self.arms_inventory:
                print(item)

    def attack(self, monster):
        distance = abs(self.row - monster.row) + abs(self.col - monster.col)
        if distance == 1 and self.arms_inventory:
            print("Opciones de arma:")
            for i, weapon in enumerate(self.arms_inventory):
                print(f"{i + 1}. {weapon}")

            selected_option = input("Selecciona el número del arma a utilizar: ")
            if selected_option.isdigit() and 1 <= int(selected_option) <= len(self.arms_inventory):
                selected_weapon = self.arms_inventory[int(selected_option) - 1]
                damage = self.weapon_damage.get(selected_weapon, 0)
                monster.life -= damage
                self.life -= damage  # Restar el daño al jugador
                print(f"Atacaste al monstruo con {selected_weapon} y le quitaste {damage} de vida.")
                self.arms_inventory.remove(selected_weapon)  # Eliminar el arma del inventario del jugador
            else:
                print("Opción de arma inválida.")
        else:
            print("El monstruo no está cerca para atacar.")



