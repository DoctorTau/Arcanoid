import pygame as pg
import sys


class Platform:
    width = 0
    height = 0
    x_place = 0
    y_place = 0
    speed = 10

    def __init__(self, w, h, x, y):
        self.width = w
        self.height = h
        self.x_place = x
        self.y_place = y

    def paint(self, screen):
        pg.draw.rect(screen, white, (self.x_place, self.y_place, self.width, self.height), 0)

    def moving(self, direction):
        if self.x_place + self.width + self.speed * direction < width and self.x_place + self.speed * direction > 0:
            self.x_place += self.speed * direction

    def get_position(self):
        position = self.x_place + self.width, self.y_place + self.height
        return position


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
        screen.blit(ts_1, (width // 2 - 90, height // 2 - 50))
        screen.blit(ts_2, (width // 2 - 85, height // 2))

        font_tip =pg.font.SysFont('Comic Sans MS', 30, True)
        ts_tip = font_tip.render(self.tip, False, white)
        screen.blit(ts_tip, (width // 2 - 120, height // 2 + 70))


size = width, height = 800, 600
black = 0, 0, 0
white = 255, 255, 255


def main():
    pg.init()
    pg.font.init()
    screen = pg.display.set_mode(size)
    game_over = False
    game_over_flag = False

    ball = pg.image.load("basketball.png")
    ballrect = ball.get_rect()
    ballrect.x = width//2
    ballrect.y = 0
    ball_speed = 5
    ball_direction_x, ball_direction_y = 1, 1

    platform = Platform(250, 40, width // 2 - 250 // 2, 9 * height // 10)
    platform_direction = 0

    score = Score()
    game_over_text = GameOverText()

    while not game_over:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                game_over = True

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_RIGHT:
                    platform_direction = 1
                elif event.key == pg.K_LEFT:
                    platform_direction = -1

            elif event.type == pg.KEYUP:
                if event.key == pg.K_RIGHT and platform_direction == 1 or \
                        event.key == pg.K_LEFT and platform_direction == -1:
                    platform_direction = 0

        moving_x = ball_speed * ball_direction_x
        moving_y = ball_speed * ball_direction_y

        platform_position = platform.get_position()

        if ballrect.x + 100 + moving_x >= width or ballrect.x + moving_x <= 0:
            ball_direction_x *= -1
        if ballrect.y + moving_y <= 0:
            ball_direction_y *= -1
        elif ballrect.y + 100 + moving_y >= height:
            ball_direction_x = ball_direction_y = 0
            game_over_flag = True

        if ((ballrect.x + 100 + moving_x >= platform.x_place and ballrect.x + moving_x <= platform_position[0]) and \
                (ballrect.y + 100 + moving_y >= platform.y_place)):
            ball_direction_x *= -1
            ball_direction_y *= -1
            score.score += 1
            ball_speed += 0.2

        ballrect.x += moving_x
        ballrect.y += moving_y
        platform.moving(platform_direction)

        screen.fill(black)
        screen.blit(ball, ballrect)
        platform.paint(screen)
        score.paint(screen, width - 150, 0)

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
            score.paint(screen, width // 2 - 50, height // 2 + 45)
            game_over_text.paint(screen)
            pg.display.flip()

    sys.exit()


if __name__ == '__main__':
    main()
