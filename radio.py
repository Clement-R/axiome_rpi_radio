import pygame
import RPi.GPIO as GPIO

volume_pot = 0
main_volume = 0
toggle_track = False

# Raspberry pi management
def change_volume(channel):
    volume_pot_str = "%d%d%d" % (GPIO.input(22), GPIO.input(27), GPIO.input(4))
    global volume_pot
    volume_pot = int(volume_pot_str, 2)
    GPIO.output(17, GPIO.input(4))

def change_track(channel):
    global toggle_track
    
    if GPIO.input(26):
        toggle_track = False
    else:
        toggle_track = True

def ajdust_volume(sound1, sound2):
    global main_volume
    global volume_pot
    
    if main_volume != volume_pot:
        main_volume = volume_pot * 0.2
        #print main_volume
        sound1.set_max_volume(main_volume)
        sound2.set_max_volume(main_volume)

# Set the GPIO reading system to BOARD, it uses rPi board numbering
GPIO.setmode(GPIO.BCM)
# Set a GPIO port as an output, with an initial value
GPIO.setup(17, GPIO.OUT, initial=GPIO.LOW)
# Set a GPIO port as an entry
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.add_event_detect(4, GPIO.BOTH)
GPIO.add_event_callback(4, change_volume)
GPIO.add_event_detect(27, GPIO.BOTH)
GPIO.add_event_callback(27, change_volume)
GPIO.add_event_detect(22, GPIO.BOTH)
GPIO.add_event_callback(22, change_volume)

GPIO.add_event_detect(26, GPIO.BOTH)
GPIO.add_event_callback(26, change_track)

GPIO.output(17, GPIO.input(4))
# End of raspberry pi part

pygame.mixer.init()
pygame.init()


screen = pygame.display.set_mode((100, 100))

class Fader(object):
    instances = []
    def __init__(self, fname):
        super(Fader, self).__init__()
        assert isinstance(fname, basestring)
        self.sound = pygame.mixer.Sound(fname)
        self.increment = 0.01
        self.next_vol = 0
        self.active = False
        Fader.instances.append(self)

    def fade_to(self, new_vol):
        self.next_vol = new_vol

    def set_max_volume(self, max_vol):
        if self.active:
            self.next_vol = max_vol
            self.fade_to(max_vol)
        else:
            self.next_vol = 0

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
sound1.active = True
sound2.sound.play(-1)
sound2.active = False

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_ESCAPE:
                running = False
                GPIO.cleanup()
        if event.type == pygame.QUIT:
            running = False
            GPIO.cleanup()

    if not toggle_track and not sound1.active:
        sound1.active = True
        sound2.active = False
                
        sound1.fade_to(0)
        sound2.fade_to(main_volume)
        
    if toggle_track and sound1.active:
        sound1.active = False
        sound2.active = True
                
        sound1.fade_to(main_volume)
        sound2.fade_to(0)

    ajdust_volume(sound1, sound2)
    
    # Update faders
    Fader.update()

    screen.fill((0, 0, 0))
    pygame.display.flip()
