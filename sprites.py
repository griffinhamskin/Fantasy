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
        global lives
        lives = 5
        pygame.sprite.Sprite.__init__(self,self.groups)

        self.powerupspeed = 1

        self.x = x *TILESIZE
        self.y = y *TILESIZE
        self.width = TILESIZE/1.2
        self.height = TILESIZE/1.2

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
        self.collide_enemy()
        self.collide_powerup()

        self.rect.x += self.x_change
        self.collide_blocks('x')
        self.rect.y += self.y_change
        self.collide_blocks('y')

        self.x_change = 0
        self.y_change = 0
    
    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            for sprite in self.game.all_sprites:
                sprite.rect.x += PLAYER_SPEED*self.powerupspeed
            self.x_change -= PLAYER_SPEED*self.powerupspeed
            self.facing = 'left'
        if keys[pygame.K_RIGHT]:
            for sprite in self.game.all_sprites:
                sprite.rect.x -= PLAYER_SPEED*self.powerupspeed
            self.x_change += PLAYER_SPEED*self.powerupspeed
            self.facing = 'right'
        if keys[pygame.K_UP]:
            for sprite in self.game.all_sprites:
                sprite.rect.y += PLAYER_SPEED*self.powerupspeed
            self.y_change -= PLAYER_SPEED*self.powerupspeed
            self.facing = 'up'
        if keys[pygame.K_DOWN]:
            for sprite in self.game.all_sprites:
                sprite.rect.y -= PLAYER_SPEED*self.powerupspeed
            self.y_change += PLAYER_SPEED*self.powerupspeed
            self.facing = 'down'
            

    def collide_blocks(self,direction):
        if direction =="x":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                    for sprite in self.game.all_sprites:
                        sprite.rect.x+= PLAYER_SPEED*self.powerupspeed
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right 
                    for sprite in self.game.all_sprites:
                        sprite.rect.x-= PLAYER_SPEED*self.powerupspeed
        if direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change>0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                    for sprite in self.game.all_sprites:
                        sprite.rect.y+= PLAYER_SPEED*self.powerupspeed
                if self.y_change<0:
                    self.rect.y = hits[0].rect.bottom
                    for sprite in self.game.all_sprites:
                        sprite.rect.y-= PLAYER_SPEED*self.powerupspeed
    def collide_enemy(self):
        hits=pygame.sprite.spritecollide(self, self.game.enemies, True)
        if hits:
            lives -=1
            

    
    def collide_powerup(self):
        hits=pygame.sprite.spritecollide(self, self.game.powerups, True)
        if hits:
            self.powerupspeed+=1
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
    def __init__(self, game, x, y):
        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

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
        self.rect.x+= self.x_change
        self.rect.y += self.y_change
        self.animate()

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
    def animate(self):
        down_animations = [
            self.game.enemy_idle.get_sprite(0,0, self.width,self.height)
        ]
        left_animations = [
            self.game.enemy_left.get_sprite(0,0, self.width,self.height)
        ]
        right_animations = [
            self.game.enemy_right.get_sprite(0,0, self.width,self.height)
        ]

        if self.facing == "down":
            self.image = self.game.enemy_idle.get_sprite(0,0,self.width, self.height)
        if self.facing == "up":
            self.image = self.game.enemy_idle.get_sprite(0,0,self.width, self.height)
        if self.facing == "left":
            self.image = self.game.enemy_left.get_sprite(0,0,self.width, self.height)
        if self.facing == "right":
            self.image = self.game.enemy_right.get_sprite(0,0,self.width, self.height)
    

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

class Button:
    def __init__(self, x, y, width, height, fg, bg, content, fontsize):
        self.font = pygame.font.Font('freesansbold.ttf', fontsize)
        self.content =content

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.fg = fg
        self.bg = bg

        self.image =pygame.Surface((self.width, self.height))
        self.image.fill(self.bg)
        self.rect = self.image.get_rect()

        self.rect.x =self.x
        self.rect.y = self.y

        self.text = self.font.render(self.content, True, self.fg)
        self.text_rect = self.text.get_rect(center=(self.width/2, self.height/2))
        self.image.blit(self.text, self.text_rect)

    def is_pressed(self,pos,pressed):
        if self.rect.collidepoint(pos):
            if pressed[0]:
                return True
            return False
        return False

class Attack(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.attacks
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.x =x
        self.y = y
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.attack1.get_sprite(0,0, self.width, self.height)
        self.animation_loop =0

        self.rect= self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.animate()
        self.collide()

    def collide(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, True)


    def animate(self):
        direction = self.game.player.facing

        down_animations = [self.game.attack1.get_sprite(0,0, self.width, self.height),
            self.game.attack2.get_sprite(0,0, self.width, self.height),
            self.game.attack3.get_sprite(0,0, self.width, self.height),
            self.game.attack4.get_sprite(0,0, self.width, self.height),
            self.game.attack5.get_sprite(0,0, self.width, self.height),]
        left_animations = [self.game.attack1.get_sprite(0,0, self.width, self.height),
            self.game.attack2.get_sprite(0,0, self.width, self.height),
            self.game.attack3.get_sprite(0,0, self.width, self.height),
            self.game.attack4.get_sprite(0,0, self.width, self.height),
            self.game.attack5.get_sprite(0,0, self.width, self.height),]
        right_animations = [self.game.attack1.get_sprite(0,0, self.width, self.height),
            self.game.attack2.get_sprite(0,0, self.width, self.height),
            self.game.attack3.get_sprite(0,0, self.width, self.height),
            self.game.attack4.get_sprite(0,0, self.width, self.height),
            self.game.attack5.get_sprite(0,0, self.width, self.height),]
        up_animations = [self.game.attack1.get_sprite(0,0, self.width, self.height),
            self.game.attack2.get_sprite(0,0, self.width, self.height),
            self.game.attack3.get_sprite(0,0, self.width, self.height),
            self.game.attack4.get_sprite(0,0, self.width, self.height),
            self.game.attack5.get_sprite(0,0, self.width, self.height),]
            
            

        if direction == 'up':
            self.image = up_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >=5:
                self.kill()
        if direction == 'down':
            self.image = down_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >=5:
                self.kill()
        if direction == 'left':
            self.image = left_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >=5:
                self.kill()
        if direction == 'right':
            self.image = right_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >=5:
                self.kill()


class Berryup(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game.powerups
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.x =x*TILESIZE
        self.y = y*TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.berryup.get_sprite(0,0, self.width, self.height)

        self.rect= self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def collide(self):
        hits = pygame.sprite.spritecollide(self, self.game.powerups, True)

        if hits:
            PLAYER_SPEED +=1
            print('balls')


class Lives(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.attacks
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.x =x
        self.y = y
        self.width = TILESIZE/2
        self.height = TILESIZE/2

        self.image = self.game.heart.get_sprite(0,0, self.width, self.height)
        self.animation_loop =0

        self.rect= self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        pass

    def collide(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, True)


