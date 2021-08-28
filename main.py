import pygame

from Button import Button
from Color import Color
from SimulationModel import SimulationModel

pygame.init()
pygame.display.set_caption('Ant Simulation')

# screen size
main_area_width = 800
main_area_height = 600
control_area_width = 800
control_area_height = 100

# function area
screen = pygame.display.set_mode((main_area_width, main_area_height + control_area_height))
main_area = pygame.Surface.subsurface(screen, (0, 0, main_area_width, main_area_height))
control_area = pygame.Surface.subsurface(screen, (0, main_area_height, control_area_width, control_area_height))
the_model = SimulationModel(main_area_width, main_area_height)
the_model.reset()

# reset
reset_img = pygame.image.load('image/reset.png')
reset_btn = Button((0, 0), (80, 50), reset_img, the_model.reset)

# start
start_img = pygame.image.load("image/start.png")
stop_img = pygame.image.load("image/stop.png")
start_btn = Button((reset_btn.position[0] + reset_btn.size[0], 0),
                   (80, 50), start_img, the_model.run_one_event())

# font
myfont = pygame.font.SysFont('Comic Sans MS', 25)
text_width, text_height = myfont.size("Collected Food: xxxxx")
text_rect = pygame.Rect(start_btn.rect.right + 5, start_btn.position[1] + 2,
                        text_width, text_height)
text_surface = myfont.render("Collected Food: 0", False, (0, 0, 0))

done = False
if __name__ == '__main__':
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            # checks if a mouse is clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                relative_x, relative_y = pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]-main_area.get_height()
                reset_btn.on_click((relative_x, relative_y))
                start_btn.on_click((relative_x, relative_y))

        screen.fill(Color.WHITE)
        the_model.draw(main_area)
        pygame.draw.line(main_area, Color.SLATE_GREY, (0, main_area.get_height()),
                         (main_area.get_width(), main_area.get_height()), width=3)
        control_area.blit(start_btn.image, start_btn.rect)
        control_area.blit(reset_btn.image, reset_btn.rect)
        control_area.blit(text_surface, (text_rect.left, text_rect.top))
        pygame.display.flip()
