#initialize the pygame
import pygame
import math
import random
from pygame import mixer


pygame.init ()
#create the screen
screen = pygame.display.set_mode((900, 600))

background = pygame.image.load('background.png')

mixer.music.load('background.wav')
mixer.music.play(-1)

#Caption and Icon
pygame.display.set_caption("my_first_game")
icon = pygame.image.load('iconita.png')
pygame.display.set_icon(icon)


#Player
playerImg = pygame.image.load('spaceship.png')
playerX = 410
playerY = 480
playerX_change = 0

#Inamicii
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
enemies_num = 6

for i in range(enemies_num):
  
  enemyImg.append(pygame.image.load('inamic.png'))
  enemyX.append(random.randint (0, 836))
  enemyY.append(random.randint (50, 150))
  enemyX_change.append(3)
  enemyY_change.append(40)

#gloantele
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"


score_value = 0

font = pygame.font.Font(None, 32)
textX = 10
textY = 10

#text RIP
game_over_font = pygame.font.Font(None, 66)



def show_score(x, y):
  score = font.render("Scor: " + str(score_value),True, 'white')
  screen.blit(score, (x, y))
  
def game_over_text():
  game_over_text = font.render("Not Good Enough " +  str(score_value),True, 'white')
  screen.blit(game_over_text, (300, 350))
  
def player(x, y):
  screen.blit(playerImg, (x, y))
  
def enemy(x, y, i):
  screen.blit(enemyImg[i], (x, y))
  
def bullet_fire(x, y):
  global bullet_state
  bullet_state = "fire"
  screen.blit(bulletImg, (x + 16, y + 13))

def iscollision (enemyX,enemyY,bulletX,bulletY):
  distance = math.sqrt((math.pow(enemyX-bulletX,2)) + (math.pow(enemyY-bulletY,2)))
  if distance < 27:
    return True
  else:
    return False


running  = True
while running:
  
  screen.fill((0, 0, 0))
  
  screen.blit(background, (0,0))
  
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    
    #if a Keystroke is pressed, check whether is yhe right or the left  
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_LEFT:
        playerX_change = -4
      if event.key == pygame.K_RIGHT:
        playerX_change = 4
      if event.key == pygame.K_SPACE:
        if bullet_state == "ready":
          bullet_Sound = mixer.Sound('laser.wav')
          bullet_Sound.play()
          
          bulletX = playerX
          bullet_fire(bulletX, bulletY)
      
    if event.type == pygame.KEYUP:
       if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
        playerX_change = 0
      
  
  playerX += playerX_change
  
  if playerX <= 0:
    playerX = 0
  elif playerX >= 836:
    playerX = 836
    
    #controlul vitezei inamicilor
  for i in range(enemies_num):  
    
    # RIP
    if enemyY[i] > 460:
      for j in range(enemies_num):
        enemyY[j] = 2000
      game_over_text()
      break
      
    
    
    enemyX[i] += enemyX_change[i] 
    if enemyX[i]  <= 0:
      enemyX_change[i] += 3
      enemyY[i] += enemyY_change[i]
    elif enemyX[i] >= 836:
      enemyX_change[i] = -3
      enemyY[i] += enemyY_change[i]
      
    collision = iscollision(enemyX[i],enemyY[i],bulletX,bulletY)
    if collision:
      explosion_Sound = mixer.Sound('explosion.wav')
      explosion_Sound.play()
      bulletY = 480
      bullet_state = "ready"
      score_value += 1
      enemyX[i] = random.randint (0, 836)
      enemyY[i] = random.randint (50, 150)
    
    enemy(enemyX[i],enemyY[i], i)   
      
    # controlul miscarii glontului
  if bulletY <= 0:
    bulletY = 480
    bullet_state = "ready"

  
  if bullet_state == "fire":
    bullet_fire(bulletX, bulletY)
    bulletY -= bulletY_change
    
  
    
  
  player(playerX, playerY)
  show_score(textX, textY)
  pygame.display.update()
