import pygame
from random import shuffle
import random ,os
import sys
import Timer as Timer
import math
from button import Button
from heart import Lives

class Maze:
    def __init__(self, rows=15, cols=15):
        self.rows = rows
        self.cols = cols
        self.keep_going = 1 #to keep generating 

        self.wall_thickness = 15 # Define thickness of the walls

        self.maze = {}
        for y in range(rows):
            for x in range(cols):
                cell = {'south': 1, 'east': 1, 'visited': 0}
                self.maze[(x, y)] = cell
        self.wall_positions = []
        self.wall_sprites = [ ]
        self.fireball_trap_positions =[  ]  #not necessary
        
        self.dragonball_img =[]  #not necessary
        dragonball_dir = "images/dragonballs"
        # Load each image and append it to the fireball_images list
        for i in range(1, 7):  #  images are named in here
            file_name = f"dragonball_{i}.png"
            image = pygame.image.load(os.path.join(dragonball_dir, file_name)).convert_alpha()
            self.dragonball_img.append(image)

        self.dragonball_positions =[] #not necessary
        self.dragonball_sprites = [] #not necessary

        self.add_dragon_ball()

    def add_dragon_ball(self): ##not necessary
        # Load each image and append it to the fireball_images list
        for image in self.dragonball_img:
        # Randomly select a position
         x = random.randint(0, self.cols - 1) * (screen.get_width() // self.cols)
         y = random.randint(0, self.rows - 1) * (screen.get_height() // self.rows)

            # Add position and sprite to lists
         self.dragonball_positions.append((x, y))
         self.dragonball_sprites.append(Dragonball(x, y, image))



   ## genrating maze using DFS
    def generate(self, start_cell=None, stack=[]):
        if start_cell is None:
            start_cell = self.maze[(self.cols - 1, self.rows - 1)]

        if not self.keep_going:
            return

        self.check_finished()
        neighbors = []

        if len(stack) == 0:
            stack.append(start_cell)

        curr_cell = stack[-1]
        neighbors = self.get_neighbors(curr_cell)
        shuffle(neighbors)

        for neighbor in neighbors:
            if neighbor['visited'] == 0:
                neighbor['visited'] = 1
                stack.append(neighbor)
                self.knock_wall(curr_cell, neighbor)

                self.generate(start_cell, stack)
        
    ## to know `if the maze is finished``
    def get_coords(self, cell):
        coords = (-1, -1)
        for k in self.maze:
            if self.maze[k] is cell:
                coords = (k[0], k[1])
                break
        return coords
    
    ## to get neighbours so we can know if we can knock a wall
    def get_neighbors(self, cell):
        neighbors = []

        (x, y) = self.get_coords(cell)
        if (x, y) == (-1, -1):
            return neighbors

        north = (x, y - 1)
        south = (x, y + 1)
        east = (x + 1, y)
        west = (x - 1, y)

        if north in self.maze:
            neighbors.append(self.maze[north])
        if south in self.maze:
            neighbors.append(self.maze[south])
        if east in self.maze:
            neighbors.append(self.maze[east])
        if west in self.maze:
            neighbors.append(self.maze[west])

        return neighbors
    ### to just know if a wall is there or not
    def knock_wall(self, cell, neighbor):
        xc, yc = self.get_coords(cell)
        xn, yn = self.get_coords(neighbor)

        if xc == xn and yc == yn + 1:
            neighbor['south'] = 0
        elif xc == xn and yc == yn - 1:
            cell['south'] = 0
        elif xc == xn + 1 and yc == yn:
            neighbor['east'] = 0
        elif xc == xn - 1 and yc == yn:
            cell['east'] = 0
    ## generates maze for whole image
    def check_finished(self):
        done = 1
        for k in self.maze:
            if self.maze[k]['visited'] == 0:
                done = 0
                break
        if done:
            self.keep_going = 0
    ## putting walls and colours and making sprites of wall 

    def draw_maze(self, screen):
        wall_color = (95,32,0)  # Define color of the walls

        cell_width = screen.get_width() // self.cols
        cell_height = screen.get_height() // self.rows

        for y in range(self.rows):
            for x in range(self.cols):
                cell = self.maze[(x, y)]

                # Draw walls for the cell
                if cell['south'] == 1:
                    wall_rect =pygame.draw.rect(screen, wall_color, (x * cell_width, y * cell_height + cell_height - self.wall_thickness, cell_width, self.wall_thickness))
                    self.wall_positions.append((x * cell_width, y * cell_height + cell_height - self.wall_thickness, cell_width, self.wall_thickness))
                    self.wall_sprites.append(Wall(wall_rect.x, wall_rect.y, wall_rect.width, wall_rect.height))

                if cell['east'] == 1:
                    wall_rect=pygame.draw.rect(screen, wall_color, (x * cell_width + cell_width - self.wall_thickness, y * cell_height, self.wall_thickness, cell_height))
                    self.wall_positions.append((x * cell_width + cell_width - self.wall_thickness, y * cell_height, self.wall_thickness, cell_height))
                    self.wall_sprites.append(Wall(wall_rect.x, wall_rect.y, wall_rect.width, wall_rect.height))

        
        # Return both the wall sprites and the decoration sprites to draw on maze
        return self.wall_sprites #, self.dragonball_sprites


    
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Load sprite sheet
        self.sprite_sheet = pygame.image.load("images/gokusprite.png").convert_alpha()
        self.sheet_columns = 3  # Number of columns in the sprite sheet
        self.sheet_rows = 4  # Number of rows in the sprite sheet
        self.frame_width = self.sprite_sheet.get_width() // self.sheet_columns
        self.frame_height = self.sprite_sheet.get_height() // self.sheet_rows
        self.current_frame = 0
        self.animation_frames = 3  # Number of frames for each animation
        self.direction = "front"  # Current direction of the player
        self.image = self.get_frame(0)  # Set initial image
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)  # Set initial position
        self.animation_stop = False  # Flag to indicate whether to stop animation after one cycle
        self.stop_after_cycle = False  # Flag to indicate whether to stop animation after one cycle
        self.collision_rect = pygame.Rect(54,36,24,48) ### collision rect for player in the image 
        
        self.scale_factor = 1.4
        self.image = pygame.transform.scale(self.image, (self.frame_width * self.scale_factor, self.frame_height * self.scale_factor))
        self.rect = self.image.get_rect()

        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)  # Set initial position
        self.animation_stop = False  # Flag to indicate whether to stop animation after one cycle
        self.stop_after_cycle = False  # Flag to indicate whether to stop animation after one cycle
        self.collision_rect = pygame.Rect(54 * self.scale_factor, 36 * self.scale_factor, 24 * self.scale_factor, 48 * self.scale_factor)  # collision rect for player in the image
    


    def get_frame(self, frame_number):
        """
        Extracts a frame from the sprite sheet based on its position.
        """
        if self.direction == "down":
            row = 0
        elif self.direction == "left":
            row = 1
        elif self.direction == "right":
            row = 2
        elif self.direction == "front":
            row = 3
        x = (frame_number % self.animation_frames) * self.frame_width
        y = row * self.frame_height
        frame_surface = pygame.Surface((self.frame_width, self.frame_height), pygame.SRCALPHA)
        frame_surface.blit(self.sprite_sheet, (0, 0), (x, y, self.frame_width, self.frame_height))
        self.scale_factor = 1.4
        frame_surface = pygame.transform.scale(frame_surface, (self.frame_width * self.scale_factor, self.frame_height * self.scale_factor))
        return frame_surface

    def update_animation(self):
        if not self.animation_stop or self.current_frame < self.animation_frames - 1:
            self.current_frame = (self.current_frame + 1) % self.animation_frames
            self.image = self.get_frame(self.current_frame)
            if self.current_frame == self.animation_frames - 1 and self.stop_after_cycle:
                self.animation_stop = True
        if self.direction != "front":
            if not self.animation_stop or self.current_frame < self.animation_frames - 1:
                self.current_frame = (self.current_frame + 1) % self.animation_frames
                self.image = self.get_frame(self.current_frame)
                if self.current_frame == self.animation_frames - 1 and self.stop_after_cycle:
                    self.animation_stop = True

                
    def move(self, dx, dy, maze):
        global p
        global q
        # Store the current position in case we need to revert
        old_x, old_y = self.rect.x, self.rect.y

        # Calculate the new position
        new_x = self.rect.x + dx
        new_y = self.rect.y + dy

        # Create a new rectangle representing the player's potential new position
        new_rect = pygame.Rect(new_x + self.collision_rect.x+p, new_y + self.collision_rect.y+q, self.collision_rect.width, self.collision_rect.height)

        # Check for collisions with walls
        for wall in maze.wall_sprites:
            if new_rect.colliderect(wall.rect):
                # If there is a collision, revert the player's position
                print("collision")
                
                self.move1(-dx,-dy,maze)
                p = p+dx
                q = q+dy
                print(p,q)
                # If the player is moving into a wall, stop the player
                return

        # If no collisions, update the player's position
        self.rect.x = new_x 
        self.rect.y = new_y 
        p = new_x  # Update p with the new x position
        q = new_y  # Update q with the new y position
        
        

    def move1(self,dx,dy,maze) :
        global p,q
        pygame.mixer.music.stop()
        pygame.mixer.music.load("music/collisionwithwall.mp3")
        pygame.mixer.music.play()
        pygame.time.wait(100)
        pygame.mixer.music.stop()
        pygame.mixer.music.load("music/game.mp3")
        pygame.mixer.music.play()
        self.rect.x += dx
        self.rect.y += dy 
        p = p+dx
        q = q+dy
     
