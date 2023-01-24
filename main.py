import pygame
from config import *
from sprites import *
import sys

class Game:
    def __init__(self):
        pygame.init()
        self.screen=pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        self.character_spritesheet = Spritesheet('img/baer_idle.png')
        self.character_left = Spritesheet('img/bear_left.png')
        self.character_right = Spritesheet('img/bear_right.png')
        self.character_attack = Spritesheet('img/bear_attack.png')
        self.terrain_spritesheet = Spritesheet('img/rock.png')
        self.background_sprite = Spritesheet('img/background.png')

        self.enemy_idle = Spritesheet('img/idle_turtle.png')
        self.enemy_left = Spritesheet('img/left_turtle.png')
        self.enemy_right = Spritesheet('img/right_turtle.png')
        self.enemy_dead = Spritesheet('img/dead_turtle.png')
        self.enemy_attack = Spritesheet('img/attack_turtle.png')

    def createTilemap(self):
        for i, row in enumerate(tilemap): 
            for j, column in enumerate(row):
                Ground(self,j,i)
                if column == "B":
                    Block(self, j, i)
                if column == "P":
                    Player(self, j, i)
                if column == "E":
                    Enemy(self, j, i)



    def new(self):
        self.playing = True

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()

        self.createTilemap()

    def events(self):
        for event in pygame.event.get():
            if event.type ==pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        self.all_sprites.update()
    
    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.clock.tick(FPS)
        pygame.display.update()

    def main(self):
        while self.playing:
            self.events()
            self.update()
            self.draw()
        self.running = False

    def game_over(self):
        pass

    def intro_screen(self):
        pass
g = Game()
g.intro_screen()
g.new()
while g.running:
    g.main()
    g.game_over()

pygame.quit()
sys.exit()



