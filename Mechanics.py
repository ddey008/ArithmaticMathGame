# Mechanics class essentially implements the drop algorithm with physics.
# It also holds the out of bounds checker which if true makes the question delete itself


class Mechanics:

    def __init__(self, x, y, ground_level, max_y):
        self.x = x
        self.y = y
        self.accel = 0
        self.velocity = 6
        self.ground_level = ground_level
        self.max_y = max_y

    def update(self):
        self.velocity += self.accel
        self.y -= self.velocity

    def delete(self):
        del self

    def check_out_of_bounds(self):
        if self.y > self.max_y or self.y < self.ground_level:
            return True
        else:
            return False

    def stop_movement(self):
        self.velocity = 0
        self.accel = 0
