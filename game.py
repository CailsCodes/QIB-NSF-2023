# Remember to include #! feature and remove .py extension so can be fun as an executable


#------------------------------------------------------------------
#------------------------------------------------------------------

import pygame

pygame.display.init()


DISPLAY_SIZE = (1920,1080)
REFRESH_RATE = 24

background_img_fp = ""
screen = pygame.display.set_mode(DISPLAY_SIZE, pygame.FULLSCREEN)
background = pygame.image.load(background_img_fp).convert()
screen.blit(background, (1,1))
pygame.update()

#------------------------------------------------------------------
#------------------------------------------------------------------

from collections import deque
from datetime import datetime
from time import time

from lib import Scores, TestOption1, TestOption2, TestOption3

POPULATION  = 10000



INPUT_OPTIONS = {
    "start" : None,
    "build" : None,
    "bloodtest" : None,
    "spittest" : None,
    "DNAtest" : None,
    }


SCIENTIST_NUM = 1
def update_scientist_num(num:int):
    global SCIENTIST_NUM
    SCIENTIST_NUM = num
    # Render player image


def calc_outcome(cost, cutoff, stag_dis):
    "Calculates number of tests delivered"
    f1 = POPULATION / cost
    f2 = cutoff / (1+stag_dis)
    return f1 * f2





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








def time_to_complete(self):
    return _start_time - time.now()


def save_results():
    ID              = next(Scores._id)
    timestamp       = datetime.now()
    time_length     = time_to_complete()
    test_sel        = options_selected['test']
    cutoff_sel      = options_selected['cut-off']
    sod_sel         = options_selected['stage-of-disease']

    Scores.add_results(
                ID, 
                timestamp, 
                SCIENTIST_NUM, 
                test_sel, 
                cutoff_sel, 
                sod_sel,
                _outcome,
                time_length,
                _num_scans)




def main():
    pygame.event.init()
    clock = pygame.time.Clock()

    # load images


    num_scans = 0
    start_time = 0



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

    options_selected = {
        "Box 1" : None,
        "Box 2" : None,
        "Box 3" : None
        }


    while True:

        for e in pygame.event.get():
            et = e.type

            if (et == pygame.QUIT) or (et == pygame.KEYUP and e.key == pygame.K_ESCAPE):
                Scores._db.close()
                pygame.quit()
                quit()

            elif et == pygame.TEXTINPUT:
                text = e.text
                # action

                

        # pygame.display.flip()
        clock.tick(REFRESH_RATE)
    


if __name__ == '__main__':
    main()
    