import cv2
import keyboard

from cvzone.HandTrackingModule import HandDetector

from button import Button
from misc import Display, ClearButton, CalculationButtons, ResultDisplay, Fingers, Delay

# Web kamerası
cap = cv2.VideoCapture(0)
cap.set(3, Display.DISPLAY_DIMENSIONS[0])  # width
cap.set(4, Display.DISPLAY_DIMENSIONS[1])  # height
detector = HandDetector(detectionCon=0.5, maxHands=1)

CALCULATION_BUTTONS_LIST = []
for x_distance in range(len(CalculationButtons.BUTTON_VALUES_LIST)):  # Since we have 4 x 4 grid
    for y_distance in range(len(CalculationButtons.BUTTON_VALUES_LIST)):
        x_position = x_distance * Display.MAIN_BUTTON_SIZE + Display.MAIN_X_OFFSET
        y_position = y_distance * Display.MAIN_BUTTON_SIZE + Display.MAIN_Y_OFFSET
        CALCULATION_BUTTONS_LIST.append(
            Button(position=(x_position, y_position),
                   width=Display.MAIN_BUTTON_SIZE,
                   height=Display.MAIN_BUTTON_SIZE,
                   value=CalculationButtons.BUTTON_VALUES_LIST[y_distance][x_distance]
                   )
        )
clear_button = Button(position=(Display.MAIN_X_OFFSET + Display.MAIN_BUTTON_SIZE *
                                (len(CalculationButtons.BUTTON_VALUES_LIST) - 1), Display.MAIN_BUTTON_SIZE),
                      width=Display.MAIN_BUTTON_SIZE, height=Display.MAIN_BUTTON_SIZE, value=ClearButton.START_VALUE)

# Variables
EQUATION = ResultDisplay.START_VALUE
DELAY_COUNTER = 0
CALCULATION = True

BEGINNING_OF_EQUALITY = ''

# Loop
while True:
    success, img = cap.read()
    img = cv2.flip(src=img, flipCode=1)

    hands, img = detector.findHands(img=img, flipType=False)

    cv2.rectangle(img=img,
                  pt1=(Display.MAIN_X_OFFSET, Display.MAIN_BUTTON_SIZE),
                  pt2=(
                    Display.MAIN_X_OFFSET + Display.MAIN_BUTTON_SIZE * (len(CalculationButtons.BUTTON_VALUES_LIST) - 1),
                    Display.MAIN_Y_OFFSET + Display.MAIN_BUTTON_SIZE
                  ),
                  color=ResultDisplay.BUTTON_COLOR,
                  thickness=cv2.FILLED
                  )
    cv2.rectangle(img=img,
                  pt1=(Display.MAIN_X_OFFSET,
                       Display.MAIN_BUTTON_SIZE),
                  pt2=(
                    Display.MAIN_X_OFFSET + Display.MAIN_BUTTON_SIZE * (len(CalculationButtons.BUTTON_VALUES_LIST) - 1),
                    Display.MAIN_Y_OFFSET + Display.MAIN_BUTTON_SIZE
                  ),
                  color=ResultDisplay.MAIN_BORDER_COLOR,
                  thickness=Display.MAIN_THICKNESS
                  )

    # Tüm düğmeleri çiz    
    for button in CALCULATION_BUTTONS_LIST:
        button.draw_button(img=img,
                           rectangle_color=CalculationButtons.BUTTON_COLOR,
                           text_color=CalculationButtons.TEXT_COLOR,
                           font_scale=CalculationButtons.MAIN_FONT_SCALE,
                           thickness=CalculationButtons.THICKNESS
                           )
    clear_button.draw_button(img=img,
                             rectangle_color=ClearButton.BUTTON_COLOR,
                             text_x_margin=-ClearButton.X_MARGIN,
                             text_color=ClearButton.TEXT_COLOR,
                             font_scale=ClearButton.MAIN_FONT_SCALE,
                             thickness=ClearButton.THICKNESS
                             )

    # Elini kontrol et    
    if hands:
        lm_list = hands[0]['lmList']  # landmark list
        length, _, img = detector.findDistance(p1=lm_list[Fingers.FINGER_TIP_1][0:2],
                                               p2=lm_list[Fingers.FINGER_TIP_2][0:2],
                                               img=img
                                               )
        x, y = lm_list[Fingers.FINGER_TIP_1][0:2]
        if length < Fingers.CRITICAL_FINGERS_DISTANCE:

            if clear_button.check_click(x=x, y=y, img=img,
                                        rectangle_color=ClearButton.CHECK_BUTTON_COLOR,
                                        text_x_margin=-ClearButton.X_MARGIN,
                                        text_color=ClearButton.CHECK_TEXT_COLOR,
                                        thickness=ClearButton.CHECK_THICKNESS) \
                    and DELAY_COUNTER == 0:
                EQUATION = ResultDisplay.START_VALUE
                CALCULATION = True

            for index, button in enumerate(CALCULATION_BUTTONS_LIST):
                if button.check_click(x=x, y=y, img=img,
                                      rectangle_color=CalculationButtons.CHECK_BUTTON_COLOR,
                                      text_color=CalculationButtons.CHECK_TEXT_COLOR,
                                      thickness=CalculationButtons.CHECK_THICKNESS) \
                        and DELAY_COUNTER == 0:
                    
                    #mevcut değerin alınması
                    current_value = CalculationButtons.BUTTON_VALUES_LIST[
                        int(index % len(CalculationButtons.BUTTON_VALUES_LIST))
                    ][
                        int(index / len(CalculationButtons.BUTTON_VALUES_LIST))
                    ]
                    if current_value == '=':
                        try:
                            EQUATION = BEGINNING_OF_EQUALITY + EQUATION
                            BEGINNING_OF_EQUALITY = ''
                            EQUATION = str(round(eval(EQUATION.replace('x', '*')), 3))
                        except (SyntaxError, NameError, ZeroDivisionError):
                            EQUATION = Display.EXCEPTION_MESSAGE
                            CALCULATION = True
                    else:
                        if CALCULATION: 
                            EQUATION = ''
                            CALCULATION = False
                        
                        EQUATION += current_value

                        if len(EQUATION) > Display.MAX_NUM_OF_CHARACTERS:
                            BEGINNING_OF_EQUALITY += EQUATION[0]
                            EQUATION = EQUATION[1:]
                    DELAY_COUNTER = 1

    # Tekrarlardan kaçının (gecikme)
    if DELAY_COUNTER != 0:
        DELAY_COUNTER += 1
        if DELAY_COUNTER > Delay.MAX_DELAY:
            DELAY_COUNTER = 0

    
    text_size = cv2.getTextSize(text=EQUATION, fontFace=ResultDisplay.MAIN_FONT,
                                fontScale=ResultDisplay.FONT_SCALE, thickness=ResultDisplay.THICKNESS
                                )
    text_y = int(Display.MAIN_Y_OFFSET - Display.MAIN_BUTTON_SIZE / 2 + text_size[1])  # Centering position
    cv2.putText(img=img, text=EQUATION, org=(Display.MAIN_X_OFFSET + ResultDisplay.X_MARGIN, text_y),
                fontFace=ResultDisplay.MAIN_FONT, fontScale=ResultDisplay.FONT_SCALE,
                color=ResultDisplay.TEXT_COLOR, thickness=ResultDisplay.THICKNESS)

    
    cv2.imshow(winname=Display.WIN_NAME, mat=img)
    cv2.waitKey(1)

    # Exit
    if keyboard.is_pressed('esc'):
        break

cv2.destroyAllWindows()
