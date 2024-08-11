import pygame
import subprocess
import sys
from button import Button
pygame.init()
screen = (1200,800)
SCREEN = pygame.display.set_mode(screen)
#BackGround
BackG = pygame.image.load("images/home.jpeg")
BackG = pygame.transform.scale(BackG,(1200,800))
Play_BackG = pygame.image.load("images/play_screen.jpg")
Play_BackG = pygame.transform.scale(Play_BackG,(1200,800))
highscores_BackG = pygame.image.load("images/hscore_backg.jpg")
highscores_BackG = pygame.transform.scale(highscores_BackG,(1200,800))

#diff button
imagenum1 = pygame.image.load("images/number1.jpeg")
imagenum1 = pygame.transform.scale(imagenum1,(250,250))
imagenum2 = pygame.image.load("images/number2.jpeg")
imagenum2 = pygame.transform.scale(imagenum2,(250,250))
imagenum3 = pygame.image.load("images/number3.jpeg")
imagenum3 = pygame.transform.scale(imagenum3,(250,250))

#music load
pygame.mixer.music.load("music/homemusic.mp3")
pygame.mixer.music.play(-1)
#home font
def get_font(size): 
    return pygame.font.Font("fonts/DripOctober.ttf", size)
# button image scaling
button_image = pygame.image.load("images/button1.png")
button_image = pygame.transform.scale(button_image,(250,125))
#main_font
main_font = pygame.font.SysFont("Cambria",50)
def play() :
        pygame.display.set_caption("Play")
        
        while True:
         Play_mouse_POS = pygame.mouse.get_pos()

         SCREEN.fill("black")
         SCREEN.blit(Play_BackG,(0,0))
         Play_text = get_font(45).render("Difficulty Level", True, "White")
         Play_rect = Play_text.get_rect(center=(620, 100))
         SCREEN.blit(Play_text, Play_rect)

         Back_B = Button(image=None, pos=(600,650), 
                            text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")
         Diff1_B = Button(image=None, pos=(130, 400), 
                            text_input="Lvl1", font=get_font(80), base_color="Red", hovering_color="Green")
         Diff2_B = Button(image=None, pos=(580, 400), 
                            text_input="Lvl2", font=get_font(80), base_color="Red", hovering_color="Green")
         Diff3_B = Button(image=None, pos=(1030, 400), 
                            text_input="Lvl3", font=get_font(80), base_color="Red", hovering_color="Green")
         for button in [Back_B,Diff3_B,Diff1_B,Diff2_B]:
            button.Changecolor(Play_mouse_POS)
            button.update(SCREEN)

         for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

                #1.py

            if event.type == pygame.MOUSEBUTTONDOWN:

                #Back 

                if Back_B.Checkinput(Play_mouse_POS):
                    Home()
                
                if Diff1_B.Checkinput(Play_mouse_POS):
                    # Closing this to open 1.py
                 diff_1 = "difficulties/1.py"
                 # Executing 1.py
                 pygame.mixer.music.stop()
                 subprocess.run([sys.executable, diff_1])

                #2.py

                if Diff2_B.Checkinput(Play_mouse_POS):
                    # Closing this to open 2.py
                 #pygame.quit()
                 diff_2 = "difficulties/2.py"
                 # Executing 2.py
                 pygame.mixer.music.stop()
                 subprocess.run([sys.executable, diff_2])

                #3.py

                if Diff3_B.Checkinput(Play_mouse_POS):
                    # Closing this to open 3.py
                 #pygame.quit()
                 diff_3 = "difficulties/3.py"
                 pygame.mixer.music.stop()
                 # Executing 3.py
                 subprocess.run([sys.executable, diff_3])
 
         pygame.display.update()

def Highscores() :
        pygame.display.set_caption("High Scores")
        # Read scores from the file
        with open("highscores.txt", "r") as file:
            scores = [int(line.strip()) for line in file]

    # Sort the scores in descending order
        scores.sort(reverse=True)
        
        while True:
         Play_mouse_POS = pygame.mouse.get_pos()

         SCREEN.fill("black")
         SCREEN.blit(highscores_BackG, (0, 0))
         Play_text = get_font(65).render("High Scores", True, "White")
         Play_rect = Play_text.get_rect(center=(900, 100))
         SCREEN.blit(Play_text, Play_rect)

         for i, score in enumerate(scores[:3]):
            score_text = get_font(40).render(f"{i+1}  {score}", True, "White")
            score_rect = score_text.get_rect(center=(900, 200 + i * 50))
            SCREEN.blit(score_text, score_rect)

         Play_Back = Button(image=None, pos=(600, 720), 
                            text_input="BACK", font=get_font(75), base_color="Blue", hovering_color="Green")

         Play_Back.Changecolor(Play_mouse_POS)
         Play_Back.update(SCREEN)

         for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if Play_Back.Checkinput(Play_mouse_POS):
                    Home()

         pygame.display.update()   

def Home():
    pygame.display.set_caption("Home Screen")
    
    while True :
        SCREEN.fill("black")
        SCREEN.blit(BackG,(0,0))
        Home_mouse_pos = pygame.mouse.get_pos()
        #Intro
        Home_text = get_font(80).render("Dragon Ball",True,"White")
        Home_rect = Home_text.get_rect( center= (650,100))
        #button 
        play_button = Button(image=None,pos=(800,450),text_input="Play",font=get_font(60),base_color="white",hovering_color="green")
        quit_button = Button(image=None,pos=(800,750),text_input="Quit",font=get_font(60),base_color="white",hovering_color="green")
        Highscore_button = Button(image=None,pos=(800,600),text_input="Top Scores",font=get_font(60),base_color="white",hovering_color="green")
        SCREEN.blit(Home_text,Home_rect)
        for button in [play_button,quit_button,Highscore_button]:
            button.Changecolor(Home_mouse_pos)
            button.update(SCREEN)
        #button Completed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if Highscore_button.Checkinput(Home_mouse_pos):
                    Highscores()
                if play_button.Checkinput(Home_mouse_pos):
                    play()
                if quit_button.Checkinput(Home_mouse_pos):
                    pygame.quit()
                    sys.exit()


        pygame.display.update()


Home()