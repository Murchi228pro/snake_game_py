import pygame as pg
import sys
import random as rn


class Head(pg.Rect):
    def __init__(self, x, y, rotation):
        super().__init__(x, y, 20, 20)
        self.rotation = rotation

    def ifCollisionApple(self, apple):
        if self.colliderect(apple):
            return True


rotation_speeds = {
    'u': (0, -20),
    'd': (0, 20),
    'l': (-20, 0),
    'r': (20, 0)
}
rotation_permissions = {
    'u': (1, 1, 1, 0),
    'd': (1, 1, 0, 1),
    'l': (1, 0, 1, 1),
    'r': (0, 1, 1, 1)
}

clock = pg.time.Clock()
pg.init()
pg.font.init()
window = pg.display.set_mode((800, 400))
try:
    font = pg.font.Font('Decrypted.ttf', 36)
except FileNotFoundError:
    font = pg.font.SysFont('consolas', 20)

game_over_font = pg.font.Font(pg.font.match_font('papyrus'), 40)
game_over_text = game_over_font.render(
    'press any button', False, (255, 255, 255))


def new_apple():
    apple_coords = (rn.randrange(40, 760, 20), rn.randrange(40, 360, 20))
    return pg.Rect(*apple_coords, 20, 20)


while True:
    head = Head(140, 60, 'r')
    length = [(80, 60), (100, 60), (120, 60)]

    apple = new_apple()
    score = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_UP and rotation_permissions[head.rotation][2]:
                    head.rotation = 'u'
                if event.key == pg.K_DOWN and rotation_permissions[head.rotation][3]:
                    head.rotation = 'd'
                if event.key == pg.K_LEFT and rotation_permissions[head.rotation][0]:
                    head.rotation = 'l'
                if event.key == pg.K_RIGHT and rotation_permissions[head.rotation][1]:
                    head.rotation = 'r'

        if head.ifCollisionApple(apple):
            apple = new_apple()
            length.append(None)
            score += 1

        length.insert(0, (head.x, head.y))
        length.__delitem__(-1)
        head.x += rotation_speeds[head.rotation][0]
        head.y += rotation_speeds[head.rotation][1]

        window.fill((0, 100, 0))
        window.blit(font.render('scr: %d' %
                    score, False, (255, 255, 255)), (50, 45))
        window.blit(font.render('len: %d' % (len(length)+1),
                    False, (255, 255, 255)), (680, 45))
        pg.draw.rect(window, (0, 255, 0), head)
        pg.draw.rect(window, (255, 0, 0), apple)
        body = [pg.draw.rect(window, (0, 255, 0), (snake[0], snake[1], 20, 20))
                for snake in length]
        blocks = [pg.draw.rect(window, (255, 255, 255), (20, 20, 760, 20)),
                  pg.draw.rect(window, (255, 255, 255), (20, 20, 20, 360)),
                  pg.draw.rect(window, (255, 255, 255), (20, 360, 760, 20)),
                  pg.draw.rect(window, (255, 255, 255), (760, 20, 20, 360))]
        pg.display.update()
        if head.collidelist(blocks) > -1:
            break

        if head.collidelist(body) > -1:
            col = head.collidelist(body)
            length = length[:col]

        clock.tick(10)

    while True:
        game_over = True
        window.blit(game_over_text, (270, 150))
        pg.display.update()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            elif event.type == pg.KEYDOWN:
                game_over = False
        if not game_over:
            break
