import pygame as pg
import sys


class GameObject:
    x_place = 0
    y_place = 0
    width = 0
    height = 0

    def __init__(self, x_place, y_place, width, height):
        self.x_place = x_place
        self.y_place = y_place
        self.width = width
        self.height = height

    def is_crossing_object(self, other):
        return not (self.y_place > other.y_place + other.height or
                    self.y_place + self.height < other.y_place or
                    self.x_place + self.width < other.x_place or
                    self.x_place > other.x_place + other.width)


class PlatformGreen(GameObject):

    def __init__(self, x_place, y_place, width, height, color=None):
        super().__init__(x_place, y_place, width, height)
        if color is None:
            color = [0, 0, 0]
        self.color = color

    def paint(self, screen):
        pg.draw.rect(screen, self.color, (self.x_place, self.y_place, self.width, self.height), 0)

    def get_type(self):
        return str(self.color)


class PlatformPlayer(GameObject):

    def __init__(self, x_place, y_place, width, height, speed):
        super().__init__(x_place, y_place, width, height)
        self.speed = speed
        self.direction_x = 0
        self.direction_y = 0

    def paint(self, screen):
        pg.draw.rect(screen, white, (self.x_place, self.y_place, self.width, self.height), 0)

    def move(self):
        if not self.is_crossing_screen_x():
            self.x_place += self.speed * self.direction_x

    def is_crossing_screen_x(self):
        return self.x_place + self.width + self.speed * self.direction_x >= screen_width or \
               self.x_place + self.speed * self.direction_x <= 0

    def is_crossing_screen_y_top(self):
        return self.y_place + self.speed * self.direction_y <= 0

    def is_crossing_screen_y_bottom(self):
        return self.y_place + self.height + self.speed * self.direction_y >= screen_height

    def get_position(self):
        position = self.x_place + self.width, self.y_place + self.height
        return position


class Ball(PlatformPlayer):

    def __init__(self, x_place, y_place, width, height, speed, picture=None):
        super().__init__(x_place, y_place, width, height, speed)
        if picture:
            self.picture = pg.image.load(picture)
        self.rect = self.picture.get_rect()
        self.width = self.rect.width
        self.height = self.rect.height
        self.rad = self.width // 2
        self.centre_x = self.x_place + self.rad
        self.centre_y = self.y_place + self.rad
        self.direction_x = 1
        self.direction_y = -1

    def move(self):
        if self.is_crossing_screen_x():
            self.direction_x *= -1
        if self.is_crossing_screen_y_top():
            self.direction_y *= -1
        self.x_place += self.speed * self.direction_x
        self.y_place += self.speed * self.direction_y
        self.centre_x = self.x_place + self.rad
        self.centre_y = self.y_place + self.rad

    def paint(self, screen):
        screen.blit(self.picture, (self.x_place, self.y_place))

    def ball_cross_platform(self, other):
        if (abs(self.centre_y + self.rad - other.y_place) <= self.speed or
            abs(self.centre_y - self.rad - other.y_place - other.height) <= self.speed) and \
                other.x_place <= self.centre_x <= other.x_place + other.width:
            self.direction_y *= -1
            return True
        elif abs((self.centre_x - other.x_place)**2 + (self.centre_y - other.y_place)**2) <= self.rad**2 + self.speed or\
            abs((self.centre_x - other.x_place - other.width)**2 + (self.centre_y - other.y_place)**2) <= self.rad**2 \
            + self.speed or abs((self.centre_x - other.x_place)**2 + (self.centre_y - other.y_place - other.height)**2)\
            <= self.rad**2 + self.speed or abs((self.centre_x - other.x_place - other.width)**2 +
            (self.centre_y - other.y_place - other.height)**2) <= self.rad**2 + self.speed:
            self.direction_y *= -1
            self.direction_x *= -1
            return True
        elif (abs(self.centre_x + self.rad - other.x_place) <= self.speed
              or abs(self.centre_x - self.rad - other.x_place + other.width) <= self.speed) and \
                other.y_place <= self.y_place <= other.y_place + other.height:
            self.direction_x *= -1
            return True
        return False


class Score:
    score = 0

    def paint(self, screen, position_x, position_y):
        font = pg.font.SysFont('Comic Sans MS', 30, True)
        data = 'Score: {}'.format(self.score)
        ts = font.render(data, False, white)
        screen.blit(ts, (position_x, position_y))


class GameOverText:
    data_1 = 'GAME'
    data_2 = 'OVER'
    tip = "Press Space to exit"

    def paint(self, screen):
        font = pg.font.SysFont('Comic Sans MS', 70, True)
        ts_1 = font.render(self.data_1, False, white)
        ts_2 = font.render(self.data_2, False, white)
        screen.blit(ts_1, (screen_width // 2 - 90, screen_height // 2 - 50))
        screen.blit(ts_2, (screen_width // 2 - 85, screen_height // 2))

        font_tip = pg.font.SysFont('Comic Sans MS', 30, True)
        ts_tip = font_tip.render(self.tip, False, white)
        screen.blit(ts_tip, (screen_width // 2 - 120, screen_height // 2 + 70))


size = screen_width, screen_height = 1200, 800
black = 0, 0, 0
white = 255, 255, 255
green = 0, 255, 0
yellow = 255, 255, 0


def main():
    pg.init()
    pg.font.init()
    screen = pg.display.set_mode(size)
    game_over = False
    game_over_flag = False

    ball = Ball(screen_width // 2, screen_height // 2, 100, 100, 5, 'basketball.png')

    platform = PlatformPlayer(screen_width // 2 - 250 // 2, screen_height // 10 * 9, 250, 40, 7)

    score = Score()
    game_over_text = GameOverText()

    colors = [green, yellow]
    platform_list = [PlatformGreen(20 + i, 20, 180, 30, green) for i in range(0, screen_width, 200)]
    platform_list_yellow = [PlatformGreen(20 + i, 70, 180, 30, yellow) for i in range(0, screen_width, 200)]

    while not game_over:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                game_over = True

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_RIGHT:
                    platform.direction_x = 1
                elif event.key == pg.K_LEFT:
                    platform.direction_x = -1

            elif event.type == pg.KEYUP:
                if event.key == pg.K_RIGHT and platform.direction_x == 1 or \
                        event.key == pg.K_LEFT and platform.direction_x == -1:
                    platform.direction_x = 0

        if ball.is_crossing_screen_y_bottom():
            game_over_flag = True

        if ball.ball_cross_platform(platform):
            score.score += 1
            ball.speed += 0.2
        platform.move()
        ball.move()

        for i in range(len(platform_list)):
            if ball.ball_cross_platform(platform_list[i]) != 0:
                platform_list[i] = PlatformGreen(0, 0, 0, 0)
        for i in range(len(platform_list_yellow)):
            if ball.ball_cross_platform(platform_list_yellow[i]) != 0:
                platform_list_yellow[i] = PlatformGreen(0, 0, 0, 0)

        screen.fill(black)
        ball.paint(screen)
        platform.paint(screen)
        score.paint(screen, screen_width - 150, 0)
        for i in platform_list:
            i.paint(screen)
        for i in platform_list_yellow:
            i.paint(screen)

        pg.display.flip()
        pg.time.wait(10)

        while game_over_flag:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    game_over = True
                    game_over_flag = False
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        game_over = True
                        game_over_flag = False
            screen.fill(black)
            score.paint(screen, screen_width // 2 - 50, screen_height // 2 + 45)
            game_over_text.paint(screen)
            pg.display.flip()

    sys.exit()


if __name__ == '__main__':
    main()
