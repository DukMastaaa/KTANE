# Countdown Timer
TIME_STEP = 0.1

# Bomb
STRIKE_LIMIT = 3
STRIKE_TO_COUNTDOWN_SPEED = {
    0: 1,
    1: 1.25,
    2: 1.5
}

# Global Module View
VIEW_MODULES_WIDTH = 5  # How many modules fit in width of BombView
VIEW_MODULES_HEIGHT = 3  # How many modules fit in height of BombView

# Module Views
MODULE_WIDTH = 200
MODULE_HEIGHT = 200
MODULE_BG = "gray"
MODULE_LED_DIAMETER = 20
MODULE_LED_PAD = 5
MODULE_LED_NEUTRAL = "white"
MODULE_LED_SOLVED = "green"
MODULE_LED_WRONG = "red"

# Edgework View
pass

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

# Batteries
BAT_AA = "AA"
BAT_D = "D"
BATTERIES = [BAT_AA, BAT_D]

# Ports
PRT_DVID = "DVI-D"
PRT_PARA = "PARALLEL"
PRT_PS2 = "PS/2"
PRT_RJ45 = "RJ-45"
PRT_SRL = "SERIAL"
PRT_RCA = "RCA"
PORTS = [PRT_DVID, PRT_PARA, PRT_PS2, PRT_RJ45, PRT_SRL, PRT_RCA]

# Serial
ALPHA = "ABCDEFGHIJKLMNOPQRSTUVWXZ"  # "Y" omitted
NUMER = "0123456789"

# Colours
COL_RED = "red"
COL_BLUE = "blue"
COL_BLACK = "black"
COL_YELLOW = "yellow"
COL_GREEN = "green"
COL_WHITE = "white"
