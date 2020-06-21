import cairo
import math
import random

#General parameters
WIDTH = 600
HEIGHT = 600
bgcolor = (0/255,0/255,0/255)
linecolor = (0/255,0/255,0/255)
minline = 6
iter = 0
constantcolor = random.randint(0,2)

#Alternator function (unused)
def alternate():
    while True:
        yield 1
        yield 0

#Triangle drawing function
def draw_triangle(a,b,c,ctx):
    
    #Set colors
    colors = [random.random(),random.random(),random.random()]
    colors[constantcolor] = 200
    ctx.set_source_rgb(*colors)

    #Draw the thing
    ctx.move_to(*a)
    ctx.line_to(*b)
    ctx.move_to(*b)
    ctx.line_to(*c)
    ctx.move_to(*c)
    ctx.line_to(*a)
    ctx.stroke()    

#Main recurrent function
def recur_triangle(a,b,c,ctx):
    global iter
    iter+= 1
    draw_triangle(a,b,c,ctx)

    distance = math.sqrt(((a[0]-b[0])**2)+((a[1]-b[1])**2))
    print("Iteration "+str(iter)+" -- Current length: "+str(distance))

    if distance > minline:
        recur_triangle(a,((a[0]+b[0])/2,(a[1]+b[1])/2),((a[0]+c[0])/2,(a[1]+c[1])/2),ctx)
        recur_triangle(((a[0]+b[0])/2,(a[1]+b[1])/2),b,((b[0]+c[0])/2,(b[1]+c[1])/2),ctx)
        recur_triangle(((a[0]+c[0])/2,(a[1]+c[1])/2),((b[0]+c[0])/2,(b[1]+c[1])/2),c,ctx)
        #Drawing middle triangle removed (doesn't look as good)
        #recur_triangle(((a[0]+b[0])/2,(a[1]+b[1])/2),((b[0]+c[0])/2,(b[1]+c[1])/2),((a[0]+c[0])/2,(a[1]+c[1])/2))



####################################################################################
#########################               MAIN               #########################
####################################################################################

def main():
    #Set up alternator
    alter = alternate()

    #Setting up canvas
    ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
    ctx = cairo.Context(ims)
    ctx.set_source_rgb(*bgcolor)
    ctx.paint()

    #Line color
    ctx.set_source_rgb(*linecolor)
    ctx.set_line_width(1)

    #Draw the four quadrants recursively
    recur_triangle((0,0),(WIDTH/2,HEIGHT/2),(0,HEIGHT),ctx)
    recur_triangle((0,0),(WIDTH/2,HEIGHT/2),(WIDTH,0),ctx)
    recur_triangle((WIDTH,0),(WIDTH/2,HEIGHT/2),(WIDTH,HEIGHT),ctx)
    recur_triangle((WIDTH,HEIGHT),(WIDTH/2,HEIGHT/2),(0,HEIGHT),ctx)

    #Write to file
    ims.write_to_png("testTRI.png")


if __name__ == '__main__':
    main()
