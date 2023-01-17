
"""
Testing, testing, 1-2-3!


...

Author: Cailean Carter
Contact: cailean.carter@quadram.ac.uk
Affiliation: Quadram Institute, Norwich, UK

"""

from collections import ChainMap
from time import localtime, strftime, time

import pygame

from lib import (Options, Scores, TestOption1, TestOption2, TestOption3,
                 TestOptions)

#------------------------------------------------------------------
#               GLOBAL VARIABLES
#------------------------------------------------------------------

DISPLAY_SIZE = (1920,1080)
REFRESH_RATE = 24
POPULATION  = 10000
SCIENTIST_NUM = 1
SCIENTIST_IMGS = ("assets/scientist1.png", "assets/scientist2.png")
BUILDING = False
start_time = time()

TESTS_DELIVERED = 0
PEOPLE_TREATED = 0

scanner_input = ""

#------------------------------------------------------------------
#               INITIALISE METHODS
#------------------------------------------------------------------

pygame.display.init()
screen = pygame.display.set_mode(DISPLAY_SIZE, pygame.FULLSCREEN)
pygame.font.init()
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)

scoring = Scores()

#------------------------------------------------------------------
#               LOAD GAME ASSETS
#------------------------------------------------------------------

background          = pygame.image.load("assets/Background.png").convert()
ScientistImg        = pygame.image.load(SCIENTIST_IMGS[0]).convert_alpha()
ScientificReport    = pygame.image.load("assets/scientific_report.png").convert_alpha()
peopleTreated       = pygame.image.load("assets/people_treated.png").convert_alpha()
testsDelivered      = pygame.image.load("assets/tests_delivered.png").convert_alpha()

cabinsketch_font    = pygame.font.Font("assets/fonts/CabinSketch-Bold.ttf", 68)

Box1img             = pygame.image.load("assets/box1.png").convert_alpha()
Box2img             = pygame.image.load("assets/box2.png").convert_alpha()
Box3img             = pygame.image.load("assets/box3.png").convert_alpha()

StarImgOutline      = pygame.image.load("assets/starOutline.png").convert_alpha()
StarImg             = pygame.image.load("assets/star.png").convert_alpha()
StarPoints          = pygame.image.load("assets/starPoints.png").convert_alpha()
reportComments      = pygame.image.load("assets/reportComments.png").convert_alpha()

B1O0 = Options("Null", 1, 0, None, None, True)
B1O1 = TestOptions("Blood test", 1, 1, Box1img, False, TestOption1)
B1O2 = TestOptions("Spit test", 1, 2, Box1img, False, TestOption2)
B1O3 = TestOptions("DNA test", 1, 3, Box1img, False, TestOption3)

B2O0 = B1O0._replace(box=2)
B2O1 = Options("Everybody", 2, 1, 0.7, Box2img, False)
B2O2 = Options("Those who feel sick", 2, 2, 1, Box2img, False)
B2O3 = Options("The very sick", 2, 3, .4, Box2img, False)

B3O0 = B1O0._replace(box=3)
B3O1 = Options("Weak", 3, 1, .5, Box3img, False)
B3O2 = Options("Balanced", 3, 2, .8, Box3img, False)
B3O3 = Options("Strong", 3, 3, 1, Box3img, False)

options = [B1O0, B1O1, B1O2, B1O3, B2O0, B2O1, B2O2, B2O3, B3O0, B3O1, B3O2, B3O3]
refs = {o.__str__() : o for o in options}


#------------------------------------------------------------------
#               GAME METHODS
#------------------------------------------------------------------

def close_game(*_):
    scoring._db.close()
    pygame.quit()
    quit()

def calc_outcome(v1:int, v2:int, v3:int):
    """
    Arguments:
    ----------
        v1 (int) : cost of test
        v2 (int) : who takes the test
        v3 (int) : detection strength
    
    Returns:
    --------
        Tests delivered (int)
        People treated (int)
    """
    tests_delivered = (POPULATION / v1) * v2 * 1.0245
    people_treated = tests_delivered * v3
    return int(tests_delivered), int(people_treated)

def get_selected(): return (option for option in refs.values() if option.selected)
def get_null(): return (option for option in refs.values() if option.name == 'Null')
def ready_to_build(): return not any((option for option in get_selected() if option.name == 'Null')) and not BUILDING

def get_selected_in_box(box:int):
    for i in get_selected():
        if i.box == box:
            return i

