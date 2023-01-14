import math
import random
import numpy as np
from math import sqrt
from random import randrange

import pygame

#dimensions of the screen
WIDTH = 900
HEIGHT = 900

#The gravitation constant of the universe taht's about a 7 orders of magnitude stronger than in real life
GRAVITY = 0.01#6.67e-4

#color of space/background
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#initializes game
pygame.init()

class Body:
    
    def __init__(self, mass, x, y, v):
        self.mass = mass #Mass of the body
        self.x = x #positional coordinate X *used for inital x value
        self.y = y #positional coordinate Y *used for initial y value
        self.p = np.array([self.x, self.y], dtype = float) #tracks position in space over time
        self.v = np.array(v, dtype = float) #Velocity
        #radius assumes density is 1
        self.r = (self.mass / np.pi)**(1/3)
        self.color = (random.randrange(1, 255), random.randrange(0, 255), random.randrange(0, 255)) #random color generated for body
    
    def gravitationalForce(self, other):
        if self == other:
            self.dv = np.array([0,0], dtype = float)
        else:
            #distance
            self.dist = math.sqrt((self.p[0] - other.p[0])**2 + (self.p[1] - other.p[1])**2)
            self.dv = np.array([0,0], dtype = float)
            if self.dist == 0:
                self.dv = 0
            else:
                #force
                self.f = (-GRAVITY * self.mass * other.mass / self.dist**2) * (self.p - other.p) / self.dist
                #delta velocity vectorized
                self.dv = self.f / self.mass
                #collision between two bodies occurs
                if self.dist < self.r + other.r + 5:
                    self.dv *= -0.9
                if self.dist < self.r + other.r:
                    if self.r > other.r:
                        self.r += (other.r) * 0.01 #steals mass/radius from other if collision occurs
                        other.r -= (other.r) * 0.05 #loses mass/radius
                    elif  self.r < other.r:
                        other.r += (self.r) * 0.01
                        self.r -= (self.r) * 0.05
        self.v += self.dv
        
    #draws bodies at current position    
    def draw(self, SCREEN):
        p = self.p
        pygame.draw.circle(SCREEN, self.color, p, self.r)

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gravity Simulator")

font = pygame.font.SysFont("Arial", 18)

BODIES = 75 #number of bodies to start out
Bodies = []

#gives random values to the attributes of our bodies
for i in range(0, BODIES):
    Bodies.append(
        Body(
            random.randrange(50, 9000), #random mass
            random.randrange(0, 800), #random initial x coordinate
            random.randrange(0, 800), #random initial y coordinate
            [(random.randrange(-10, 10) / 20), (random.randrange(-10, 10) /20)] #random start velocity
    ))

playing = True
clock = pygame.time.Clock()

#shows number of bodies left
def numberOfBodies(Bodies):
    bodiesCount = str(len(Bodies))
    Bodies_text = font.render("Number of Bodies: " + bodiesCount, 1, WHITE)
    return Bodies_text

while playing:
    
    clock.tick(60) #frame rate cap
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
    
    SCREEN.fill(BLACK)
    
    for body in Bodies:
        for body_1 in Bodies:
            body.gravitationalForce(body_1)    
        body.p += body.v
    
        
        #Makes it so the edge of the screen acts as borders of the simulated universe
        if body.p[1] < 2:
            body.v[1] *= -0.9
            body.p += 1
        if body.p[1] > HEIGHT:
            body.v[1] *= -0.9
            body.p -= 1
             
        if body.p[0] < 2:
            body.v[0] *= -0.9
            body.p += 1
        if body.p[0] > WIDTH:
            body.v[0] *= -0.9
            body.p -= 1
        
        #if body has too many collisions it gets destroyed
        if body.r <= 1:
            Bodies.remove(body)
        
        body.draw(SCREEN)
    
    SCREEN.blit(numberOfBodies(Bodies), (10, 0))
    
    pygame.display.update()