class Explosion(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.fireball_images = []
        fireball_dir = "images/fireball"
        # Load each image and append it to the fireball_images list
        for i in range(1, 7):  # Assuming images are named fireball_1.png to fireball_6.png
            file_name = f"fireball_{i}.png"
            image = pygame.image.load(os.path.join(fireball_dir, file_name)).convert_alpha()
            self.fireball_images.append(image)
        self.image_index = 0
        self.image = self.get_frame(0)
        self.rect = self.image.get_rect()
        self.animation_frames = 6  # Number of frames for each animation
        self.current_frame = 0
        self.animation_stop = False
        self.stop_after_cycle = False  # Set to True if you want to stop after one cycle
        self.position = (0, 0)
        self.collision_rect = pygame.Rect(self.position[0], self.position[1], 20, 20)
        self.collision_rect_ratio = 0.5  # Collision rectangle ratio
        self.relative_to_maze = True 
        

    def get_frame(self, frame_number):
        return pygame.transform.scale(self.fireball_images[frame_number], (40, 40))

    def update_animation(self):
        if not self.animation_stop or self.current_frame < self.animation_frames - 1:
            self.current_frame = (self.current_frame + 1) % self.animation_frames
            self.image = self.get_frame(self.current_frame)
            if self.current_frame == self.animation_frames - 1 and self.stop_after_cycle:
                self.animation_stop = True

    def set_position(self, x, y):
        """
        Set the position of the explosion.
        """
        self.position = (x, y)
        self.rect.topleft = (x, y)  # Update the rectangle position
    
    def update_position(self, dx, dy):
        """
        Update the position of the explosion based on the movement of the maze.
        """
        if self.relative_to_maze:
            self.position = (self.position[0] - dx, self.position[1] - dy)
            self.rect.topleft = (self.position[0], self.position[1])

class Villian(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.villian_images = []
        broly_dir = "images/villian"
        # Load each image and append it to the villian _images list
        for i in range(2, 8):  # 
            file_name = f"Broly{i}.png"
            image = pygame.image.load(os.path.join(broly_dir, file_name)).convert_alpha()
            self.villian_images.append(image)
        self.image_index = 0
        self.image = self.get_frame(0)
        self.rect = self.image.get_rect()
        self.animation_frames = 6  # Number of frames for each animation
        self.current_frame = 0
        self.animation_stop = False
        self.stop_after_cycle = False  # Set to True if you want to stop after one cycle
        self.position = (0, 0)
        self.collision_rect = pygame.Rect(self.position[0], self.position[1], 20, 20)
        self.collision_rect_ratio = 0.5  # Collision rectangle ratio
        self.relative_to_maze = True 
        

    def get_frame(self, frame_number):
        return pygame.transform.scale(self.villian_images[frame_number], (60, 60))

    def update_animation(self):
        if not self.animation_stop or self.current_frame < self.animation_frames - 1:
            self.current_frame = (self.current_frame + 1) % self.animation_frames
            self.image = self.get_frame(self.current_frame)
            if self.current_frame == self.animation_frames - 1 and self.stop_after_cycle:
                self.animation_stop = True

    def set_position(self, x, y):
        """
        Set the position of the explosion.
        """
        self.position = (x, y)
        self.rect.topleft = (x, y)  # Update the rectangle position
    
    def update_position(self, dx, dy):
        """
        Update the position of the explosion based on the movement of the maze.
        """
        if self.relative_to_maze:
            self.position = (self.position[0] -dx, self.position[1] - dy)
            self.rect.topleft = (self.position[0], self.position[1])

class DragonBall(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("images/dragonballs/DragonBall_7.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect()
        self.position = (0, 0)
        self.rect.topleft = self.position
        self.relative_to_maze = True 
        self.collision_rect = pygame.Rect(self.position[0], self.position[1], 20, 20)
    def set_position(self, x, y):
        """
        Set the position of the dragon ball.
        """
        self.position = (x, y)
        self.rect.topleft = (x, y)  # Update the rectangle position
    
    def update_position(self, dx, dy):
        """
        Update the position of the dragon ball based on the movement of the maze.
        """
        if self.relative_to_maze:
            self.position = (self.position[0] - dx, self.position[1] - dy)
            self.rect.topleft = (self.position[0], self.position[1])


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((255, 0, 0))
          # Red color for walls, you can replace it with an actual wall image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)



     
class Dragonball(pygame.sprite.Sprite):    ### Not Completed yet
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

def pausegame():    #### Press Space to Pause the game
    pygame.display.set_caption("Paused")
    global paused
    
    # Create a surface to draw the pause image
    pause_surface = pygame.Surface((800, 450))
    pause_surface.fill((255, 255, 255))  # Fill with white color

    while True:
        # Load and scale the pause image
        pauseimage = pygame.image.load("images/pausescreen.jpeg")
        pauseimage = pygame.transform.scale(pauseimage, (800, 450))

        # Blit the pause image onto the surface
        pause_surface.blit(pauseimage, (0, 0))

        # Blit the surface onto the screen
        screen.blit(pause_surface, (300, 200))

        pausemenu_mouse_pos = pygame.mouse.get_pos()
        resume_button = Button(image=None, pos=(450, 290), text_input="Resume", font=get_font(40), base_color="white", hovering_color="green")
        quit_button = Button(image=None, pos=(450, 390), text_input="Quit", font=get_font(40), base_color="white", hovering_color="green")
        mute_button = Button(image=None, pos=(490, 510), text_input="Mute or Unmute", font=get_font(40), base_color="white", hovering_color="green")
        
        for button in [resume_button, quit_button, mute_button]:
            button.Changecolor(pausemenu_mouse_pos)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                if mute_button.Checkinput(pausemenu_mouse_pos):
                    if pygame.mixer.music.get_busy():  # Check if music is playing
                        pygame.mixer.music.pause()  # Pause the music
                    else:
                        pygame.mixer.music.unpause()
                if resume_button.Checkinput(pausemenu_mouse_pos):
                    paused = not paused
                    return
                if quit_button.Checkinput(pausemenu_mouse_pos):
                    pygame.quit()
                    sys.exit()
        pygame.display.update()



def gameover(lives,time,completed) :
    if completed:
     pygame.display.set_caption("U WIN")
     score = lives*100 + time*10+1000
    if not completed:
     pygame.display.set_caption("Game Over")
     score = lives*100 + time*10 

    scores_written = False
    while True:
        # Load and scale the pause image
        completed_game_bg = pygame.image.load("images/game_comp.jpg")
        completed_game_bg = pygame.transform.scale(completed_game_bg,(1200, 800))

        # Blit the bg onto the screen
        screen.blit(completed_game_bg, (0, 0))
        if completed :
            headover_text = get_font(80).render("U WIN",True,"White")
            headover_rect = headover_text.get_rect( center= (600,100))
        if not completed:
            headover_text = get_font(80).render("Game Over",True,"White")
            headover_rect = headover_text.get_rect( center= (600,100))
        
        score_text = get_font(80).render("Your Score" ,True,"White")
        score_rect = headover_text.get_rect( center= (250,300))
        score_value_text = get_font(80).render(str(score) ,True,"White")
        score_value_rect = headover_text.get_rect( center= (850,300))

        lives_text = get_font(40).render("Lives" ,True,"White")
        lives_rect = lives_text.get_rect( center= (350,400))
        lives_value_text = get_font(40).render(str(lives) ,True,"White")
        lives_value_rect = lives_value_text.get_rect( center= (550,400))

        time_text = get_font(40).render("Time taken" ,True,"White")
        time_rect = time_text.get_rect( center= (350,500))
        remtime = 120 - time
        time_value_text = get_font(40).render(str(remtime) ,True,"White")
        time_value_rect = time_value_text.get_rect( center = (550,500))
        
        if not scores_written:
         with open("highscores.txt", "a") as file:
            file.write(f"{score}\n")
            scores_written = True

        # Blit the text onto the screen
        screen.blit(headover_text, headover_rect)
        screen.blit(score_text, score_rect)
        screen.blit(score_value_text, score_value_rect)
        screen.blit(lives_text, lives_rect)
        screen.blit(lives_value_text, lives_value_rect)
        screen.blit(time_text, time_rect)
        screen.blit(time_value_text, time_value_rect)
        gameover_mouse_pos = pygame.mouse.get_pos()
        
        quit_button = Button(image=None, pos=(600,700), text_input="Quit", font=get_font(40), base_color="white", hovering_color="green")
        
        for button in [ quit_button, ]:
            button.Changecolor(gameover_mouse_pos)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                if quit_button.Checkinput(gameover_mouse_pos):
                    pygame.quit()
                    sys.exit()
        pygame.display.update()
    
    

### to stop the game for 3s 
def display_wasted(screen, image, image_x, image_y, dis_wasted_time):
    # Display the "wasted" image
    screen.blit(image, (image_x, image_y))

    # Get the current time
    start_time = pygame.time.get_ticks()

    # Keep displaying the image for 3 seconds
    while pygame.time.get_ticks() - start_time < dis_wasted_time:
        pygame.display.flip()

    
    
    pygame.display.flip()
### main loop
def loop() :
    running = True
    global paused
    global p
    global q
    clock = pygame.time.Clock()
    prev_direction = None
    timer = Timer.Timer(120)
    background_image = pygame.image.load("images/mazebg.png").convert()
    background_image = pygame.transform.scale(background_image,(2400,2400))
    pause_button = Button(image=pygame.image.load("images/pause.jpg"), pos=(700, 700), text_input="", font=get_font(54), base_color="White", hovering_color="White")
    score =0 
    ball1 = DragonBall()
    ball1.set_position(450, 650)
    old_p5 = 450
    old_q5 =650
    ###  explode 1  sprite ###
    explosion1  = Explosion()
    explosion1.set_position(400,500)
    lives = 3
    old_p1 =800
    old_q1 =200
    ### explode 2 sprite ###
    explosion2 = Explosion()
    explosion2.set_position(300, 550)
    old_p2 = 300
    old_q2 = 550
    explosion3 = Explosion()
    explosion3.set_position(100,500)
    old_p6 = 100
    old_q6 = 500
     ### villian 1 sprite ###
    villian1  = Villian()
    villian1.set_position(160, 600)
    old_p3 = 160
    old_q3 = 600
     ### villian 2 sprite ###
    villian2 = Villian()
    villian2.set_position(110, 110)
    old_p4 = 110
    old_q4 = 110
    
    villian3 =Villian()
    villian3 = Villian()
    villian3.set_position(450, 700)
    old_p7 = 450
    old_q7 = 700
    
    
    mouse_pos = pygame.mouse.get_pos()

    image = pygame.image.load("images/wasted.png")  ## initializing wasted img to be on the safer side
    
    pygame.mixer.music.load("music/game.mp3")
    pygame.mixer.music.play(-1)
    
# Get the dimensions of the image
    wasted_width, wasted_height = image.get_rect().size

# Set initial position of the wasted image
    image_x = (screen.get_width() - wasted_width) // 2
    image_y = (screen.get_height()- wasted_height) // 2 ###image of wasted
    
    
    # Get the coordinates of the last cell in the maze
    cell_width = maze_image.get_width() // maze.cols
    cell_height = maze_image.get_height() // maze.rows

    last_cell_col = maze.cols - 1
    last_cell_row = maze.rows - 1

    last_cell_x = last_cell_col * cell_width
    last_cell_y = last_cell_row * cell_height

    last_cell_coords = (last_cell_x, last_cell_y)
    
    
    while running:
        
        screen.fill((255,0,0))
        
        maze_image.blit(background_image, (0, 0))
        # Draw the background image on maze_image
        
        p = min(max(p, 0), maze_image.get_width() - screen.get_width())
        q = min(max(q, 0), maze_image.get_height() - screen.get_height())
        #to bring villian 1 which is out of bounds so i can see

        ## not using now
        offset_x = max(min(player.rect.x - (screen.get_width() // 2), maze_image.get_width() - screen.get_width()), 0)
        offset_y = max(min(player.rect.y - (screen.get_height() // 2), maze_image.get_height() - screen.get_height()), 0)
        ## not using now 

        display_surface = pygame.Rect(p,q,1200+0,800+0)
        part_maze=maze_image.subsurface(display_surface)
        
        maze.draw_maze(maze_image)
    
        screen.blit(part_maze,(0,0))
        
        screen.blit(player.image, player.rect)
        
        Lives.show_lives(screen, lives)
        #### blitting explosion
        screen.blit(explosion1.image, explosion1.rect)
        explosion1.update_position(p - old_p1, q - old_q1)
        screen.blit(explosion2.image, explosion2.rect)
        explosion2.update_position(p - old_p2, q - old_q2)
        screen.blit(explosion3.image,explosion3.rect)
        explosion3.update_position(p-old_p6,q-old_q6)
        #### blitting villians
        screen.blit(villian1.image, (villian1.rect.x , villian1.rect.y ))
        villian1.update_position(p - old_p3, q - old_q3)
        screen.blit(villian2.image, villian2.rect)
        villian2.update_position(p - old_p4, q - old_q4)
        screen.blit(villian3.image,villian3.rect)
        villian3.update_position(p-old_p7,q-old_q7)

        screen.blit(ball1.image,(ball1.rect.x,ball1.rect.y))
        ball1.update_position(p-old_p5,q-old_q5)

        old_p1, old_q1= p, q
        old_p2,old_q2 = p,q
        old_p3, old_q3= p, q
        old_p4,old_q4 = p,q
        old_p5,old_q5 = p,q
        old_p6,old_q6 = p,q
        old_p7,old_q7 = p,q


        ### when player collides with villians and explosions
        def reset_player_position():
         player.rect.topleft = (0, 0)  # Reset player position to initial maze position
        
        ## updating when colliding#########
        ###------------------------------------------------------------------------------------------------------------------------------------------------
        if pygame.sprite.collide_rect_ratio(0.2)(ball1, player):
            gameover(lives,timer.counter,True)
            running = False
            
        if pygame.sprite.collide_rect_ratio(0.2)(explosion1, player):
            
            pygame.mixer.music.load("music/wasted.mp3")
            pygame.mixer.music.play()
            display_wasted(screen, image, image_x, image_y, 3000)
            timer.counter += 5 ### for not losing time because of wasted img showing
            lives -= 1
            p=0
            q=0
            #player.reset_position()
            reset_player_position()
           
            if lives <= 0:
                gameover(lives,timer.counter,False)
                running = False
                explosion1.remove
        
        if pygame.sprite.collide_rect_ratio(0.2)(explosion2, player):
            pygame.mixer.music.play()
            pygame.mixer.music.load("music/wasted.mp3")
            display_wasted(screen, image, image_x, image_y, 3000)
            lives -= 1
            timer.counter += 5 ### for not losing time because of wasted img showing
            p=0
            q=0
            #player.reset_position()
            reset_player_position()

            if lives <= 0:
                explosion2.remove
                gameover(lives,timer.counter,False)
                running = False

        if pygame.sprite.collide_rect_ratio(0.2)(explosion3, player):
            pygame.mixer.music.play()
            pygame.mixer.music.load("music/wasted.mp3")
            display_wasted(screen, image, image_x, image_y, 3000)
            lives -= 1
            timer.counter += 5 ### for not losing time because of wasted img showing
            p=0
            q=0
            #player.reset_position()
            reset_player_position()

            if lives <= 0:
                explosion3.remove
                gameover(lives,timer.counter,False)
                running = False

        if pygame.sprite.collide_rect_ratio(0.2)(villian1, player):
            
            pygame.mixer.music.load("music/wasted.mp3")
            pygame.mixer.music.play()
            display_wasted(screen, image, image_x, image_y, 3000)
            lives -= 1
            timer.counter += 5 ### for not losing time because of wasted img showing
            p=0
            q=0
            #player.reset_position()
            reset_player_position()

            
            if lives <= 0:

                gameover(lives,timer.counter,False)
                running = False
                villian1.remove

        if pygame.sprite.collide_rect_ratio(0.2)(villian2, player):
            pygame.mixer.music.load("music/wasted.mp3")
            pygame.mixer.music.play()
            display_wasted(screen, image, image_x, image_y, 3000)
            pygame.time.wait(1000)
            pygame.mixer.music.stop()
            pygame.mixer.music.load("music/game.mp3")
            pygame.mixer.music.play()
            lives -= 1
            timer.counter += 5 ### for not losing time because of wasted img showing
            p=0
            q=0
            
            #player.reset_position()
            reset_player_position()
            
            if lives <= 0:
                
                gameover(lives,timer.counter,False)
                running = False
                villian2.remove
        
        if pygame.sprite.collide_rect_ratio(0.2)(villian3, player):
            
            pygame.mixer.music.load("music/wasted.mp3")
            pygame.mixer.music.play()
            display_wasted(screen, image, image_x, image_y, 3000)
            lives -= 1
            timer.counter += 5 ### for not losing time because of wasted img showing
            p=0
            q=0
            #player.reset_position()
            reset_player_position()

            
            if lives <= 0:

                gameover(lives,timer.counter,False)
                running = False
                villian3.remove

        ## updating when colliding#########
        ####--------------------------------------------------------------------------------------------------------
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
             
            prev_direction = player.direction

            if event.type == pygame.USEREVENT + 1:
                if not paused :
                    timer.update()
       

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                    if paused :
                        pausegame()
                if pause_button.Checkinput(mouse_pos):
                    paused = not paused
                    if paused :
                        pausegame()
                    pausegame()
                if event.key == pygame.K_UP:
                    player.direction = "front"
                    player.animation_stop = False
                    player.stop_after_cycle = True
                    player.rect.y -= 10  # Move the player up
                    player.move(0, -10, maze)  # Move the player up
                    #explosion.update_position(0, -10)
                elif event.key == pygame.K_DOWN:
                    player.direction = "down"
                    player.animation_stop = False
                    player.stop_after_cycle = True
                    player.rect.y += 10  # Move the player down
                    player.move(0, 10, maze)  # Move the player down
                    #explosion.update_position(0,10)                  
                elif event.key == pygame.K_LEFT:
                    player.direction = "left"
                    player.animation_stop = False
                    player.stop_after_cycle = True
                    player.rect.x -= 10  # Move the player left
                    player.move(-10,0, maze)  # Move the player left
                    #explosion.update_position(-10,0)
                elif event.key == pygame.K_RIGHT:
                    player.direction = "right"
                    player.animation_stop = False
                    player.stop_after_cycle = True
                    player.rect.x += 10  # Move the player right
                    player.move(10,0, maze)  # Move the player right
                    #explosion.update_position(10,0)
            # Handle keyboard input for player movement continously

            pressed_key = pygame.key.get_pressed() ## not using now

        
          ###updating animations  
        player.update_animation()
        explosion1.update_animation()
        explosion2.update_animation()
        villian1.update_animation()
        villian2.update_animation()
        
        # timerArc Drawing

        text_rect = timer.timer_text.get_rect(center = (100,100))
        screen.blit(timer.timer_text, text_rect)
        if timer.counter <= 0:
            gameover(lives,timer.counter)
            running = False
            
        if timer.counter > 75 :
            timer.drawArc(screen, (255, 255, 255), (100, 100), 90, 10, 2*math.pi*timer.counter/100)
        
        elif timer.counter > 30:
            timer.drawArc(screen, (242,225, 11), (100, 100), 90, 10, 2*math.pi*timer.counter/100)
        else:
            timer.drawArc(screen, (255, 0, 0), (100, 100), 90, 10, 2*math.pi*timer.counter/100)

        if paused:
            pausegame()

        pygame.display.flip()
    

        # Cap the frame rate
        clock.tick(10)
    if player.direction != prev_direction:
            player.update_animation()   ## to stop blinking

    
    


def get_font(size): 
    return pygame.font.Font("fonts/DripOctober.ttf", size)

def get_font1(size): 
    return pygame.font.SysFont("Cambria", size)

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Maze")
    screen = pygame.display.set_mode((1200,800))
    maze_image=pygame.Surface((2400,2400))

    maze = Maze()
    maze.generate()
    maze.wall_sprites =maze.draw_maze(maze_image)
    

    paused = False
    p=0 ## to move the maze when player moves horiz
    q=0 ## to move the maze when player moves verti
    
    player = Player()  # Create an instance of the Player class
    loop()
    paused = False
    pygame.quit()
    sys.exit()
#    maze.draw_maze(screen)