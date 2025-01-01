import pygame, sys, os, random
from pygame.locals import *
pygame.mixer.pre_init(44100, -16, 2, 512)#initiates the mixer
pygame.init() # initiates pygame
clock = pygame.time.Clock()#create instance of clock for framerate 
pygame.mixer.set_num_channels(64)
pygame.display.set_caption('Pygame Platformer')

WINDOW_SIZE = (900,600)
screen = pygame.display.set_mode(WINDOW_SIZE,0,32) # initiate the window
display = pygame.Surface((300,200)) # used as the surface for rendering, which is scaled
level=''

moving_right = False
moving_left = False
vertical_momentum = 0
air_timer = 0
true_scroll = [0,0]
jmp=0
lvlChange=False
in_menu=True
game_tiles_path = 'game_tiles/'

# white color  
txt_color = (255,255,255)
# light shade of the button  
color_light = (170,170,170)  
# dark shade of the button  
color_dark = (100,100,100)  
# stores the width of the screen  
width = screen.get_width()        
# stores the height of the screen 
height = screen.get_height()  
# defining a font  
smallfont = pygame.font.SysFont('Corbel',35)        
#to initialize location of menu icons
menu_y=[]
for i in range (5):
    y=int((i+1)*((WINDOW_SIZE[1]-200)/6)+i*((WINDOW_SIZE[1]-400)/5))
    menu_y.append(y)

# rendering a text written in  
def text(a):
     return smallfont.render(a , True , txt_color)

#to load map
def load_map(level):
    f = open('maps/'+ level + '.txt','r')
    data = f.read()
    f.close()
    data = data.split('\n')
    global game_map
    game_map=[]
    for row in data:
        game_map.append(list(row))

global animation_frames
animation_frames = {}

def load_animation(path,frame_durations):
    global animation_frames
    animation_name = path.split('/')[-1]
    animation_frame_data = []
    n = 0
    for frame in frame_durations:
        animation_frame_id = animation_name + '_' + str(n)
        img_loc = path + '/' + animation_frame_id + '.png'
        # player_animations/idle/idle_0.png
        animation_image = pygame.image.load(img_loc).convert()
        animation_image.set_colorkey((255,255,255))
        animation_frames[animation_frame_id] = animation_image.copy()
        for i in range(frame):
            animation_frame_data.append(animation_frame_id)
        n += 1
    return animation_frame_data

def change_action(action_var,frame,new_value):
    if action_var != new_value:
        action_var = new_value
        frame = 0
    return action_var,frame


animation_database = {}

animation_database['run'] = load_animation('player_animations/run',[7,7])
animation_database['idle'] = load_animation('player_animations/idle',[1])
animation_database['jump'] = load_animation('player_animations/jump',[1])

grass_img   = pygame.image.load(game_tiles_path + 'grass.png')
dirt_img    = pygame.image.load(game_tiles_path + 'dirt.png')
spikes_img  = pygame.image.load(game_tiles_path + 'spikes.png').convert()#for making white background transparent
spikes_img.set_colorkey((255,255,255))
lava_img    = pygame.image.load(game_tiles_path + 'lava.png').convert()
lava_img.set_colorkey((255,255,255))
lavatop_img = pygame.image.load(game_tiles_path + 'lavatop.png').convert()
lavatop_img.set_colorkey((255,255,255))
exit_img    = pygame.image.load(game_tiles_path + 'exit.png').convert()
exit_img.set_colorkey((255,255,255))

jump_sound = pygame.mixer.Sound('sounds/jump.wav')
grass_sounds = [pygame.mixer.Sound('sounds/grass_0.wav'),pygame.mixer.Sound('sounds/grass_1.wav')]
grass_sounds[0].set_volume(0.2)
grass_sounds[1].set_volume(0.2)

pygame.mixer.music.load('sounds/music.wav')
pygame.mixer.music.play(-1)

player_action = 'idle'
player_frame = 0
player_flip = False

grass_sound_timer = 0

player_rect = pygame.Rect(100,100,20,27)

background_objects = [[0.25,[120,10,70,400]],[0.25,[280,30,40,400]],[0.5,[30,40,40,400]],[0.5,[130,90,100,400]],[0.5,[300,80,120,400]]]

def reinit():
    global moving_right,moving_left,vertical_momentum,air_timer,true_scroll,jmp,player_rect
    moving_right = False
    moving_left = False
    vertical_momentum = 0
    air_timer = 0
    if level=='lvl3':
        player_rect = pygame.Rect(550,80,20,27)
    else:
        player_rect = pygame.Rect(100,80,20,27)
    jmp=0
    true_scroll=[0,0] 

