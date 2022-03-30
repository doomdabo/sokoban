#sprites파일_개체의 움직임 제어
import os
import pygame
from settings import Setting

#상자 밀기
class pusherSprite(pygame.sprite.Sprite):
	def __init__(self, col, row):
		pygame.sprite.Sprite.__init__(self)
		self.image_path = os.path.join(Setting.get('resources_path'), Setting.get('imgfolder'), 'player.png')
		self.image = pygame.image.load(self.image_path).convert()
		color = self.image.get_at((0, 0))
		self.image.set_colorkey(color, pygame.RLEACCEL)
		self.rect = self.image.get_rect()
		self.col = col
		self.row = row
	'''이동'''
	def move(self, direction, is_test=False):
		if is_test:
			if direction == 'up':
				return self.col, self.row - 1
			elif direction == 'down':
				return self.col, self.row + 1
			elif direction == 'left':
				return self.col - 1, self.row
			elif direction == 'right':
				return self.col + 1, self.row
		else:
			if direction == 'up':
				self.row -= 1
			elif direction == 'down':
				self.row += 1
			elif direction == 'left':
				self.col -= 1
			elif direction == 'right':
				self.col += 1
	'''플레이어 그리기'''
	def draw(self, screen):
		self.rect.x = self.rect.width * self.col
		self.rect.y = self.rect.height * self.row
		screen.blit(self.image, self.rect)


#게임요소
class elementSprite(pygame.sprite.Sprite):
	def __init__(self, sprite_name, col, row):
		pygame.sprite.Sprite.__init__(self)
		# box.png/target.png/wall.png에서 가져옴
		self.image_path = os.path.join(Setting.get('resources_path'), Setting.get('imgfolder'), sprite_name)
		self.image = pygame.image.load(self.image_path).convert()
		color = self.image.get_at((0, 0))
		self.image.set_colorkey(color, pygame.RLEACCEL)
		self.rect = self.image.get_rect()
		# 유형 
		self.sprite_type = sprite_name.split('.')[0]
		# 위치
		self.col = col
		self.row = row
	'''게임요소 그리기'''
	def draw(self, screen):
		self.rect.x = self.rect.width * self.col
		self.rect.y = self.rect.height * self.row
		screen.blit(self.image, self.rect)
	'''이동'''
	def move(self, direction, is_test=False):
		if self.sprite_type == 'box':
			if is_test:
				if direction == 'up':
					return self.col, self.row - 1
				elif direction == 'down':
					return self.col, self.row + 1
				elif direction == 'left':
					return self.col - 1, self.row
				elif direction == 'right':
					return self.col + 1, self.row
			else:
				if direction == 'up':
					self.row -= 1
				elif direction == 'down':
					self.row += 1
				elif direction == 'left':
					self.col -= 1
				elif direction == 'right':
					self.col += 1
