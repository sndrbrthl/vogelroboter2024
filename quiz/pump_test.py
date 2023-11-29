import pdb

import sys
from hellodrinkbot import HelloDrinkbot
try:
    hd= HelloDrinkbot()
    EMULATION=0
except:
    EMULATION=1
    print('Motor initialization failed')


pump = int(sys.argv[1])
sec = int(sys.argv[2])
print('dispenseing pump {pump} for {sec} seconds')

hd.dispense(pump, sec) 
