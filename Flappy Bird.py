import pygame
from pygame.locals import *
import random

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 864
screen_height = 936

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy Plane')


#definuje proměnné
ground_scroll = 0
scroll_speed = 4
flying = False
game_over = False
pipe_gap = 150
pipe_frequency = 1500 #milisekund
last_pipe = pygame.time.get_ticks() - pipe_frequency

#načte obrázky
bg = pygame.image.load('img/bg.png')
ground_img = pygame.image.load('img/ground.png')


class Bird(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.imagesFly = []
		self.imagesCrash = []
		self.index = 0
		self.counter = 0
		for num in range(1, 4):
			img = pygame.image.load(f'img/bird{num}.png')
			self.imagesFly.append(img)
		self.image = self.imagesFly[self.index]
		for num in range(1, 4):
			img = pygame.image.load(f'img/bird{num}crash.png')
			self.imagesCrash.append(img)
		self.image = self.imagesFly[self.index]
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]
		self.vel = 0
		self.clicked = False

	def update(self):
		if flying == True:
			#gravitace
			self.vel += 0.5
			if self.vel > 8:
				self.vel = 8
			if self.rect.bottom < 768:
				self.rect.y += int(self.vel)

		if game_over == False:
			#skok
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				self.vel = -10
			if pygame.mouse.get_pressed()[0] == 0:
				self.clicked = False
				
			#stará se o animaci
			self.counter += 1
			flap_cooldown = 5   #tohle je pro 

			if self.counter > flap_cooldown:
				self.counter = 0
				self.index += 1
				if self.index >= len(self.imagesFly):
					self.index = 0
			self.image = self.imagesFly[self.index]

			#rotace letadla
			self.image = pygame.transform.rotate(self.imagesFly[self.index], self.vel * -2)
		else:
			self.counter += 1
			flap_cooldown = 5
			self.counter = 0
			if self.counter > flap_cooldown:
				self.counter = 0
				self.index += 1
				if self.index >= len(self.imagesFly):
					self.index = 0
			self.image = self.imagesCrash[self.index]
			self.image = pygame.transform.rotate(self.imagesCrash[self.index], -90)

			
class Pipe(pygame.sprite.Sprite):
	def __init__(self, x, y, position):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('img/pipe1.png')
		self.rect = self.image.get_rect()
		if position == 1:
			self.image = pygame.transform.flip(self.image, False, True)
			self.rect.bottomleft = [x, y - int(pipe_gap / 2)]
		if position == -1:
			self.rect.topleft = [x, y + int(pipe_gap / 2)]

	def update(self):
		self.rect.x -= scroll_speed
		if self.rect.right < 0:
			self.kill()




bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

flappy = Bird(100, int(screen_height / 2))

bird_group.add(flappy)



run = True
while run:

	clock.tick(fps)

	#nakreslí pozadí
	screen.blit(bg, (0,0))

	bird_group.draw(screen)
	bird_group.update()
	pipe_group.draw(screen)


	#nakreslí zem
	screen.blit(ground_img, (ground_scroll, 768))
	#sleduje kolize
	if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
		game_over = True
	#zkontroluje jestli letadlo narazilo do země
	if flappy.rect.bottom >= 768:
		game_over = True  
		flying = False

		

	
	if game_over == False and flying == True:

		#generuje nové pipes
		time_now = pygame.time.get_ticks()
		if time_now - last_pipe > pipe_frequency:
			pipe_height = random.randint(-100 , 100)
			btm_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, -1)
			top_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, 1)
			pipe_group.add(btm_pipe)
			pipe_group.add(top_pipe)
			last_pipe = time_now

		#nakreslí a roluje zem
		ground_scroll -= scroll_speed
		if abs(ground_scroll) > 35:
			ground_scroll = 0

		pipe_group.update()


	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
			flying = True

	pygame.display.update()

pygame.quit()
