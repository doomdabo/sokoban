import os #디렉토리랑 파일경로다룸
import sys 
import pygame
from Sprites import * #이미지, 위치, 충돌 처리 
from settings import Setting #프로그램을 실행할때마다 설정을 다르게 주고 싶을때
from itertools import chain #자신만의 반복자 만듦

#게임종료
def quitGame():
   pygame.quit()
   sys.exit(0)

#게임 맵
class gameMap():
   def __init__(self, num_cols, num_rows):
      self.walls = []
      self.boxes = []
      self.targets = []
      self.num_cols = num_cols
      self.num_rows = num_rows
   '''게임요소추가'''
   def addElement(self, elem_type, col, row):
      if elem_type == 'wall':#게임 요소에 벽 추가
         self.walls.append(elementSprite('wall.png', col, row))#벽 이미지 파일을 가져옴
      elif elem_type == 'box':#게임 요소에 박스 추가
         self.boxes.append(elementSprite('box.png', col, row))#박스 이미지 파일을 가져옴
      elif elem_type == 'target':#게임 요소에 타겟 추가
         self.targets.append(elementSprite('target.png', col, row))#타겟 이미지 파일을 가져옴
   '''게임맵그리기'''
   def draw(self, screen):
      for elem in self.elemsIter():
         elem.draw(screen)
   '''게임요소 이터레이터(반복자)'''
   def elemsIter(self):
      for elem in chain(self.targets, self.walls, self.boxes):
         yield elem
   '''이 레벨에서 모든 상자가 지정된 위치에 있으면, 레벨 통과'''
   def levelCompleted(self):
      for box in self.boxes: #self.boxes안에 box있으면
         is_match = False
         for target in self.targets:
            if box.col == target.col and box.row == target.row:
               is_match = True 
               break
         if not is_match:
            return False
      return True
   '''어떤 위치에 도달할 수 있는지 여부'''
   def isValidPos(self, col, row):
      if col >= 0 and row >= 0 and col < self.num_cols and row < self.num_rows:
         block_size = Setting.get('block_size')
         temp1 = self.walls + self.boxes
         temp2 = pygame.Rect(col * block_size, row * block_size, block_size, block_size) #사각형그리기
         return temp2.collidelist(temp1) == -1
      else:
         return False
   '''박스 위치'''
   def getBox(self, col, row):
      for box in self.boxes:
         if box.col == col and box.row == row:
            return box
      return None


#게임 인터페이스
class gameInterface():
   def __init__(self, screen):
      self.screen = screen
      self.levels_path = Setting.get('levels_path')
      self.initGame()
   '''레벨 가져오기'''
   def loadLevel(self, game_level):
      with open(os.path.join(self.levels_path, game_level), 'r') as f:
         lines = f.readlines()
      # 게임지도
      self.game_map = gameMap(max([len(line) for line in lines]) - 1, len(lines))
      # 게임surface
      height = Setting.get('block_size') * self.game_map.num_rows#높이지정
      width = Setting.get('block_size') * self.game_map.num_cols#너비지정
      self.game_surface = pygame.Surface((width, height))
      self.game_surface.fill(Setting.get('bg_color'))
      self.game_surface_blank = self.game_surface.copy()
      for row, elems in enumerate(lines):
         for col, elem in enumerate(elems):
            if elem == 'p':#player
               self.player = pusherSprite(col, row)
            elif elem == '*':#벽
               self.game_map.addElement('wall', col, row)
            elif elem == '#':#box
               self.game_map.addElement('box', col, row)
            elif elem == 'o':#target
               self.game_map.addElement('target', col, row)

   #게임 초기화
   def initGame(self):
      self.scroll_x = 0
      self.scroll_y = 0
      
   #인터페이스 그리기
   def draw(self, *elems):
      self.game_surface.blit(self.game_surface_blank, dest=(0, 0))
      for elem in elems:
         elem.draw(self.game_surface)
      self.screen.blit(self.game_surface, dest=(self.scroll_x, self.scroll_y))
            
def runGame(screen, game_level):
   clock = pygame.time.Clock()
   game_interface = gameInterface(screen)
   game_interface.loadLevel(game_level)
   font_path = os.path.join(Setting.get('resources_path'), Setting.get('fontfolder'), 'BMHANNAPro.ttf')
   text = '다시 시작하려면 R키를 누르세요.'
   font = pygame.font.Font(font_path, 30)
   text_render = font.render(text, 1, (0,0,0))
   while True:
      for event in pygame.event.get():
         if event.type == pygame.QUIT:
            quitGame()
         elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
               next_pos = game_interface.player.move('left', is_test=True)
               if game_interface.game_map.isValidPos(*next_pos):
                  game_interface.player.move('left')
               else:
                  box = game_interface.game_map.getBox(*next_pos)
                  if box:
                     next_pos = box.move('left', is_test=True)
                     if game_interface.game_map.isValidPos(*next_pos):
                        game_interface.player.move('left')
                        box.move('left')
               break
            if event.key == pygame.K_RIGHT:
               next_pos = game_interface.player.move('right', is_test=True)
               if game_interface.game_map.isValidPos(*next_pos):
                  game_interface.player.move('right')
               else:
                  box = game_interface.game_map.getBox(*next_pos)
                  if box:
                     next_pos = box.move('right', is_test=True)
                     if game_interface.game_map.isValidPos(*next_pos):
                        game_interface.player.move('right')
                        box.move('right')
               break
            if event.key == pygame.K_DOWN:
               next_pos = game_interface.player.move('down', is_test=True)
               if game_interface.game_map.isValidPos(*next_pos):
                  game_interface.player.move('down')
               else:
                  box = game_interface.game_map.getBox(*next_pos)
                  if box:
                     next_pos = box.move('down', is_test=True)
                     if game_interface.game_map.isValidPos(*next_pos):
                        game_interface.player.move('down')
                        box.move('down')
               break
            if event.key == pygame.K_UP:
               next_pos = game_interface.player.move('up', is_test=True)
               if game_interface.game_map.isValidPos(*next_pos):
                  game_interface.player.move('up')
               else:
                  box = game_interface.game_map.getBox(*next_pos)
                  if box:
                     next_pos = box.move('up', is_test=True)
                     if game_interface.game_map.isValidPos(*next_pos):
                        game_interface.player.move('up')
                        box.move('up')
               break
            if event.key == pygame.K_r:
               game_interface.initGame()
               game_interface.loadLevel(game_level)
      game_interface.draw(game_interface.player, game_interface.game_map)
      if game_interface.game_map.levelCompleted():
         return
      screen.blit(text_render, (5, 5))
      pygame.display.flip()
      clock.tick(100)


