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
        self.font = pygame.font.Font('freesansbold.ttf', 32)

        self.character_spritesheet = Spritesheet('img/baer_idle.png')
        self.character_left = Spritesheet('img/bear_left.png')
        self.character_right = Spritesheet('img/bear_right.png')
        self.character_attack = Spritesheet('img/bear_attack.png')
        self.terrain_spritesheet = Spritesheet('img/rock.jfif')
        self.background_sprite = Spritesheet('img/background.png')
        self.attack_spritesheet = Spritesheet('img/fruit.png')

        self.enemy_idle = Spritesheet('img/idle_turtle.png')
        self.enemy_left = Spritesheet('img/left_turtle.png')
        self.enemy_right = Spritesheet('img/right_turtle.png')
        self.enemy_dead = Spritesheet('img/dead_turtle.png')
        self.enemy_attack = Spritesheet('img/attack_turtle.png')

        self.gameover_bg = pygame.image.load('./img/lose_screen.png')
        self.gameover_bg = pygame.transform.scale(self.gameover_bg, (800,640))

    def createTilemap(self):
        for i, row in enumerate(tilemap): 
            for j, column in enumerate(row):
                Ground(self,j,i)
                if column =="R":
                    x=random.randint(1,2)
                    if x == 1:
                        Block(self,j,i)
                    else:
                        Enemy(self,j,i)
                if column == "B":
                    Block(self, j, i)
                if column == "E":
                    Enemy(self, j, i)
                if column == "P":
                    self.player = Player(self, j, i)
                

                



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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.player.facing == 'up':
                        Attack(self, self.player.rect.x, self.player.rect.y-TILESIZE)
                    if self.player.facing == 'down':
                        Attack(self, self.player.rect.x, self.player.rect.y+TILESIZE)
                    if self.player.facing == 'left':
                        Attack(self, self.player.rect.x-TILESIZE, self.player.rect.y)
                    if self.player.facing == 'right':
                        Attack(self, self.player.rect.x+ TILESIZE, self.player.rect.y)

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


    def game_over(self):
        restart_button = Button(300,WIN_HEIGHT/2, 200, 60, BLACK, WHITE, 'Play Again', 32)

        for sprite in self.all_sprites:
            sprite.kill()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            mouse_pos =pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if restart_button.is_pressed(mouse_pos, mouse_pressed):
                self.new()
                self.main()
            
            self.screen.blit(self.gameover_bg, (0,0))
            self.screen.blit(restart_button.image, restart_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()

g = Game()
g.new()
while g.running:
    g.main()
    g.game_over()

pygame.quit()
sys.exit()
