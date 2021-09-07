import datetime

import pygame

print(datetime.datetime.now().__str__())

pygame.init()
text = datetime.datetime.now().__str__()
font = pygame.font.SysFont("stxihei", 40)
rtext = font.render(text, True, '#22ddcc', '#cc22aa')
pygame.image.save(rtext, "t.png")

