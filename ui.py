import pygame

pygame.font.init()
default_font = pygame.font.SysFont("Arial", 30)

def draw_text(screen, text, x, y, color=(255, 255, 255), font=default_font):
    outline_color = (0, 0, 0)
    offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # left, right, up, down

    for dx, dy in offsets:
        outline = font.render(text, True, outline_color)
        screen.blit(outline, (x + dx, y + dy))

    rendered = font.render(text, True, color)
    screen.blit(rendered, (x, y))

def draw_text_bottom_right(screen, text, right_x, y, color=(255, 255, 255), font=default_font):
    outline_color = (0, 0, 0)
    rendered = font.render(text, True, color)
    text_width = rendered.get_width()

    offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dx, dy in offsets:
        outline = font.render(text, True, outline_color)
        screen.blit(outline, (right_x - text_width + dx, y + dy))

    screen.blit(rendered, (right_x - text_width, y))

def draw_text_center(screen, text, y, color=(255, 255, 255), font=default_font):
    outline_color = (0, 0, 0)
    rendered = font.render(text, True, color)
    text_width = rendered.get_width()
    screen_width = screen.get_width()
    x = (screen_width - text_width) // 2

    offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dx, dy in offsets:
        outline = font.render(text, True, outline_color)
        screen.blit(outline, (x + dx, y + dy))

    screen.blit(rendered, (x, y))

def draw_game_state(screen, balls_left, peg_inventory, selected_peg, balls_scored, balls_needed, current_level, level_count):
    draw_text(screen, f"balls left: {balls_left}", 20, 20)
    y = 1280 - 35* len(peg_inventory.items())
    draw_text_bottom_right(screen, f"level {current_level}/{level_count}", 720 - 20, 20)
    for peg_type, count in peg_inventory.items():
        draw_text(screen, f"{peg_type}: {count}", 20, y, (0, 255, 0) if selected_peg == peg_type else (255, 255, 255))
        y += 30

    draw_text_bottom_right(screen, f"Scored Balls: {balls_scored}/{balls_needed}", 720 - 20, 1280 - 40)
