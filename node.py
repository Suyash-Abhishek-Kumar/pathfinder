import pygame

RADIUS = 5
BASECOLOR = (205, 205, 205)
HOVERCOLOR = (205, 0, 0)
SELECTEDCOLOR = (0, 205, 0)
def create_hitbox(coords):
    topleft = (coords[0] - 4, coords[1] - 4)
    bottomright = (coords[0] + 4, coords[1] + 4)
    return (topleft, bottomright)

class Button:
    def __init__(self, screen, name, coords):
        self.screen = screen
        self.coords = coords
        self.name = name
        self.selected = False
        self.hitbox = create_hitbox(self.coords)

    def display(self):
        if self.selected:
            pygame.draw.circle(self.screen, SELECTEDCOLOR, self.coords, RADIUS + 1)
        elif self.mouse_touched():
            pygame.draw.circle(self.screen, HOVERCOLOR, self.coords, RADIUS + 1)
        else:
            pygame.draw.circle(self.screen, BASECOLOR, self.coords, RADIUS)
    
    def mouse_touched(self):
        mouse = pygame.mouse.get_pos()
        if self.hitbox[0][0] < mouse[0] < self.hitbox[1][0] and self.hitbox[0][1] < mouse[1] < self.hitbox[1][1]:
            return True
        else:
            return False