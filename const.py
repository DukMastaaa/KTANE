# Countdown Timer
TIME_STEP = 0.1

# Bomb
STRIKE_LIMIT = 3
STRIKE_TO_COUNTDOWN_SPEED = {
    0: 1,
    1: 1.25,
    2: 1.5
}
DEFAULT_TIME_LIMIT = 60 * 5

# Module Views
MODULE_BORDER_WIDTH = 1
MODULE_BORDER_COLOUR = "black"
MODULE_WIDTH = 200
MODULE_HEIGHT = 200
MODULE_BG = "gray"
MODULE_LED_DIAMETER = 20
MODULE_LED_PAD = 20
MODULE_LED_NEUTRAL = "white"
MODULE_LED_SOLVED = "green"
MODULE_LED_WRONG = "red"

# Global Module View
VIEW_MODULES_WIDTH = 4  # How many modules fit in width of BombView
VIEW_MODULES_HEIGHT = 3  # How many modules fit in height of BombView
VIEW_MODULES_PX_WIDTH = (MODULE_WIDTH + MODULE_BORDER_WIDTH) * VIEW_MODULES_WIDTH
VIEW_MODULES_PX_HEIGHT = (MODULE_HEIGHT + MODULE_BORDER_WIDTH) * VIEW_MODULES_HEIGHT + 10

# Edgework View
EVIEW_FONT_TIMER_STRIKES = ("Courier", 20)
EVIEW_WIDTH = 300

# App
# todo: `APP_GEOMETRY` definition subject to change if UI changes
APP_GEOMETRY = f"{VIEW_MODULES_PX_WIDTH+EVIEW_WIDTH}x{VIEW_MODULES_PX_HEIGHT}"

# Indicators
IND_ON = True
IND_OFF = False
IND_SND = "SND"
IND_CLR = "CLR"
IND_CAR = "CAR"
IND_IND = "IND"
IND_FRQ = "FRQ"
IND_SIG = "SIG"
IND_NSA = "NSA"
IND_MSA = "MSA"
IND_TRN = "TRN"
IND_BOB = "BOB"
IND_FRK = "FRK"
INDICATORS = [IND_SND, IND_CLR, IND_CAR, IND_IND, IND_FRK, IND_SIG, IND_NSA, IND_MSA,
              IND_TRN, IND_BOB, IND_FRK]

# Indicator Label
LIT_CIRCLE = "●"
UNLIT_CIRCLE = "○"
INDICATOR_BG = "dim gray"
INDICATOR_FG = "white"
INDICATOR_FONT = ("Courier", 20)

# Batteries
BAT_AA = "AA"
BAT_D = "D"
BATTERIES = [BAT_AA, BAT_D]

# Battery Label
pass

# Ports
PRT_DVID = "DVI-D"
PRT_PARA = "PARALLEL"
PRT_PS2 = "PS/2"
PRT_RJ45 = "RJ-45"
PRT_SRL = "SERIAL"
PRT_RCA = "RCA"
PORTS = [PRT_DVID, PRT_PARA, PRT_PS2, PRT_RJ45, PRT_SRL, PRT_RCA]

# Port Label
pass

# Serial
ALPHA = "ABCDEFGHIJKLMNOPQRSTUVWXZ"  # "Y" omitted
NUMER = "0123456789"

# Serial Label
SERIAL_FONT = ("Courier", 20)
SERIAL_BG = "dim gray"
SERIAL_FG = "white"

# Colours
COL_RED = "red"
COL_BLUE = "blue"
COL_BLACK = "black"
COL_YELLOW = "yellow"
COL_GREEN = "green"
COL_WHITE = "white"

# tkinter event bindings
BIND_LEFT_PRESS = "<ButtonPress-1>"
BIND_LEFT_RELEASE = "<ButtonRelease-1>"
