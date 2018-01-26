from __future__ import print_function
import os, sys, random
import pygame
from pygame.locals import *

### global variables
WIDTH = 600
HEIGHT = 600
BLACK = pygame.Color(0,0,0)
WHITE = pygame.Color(255,255,255)
FPS = 5
HEAD = {"left":"snakeheadleft.png","right":"snakeheadright.png",\
	"up":"snakeheadup.png","down":"snakeheaddown.png"}
WALL = {"left":(0,0),"right":(550,0),"up":(0,0),"down":(0,550)}
FRUIT = {"0":"strawberry.png","1":"strawberry.png","2":"strawberry.png",\
	"3":"strawberry.png","4":"strawberry.png","5":"poison.png",\
	"6":"poison.png","7":"melon.png","8":"melon.png","9":"pill.png"}
POINT = {"0":1,"1":1,"2":1,"3":1,"4":1,"5":-5,"6":-5,"7":5,"8":5,"9":1}
BGM = os.path.join("data", "bgm.wav")

### class fruit
class Wall(pygame.sprite.Sprite):
	def __init__(self,position):
		pygame.sprite.Sprite.__init__(self)
		if position == "left" or position == "right":
			self.image, self.rect = load_image("wall_vertical.png",BLACK)
		else:
			self.image, self.rect = load_image("wall_parallel.png",BLACK)
		self.rect.topleft = WALL[position]

class Fruit(pygame.sprite.Sprite):
	def __init__(self,fruit):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = load_image(FRUIT[fruit],BLACK)
		self.point = POINT[fruit]
		self.rect.topleft = (random.randint(2,20)*25 ,random.randint(2,20)*25)
		
### class snake
class SnakeBody(pygame.sprite.Sprite):
	def __init__(self,x,y):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = load_image("snakebody.png",BLACK)
		self.rect.topleft = (x,y)
		
class SnakeHead(pygame.sprite.Sprite):
	def __init__(self,x,y,DIRECTION):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = load_image(HEAD[DIRECTION],BLACK)
		self.rect.topleft = (x,y)

### loading image - snake and fruit
def load_image(name,colorkey=None):
	path = os.path.join("data", name)
	try:
		image = pygame.image.load(path)
	except pygame.error, message:
		print("Cannot load image: {}".format(path))
		raise SystemExit, message
	image = image.convert()
	if colorkey is not None:
		if colorkey is -1:
			colorkey = image.get_at( (0,0) )
		image.set_colorkey(colorkey, RLEACCEL)
	return image, image.get_rect()

### loading audio from the name file
def load_sound(name):
	class NoneSound:
		def play(self): pass
	if not pygame.mixer:
		return NoneSound()
	path = os.path.join('data',name)
	try:
		sound = pygame.mixer.Sound(path)
	except pygame.error, message:
		print('Cannot load sound: {}', path)
	return sound

### setting the world
def main():
	pygame.init()
	window = pygame.display.set_mode( (WIDTH,HEIGHT) )
	window.set_alpha(BLACK)
	pygame.display.set_caption("Snake")
	## font
	font = pygame.font.Font(None, 32)
	## clock
	clock = pygame.time.Clock()
	## group
	walls = pygame.sprite.Group()
	fruits = pygame.sprite.Group()
	snake = pygame.sprite.Group()
	snakehead = pygame.sprite.Group()
	## Create sound
	bright = load_sound('bright.wav')
	witch = load_sound('witch.wav')
	pygame.mixer.music.load (BGM)
	pygame.mixer.music.play(100)
	pygame.mixer.music.queue(BGM)
	## create snake
	vx, vy = 0,0
	x = 50
	y = 50
	d = {}
	direction = 'right'
	l = [(x,y)]
	## create fruit
	fruit = Fruit("1")
	fruits.add(fruit)
	grow = True
	## create wall
	wall1 = Wall("left");wall2 = Wall("right");wall3 = Wall("up");wall4 = Wall("down")
	walls.add(wall1);walls.add(wall2);walls.add(wall3);walls.add(wall4)
	## update
	count = 0
	score = 0
	highscore = 0
	gameover = False
	## loop
	while True:
		#render
		window.fill(BLACK)
		#snakehead
		y = y + vy
		x = x + vx
		l.append((x,y))
		l.pop(0)
		del snakehead
		snakehead = pygame.sprite.Group()
		head = SnakeHead(l[-1][0],l[-1][1],direction)
		snakehead.add(head)
		snakehead.draw(window)
		check = str(random.randint(0,9))
		#input
		for event in pygame.event.get():
			if event.type == KEYDOWN and gameover == False:
				if event.key == K_RIGHT and direction != "left":
					vx, vy = 25,0
					direction = "right"
					break
				elif event.key == K_LEFT and direction != "right":
					vx, vy = -25,0
					direction = "left"
					break
				elif event.key == K_UP and direction != "down":
					vx, vy = 0,-25
					direction = "up"
					break
				elif event.key == K_DOWN and direction != "up":
					vx, vy = 0,25					
					direction = "down"
					break
			elif event.type == QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == KEYUP and event.key == K_ESCAPE:
				pygame.event.post(pygame.event.Event(QUIT))
			elif event.type == KEYDOWN and gameover == True:
				if event.key == K_SPACE:
					gameover = False
					fruits.remove(fruit)
					fruit = Fruit(check)
					fruits.add(fruit)
					count = 0
					x, y = 50, 50
					vx, vy = 0, 0
					l = [(x,y)]
					direction = "right"
		walls.draw(window)
		#snakebody
		del snake
		snake = pygame.sprite.Group()
		for i in range(0,len(l)-1):
			d["square{}".format(i)] = SnakeBody(l[i][0],l[i][1])
			snake.add(d["square{0}".format(i)])
		snake.draw(window)
		#gameover
		if gameover:
			vx,vy = 0,0
			score = 0
			die = font.render('YOU DIED!', False, WHITE)
			space = font.render('Press space to restart.', False, WHITE)
			die_rect = die.get_rect()
			space_rect = space.get_rect()
			die_rect.center = (WIDTH / 2, HEIGHT / 2)
			space_rect.center = (WIDTH / 2, HEIGHT / 2 + 50)
			window.blit(die, die_rect)
			window.blit(space, space_rect)
		#fruits
		if count == 30:
			fruits.remove(fruit)
			fruit = Fruit(check)
			fruits.add(fruit)
			count = 0
			grow = True
			if check == "5" or check == "6":
				count = 10
			elif check == "9":
				grow = False
		#collision
		if vx + vy != 0:
			for i in range(0,len(l)-1):
				if l[i] == (x,y):
					witch.play()
					gameover = True
			if head.rect.colliderect(fruit.rect):
				bright.play()
				score += fruit.point				
				fruits.remove(fruit)
				if grow:
					l.insert(0,(l[0][0]-10,l[0][1]-10))
				else:
					n = 0
					for i in range(1,len(l)):
						l.pop(0)
						n += 1
						if n == 3:
							break
				fruit = Fruit(check)
				count = 0
				grow = True
				if check == "9":
					grow = False
				if check == "5" or check == "6":
					count = 10
				fruits.add(fruit)
			for wall in walls:
				if head.rect.colliderect(wall.rect):
					witch.play()
					gameover = True
		fruits.draw(window)
		if highscore < score:
			highscore = score
		scores = font.render('Score/High: {}'.format(str(score) + \
			"/" + str(highscore)), False, WHITE)
		scores_rect = scores.get_rect()
		scores_rect.topleft = (10,10)
		window.blit(scores, scores_rect)
		#delay
		count += 1
		pygame.display.flip()
		clock.tick(FPS)
main()
