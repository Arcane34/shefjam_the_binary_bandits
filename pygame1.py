import pygame, os, sys
from pygame.locals import *
#health bar & text things
#nb - pygame rectangles (wheretodraw,color, (x,y,length,width)) :p
x = 400
y = 400
vel = 10
spell1 = ["Rongaire Balorum Eunarach Vicit Romnia."]

class GetImage():
    
    def get_image(sheet, frame, width, height, scale, colour):
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(sheet, (0, 0), ((frame * width), 0, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(colour)
        return image

class Player():

    #####
    def __init__(self,x,y,w,h):
        self.pos = [x,y]
        self.dim = [w,h]
        self.rect = pygame.Rect(self.pos[0] - self.dim[0] / 2, self.pos[1] - self.dim[1] / 2, self.dim[0], self.dim[1])
        #####
        
        #health variables:
        self.maximum_health = 1000
        self.health_bar_length = 400
        self.health_ratio = self.maximum_health/self.health_bar_length #for converting health -> bar length
        self.current_health = 200
        self.target_health = 500
        self.health_transition_speed = 5 

    #updates game status every 60ms
    def update(self): 
        self.health()
        self.movement()

        #####
        pygame.draw.rect(screen, (240,240,240), self.rect)
        #####

    #subtract from player health
    def take_damage(self,damage):
        if self.target_health > 0:
            self.target_health -= damage
        if self.target_health <= 0:
            self.target_health = 0

    #add to player health
    def get_health(self,health):
        if self.target_health < self.maximum_health:
            self.target_health += health
        if self.target_health >= self.maximum_health:
            self.target_health = self.maximum_health

    def movement(self):
        keys = pygame.key.get_pressed()

        #####
        if keys[pygame.K_LEFT]:
            self.pos[0] -= vel
            self.rect = pygame.Rect(self.pos[0] - self.dim[0] / 2, self.pos[1] - self.dim[1] / 2, self.dim[0], self.dim[1])

        if keys[pygame.K_RIGHT] :
            self.pos[0] += vel
            self.rect = pygame.Rect(self.pos[0] - self.dim[0] / 2, self.pos[1] - self.dim[1] / 2, self.dim[0], self.dim[1])

        if keys[pygame.K_UP]:
            self.pos[1] -= vel
            self.rect = pygame.Rect(self.pos[0] - self.dim[0] / 2, self.pos[1] - self.dim[1] / 2, self.dim[0], self.dim[1])

        if keys[pygame.K_DOWN]:
            self.pos[1] += vel
            self.rect = pygame.Rect(self.pos[0] - self.dim[0] / 2, self.pos[1] - self.dim[1] / 2, self.dim[0], self.dim[1])

        #####

    #draw health bar
    def health(self):
        transition_width = 0
        transition_color = (0,255,0)

        #if player gained health -> green rectangle
        if self.current_health < self.target_health:
            self.current_health += self.health_transition_speed
            transition_width = int((self.target_health - self.current_health)/self.health_ratio)
            transition_color = (0,255,0)

        #if player took damage -> yellowy/orange rectangle
        if self.current_health > self.target_health:
            self.current_health -= self.health_transition_speed
            transition_width = int((self.target_health - self.current_health)/self.health_ratio)
            transition_color = (255,200,0)

        #creates rectangles
        health_bar_rect = pygame.Rect(10,45,self.current_health/self.health_ratio,25)
        transition_bar_rect = pygame.Rect(health_bar_rect.right,45,transition_width/self.health_ratio,25)
        transition_bar_rect.normalize() #flip -ive rectangle
        #draws main heath bar, transitional health bar & surrounding white grid
        pygame.draw.rect(screen, (255,0,0), health_bar_rect)
        pygame.draw.rect(screen, transition_color, transition_bar_rect)
        pygame.draw.rect(screen,(255,255,255), (10,45, self.health_bar_length,25),4)


    
        
#setup
pygame.init()
screen = pygame.display.set_mode((800,800))
clock = pygame.time.Clock()

#####
player = Player(400,400,40,40)
#####


background = pygame.Color(50, 50 ,50)
sprite_sheet_image = pygame.image.load('spritesheet.png').convert_alpha()
BLACK = (0,0,0)
colour = pygame.Color(144, 44, 44)

#text stuff 
font = pygame.font.SysFont(None, 24)
font1 = pygame.font.SysFont(None, 48)
text_color = (200,100,50)
text = ''
lst = spell1[0].split
spell_text = spell1[0]
run = True

#main game loop
while run:
    screen.fill(background)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            pygame.quit()
        #add/sub health on up/down arrow
        elif event.type == pygame.KEYDOWN:
            #text stuff 
            if event.key == pygame.K_BACKSPACE:
                if len(text) > 0:
                    text = text[:-1]
            elif pygame.key.name(event.key).isalnum() :
                text += event.unicode
               # print(text)

    #text drawing stuff
    text_surface = font.render(text, True, text_color)

    #####
    text_width, text_height = text_surface.get_size()
    screen.blit(text_surface, (player.pos[0] - (text_width//2), player.pos[1] - (text_height//2) - 50))
    #####
    
    spell = font1.render(spell_text, True, text_color)
    screen.blit(spell, (50,700))

    #####remove player draw
    
    player.update()
    pygame.display.update()
    clock.tick(30)
