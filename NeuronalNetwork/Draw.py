import pygame
import numpy as np

def draw_Neuronal_Network(screen, width):
    sep_ver = 60
    sep_hor = 100


    font = pygame.font.SysFont('Consolas',20)

    screen.fill((255, 255, 255))
    iz_font = font.render("Right", True, (0, 0, 0))
    ent_font = font.render("Entrada", True, (0, 0, 0))
    na_font = font.render("Left", True, (0, 0, 0))
    der_font = font.render("Go", True, (0, 0, 0))
    screen.blit(ent_font, (width // 2 + 40, 30))
    screen.blit(iz_font, (width // 2 + 600, 175 + (int(0 * sep_ver * 1.5))))
    screen.blit(na_font, (width // 2 + 600, 175 + (int(1 * sep_ver * 1.5))))
    screen.blit(der_font, (width // 2 + 600, 175 + (int(2 * sep_ver * 1.5))))

    co1 = font.render("C.O. 1", True, (0, 0, 0))
    co2 = font.render("C.O. 2", True, (0, 0, 0))
    sal = font.render("Salida", True, (0, 0, 0))
    screen.blit(co1, (width // 2 + 260, 20))
    screen.blit(co2, (width // 2 + 410, 90))
    screen.blit(sal, (width // 2 + 530, 120))

def draw_nn(we, arg_max, state_old, screen, width):
    sep_ver = 60
    sep_hor = 100

    we = np.array([(w + 1) / 2 for w in we])
    we_0, we_1, we_2, we_3, we_4 = we[0], we[1], we[2], we[3], we[4]
    we_0 = (we_0 - np.min(we_0)) / np.ptp(we_0)
    we_1 = (we_1 - np.min(we_1)) / np.ptp(we_1)
    we_2 = (we_2 - np.min(we_2)) / np.ptp(we_2)
    we_3 = (we_3 - np.min(we_3)) / np.ptp(we_3)
    we_4 = (we_4 - np.min(we_4)) / np.ptp(we_4)

    try:
        for i in range(len(state_old)):
            pygame.draw.circle(screen, (state_old[i] * 255, 100, 0), (width // 2 + 80, 80 + (int(i * sep_ver/1))), 10)
            for j in range(len(we_0[i])):
                pygame.draw.line(screen,
                                (we_0[i][j] * 255, 100, 0), (width // 2 + 80 + 20, 80 + (int(i * sep_ver/1))),#Izquierda
                                (width // 2 + 300 - 20, 80 + (int(j * sep_ver / 1.2))), 2)#Derecha
        for i in range(len(we_1)):
            pygame.draw.circle(screen, (we_1[i] * 255, 0, 0), (width // 2 + 300, 80 + (i * sep_ver / 1.2)), 20)
            for j in range(len(we_2[i])):
                pygame.draw.line(screen,
                                (we_2[i][j] * 255, 0, 0), (width // 2 + 300 + 20, 80 + (i * sep_ver / 1.2)),#Izquierda
                                (width // 2 + 450 - 20, 150 + (int(j * sep_ver * 1))), 2)#Derecha
        for i in range(len(we_3)):
            pygame.draw.circle(screen, (0, 0, we_3[i] * 255), (width // 2 + 450, 150 + (int(i * sep_ver / 1))), 20)
            for j in range(len(we_4[i])):
                pygame.draw.line(screen,
                                (0, 0, we_4[i][j] * 255), (width // 2 + 450 + 20, 150 + int(i * sep_ver / 1)),#Izquierda
                                (width // 2 + 570 - 20, 190 + (int(j * sep_ver * 1.5))), 2)#Derecha
        for i in range(3):
            if i == arg_max:
                pygame.draw.circle(screen, (0, 255, 0), (width // 2 + 570, 190 + (int(i * sep_ver * 1.5))), 20)
            else:
                pygame.draw.circle(screen, (150, 150, 150), (width // 2 + 570, 190 + (int(i * sep_ver * 1.5))), 20)
    except:
        pass
