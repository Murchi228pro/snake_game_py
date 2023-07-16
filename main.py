import pygame
import sys
from pygame import K_DOWN, K_UP, K_LEFT, K_RIGHT
from pygame.font import match_font
import random


HEIGHT = 400
WIDTH = 800

BG_COLOR = pygame.Color(0, 0, 0)
PERSON_COLOR = pygame.Color(0, 255, 0)
RANDOM_COLORS = (pygame.Color(0, 255, 0), pygame.Color(
    255, 0, 0), pygame.Color(0, 0, 255))


class Hero(pygame.Rect):

    def __init__(self, x, y, rotation: str):
        super().__init__((x, y, 15, 15))
        self.x, self.y = x, y
        self.rotation = rotation
        self.score = 0

    def ifCollision(self, lst):
        if super().colliderect(lst):
            return True

    def score_up(self):
        self.score += 1


rotations = {
    'r': (15, 0),
    'l': (-15, 0),
    'u': (0, -15),
    'd': (0, 15)
}


pygame.init()

fonts = {
    'papyrus': pygame.font.Font(match_font('papyrus'), 36),
    'jokerman': pygame.font.Font(match_font('jokerman'), 23)
}

window = pygame.display.set_mode((WIDTH, HEIGHT))

person = Hero(10, 50, rotation='r')
while True:
    person.score = 0
    food_list = [(random.randrange(15, WIDTH-15, 15),
                  random.randrange(10, HEIGHT-15, 15)) for i in range(11)]
    menu = True
    while menu:
        menu = fonts['papyrus'].render(
            'START', False, random.choice(RANDOM_COLORS))
        start = fonts['jokerman'].render(
            'press any key', False, random.choice(RANDOM_COLORS))
        window.blit(menu, (WIDTH//2-80, HEIGHT//2-72))
        window.blit(start, (WIDTH//2-80, HEIGHT//2-10))
        pygame.display.update()
        pygame.time.delay(100)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                menu = False

    before_death = 10

    while True:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == K_DOWN:
                    person.rotation = 'd'
                elif event.key == K_UP:
                    person.rotation = 'u'
                elif event.key == K_LEFT:
                    person.rotation = 'l'
                elif event.key == K_RIGHT:
                    person.rotation = 'r'

        person.x += rotations[person.rotation][0]
        person.y += rotations[person.rotation][1]

        window.fill(BG_COLOR)

        pygame.draw.rect(window, PERSON_COLOR, person, 10)
        foods = [pygame.draw.rect(window, random.choice(RANDOM_COLORS),
                                  (*i, 5, 5))for i in food_list]
        for food in enumerate(foods, 0):
            if person.ifCollision(food[1]):
                food_list.__delitem__(food[0])
                person.score_up()
                before_death += 2.0
                if len(food_list) < 5:
                    food_list.append((random.randrange(15, WIDTH-15, 15),
                                      random.randrange(10, HEIGHT-15, 15)))

        score = fonts['papyrus'].render(
            'score: %d' % person.score, False, PERSON_COLOR)
        before_death_text = fonts['papyrus'].render(
            'secs: %d' % int(
                before_death), False, PERSON_COLOR if before_death > 3.0 else pygame.Color(250, 0, 0)
        )
        window.blit(score, (10, 10))
        window.blit(before_death_text, (650, 10))

        pygame.display.update()

        before_death -= 0.2

        if before_death < 0:
            break

        pygame.time.delay(200)
