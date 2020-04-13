import pygame
import math
import time
import random

def Supershape(a, b ,m ,n1 ,n2 ,n3 ):
    path = []
    points = 800

    for n in range(points):
        u = m* math.pi * n /points

        r = (math.fabs(math.cos(u)/a)**n2 + math.fabs(math.sin(u)/b)**n3)**(-1/n1)
        path.append(r)

    max_r = max(path)

    normalised_path = [r/max_r for r in path]
    return normalised_path

def drawShape(radii,  colour=(0,0,0),size=500,angle = 0):
    surface = pygame.Surface((size+2,size+2))

    # surface.fill((255, 255, 255))

    # surface.set_colorkey((255,255,255))
    size -=2

    x=[]
    y=[]
    for n in range(len(radii)):
        u = 2*math.pi*n/len(radii)
        x.append(radii[n] * math.cos(u-angle))
        y.append(radii[n] * math.sin(u-angle))

    if max(x) - min(x) > max(y) - min(y):
        scale = size/(max(x)-min(x))
    else:
        scale = size/(max(y)-min(y))

    midX=1+size/2 - scale*(min(x) + max(x))/2
    midY=1+size/2 - scale*(min(y) + max(y))/2

    points= [(x1*scale + midX, y1*scale + midY) for (x1,y1) in zip(x,y)]

    return points
    # pygame.draw.aalines(surface,colour,True,points)
    # return surface

pygame.init()
screen = pygame.display.set_mode((1200, 900))

a = 1
b = 1
n1 = 1
n2 = 1
n3 = 1
m = 1

while(True):
    screen.fill((255, 255, 255))

    a = 1
    b = 1
    n1 = 1
    n2 = 1
    # n3 = 1
    n3 = random.randrange(10)
    m = 1

    # a = a
    # b = b
    # m = (m )% 60 + 1
    # n1 = (n1 ) % 50 + 1
    # n2 = (n2 + 1) % 30
    # n3 = (n3 + 1) % 15

    # a = random.randrange(5) + 1
    # b = random.randrange(5) + 1
    m = random.randrange(10)
    # n1 = random.randrange(5) + 1
    # n2 = random.randrange(5)
    # n3 = random.randrange(5)

    print( a,b,m,n1,n2,n3)

    radii = Supershape(a = a, b = b ,m = m ,n1 =n1 ,n2 = n2 ,n3 =n3 )

    shape_points = drawShape(radii,size = 500)
    # shape.get_rect(center = screen.get_rect(topleft = (0,0)).center)
    # screen.blit(shape,(10,10))

    pygame.draw.aalines(screen,shape_points)


    # inverted = pygame.transform.flip(shape,0,1)
    # new_window = inverted.get_rect(center = screen.get_rect(topleft = (0,0)).center)
    # screen.blit(inverted,new_window.topleft)

    inverted = pygame.transform.flip(shape, 1, 0)
    new_window = inverted.get_rect(center=screen.get_rect(topleft=(0, 0)).center)
    screen.blit(inverted, new_window.topleft)

    pygame.display.update()
    time.sleep(1)
