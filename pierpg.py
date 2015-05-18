import gamepie as pie

SPRITE_SIZE = (16, 16)
RESIZE = (64, 64)

BTN_SIZE = (15, 9)
BTN_RESIZE = (60, 36)

# Colors
WHITE = (255, 255, 255)

class Player(pie.graphics.Sprite):
    def setup(self):
        self.walkdown = pie.tmx.TileSet(
            "assets/player.png", (0, 0), SPRITE_SIZE, 2, WHITE)
        self.walkdown.resize(*RESIZE)
        self.walkup = pie.tmx.TileSet(
            "assets/player.png", (32, 32), SPRITE_SIZE, 2, WHITE)
        self.walkup.resize(*RESIZE)
        self.walkright = pie.tmx.TileSet(
            "assets/player.png", (64, 64), SPRITE_SIZE, 4, WHITE)
        self.walkright.resize(*RESIZE)
        self.walkleft = pie.tmx.TileSet(
            "assets/player.png", (128, 128), SPRITE_SIZE, 4, WHITE)
        self.walkleft.resize(*RESIZE)

        self.sheet = self.walkdown
        self.rect = pie.types.Rect(0, 0, 64, 64)
        self.anim_delay = 0.3
        self.speed = 175
        self.walk = 0

        self.up = False
        self.down = False

    def update(self, dt):
        self.up = False
        self.down = False

        if pie.keyboard.isDown("up", "w"):
            self.moveUp(dt)
        elif pie.keyboard.isDown("down", "s"):
            self.moveDown(dt)

        if pie.keyboard.isDown("left", "a"):
            self.moveLeft(dt)
        elif pie.keyboard.isDown("right", "d"):
            self.moveRight(dt)

    def moveLeft(self, dt):
        if self.sheet != self.walkleft and not (self.up or self.down):
            self.sheet = self.walkleft
            self.walk = 0
            
        self.walk += dt
        if self.walk >= self.anim_delay:
            self.walk = 0
            self.sheet.advance()

        self.rect.x -= self.speed * dt
        for tile in pie.getGame().world.top:
            rect = tile.getRect()
            if rect.collideRect(self.rect):
                self.rect.x = rect.x + rect.w

    def moveRight(self, dt):
        if self.sheet != self.walkright and not (self.up or self.down):
            self.sheet = self.walkright
            self.walk = 0
            
        self.walk += dt
        if self.walk >= self.anim_delay:
            self.walk = 0
            self.sheet.advance()

        self.rect.x += self.speed * dt
        for tile in pie.getGame().world.top:
            rect = tile.getRect()
            if rect.collideRect(self.rect):
                self.rect.x = rect.x - rect.w

    def moveUp(self, dt):
        self.up = True
        if self.sheet != self.walkup:
            self.sheet = self.walkup
            self.walk = 0
            
        self.walk += dt
        if self.walk >= self.anim_delay:
            self.walk = 0
            self.sheet.advance()

        self.rect.y -= self.speed * dt
        for tile in pie.getGame().world.top:
            rect = tile.getRect()
            if rect.collideRect(self.rect):
                self.rect.y = rect.y + rect.h

    def moveDown(self, dt):
        self.down = True
        if self.sheet != self.walkdown:
            self.sheet = self.walkdown
            self.walk = 0

        self.walk += dt
        if self.walk >= self.anim_delay:
            self.walk = 0
            self.sheet.advance()

        self.rect.y += self.speed * dt
        for tile in pie.getGame().world.top:
            rect = tile.getRect()
            if rect.collideRect(self.rect):
                self.rect.y = rect.y - rect.h

    def draw(self):
        pie.graphics.draw(self.sheet.getImage(),
                            self.rect.x, self.rect.y)


class World(object):
    def __init__(self):
        self.map = pie.tmx.TileMap("map.tmx", RESIZE)
        self.ground = self.map.layers["ground"].getAll()
        self.top = self.map.layers["top"].getAll()

    def render(self):
        for tile in self.ground:
            img = tile.getImage()
            rect = img.rect
            pie.graphics.draw(img, rect.x, rect.y)

        for tile in self.top:
            img = tile.getImage()
            rect = img.rect
            pie.graphics.draw(img, rect.x, rect.y)


class Button(pie.graphics.Sprite):
    def setup(self, image, x, y, name):
        self.rect = image.getRect()
        self.rect.x = x
        self.rect.y = y
        self.image = image
        self.name = name

    def draw(self):
        pie.graphics.draw(self.image, self.rect.x, self.rect.y, False)


class PieRPG(pie.Game):
    def conf(self):
        self.gamepie = "0.2"
        self.version = "0.1"
        self.title = "PieRPG"
        self.size = (640, 512)

    def load(self):
        self.player = Player()
        self.world = World()
        self.buttons = pie.tmx.TileSet(
            "assets/buttons.png", (0, 0), BTN_SIZE, 4, WHITE)
        self.buttons.resize(*BTN_RESIZE)

        sy = pie.graphics.getHeight()
        self.btns = [
            Button(self.buttons.images[0], 70, sy - 86, "Up"),
            Button(self.buttons.images[1], 70, sy - 50, "Down"),
            Button(self.buttons.images[2], 10, sy - 50, "Left"),
            Button(self.buttons.images[3], 130, sy - 50, "Right")
        ]
        self.pressed = None

        pie.graphics.setBackgroundColor(123, 186, 255)

    def mousepressed(self, x, y, button):
        for button in self.btns:
            if button.rect.collidePoint((x, y)):
                self.pressed = button.name
                break

    def mousereleased(self, x, y, button):
        self.pressed = None

    def updatePC(self, dt):
        if pie.keyboard.isDown("escape"):
            self.exit()

        self.player.update(dt)

    def updateiOS(self, dt):
        if self.pressed:
            getattr(self.player, "move" + self.pressed)(dt)

    def update(self, dt):
        self.camera.update(self.player.rect)

    def drawiOS(self, dt):
        for button in self.btns:
            button.draw()

    def draw(self, dt):
        self.world.render()
        self.player.draw()

pierpg = PieRPG()
pie.run(pierpg)