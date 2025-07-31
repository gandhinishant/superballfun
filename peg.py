import pygame

# values
colors = {
    "EMPTY": (176, 176, 176),
    "PLAIN": (74, 74, 74),
    "BOUNCY": (33, 173, 102),
    "GOAL": (0, 0, 255),
    "KILL": (255, 0, 0),
    "CONFETTI": (255, 105, 180),
    "SPLITTER": (255, 255, 0),
    "EXPLODE": (255, 128, 0),
}
hover_colors = {
    "EMPTY": (200, 200, 200), 
    "PLAIN": (100, 100, 100), 
    "BOUNCY": (50, 200, 130), 
    "GOAL": (80, 80, 255),
    "KILL": (255, 80, 80),
    "CONFETTI": (255, 135, 200),
    "SPLITTER": (255, 255, 100),
    "EXPLODE": (255, 160, 60),
}
# bounciness
bounce = {
    "EMPTY": -1, # should never matter
    "PLAIN": 0.7,
    "BOUNCY": 1.05,
    "GOAL": 0, # should never matter either
    "KILL": 0,
    "CONFETTI": 0.7,
    "SPLITTER": 0.7,
    "EXPLODE": 0.7,
}

# peg type
class Peg:
    def __init__(self, x, y, peg_type, radius, editable):
        self.x = x
        self.y = y
        self.type = peg_type
        self.radius = radius
        self.bounciness = bounce[peg_type]
        self.color = colors[peg_type]
        self.hover_color = hover_colors[peg_type]
        self.editable = editable
        self.hovered = False
        self.queue_delete = False
    
    def draw(self, screen):
        color = self.hover_color if self.hovered else self.color;
        pygame.draw.circle(screen, color, (self.x, self.y), self.radius)

    def switch(self, new_peg_type):
        self.type = new_peg_type
        self.bounciness = bounce[new_peg_type]
        self.color = colors[new_peg_type]
        self.hover_color = hover_colors[new_peg_type]
        self.queue_delete = False
        self.editable = True
    
    def effects(self, ball):
        if self.type == "CONFETTI":
            ball.confetti = True
        if self.type == "GOAL":
            ball.confetti = True
            ball.touching_goal = True
        if self.type == "KILL":
            ball.queue_delete = True
        if self.type == "SPLITTER":
            ball.split = True
            self.queue_delete = True
        if self.type == "EXPLODE":
            ball.explode = True
            self.queue_delete = True
