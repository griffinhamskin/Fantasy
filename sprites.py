import pygame
from config import *
import math
import random

class Spritesheet:
    def __init__(self,file):
        self.sheet = pygame.image.load(file).convert()
    def get_sprite(self,x,y,width,height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet,(0,0), (x,y,width,height))
        sprite.set_colorkey(BLACK)
        return sprite

class Player(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self,self.groups)

        self.x = x *TILESIZE
        self.y = y *TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = 'down'
        self.animation_loop = 1


        self.image = self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y=self.y

    def update(self):
        self.movement()
        self.animate()

        self.rect.x += self.x_change
        self.collide_blocks('x')
        self.rect.y += self.y_change
        self.collide_blocks('y')

        self.x_change = 0
        self.y_change = 0
    
    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x_change -= PLAYER_SPEED
            self.facing = 'left'
        if keys[pygame.K_RIGHT]:
            self.x_change += PLAYER_SPEED
            self.facing = 'right'
        if keys[pygame.K_UP]:
            self.y_change -= PLAYER_SPEED
            self.facing = 'up'
        if keys[pygame.K_DOWN]:
            self.y_change += PLAYER_SPEED
            self.facing = 'down'

    def collide_blocks(self,direction):
        if direction =="x":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right 
        if direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change>0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change<0:
                    self.rect.y = hits[0].rect.bottom
    def animate(self):
        down_animations = [
            self.game.character_spritesheet.get_sprite(0,0, self.width,self.height)
        ]
        left_animations = [
            self.game.character_left.get_sprite(0,0, self.width,self.height)
        ]
        right_animations = [
            self.game.character_right.get_sprite(0,0, self.width,self.height)
        ]

        if self.facing == "down":
            self.image = self.game.character_spritesheet.get_sprite(0,0,self.width, self.height)
        if self.facing == "up":
            self.image = self.game.character_spritesheet.get_sprite(0,0,self.width, self.height)
        if self.facing == "left":
            self.image = self.game.character_left.get_sprite(0,0,self.width, self.height)
        if self.facing == "right":
            self.image = self.game.character_right.get_sprite(0,0,self.width, self.height)

class Enemy(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self,self.groups)

        self.x = x*TILESIZE
        self.y = y*TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = random.choice(['left','right'])
        self.animation_loop=1
        self.movement_loop = 0
        self.max_travel = random.randint(7,30)

        self.image = self.game.enemy_idle.get_sprite(0,0, self.width, self.height)

        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.movement()
        self.x+= self.x_change
        self.y += self.y_change

        self.x_change = 0
        self.y_change = 0

    def movement(self):
        if self.facing == 'left':
            self.x_change -= ENEMY_SPEED
            self.movement_loop -=1
            if self.movement_loop <= -self.max_travel:
                self.facing = 'right'
        if self.facing =='right':
            self.x_change += ENEMY_SPEED
            self.movement_loop +=1
            if self.movement_loop >= self.max_travel:
                self.facing = 'left'

class Block(pygame.sprite.Sprite):
    def __init__(self,game,x,y):

        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self,self.groups)

        self.x = x*TILESIZE
        self.y = y*TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(0,0,self.width,self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Ground(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups= self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x*TILESIZE
        self.y = y*TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.background_sprite.get_sprite(0,0, self.width,self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y