def draw_screen():
    screen.blit(background, (1,1))
    screen.blit(ScientistImg, (46, 108))
    for i in get_selected():
        if i.name != "Null":
            x, y = i.coordinates
            width = i.width
            screen.blit(i.image, (x,y), (width*(i.index - 1), 0,  width, 220))
    pygame.display.flip()

def swap_selected(new):
    old = get_selected_in_box(new.box)
    if (old.index != new.index) and not BUILDING: # type: ignore
        global refs
        refs[old.__str__()] = old._replace(selected=False) # type: ignore
        refs[new.__str__()] = new._replace(selected=True)
        draw_screen()
        
def update_scientist_num(num:int):
    global SCIENTIST_NUM
    global ScientistImg
    SCIENTIST_NUM = num+1
    img = SCIENTIST_IMGS[num]
    ScientistImg = pygame.image.load(img).convert_alpha()
    screen.blit(background, (0,73), (0, 73, 370, 138))
    screen.blit(ScientistImg, (46, 108))
    pygame.display.flip()

def start_game(*_):
    global start_time
    global BUILDING
    BUILDING = False
    for i in get_null():
        swap_selected(i)
    start_time = time()
    draw_screen()

def save_results(selected):
    timestamp       = strftime("%d %b %Y %H:%M:%S", localtime())
    time_length     = int(time() - start_time)
    B1, B2, B3 = selected
    scoring.add_results(
                timestamp, 
                time_length,
                SCIENTIST_NUM, 
                B1.index, 
                B2.index, 
                B3.index,
                TESTS_DELIVERED,
                PEOPLE_TREATED
                )

def draw_scientific_report(*_):
    screen.blit(ScientificReport, (1200, 320))
    pygame.display.flip()
    pygame.time.set_timer(SHOW_TESTS_DELIVERED_EVENT, 1000, loops=1)

def draw_tests_delivered(*_):
    screen.blit(testsDelivered, (1315, 500))
    pygame.display.flip()
    pygame.time.set_timer(SHOW_TESTS_DELIVERED_VALUE_EVENT, 1, loops=1)

def draw_tests_delivered_value(*_):
    text = "{:,}".format(TESTS_DELIVERED)
    visual = cabinsketch_font.render(text, True, (4, 186, 130))
    width, _ = cabinsketch_font.size(text)
    x = 1533 - (width/2)
    screen.blit(visual, (x, 595))
    pygame.display.flip()
    pygame.time.set_timer(SHOW_PEOPLE_TREATED_EVENT, 1500, loops=1)

def draw_people_treated(*_):
    screen.blit(peopleTreated, (1315, 712))
    pygame.display.flip()
    pygame.time.set_timer(SHOW_PEOPLE_TREATED_VALUE_EVENT, 1, loops=1)

def draw_people_treated_value(*_):
    text = "{:,}".format(PEOPLE_TREATED)
    visual = cabinsketch_font.render(text, True, (4, 186, 130))
    width, _ = cabinsketch_font.size(text)
    x = 1533 - (width/2)
    screen.blit(visual, (x, 806))
    pygame.display.flip()
    pygame.time.set_timer(STAR0_EVENT, 1500, loops=1)

def draw_star(num):
    y = 880-8
    x_coords = [1330, 1437, 1544, 1651, 1760]
    next_star_eligibility = {
        0 : (500,  STAR1_EVENT),
        1 : (1500, STAR2_EVENT),
        2 : (3000, STAR3_EVENT),
        3 : (4500, STAR4_EVENT),
        4 : (6000, STAR5_EVENT),
        5 : (10000, None)
        }
    
    fill = x_coords[:num]
    empty = x_coords[num:]
    screen.blit(background, (1318,872), (1318, 872, 538, 114))
    screen.blit(StarPoints, (1350, 960))

    for fx in fill:
        screen.blit(StarImg, (fx-8, y))
    for ex in empty:
        screen.blit(StarImgOutline, (ex-8, y))
    
    threshold, next_star_event = next_star_eligibility[num]
    if PEOPLE_TREATED >= threshold:
        pygame.time.set_timer(next_star_event, 750, loops=1)
    else:
        pygame.time.set_timer(COMMENT_EVENT, 300, loops=1)
    pygame.display.flip()

def draw_comment(*_):
    x,y = (1312, 980)
    height = 92
    width = 544
    comments = {
        6000 : 368,
        4500 : 276,
        3000 : 184,
        1500 : 92,
        500 : 0
        }
    for threshold, y_offset in comments.items():
        if PEOPLE_TREATED >= threshold:
            screen.blit(reportComments, (x,y), (0, y_offset,  width, height))
            pygame.display.flip()
            return

