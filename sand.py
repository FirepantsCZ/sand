import sys, pygame
pygame.init()

size = width, height = 500, 500

pixelsize = 5, 5
pixelwidth, pixelheight = pixelsize

black = 0, 0, 0

screen = pygame.display.set_mode(size)

debug = False

hold = False

final = False

clock=pygame.time.Clock()

#rect1 = pygame.Rect(200, 100, pixelwidth, pixelheight)
#rect2 = pygame.Rect(100, 50, pixelwidth, pixelheight)
rects = []
finalrects = []
colrects = []

lopos = 0
lopos2 = 0

def spawn_pixel():
    posx, posy = pygame.mouse.get_pos()

    refx = 0.1
    refy = 0.1

    while refx.is_integer() == False:
        posx -= 1
        refx = posx / pixelwidth
    while refy.is_integer() == False:
        posy -= 1
        refy = posy / pixelheight
    #print("spawn at " + str(refx) + ", " + str(refy))
    refy -= 1
    rects.append(pygame.Rect(refx*pixelwidth, refy*pixelheight, pixelwidth, pixelheight))
    
def reset_rects():
    del rects[:]
    del finalrects[:]
    print("reset rects")

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        #get pixel spawn location
        if event.type == pygame.MOUSEBUTTONDOWN:
            hold = True
            #print("mouse down")
        if event.type == pygame.MOUSEBUTTONUP:
            hold = False
            #print("mouse up")
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                print("moving rects: " + str(len(rects)))
                print("final rects " + str(len(finalrects)))
            if event.key == pygame.K_r:
                reset_rects()

    #set pixel positions
    #point = pygame.mouse.get_pos()#collision point
    #collide = ballrect.collidepoint(point)

    if hold:
        spawn_pixel()

    for ballrect in rects:
        #print("loop")
        #print("top: " + str(ballrect.top))
        speed = [0, pixelheight]

        #check wall collision
        if ballrect.left == 0 or ballrect.right == width:
            #print("x collision")
            speed[0] = 0

        if ballrect.bottom == height:
            #print("y collision")
            speed[1] = 0
            final = True

        if ballrect.top == 0:
            pass
            #print("top collision")
        #else:

        #if pygame.Rect(ballrect.left, ballrect.top + 100, ballrect.width, ballrect.height).collidelist(rects):
        #print(rects)
        colindex = pygame.Rect(ballrect.left, ballrect.top + ballrect.width, ballrect.width, ballrect.height).collidelist(finalrects)
        colindexright = pygame.Rect(ballrect.left + ballrect.width, ballrect.top + ballrect.height, ballrect.width, ballrect.height).collidelist(finalrects)
        colindexleft = pygame.Rect(ballrect.left - ballrect.width, ballrect.top + ballrect.height, ballrect.width, ballrect.height).collidelist(finalrects)
        if colindex != -1:
            #print("colliding with " + str(colindex))
            if colindexright == -1 and ballrect.right != width:
                #print("right is free")
                movedr = ballrect.move(pixelwidth, pixelheight)
            elif colindexleft == -1 and ballrect.left != 0:
                #print("left is free")
                movedr = ballrect.move(-pixelwidth, pixelheight)
            else:
                movedr = ballrect.move(0, 0)
                final = True
        else:
            movedr = ballrect.move(speed)
        #print(str(speed))
        #print("before move: "  + str(ballrect))
        #print("after move: "  + str(movedr))

        if final:
            finalrects.append(movedr)
            rects.remove(ballrect)
            final = False
        else:
            rects[lopos] = movedr

        #pygame.draw.rect(screen, "blue", movedr)
        lopos += 1
    lopos = 0

    #set collision rectangles around every pixel
    colrects = []
    for rect in rects:
        #left
        #colrects.append(pygame.Rect(rect.left - rect.width, rect.top, rect.width, rect.height))
        #right
        #colrects.append(pygame.Rect(rect.left + rect.width, rect.top, rect.width, rect.height))
        #top
        #colrects.append(pygame.Rect(rect.left, rect.top - rect.height, rect.width, rect.height))

        #bottom
        #colrects.append(pygame.Rect(rect.left, rect.top + rect.height, rect.width, rect.height))

        #bottom left
        #colrects.append(pygame.Rect(rect.left - rect.width, rect.top + rect.height, rect.width, rect.height))
        
        #bottom right
        #colrects.append(pygame.Rect(rect.left + rect.width, rect.top + rect.height, rect.width, rect.height))
        pass

    """for rect in rects: #i need to get colliderect's original rect
        #colindex = rect.collidelist(colrects)
        trulist = rects.copy()
        print(trulist)
        print(rects)
        trulist.remove(rect)
        print(trulist)
        print(rects)
        colindex = rect.collidelist(trulist)
        if colindex != -1:
            print("colindex is exist")
            #print(colindex)
            #colpos = colrects[colindex].left / pixelwidth, colrects[colindex].top / pixelheight
            #print(colpos)

            #print(colrects[colindex].top)
            print(rect.top)
            if rects[colindex].top == rect.top:
                print("Stopped on another")
                print("before move: "  + str(rect))
                movedr = rect.move(0, -50) #how to move the falling one
                print("after move: "  + str(movedr))

                
                rects[lopos2] = movedr
                print(rects[lopos2])
        lopos2 +=1
    lopos2 = 0"""

    #draw pixels
    screen.fill(black)
    for rect in rects:
        #pygame.draw.rect(screen, "red", pygame.Rect(0, 0, 50, 50))
        pygame.draw.rect(screen, (194,178,128), rect)
    for rect in finalrects:
        pygame.draw.rect(screen, (194,178,128), rect)

    #draw grid
    if debug:
        for y in range(int(height / pixelheight)):
            for x in range(int(width / pixelwidth)):
                pygame.draw.rect(screen, "white", (x*pixelwidth, y*pixelheight, pixelwidth, pixelheight), 1)
    
    if debug:
        for rect in colrects:
            pygame.draw.rect(screen, "green", rect, 2)

        #print("drawing...")
    pygame.display.flip()
    clock.tick(60)