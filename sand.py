import sys, pygame
pygame.init()

size = width, height = 500, 500

pixelsize = 50, 50
pixelwidth, pixelheight = pixelsize

black = 0, 0, 0

screen = pygame.display.set_mode(size)

debug = True

clock=pygame.time.Clock()

#rect1 = pygame.Rect(200, 100, pixelwidth, pixelheight)
#rect2 = pygame.Rect(100, 50, pixelwidth, pixelheight)
rects = []
colrects = []

lopos = 0
lopos2 = 0

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        #get pixel spawn location
        if event.type == pygame.MOUSEBUTTONDOWN:
            posx, posy = pygame.mouse.get_pos()

            refx = 0.1
            refy = 0.1

            while refx.is_integer() == False:
                posx -= 1
                refx = posx / pixelwidth
            while refy.is_integer() == False:
                posy -= 1
                refy = posy / pixelheight
            print("spawn at " + str(refx) + ", " + str(refy))
            rects.append(pygame.Rect(refx*pixelwidth, refy*pixelheight, pixelwidth, pixelheight))

    #set pixel positions
    #point = pygame.mouse.get_pos()#collision point
    #collide = ballrect.collidepoint(point)
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
        if ballrect.top == 0:
            pass
            #print("top collision")
        #else:


        #print(str(speed))
        #print("before move: "  + str(ballrect))
        movedr = ballrect.move(speed)
        #print("after move: "  + str(movedr))

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
        colrects.append(pygame.Rect(rect.left, rect.top + rect.height, rect.width, rect.height))

        #bottom left
        #colrects.append(pygame.Rect(rect.left - rect.width, rect.top + rect.height, rect.width, rect.height))
        
        #bottom right
        #colrects.append(pygame.Rect(rect.left + rect.width, rect.top + rect.height, rect.width, rect.height))

    for rect in rects: #i need to get colliderect's original rect
        colindex = rect.collidelist(colrects)
        if colindex != -1:
            #print(colindex)
            colpos = colrects[colindex].left / pixelwidth, colrects[colindex].top / pixelheight
            #print(colpos)

            print(colrects[colindex].top)
            print(rect.top)
            if colrects[colindex].top == rect.top:
                print("Stopped on another")
                print("before move: "  + str(rect))
                movedr = rects[colindex].move(0, 0)
                print("after move: "  + str(movedr))

                
                rects[lopos2] = movedr
                print(rects[lopos2])
        lopos2 +=1
    lopos2 = 0

    #draw pixels
    screen.fill(black)
    for rect in rects:
        pygame.draw.rect(screen, "blue", rect)

    #draw grid
    if debug:
        for y in range(int(height / pixelheight)):
            for x in range(int(width / pixelwidth)):
                pygame.draw.rect(screen, "white", (x*pixelwidth, y*pixelheight, pixelwidth, pixelheight), 1)
    
    if debug:
        for rect in colrects:
            pygame.draw.rect(screen, "green", rect, 2)

    print("drawing...")
    pygame.display.flip()
    clock.tick(1)