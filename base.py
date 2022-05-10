
class Base:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.velocity = 0.5

    def move(self):
        self.x -= self.velocity

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))
