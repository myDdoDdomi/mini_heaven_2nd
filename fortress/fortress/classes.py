damage_scale = 1
class Player:
    
    def __init__(self, initial_position, side):
        self.position = initial_position
        self.damage = 1
        self.volume = 10
        self.side = side
        self.hp = 10

    def move(self, dx, dy):
        self.position[0] += dx
        self.position[1] += dy

    def hit(self):
        self.hp -= (self.damage * damage_scale)