# Implementation of classic arcade game Pong
 
import simpleguitk as simplegui
import random
import math

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2

key_type = ["",""]
paddle1_vel=0
paddle2_vel=0
paddle1_pos = (HEIGHT/2)
paddle2_pos = (HEIGHT/2)

ball_pos = [WIDTH/2, HEIGHT/2]
ball_vel = [0, 0]    
score1 = 0
score2 = 0

# helper function that spawns a ball by updating the 
# ball's position vector and velocity vector
# if right is True, the ball's velocity is upper right, else upper left
def ball_init(right):
    global ball_pos, ball_vel # these are vectors stored as lists
    x = random.randrange(120, 240)
    y = random.randrange(60, 180)
    
    if right == "true":
        ball_vel[0] = x//60
    else:
        ball_vel[0] = -x//60
        
    ball_vel[1] = -y//60   

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel,ball_pos, ball_vel  # these are floats
    global score1, score2  # these are ints
    
    paddle1_pos = (HEIGHT/2)
    paddle2_pos = (HEIGHT/2)
    paddle1_vel=0
    paddle2_vel=0
    ball_pos = [WIDTH/2, HEIGHT/2]
    ball_vel = [0, 0]  
    score1 = 0
    score2 = 0
        
    direction = random.randrange(0, 2)
    if direction == 1:
        ball_init("true")
    else:
        ball_init("flase")

def reset(right):
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel,ball_pos, ball_vel  # these are floats
    global score1, score2  # these are ints
    
    paddle1_pos = (HEIGHT/2)
    paddle2_pos = (HEIGHT/2)
    paddle1_vel=0
    paddle2_vel=0
    ball_pos = [WIDTH/2, HEIGHT/2]
    ball_vel = [0, 0]  
  
    if right == "right":
        ball_init("true")
    else:
        ball_init("false")

def draw(c):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
 
    # update paddle's vertical position, keep paddle on the screen
    if paddle1_pos != HEIGHT-HALF_PAD_HEIGHT and key_type[0]=="s":
        paddle1_pos += paddle1_vel
    elif paddle1_pos != HALF_PAD_HEIGHT and key_type[0]=="w":
        paddle1_pos += paddle1_vel
        
    if paddle2_pos != HEIGHT-HALF_PAD_HEIGHT and key_type[1]=="down":
        paddle2_pos += paddle2_vel
    elif paddle2_pos != HALF_PAD_HEIGHT and key_type[1]=="up":
        paddle2_pos += paddle2_vel
        
    # draw mid line and gutters
    c.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    c.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    c.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
    
    # draw paddles
    c.draw_line([HALF_PAD_WIDTH,paddle1_pos-HALF_PAD_HEIGHT],[HALF_PAD_WIDTH,paddle1_pos+HALF_PAD_HEIGHT],PAD_WIDTH,"white")
    c.draw_line([WIDTH-HALF_PAD_WIDTH,paddle2_pos-HALF_PAD_HEIGHT],[WIDTH-HALF_PAD_WIDTH,paddle2_pos+HALF_PAD_HEIGHT],PAD_WIDTH,"white")
    
    # update ball
        
    if ball_pos[1] <= BALL_RADIUS or ball_pos[1] >= (HEIGHT-1)-BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]
        
    if ball_pos[0] <= PAD_WIDTH+BALL_RADIUS:       
        if (paddle1_pos - HALF_PAD_HEIGHT) <= ball_pos[1] <= paddle1_pos + HALF_PAD_HEIGHT:            
            sound.rewind()
            ball_vel[0] = -(0.1*ball_vel[0] + ball_vel[0])
            sound.play()
        else:
            score2 += 1
            reset("right")
     
    elif ball_pos[0] >= WIDTH-1-PAD_WIDTH-BALL_RADIUS:       
        if (paddle2_pos - HALF_PAD_HEIGHT) <= ball_pos[1] <= paddle2_pos + HALF_PAD_HEIGHT:            
            sound.rewind()
            ball_vel[0] = -(0.1*ball_vel[0] + ball_vel[0])
            sound.play()
        else:
            score1 += 1
            reset("left")
    
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    # draw ball and scores
    c.draw_circle([ball_pos[0], ball_pos[1]], BALL_RADIUS, 1,"white", "white")
    c.draw_text(str(score1), [(WIDTH/2)-80,50],50,"white")
    c.draw_text(str(score2), [(WIDTH/2)+50,50],50,"white")
    
def keydown(key):
    global paddle1_vel, paddle2_vel

    if key == simplegui.KEY_MAP["s"]:
        paddle1_vel += 8
        key_type[0]="s"
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel -= 8
        key_type[0]="w"
            
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel += 8
        key_type[1]="down"
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel -= 8
        key_type[1]="up"
            
def keyup(key):
    global paddle1_vel, paddle2_vel
    
    if key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 0
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = 0
            
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 0
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel = 0
    
# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)

frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
sound = simplegui.load_sound("http://www.freesoundeffects.com/pirsounds/PD_SOUNDFX/BEEPS/BEEPPURE.WAV")
button = frame.add_button("Restart", new_game, 100)
# start frame
frame.start()
direction = random.randrange(0, 2)
if direction == 1:
    ball_init("true")
else:
    ball_init("flase")