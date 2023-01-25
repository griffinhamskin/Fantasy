import random

WIN_WIDTH= 800
WIN_HEIGHT= 640
TILESIZE = 95
FPS = 60

ENEMY_SPEED = 2
ENEMY_LAYER=2
PLAYER_LAYER=4
BLOCK_LAYER=1
PLAYER_SPEED = 3
GROUND_LAYER = 1

RED = (255,0,0)
BLACK =(0,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)
WHITE =(255,255,255)

x = ['E','B']

x1=random.choice(x)

tilemap = [
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'B.R......RRR.................B',
    'B...P.RR........RRRRR........B',
    'B..RRR.......................B',
    'B.......RRRRRRR..............B',
    'B............................B',
    'B.....RRRRRRRRR..............B',
    'B............................B',
    'B...R........RR..............B',
    'B.............R..............B',
    'B...........R.....RRR........B',
    'B......R.....................B',
    'B............................B',
    'B............................B',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
]