# 버튼
def BUTTON(screen, position, text):
   bwidth = 310#너비 선언
   bheight = 65#높이 선언
   left, top = position#포지션 선언
   pygame.draw.line(screen, (150, 150, 150), (left, top), (left+bwidth, top), 5)#버튼 테두리 그리기
   pygame.draw.line(screen, (150, 150, 150), (left, top-2), (left, top+bheight), 5)#버튼 테두리 그리기
   pygame.draw.line(screen, (50, 50, 50), (left, top+bheight), (left+bwidth, top+bheight), 5)#버튼 테두리 그리기
   pygame.draw.line(screen, (50, 50, 50), (left+bwidth, top+bheight), [left+bwidth, top], 5)#버튼 테두리 그리기
   pygame.draw.rect(screen, (100, 100, 100), (left, top, bwidth, bheight))
   font_path = os.path.join(Setting.get('resources_path'), Setting.get('fontfolder'), 'BMHANNAPro.ttf')#폰트 글꼴 설정
   font = pygame.font.Font(font_path, 50)#폰트 크기 설정
   text_render = font.render(text, 1, (0, 0, 0))#색깔 설정
   return screen.blit(text_render, (left+70, top+10))#글씨의 위치 설정

#시작화면 제목 
def NAME_B(screen, position, text):
   bwidth = 310#너비 선언
   bheight = 65#높이 선언
   left, top = position#포지션 선언
   font_path = os.path.join(Setting.get('resources_path'), Setting.get('fontfolder'), 'BMHANNAPro.ttf')#폰트 글꼴 설정
   font = pygame.font.Font(font_path, 60)#폰트 크기 설정
   text_render = font.render(text, 1, (0,0,0))#색깔 설정
   return screen.blit(text_render, (left+50, top+10))#글씨의 위치 설정


# 시작화면
def startscreen(screen):
   screen.fill(Setting.get('bg_color'))#배경색을 받아옴
   clock = pygame.time.Clock()#초당 프레임수를 설정할 수 있는 Clock객체 생성
   while True:
      button_1 = BUTTON(screen, (170, 250), 'START')#BUTTON함수를 이용해 START버튼을 화면에 출력
      button_2 = BUTTON(screen, (170, 380), ' QUIT')#BUTTON함수를 이용해 QUIT버튼을 화면에 출력
      button_3=NAME_B(screen,(15,150),'<게임 소코반 리메이크>')#NAME_B함수를 이용해 게임 제목을 화면에 출력
      for event in pygame.event.get():
         if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
         if event.type == pygame.MOUSEBUTTONDOWN:
            if button_1.collidepoint(pygame.mouse.get_pos()):
               return
            elif button_2.collidepoint(pygame.mouse.get_pos()):
               quitGame()
      clock.tick(60)
      pygame.display.update()


# 레벨전환화면
def switchscreen(screen):
   screen.fill(Setting.get('bg_color'))#배경색을 받아옴
   clock = pygame.time.Clock()#초당 프레임수를 설정할 수 있는 Clock객체 생성
   while True:
      button_1 = BUTTON(screen, (170, 250), ' NEXT')#BUTTON함수를 이용해 NEXT버튼을 화면에 출력
      button_2 = BUTTON(screen, (170, 340), ' QUIT')#BUTTON함수를 이용해 QUIT버튼을 화면에 출력
      for event in pygame.event.get():
         if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
         if event.type == pygame.MOUSEBUTTONDOWN:
            if button_1.collidepoint(pygame.mouse.get_pos()):
               return
            elif button_2.collidepoint(pygame.mouse.get_pos()):
               quitGame()
      clock.tick(60)
      pygame.display.update()


# 종료화면
def endscreen(screen):
   screen.fill(Setting.get('bg_color'))
   clock = pygame.time.Clock()
   font_path = os.path.join(Setting.get('resources_path'), Setting.get('fontfolder'), 'BMHANNAPro.ttf')
   text = 'GAME CLEAR!'
   font = pygame.font.Font(font_path, 70)
   text_render = font.render(text, 1, (255, 255, 255))
   while True:
      for event in pygame.event.get():
         if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
      screen.blit(text_render, (100, 290))
      clock.tick(60)
      pygame.display.update()


#메인함수
def main():
   pygame.init()
   pygame.mixer.init()
   pygame.display.set_caption('게임 소코반 리메이크_컴퓨팅 사고')
   screen = pygame.display.set_mode([Setting.get('WIDTH'), Setting.get('HEIGHT')])
   pygame.mixer.init()
   startscreen(screen)
   levels_path = Setting.get('levels_path')
   i=1
   for level_name in sorted(os.listdir(levels_path)):
      runGame(screen, level_name)
      if i!=5:
         switchscreen(screen)
         i=i+1
   endscreen(screen)


if __name__ == '__main__':
   main()
