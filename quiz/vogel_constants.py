# Constants, feel free to adjust these
NUM_ANSWERS=3 # how many birds are shown as possible answers
NUM_ROUNDS=3  # how many birds you are shown

# Calibration - I ran each pump several times and measured
# the amount pumped and calculated the number of seconds to dispense 1 ml
# I don't think these are totally stable. Adjust as needed.
AVENO_PUMP = 0 # Pump number for the Aveno
LEMON_PUMP = 2 # Pump number for the Lemon
AVENO_SIZE = 4 # ml
AVENO_SEC_ML = .81
AVENO_TIME = round(AVENO_SIZE * AVENO_SEC_ML)
LEMON_SIZE = 1.2 # ml
LEMON_SEC_ML = .91
LEMON_TIME = round(LEMON_SIZE * LEMON_SEC_ML)
