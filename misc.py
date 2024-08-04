import cv2


class Display:
    DISPLAY_DIMENSIONS = (1280, 720)

    MAIN_BUTTON_SIZE = 75
    MAIN_X_OFFSET = 700  
    MAIN_Y_OFFSET = 150 
    MAIN_BORDER_COLOR = (50, 50, 50)
    MAIN_THICKNESS = 3
    MAIN_FONT_SCALE = 2
    MAIN_CLICKED_FONT_SCALE = 2.5
    MAIN_FONT = cv2.FONT_HERSHEY_PLAIN

    MAX_NUM_OF_CHARACTERS = 7

    EXCEPTION_MESSAGE = 'Error'
    WIN_NAME = 'Finger Movement Calculator'


class Fingers:
    FINGER_TIP_1 = 8   
    FINGER_TIP_2 = 12  
    CRITICAL_FINGERS_DISTANCE = 50


class CalculationButtons(Display):
    BUTTON_VALUES_LIST = [
        ['7', '8', '9', 'x'],
        ['4', '5', '6', '-'],
        ['1', '2', '3', '+'],
        ['0', '.', '/', '='],
    ]
    BUTTON_COLOR = (64, 64, 64)
    TEXT_COLOR = (255, 255, 255)
    CHECK_BUTTON_COLOR = (147, 142, 142)
    CHECK_TEXT_COLOR = (50, 50, 50)
    THICKNESS = 2
    CHECK_THICKNESS = 3


class ClearButton(Display):
    START_VALUE = 'AC'
    BUTTON_COLOR = (194, 190, 189)
    TEXT_COLOR = (50, 50, 50)
    X_MARGIN = 10
    CHECK_BUTTON_COLOR = (204, 199, 199)
    CHECK_TEXT_COLOR = (50, 50, 50)
    THICKNESS = 2
    CHECK_THICKNESS = 3


class ResultDisplay(ClearButton):
    START_VALUE = '0'
    FONT_SCALE = 1.2
    THICKNESS = 2
    MAIN_FONT = cv2.FONT_HERSHEY_DUPLEX


class Delay:
    MAX_DELAY = 10