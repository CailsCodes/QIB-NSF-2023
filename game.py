# Remember to include #! feature and remove .py extension so can be fun as an executable
import pygame

pygame.display.init()
pygame.time.init()
pygame.image.init()

DISPLAY_SIZE = (1920,1080)
background_img_fp = ""
screen = pygame.display.set_mode(DISPLAY_SIZE, pygame.FULLSCREEN)
background = pygame.image.load(background_img_fp).convert()
pygame.update(background)

# import _thread
from collections import deque
from datetime import datetime
# from os import path
from time import time

import serial
from lib import Scores, Scanner, LFT, PCR, Antibody

POPULATION  = 10000

cut_off = { # fraction of people who will be correctly testet tested, adjusted for penalty from including people who don't have disease
    "low"       : .65,
    "medium"    : .95,
    "high"      : .35
    }

stage_of_disease = { # fraction of people who need to be retested
    "All"                   : 0.15,
    "Early onset"           : 0.35,
    "Very symptomatic"      : 0.05
    }

_tests = ['LFT', 'Antibody', 'Blood']



def calc_outcome(cost, cutoff, stag_dis):
    f1 = POPULATION / cost
    f2 = cutoff / (1+stag_dis)
    return f1 * f2


def get_ports():
    return [p.device for p in serial.tools.list_ports.comports()]


class Box:

    def __init__(self, fp, x:int, y:int):
        self._fp = fp
        self._img = pygame.image.load(self._fp).convert_alpha()
        self._img_rect = self._img.get_rect()
        self.active = False
        self.active_pos = (x,y)

    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, value): # move square if the object has become active or de-activated
        assert isinstance(value, bool)
        self._active = value
        if value:
            self._img_rect = None
        else:
            self._img_rect = None

    

class TestImage:
    "Class object for Test"
    def __init__(self, _player:int, x=0, y=0):
        self._player = _player
        self._fp = ""
        self._img = pygame.image.load(self._fp).convert_alpha()
        self._img_rect = self._img.get_rect()
        self.x = x
        self.y = y

        



    


class Player:
    
    def __init__(self, player:int, port:str):
        self.scanner = Scanner(port)
        self._player_num = player
        self.X = self.Y = 0

        self.input_stream = deque(maxlen=10)

        self.options_selected = {
            "cut-off" : None,
            "stage-of-disease" : None,
            "test" : None
            }
        self._outcome = 0
        self._num_scans = 0
        self._start_time = 0 # time.now()


    @property
    def options_selected(self):
        return self._options_selected

    @options_selected.setter
    def options_selected(self, key, value):
        self._options_selected[key] = value
        # select which boxes to be moved


    def fetch_input(self):
        if self._input.in_waiting > 0:
            _txt = self._input.readlines().decode('utf-8')
            self.input_stream.extend(_txt)
            self._num_scans += len(_text)

    
    def reader(self):
        if self.input_stream:
            cmd = self.input_stream.pop()

            if cmd == "complete":
                self.save_results()
                #load score
            elif cmd in cut_off:
                self.options_selected['cut-off'] == cmd
            elif cmd in stage_of_disease:
                self.options_selected['stage-of-disease'] = cmd
            elif cmd in _tests:
                self.options_selected['test'] = cmd
            


    def time_to_complete(self):
        return self._start_time - time.now()


    def save_results(self):
        ID              = next(Scores._id)
        timestamp       = datetime.now()
        time_length     = self.time_to_complete()
        test_sel        = self.options_selected['test']
        cutoff_sel      = self.options_selected['cut-off']
        sod_sel         = self.options_selected['stage-of-disease']

        Scores.add_results(
                    ID, 
                    timestamp, 
                    self._player_num, 
                    test_sel, 
                    cutoff_sel, 
                    sod_sel,
                    self._outcome,
                    time_length,
                    self._num_scans)




def run():
    clock = pygame.time.Clock()
    
    usb_ports = get_ports()
    if len(usb_ports > 2):
        time.sleep(1)
        # have screen to inform player to only have scanners in USB ports
    
    player1 = Player(1, usb_ports[0])
    player2 = Player(2, usb_ports[1])


    while True:

        # pygame.display.flip()
        clock.tick(24)
    


if __name__ == '__main__':
    run()
    Scores._db.close()