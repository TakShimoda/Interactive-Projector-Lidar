import pygame, random
import win32api
import win32con
import win32gui
from ctypes import windll
SetWindowPos = windll.user32.SetWindowPos

screen = pygame.display.set_mode((1366, 768), pygame.RESIZABLE) # For borderless, use pygame.NOFRAME
SetWindowPos(pygame.display.get_wm_info()['window'], -1, -1, -1, 0, 0, 0x0001)
done = False
fuchsia = (255, 255, 255)  # Transparency color
dark_red = (139, 0, 0)

draw_on = False
#draw_on = True
last_pos = (0, 0)
color = (0, 255, 0)
radius = 3

hwnd = pygame.display.get_wm_info()["window"]
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
#win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*fuchsia), 0, win32con.LWA_COLORKEY)
win32gui.SetLayeredWindowAttributes(hwnd, 0, 70, win32con.LWA_ALPHA)
#win32gui.SetLayeredWindowAttributes(hwnd, 0, 70, win32con.LWA_COLORKEY)

def roundline(srf, color, start, end, radius=1):
    dx = end[0]-start[0]
    dy = end[1]-start[1]
    distance = max(abs(dx), abs(dy))
    for i in range(distance):
        x = int( start[0]+float(i)/distance*dx)
        y = int( start[1]+float(i)/distance*dy)
        pygame.draw.circle(srf, color, (x, y), radius)

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    screen.fill(fuchsia)  # Transparent background
    #pygame.draw.rect(screen, dark_red, pygame.Rect(0, 0, 1600, 10))
    try:
        while True:
            e = pygame.event.wait()
            if e.type == pygame.QUIT:
                raise StopIteration
            if e.type == pygame.MOUSEBUTTONDOWN:
                color = (0,0,255)
                pygame.draw.circle(screen, color, e.pos, radius)
                draw_on = True
            if e.type == pygame.MOUSEBUTTONUP:
                draw_on = False
            if e.type == pygame.MOUSEMOTION:
                if draw_on:
                    pygame.draw.circle(screen, color, e.pos, radius)
                    roundline(screen, color, e.pos, last_pos,  radius)
                last_pos = e.pos
            pygame.display.flip()
    except StopIteration:
        pass
    pygame.display.update()
pygame.quit()
