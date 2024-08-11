import pygame
import maze as Maze
class Timer :
    def __init__(self, durat):  #duration
        self.durat = durat
        self.counter = durat
        self.font = pygame.font.SysFont(None,60)
        self.timer_text = self.font.render(str(self.counter),True,(223,53,233))
        self.timer_event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.timer_event, 1000)
    
    def update(self) :
        self.counter -= 1
        self.timer_text = self.font.render(str(self.counter),True,(223,53,233))
        if self.counter == 0 :
            Maze.gameover()

    def drawArc(self,surf, color, center, radius, width, end_angle):
     arc_rect = pygame.Rect(0, 0, radius*2, radius*2)
     arc_rect.center = center
     pygame.draw.arc(surf, color, arc_rect, 0, end_angle, width)