import cairo
import random
import requests
import ast


#General parameters
WIDTH = 2160
HEIGHT = 4690
BGCOLOR = (0/255,0/255,0/255)
LINECOLOR = (255/255,255/255,255/255)
LENGTH = 15
LINES = 30000
STROKE = 1


def inside_canvas(ctx,length,direction,w,h):
    '''
    Checks if a line would fall inside the canvas. Returns Tue if so, 
    false if it wouldn't.
    Direction: 0=up, 1=down, 2=left, 3 (or other)=right
    '''
    
    current = ctx.get_current_point()
    if direction == 0:
        return current[1] - length > 0
    elif direction == 1:
        return current[1] + length < h
    elif direction == 2:
        return current[0] - length > 0
    else:
        return current[0] + length < w

def list_points(length,direction, current):
    '''
    Returns a list of the points included within a line.
    Takes the current point as parameter.
    
    '''
    if direction == 0:
        list = [(current[0],current[1]-i) for i in range(length+1)]
    elif direction == 1:
        list = [(current[0],current[1]+i) for i in range(length+1)]
    elif direction == 2:
        list = [(current[0]-i,current[1]) for i in range(length+1)]
    else:
        list = [(current[0]+i,current[1]) for i in range(length+1)]
    list.pop(0)
    return list

    
def touch_path(ctx,length,direction,totalpoints):
    '''
    Defines if a new line would cross another point in the path.
    Takes the total list of points, and tests the tentative line to see
    if there's any crossing.
    Returns True if the path is crossed, False otherwise.
    
    '''
    current = ctx.get_current_point()
    points = list_points(length, direction,current)
    return not not [i for i in points if i in totalpoints]

def draw_line(ctx,length,direction):
    '''
    Draws the specified line.
    '''
    if direction == 0:
        ctx.rel_line_to(0,-length)
    elif direction == 1:
        ctx.rel_line_to(0,length)
    elif direction == 2:
        ctx.rel_line_to(-length,0)
    else:
        ctx.rel_line_to(length,0)


def get_palette():
    '''
    Gets a palette from http://colormind.io/api/ using requests
    Returns as a list of lists
    '''
    data = '{"model":"default"}'
    response = requests.post('http://colormind.io/api/', data=data)
    content = response.text
    content.rstrip("\n")
    
    colors = ast.literal_eval(content)
    colors = colors['result']
    
    return colors

#%%
#========================== MAIN ==========================#

#Get palette
palette = get_palette()

# Set up canvas
ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
ctx = cairo.Context(ims)
#bg = random.randint(0,4)        #Defines bg color
#color = palette[random.randint(0, 4)]
#ctx.set_source_rgb(color[0]/255,color[1]/255,color[2]/255)  #Sets it up
#palette.pop(bg)
ctx.set_source_rgb(*BGCOLOR)
ctx.paint()

# Initialize line at length, length to mantain offset, set color and stroke
ctx.move_to(LENGTH, LENGTH)
#ctx.set_source_rgb(*LINECOLOR)
ctx.set_line_width(STROKE)



#Initialize total points list
totalpoints = []

for i in range(LINES):
    #Up, down, left, right
    origin = ctx.get_current_point()
    
    #Sets a random list of the 4 possible directions
    dir = random.sample(range(4),4)
    print("Attempting line "+str(i))
    
    #Flag to check for an exhausted line (no possibilities)
    exhaust = True
    
    #Tries all 4 directions
    for i in dir:
        #Checks both conditions (inside canvas and no contact with path)
        if inside_canvas(ctx, LENGTH, i, WIDTH,HEIGHT) and not touch_path(ctx, LENGTH, i, totalpoints):
            draw_line(ctx,LENGTH,i)     #Draws line
            totalpoints += list_points(LENGTH,i,origin)     #Adds all the points to total
            exhaust = False         #Sets the exhaust flag to false            
            break                   #Breaks from the direction seeking loop
    
    #Checks for exhaust flag to define a new start point
    if exhaust:
        print("Path exhausted, starting new one...")
        
        color = palette[random.randint(0, 4)]   #Gets random color from palette            
        ctx.set_source_rgb(color[0]/255,color[1]/255,color[2]/255)  #Sets color
        ctx.stroke()
        
        #Defines "units" to start the new point (always multiple of LENGTH to
        # mantain offset)
        units = (WIDTH // LENGTH, HEIGHT // LENGTH)
        newpos = (random.randint(1,units[0])*LENGTH,random.randint(1,units[1])*LENGTH)
        
        #Loop to start a line outside of currently used points
        while newpos in totalpoints:
            newpos = (random.randint(1,units[0])*LENGTH,random.randint(1,units[1])*LENGTH)
        
        #Move to new found position
        ctx.move_to(*newpos)

#Stroke all the lines                    
#ctx.stroke()

#Frame
ctx.set_source_rgb(0,0,0)
ctx.rectangle(0, 0, WIDTH, HEIGHT)
ctx.stroke()

#WRITE FILE
ims.write_to_png("circuit.png")    
               
