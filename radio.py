import pygame
#from pygame.locals import *

pygame.mixer.init()
pygame.init()

main_volume = 1
screen = pygame.display.set_mode((10, 10))

class Fader(object):
    instances = []
    def __init__(self, fname):
        super(Fader, self).__init__()
        assert isinstance(fname, basestring)
        self.sound = pygame.mixer.Sound(fname)
        self.increment = 0.01
        self.next_vol = 0
        Fader.instances.append(self)

    def fade_to(self, new_vol):
        self.next_vol = new_vol

    def set_max_volume(self, max_vol):
        if self.sound.get_volume() > 0:
            self.next_vol = max_vol
            self.fade_to(max_vol)

    @classmethod
    def update(cls):
        for inst in cls.instances:
            curr_volume = inst.sound.get_volume()
            #print inst, curr_volume, inst.next_vol
            if inst.next_vol > curr_volume:
                inst.sound.set_volume(curr_volume + inst.increment)
            elif inst.next_vol < curr_volume:
                inst.sound.set_volume(curr_volume - inst.increment)

sound1 = Fader("song1.wav")
sound2 = Fader("song2.wav")
sound1.sound.play(-1)
sound1.fade_to(1)
sound2.sound.play(-1)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                sound1.fade_to(0)
                sound2.fade_to(main_volume)
            if event.key == pygame.K_LEFT:
                sound1.fade_to(main_volume)
                sound2.fade_to(0)
            if event.key == pygame.K_UP:
                if main_volume < 1:
                    main_volume += 0.1
                    sound1.set_max_volume(main_volume)
                    sound2.set_max_volume(main_volume)
            if event.key == pygame.K_DOWN:
                if main_volume > 0:
                    main_volume -= 0.1
                    sound1.set_max_volume(main_volume)
                    sound2.set_max_volume(main_volume)
            if event.key == pygame.K_ESCAPE:
                running = False
        if event.type == pygame.QUIT:
            running = False

    # Update faders
    Fader.update()

    screen.fill((0, 0, 0))
    pygame.display.flip()