def build(*_):
    if ready_to_build():
        global BUILDING
        global TESTS_DELIVERED
        global PEOPLE_TREATED

        BUILDING = True
        B1, B2, B3 = get_selected()
        TESTS_DELIVERED, PEOPLE_TREATED = calc_outcome(B1.value, B2.value, B3.value)
        save_results((B1, B2, B3))
        draw_scientific_report()


#------------------------------------------------------------------
#               HANDLING GAME INPUTS
#------------------------------------------------------------------

SCANNER_INPUTS = {k : (swap_selected, v) for k, v in refs.items() if not k.endswith('O0')}
SCANNER_INPUTS.update({
    "start" : (start_game, None),
    "build" : (build, None),
    "close" : (close_game, None),
    "scientist1" : (update_scientist_num, 1),
    "scientist2" : (update_scientist_num, 2)
    }) # type: ignore

KB_INPUTS = {
    " " : (start_game, None), # new game / refresh
    "b" : (build, None), # build
    "1" : (update_scientist_num, 0),
    "2" : (update_scientist_num, 1),
    "q" : (swap_selected, B1O1),
    "w" : (swap_selected, B1O2),
    "e" : (swap_selected, B1O3),
    "a" : (swap_selected, B2O1),
    "s" : (swap_selected, B2O2),
    "d" : (swap_selected, B2O3),
    "z" : (swap_selected, B3O1),
    "x" : (swap_selected, B3O2),
    "c" : (swap_selected, B3O3)
    }

ALL_INPUTS = ChainMap(SCANNER_INPUTS, KB_INPUTS)

INPUT_TIMEOUT_EVENT                 = pygame.USEREVENT + 1
SHOW_TESTS_DELIVERED_EVENT          = pygame.USEREVENT + 2
SHOW_TESTS_DELIVERED_VALUE_EVENT    = pygame.USEREVENT + 3
SHOW_PEOPLE_TREATED_EVENT           = pygame.USEREVENT + 4
SHOW_PEOPLE_TREATED_VALUE_EVENT     = pygame.USEREVENT + 5
STAR0_EVENT                         = pygame.USEREVENT + 7
STAR1_EVENT                         = pygame.USEREVENT + 8
STAR2_EVENT                         = pygame.USEREVENT + 9
STAR3_EVENT                         = pygame.USEREVENT + 10
STAR4_EVENT                         = pygame.USEREVENT + 11
STAR5_EVENT                         = pygame.USEREVENT + 12
COMMENT_EVENT                       = pygame.USEREVENT + 13

scientific_report_events = {
    SHOW_TESTS_DELIVERED_EVENT          : (draw_tests_delivered, None),
    SHOW_TESTS_DELIVERED_VALUE_EVENT    : (draw_tests_delivered_value, None),
    SHOW_PEOPLE_TREATED_EVENT           : (draw_people_treated, None),
    SHOW_PEOPLE_TREATED_VALUE_EVENT     : (draw_people_treated_value, None),
    STAR0_EVENT                         : (draw_star,0),
    STAR1_EVENT                         : (draw_star,1),
    STAR2_EVENT                         : (draw_star,2),
    STAR3_EVENT                         : (draw_star,3),
    STAR4_EVENT                         : (draw_star,4),
    STAR5_EVENT                         : (draw_star,5),
    COMMENT_EVENT                       : (draw_comment, None)
    }


#------------------------------------------------------------------
#               MAIN LOOP
#------------------------------------------------------------------

draw_screen()

while True:

    for e in pygame.event.get():

        if (e.type == pygame.QUIT) or (e.type == pygame.KEYUP and e.key == pygame.K_ESCAPE):
            close_game()

        elif e.type == pygame.TEXTINPUT:
            if scanner_input == "":
                pygame.time.set_timer(INPUT_TIMEOUT_EVENT, 200, loops=1)
            scanner_input += e.text
        
        elif e.type == INPUT_TIMEOUT_EVENT:
            if scanner_input in ALL_INPUTS:
                func, args = ALL_INPUTS[scanner_input]
                func(args)
            scanner_input = ""

        elif e.type in scientific_report_events:
            func, args = scientific_report_events[e.type]
            func(args)
            
    clock.tick(REFRESH_RATE)
