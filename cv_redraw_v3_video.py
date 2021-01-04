import cairo
import cv2
import random

BGCOLOR = (0/255,0/255,0/255)
REGION = 5
ALPHA = 0.5
OFFSET = 1
STEPS = 15

#Open video capture
cap = cv2.VideoCapture('butterfly.mp4')

#Get WxH
WIDTH = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
HEIGHT = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 25.0, (WIDTH,HEIGHT))

steps_count = 1

#Main loop
while(cap.isOpened()):
    ret, frame = cap.read()
    
    print("\rFrame %i out of %i" % (cap.get(cv2.CAP_PROP_POS_FRAMES),
                                  cap.get(cv2.CAP_PROP_FRAME_COUNT)),
                                  end="")
    
    if ret==True:
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        #Initiate surface and context
        ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
        ctx = cairo.Context(ims)
        ctx.set_source_rgb(*BGCOLOR)
        ctx.paint()
        
        for w in range(0,WIDTH,REGION):
            for h in range(0,HEIGHT,REGION):
                roi = image[h:h+REGION,w:w+REGION]
                average = roi.mean(axis=0).mean(axis=0)
                colors = [i/255 for i in average]
                
                ctx.set_source_rgba(*colors,ALPHA)
                ctx.move_to(w,h)
                
                for i in range(steps_count):
                    relative = (random.randint(-OFFSET,OFFSET),random.randint(-OFFSET,OFFSET))
                    current = ctx.get_current_point()
                    while (current[0]+relative[0]) < 0 or (current[1]+relative[1]) < 0\
                    or (current[0]+relative[0]) > WIDTH or (current[1]+relative[1]) > HEIGHT:
                        relative = (random.randint(-OFFSET,OFFSET),random.randint(-OFFSET,OFFSET))
                    
                    ctx.rel_line_to(*relative)
                ctx.stroke()
        
        #Write image, load and write to frame
        ims.write_to_png("frame.png")
        newframe = cv2.imread("frame.png")
        
        out.write(newframe)
        #cv2.imshow('frame',frame)
        
        if cap.get(cv2.CAP_PROP_POS_FRAMES) % 10 == 0:
            steps_count += 1
            
        if cap.get(cv2.CAP_PROP_POS_FRAMES) % 20 == 0:
            OFFSET += 1
            
            
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    
    else:
        break

cap.release()
out.release()
cv2.destroyAllWindows()
    

        
        