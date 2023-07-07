from typing import List

import pygame as pg
import random as rnd
from math import cos, sin

SCREEN_SIZE = 400

TAU = 6.2831853071795864769252867665

FRAMES_TO_TURN = 60


class Animal:
    def __init__(self, pos: pg.Vector2, color: tuple, size: int, speed: float, is_carnivore):
        self.color = color
        self.size = size
        self.speed = speed
        self.pos = pos
        self.direction = pg.Vector2()
        self.frame_count = 0
        self.rect = pg.Rect(*self.pos, self.size, self.size)
        self.is_carnivore = is_carnivore

    def move(self, other_animals: list):
        self.pos += self.direction * self.speed
        self.frame_count += 1
        self.rect.update(*self.pos, self.size, self.size)
        if not (0 <= self.pos[0] <= SCREEN_SIZE) or not (0 <= self.pos[1] <= SCREEN_SIZE):
            self.pos = pg.Vector2(SCREEN_SIZE / 2, SCREEN_SIZE / 2)

    def draw(self, window: pg.Surface):
        pg.draw.rect(window, self.color, self.rect)

    def is_colliding(self, other_animal):
        return self.rect.colliderect(other_animal.rect)


class Rabbit(Animal):
    def __init__(self, pos, color=(150, 200, 50), size=20, speed=0.3):
        super().__init__(pos, color, size, speed, False)

    def move(self, other_animals: list):
        if self.frame_count >= FRAMES_TO_TURN:
            self.frame_count = 0
            angle = rnd.random() * TAU
            self.direction = pg.Vector2(cos(angle), sin(angle))
        super(Rabbit, self).move(other_animals)


class Fox(Animal):

    def __init__(self, pos, color=(255, 30, 50), size=30, speed=0.7):
        super().__init__(pos, color, size, speed, True)

    def move(self, other_animals: List[Animal]):
        self.chase_closest(other_animals, condition=lambda x: x.is_carnivore)
        for a in other_animals:
            if self.is_colliding(a):
                if not a.is_carnivore:
                    other_animals.remove(a)
        super(Fox, self).move(other_animals)

    def chase_closest(self, other_animals, condition=None):
        if condition is None:
            condition = lambda x: True
        min_distance = 10000000000
        closest_prey = None
        for a in other_animals:
            if not condition(a):
                if (self.pos - a.pos).length() < min_distance:
                    closest_prey = a
        if closest_prey is None:
            raise ValueError("No object to chase")
        self.direction = (closest_prey.pos - self.pos).normalize()


def draw_window(window, animals):
    window.fill((50, 200, 30))
    for a in animals:
        a.draw(window)
    pg.display.update()


def move_animals(animals):
    for a in animals:
        a.move(animals)


def main():
    window = pg.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
    animals = []
    clock = pg.time.Clock()
    while True:
        clock.tick(60)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    animals.append(
                        Rabbit(pg.Vector2(rnd.randint(50, SCREEN_SIZE - 50), rnd.randint(50, SCREEN_SIZE - 50))))
                if event.key == pg.K_f:
                    animals.append(
                        Fox(pg.Vector2(rnd.randint(50, SCREEN_SIZE - 50), rnd.randint(50, SCREEN_SIZE - 50))))
        move_animals(animals)
        draw_window(window, animals)


if __name__ == '__main__':
    main()
