import cairo
import random

#General parameters
WIDTH = 600
HEIGHT = 600
BGCOLOR = (255/255,255/255,255/255)
LINECOLOR = (0/255,0/255,0/255)
STEPS = 10000
OFFSET = 2
LINES = 500

#Setting up canvas
ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
ctx = cairo.Context(ims)
ctx.set_source_rgb(*BGCOLOR)
ctx.paint()

#Line
#ctx.set_source_rgb(*LINECOLOR)
#ctx.set_line_width(3)

for j in range(LINES):
    ctx.move_to(random.randint(0,WIDTH),random.randint(0,HEIGHT))
    color = [random.random(),random.random(),random.random(),0.5]
    ctx.set_source_rgba(*color)
    print("Line "+str(j)+" of "+str(LINES))
    for i in range(STEPS):
        relative = (random.randint(-OFFSET,OFFSET),random.randint(-OFFSET,OFFSET))
        current = ctx.get_current_point()
        while (current[0]+relative[0]) < 0 or (current[1]+relative[1]) < 0\
        or (current[0]+relative[0]) > WIDTH or (current[1]+relative[1]) > HEIGHT:
            relative = (random.randint(-OFFSET,OFFSET),random.randint(-OFFSET,OFFSET))
        
        ctx.rel_line_to(*relative)   
        
    ctx.stroke()

ims.write_to_png("test_watercolor_lines.png")