def collision_test(rect,tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list

def move(rect,movement,tiles):
    collision_types = {'top':False,'bottom':False,'right':False,'left':False}
    rect.x += movement[0]
    hit_list = collision_test(rect,tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect,tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types

def harm(harm_rects):
    hit_list=collision_test(player_rect, harm_rects)
    if hit_list != []:
        reinit()
    return player_rect
        
def lvl_change(exit_rects):
    hit_list=collision_test(player_rect, exit_rects)
    global level
    global lvlChange
    if hit_list != []:
        if level=='lvl1':
            level='lvl2'
        elif level=='lvl2':
            level='lvl3'
        elif level=='lvl3':
            level='bonus'
        elif level=='bonus':
            level=''
            pygame.quit()
        lvlChange=True
        reinit()
    return player_rect
while True: # game loop
    if (in_menu):  
        for ev in pygame.event.get():  
            if ev.type == pygame.QUIT:  
                pygame.quit()  
            #checks if a mouse is clicked  
            if ev.type == pygame.MOUSEBUTTONDOWN:  
                #if the mouse is clicked on the  button the game is terminated  
                if  380<= mouse[0] <= 380+140 :
                    if menu_y[0]<= mouse[1] <= menu_y[0]+40:
                        level='lvl1'
                        load_map(level)
                        reinit()
                        in_menu=False
                    if menu_y[1]<= mouse[1] <= menu_y[1]+40:
                        level='lvl1'
                        load_map(level)
                        reinit()
                        in_menu=False
                    if menu_y[2]<= mouse[1] <= menu_y[2]+40:
                        level='lvl2'
                        load_map(level)
                        reinit()
                        in_menu=False
                    if menu_y[3]<= mouse[1] <= menu_y[3]+40:
                        level='lvl3'
                        load_map(level)
                        reinit()
                        in_menu=False
                    if menu_y[4]<= mouse[1] <= menu_y[4]+40:
                        pygame.quit()
                        
        # fills the screen with a color  
        screen.fill((40,10,60))    
        # stores the (x,y) coordinates into mouse as a tuple 
        mouse = pygame.mouse.get_pos()  
        
        # if mouse is hovered on a button it changes to light  
        if menu_y[0]<= mouse[1] <= menu_y[0]+40 and 380<= mouse[0] <= 380+140:
            pygame.draw.rect(screen,color_light,[380,menu_y[0],140,40])
        else:  
            pygame.draw.rect(screen,color_dark,[380,menu_y[0],140,40])
        if menu_y[1]<= mouse[1] <= menu_y[1]+40 and 380<= mouse[0] <= 380+140:
            pygame.draw.rect(screen,color_light,[380,menu_y[1],140,40])
        else:  
            pygame.draw.rect(screen,color_dark,[380,menu_y[1],140,40])
        if menu_y[2]<= mouse[1] <= menu_y[2]+40 and 380<= mouse[0] <= 380+140:
            pygame.draw.rect(screen,color_light,[380,menu_y[2],140,40])
        else:  
            pygame.draw.rect(screen,color_dark,[380,menu_y[2],140,40])
        if menu_y[3]<= mouse[1] <= menu_y[3]+40 and 380<= mouse[0] <= 380+140:
            pygame.draw.rect(screen,color_light,[380,menu_y[3],140,40])
        else:  
            pygame.draw.rect(screen,color_dark,[380,menu_y[3],140,40])
        if menu_y[4]<= mouse[1] <= menu_y[4]+40 and 380<= mouse[0] <= 380+140:
            pygame.draw.rect(screen,color_light,[380,menu_y[4],140,40])  
        else:  
            pygame.draw.rect(screen,color_dark,[380,menu_y[4],140,40])                   
        
        # superimposing the text onto our button  
        screen.blit(text('Start')   , (380+20,menu_y[0]+5))  
        screen.blit(text('Level 1') , (380+20,menu_y[1]+5))
        screen.blit(text('Level 2') , (380+20,menu_y[2]+5))
        screen.blit(text('Level 3') , (380+20,menu_y[3]+5))
        screen.blit(text('Quit')    , (380+20,menu_y[4]+5))
        # updates the frames of the game  
        pygame.display.update()  
        
    if(not in_menu):
        if(lvlChange):
            load_map(level)
            lvlChange=False
            
        display.fill((146,244,255)) # clear screen by filling it with blue
    
        if grass_sound_timer > 0:
            grass_sound_timer -= 1
    
        true_scroll[0] += (player_rect.x-true_scroll[0]-152)/20
        true_scroll[1] += (player_rect.y-true_scroll[1]-106)/20
        scroll = true_scroll.copy()
        scroll[0] = int(scroll[0])
        scroll[1] = int(scroll[1])
    
        pygame.draw.rect(display,(7,80,75),pygame.Rect(0,120,300,80))
        for background_object in background_objects:
            obj_rect = pygame.Rect(background_object[1][0]-scroll[0]*background_object[0],background_object[1][1]-scroll[1]*background_object[0],background_object[1][2],background_object[1][3])
            if background_object[0] == 0.5:
                pygame.draw.rect(display,(20,170,150),obj_rect)
            else:
                pygame.draw.rect(display,(15,76,73),obj_rect)
    
        tile_rects = []
        harm_rects = []
        exit_rects = []
        y = 0
        for layer in game_map:
            x = 0
            for tile in layer:
                if tile == '1':
                    display.blit(dirt_img,(x*16-scroll[0],y*16-scroll[1]))
                if tile == '2':
                    display.blit(grass_img,(x*16-scroll[0],y*16-scroll[1]))
                if tile == '3':
                    display.blit(spikes_img,(x*16-scroll[0],y*16-scroll[1]))
                if tile == '4':
                    display.blit(lava_img,(x*16-scroll[0],y*16-scroll[1]))
                if tile == '5':
                    display.blit(lavatop_img,(x*16-scroll[0],y*16-scroll[1]))
                if tile == '6':
                    display.blit(exit_img,(x*16-scroll[0],y*16-scroll[1]))
                    
                if tile == '1' or tile == '2':
                    tile_rects.append(pygame.Rect(x*16,y*16,16,16))
                if tile=='3'or tile=='4' or tile=='5':
                    harm_rects.append(pygame.Rect(x*16,y*16,16,16))
                if tile =='6':
                    exit_rects.append(pygame.Rect(x*16,y*16,16,16))
                
                x += 1
            y += 1
    
        player_movement = [0,0]
        if moving_right == True:
            player_movement[0] += 2
        if moving_left == True:
            player_movement[0] -= 2
        player_movement[1] += vertical_momentum
        vertical_momentum += 0.2
        if vertical_momentum > 3:
            vertical_momentum = 3
    
           
        if player_movement[0] == 0:
            player_action,player_frame = change_action(player_action,player_frame,'idle')
        if air_timer>6 :
             player_action,player_frame = change_action(player_action,player_frame,'jump')
             if player_movement[0] > 0:
                player_flip = False 
             if player_movement[0] < 0:
                player_flip = True
        else:     
            if player_movement[0] > 0:
                player_flip = False
                player_action,player_frame = change_action(player_action,player_frame,'run')
            if player_movement[0] < 0:
                player_flip = True
                player_action,player_frame = change_action(player_action,player_frame,'run')
        
        
        player_rect,collisions = move(player_rect,player_movement,tile_rects)
        harm(harm_rects)
        lvl_change(exit_rects)
        
        if collisions['bottom'] == True:
            air_timer = 0
            vertical_momentum = 0
            if player_movement[0] != 0:
                if grass_sound_timer == 0:
                    grass_sound_timer = 30
                    random.choice(grass_sounds).play()
        else:
            air_timer += 1
    
        player_frame += 1
        if player_frame >= len(animation_database[player_action]):
            player_frame = 0
        player_img_id = animation_database[player_action][player_frame]
        player_img = animation_frames[player_img_id]
        display.blit(pygame.transform.flip(player_img,player_flip,False),(player_rect.x-scroll[0],player_rect.y-scroll[1]))
    
    
        for event in pygame.event.get(): # event loop
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYUP:
                if event.key == K_UP:
                    jmp=0
            if event.type == KEYDOWN:
                if event.key == K_m:
                    in_menu=True
                if event.key == K_k:
                    if pygame.mixer.music.get_busy():
                        pygame.mixer.music.fadeout(500)
                    else:
                        pygame.mixer.music.play(fade_ms=500) 
                if event.key == K_RIGHT:
                    moving_right = True
                if event.key == K_LEFT:
                    moving_left = True
                if event.key == K_UP :
                    jmp+=1
                    if air_timer < 6 and jmp<=1:
                        jump_sound.play()
                        vertical_momentum = -5
            if event.type == KEYUP:
                if event.key == K_RIGHT:
                    moving_right = False
                if event.key == K_LEFT:
                    moving_left = False           
        screen.blit(pygame.transform.scale(display,WINDOW_SIZE),(0,0))
        pygame.display.update()
        clock.tick(60)
