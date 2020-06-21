import cairo
import math

#General parameters
WIDTH = 600
HEIGHT = 600
sqside = 12
maskrad = 200
bgcolor = (64/255,0/255,128/255)
linecolor = (255/255,204/255,0/255)

#Alternator function
def alternate():
    while True:
        yield 1
        yield 0

alter = alternate()


#Setting up canvas
ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
ctx = cairo.Context(ims)
ctx.set_source_rgb(bgcolor[0],bgcolor[1],bgcolor[2])
ctx.paint()


#Line color
ctx.set_source_rgb(linecolor[0],linecolor[1],linecolor[2])
#ctx.set_line_width(3)


#Draw squiggly pattern
for i in range(0,WIDTH,sqside):
    for j in range(0,HEIGHT,sqside):
        '''
        #Squares, removed
        ctx.set_source_rgba(0.3,0.3,0.3,0.2)
        ctx.rectangle(i,j,sqside,sqside)
        ctx.stroke()
        '''
        
        #Alternate lines
        if next(alter) == 1:           
            ctx.move_to(i,j+sqside)
            ctx.line_to(i+sqside,j)
            ctx.stroke()
        else:
            ctx.move_to(i,j)
            ctx.line_to(i+sqside,j+sqside)
            ctx.stroke()


#Set up second surface and paint
im = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
ct2 = cairo.Context(im)
ct2.set_source_rgb(bgcolor[0],bgcolor[1],bgcolor[2])
ct2.paint()

#Clip squiggly pattern in circle
ct2.set_source_surface(ims)
ct2.arc(WIDTH/2, HEIGHT/2, maskrad, 0, 2*math.pi)
ct2.clip()
ct2.paint()

#MAKE FILE
im.write_to_png("testSQ.png")
