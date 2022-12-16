
import pygame
import serial
from datetime import datetime
from time import time
from collections import deque

from os import path

import Tests
import Scores


DISPLAY_SIZE = (1920,1080)
pygame.init()
screen = pygame.display.set_mode(DISPLAY_SIZE, pygame.FULLSCREEN)
clock = pygame.time.Clock()

population  = 10000

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


def calc_outcome(cost, cutoff, stag_dis):
    f1 = population / cost
    f2 = cutoff / (1+stag_dis)
    return f1 * f2


# class Box:
#     def __init__(self, x:int, y:int):
#         self._fp = ""
#         self._img = pygame.image.load(self._fp).convert_alpha()
#         self._img_rect = self._img.get_rect()
#         self.active = False

class Component:
    "Class object for Test components"
    def __init__(self, _player:int, x=0, y=0):
        self._player = _player
        self._fp = ""
        self._img = pygame.image.load(self._fp).convert_alpha()
        self._img_rect = self._img.get_rect()
        self.x = x
        self.y = y


class UpperComponent:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class LowerComponent:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        

class Scanner:

    def __init__(self, _port):
        self._port = _port
        self.conn = self.connect_scanner(_port)

    def connect_scanner(self, port):
        return serial.Serial(port)

    def close_connection(self):
        self._input.close()

    def is_connected(self):
        port_found = (self._port in [p.device for p in serial.tools.list_ports.comports()])
        return True if port_found else False

    def maintain_connection(self):
        "DO NOT RUN IN MAIN LOOP"
        CHECK_FREQUENCY = 5 #seconds
        self.conn = self.connect_scanner(self._port)
        while self.is_connected():
            time.sleep(CHECK_FREQUENCY)
        self.maintain_connection()

    


class Player:
    
    def __init__(self, _num:int, _port:str):
        self._input = serial.Serial(_port)
        # self._screen_moving = False
        self._player_num = _num
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


    def fetch_input(self):
        if self._input.in_waiting > 0:
            _txt = self._input.readlines().decode('utf-8')
            self.input_stream.extend(_txt)
            self._num_scans += len(_text)

    
    def reader(self):
        if self.input_stream:



    def time_to_complete(self):
        return self._start_time - time.now()


    def save_results(self):
        ID = next(Scores._id)
        timestamp = datetime.now()
        time_length = self.time_to_complete()
        test_sel = self.options_selected['test']
        cutoff_sel = self.options_selected['cut-off']
        sod_sel = self.options_selected['stage-of-disease']

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

    # load background
    # find USB ports
    # load players


    while True:


        pygame.display.flip()
        clock.tick(30)
    


if __name__ == '__main__':
    run()

    Scores._db.close()