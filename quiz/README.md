# Vögelroboter quiz 

- 2024-11-24 A python-flask app to display the Vögelroboter quiz


## Installation

- check out of github
- install requirements

    pip install -r requirements.txt

- The quiz uses a Raspberry Pi and AdaFruit motor hat to dispense liquids.

## Configuration

   - the file vogelroboter/constants/vogel_constants.py controls the
     pumps that are in use, the time they are run for each ingredient,
     the number of possible birds in an answer (3), and the number of 
     rounds of questions that you get (4). 

     If you have figured out how to do a git pull (see below) you can
     edit this file in github.

     If you can't edit in github let me (Rich) know so that I can add
     you (whoever you are :-) to the repository. Or, if you know what
     you are doing, you can fork the repository.

## Network

   - Click the wifi icon in the upper right, between the volume control and 
     the Blue tooth icon to connect to the internet. This is only needed
     if you want to update the quiz program.

## Updating vogelroboter

   - log into the Raspberry pi (this is currently automatic)
   - start a terminal session (click on the black terminal looking icon 
     on the top menu bar)
   - Run git pull
     cd vogelroboter

## Autostart

   - currently Chromium auto starts because of the entries in this file:
     sudo vi /etc/xdg/lxsession/LXDE-pi/autostart  
   - Desktop/start_vogel.sh is a script on the desktop which starts 
     in .bashrc. This is suboptimal.

   - Whenever you start a terminal it will run the script. It will usually
     fail because the address and port are already in use. Press enter
     to get past this error screen (unless I fix it :-)

# TODO: auto start start_vogel.sh in /etc/rc.local, or ?
 

## How to run

- The quiz is in app.py
   python -m flask run
   flask run --host=0.0.0.0 --port=5000 --reload

- in browser: http://127.0.0.0:5000

## Testing pumps

   - To make sure the pumps are working, you can run the pump_test.py
     program.
   - open a terminal
     cd vogelroboter/quiz
     python ./pumptest <pump number> <time in seconds>
   - You should be using pumps 0 and 2. Which are connected to the first
     and fourth pins on the header on the Raspberry Pi. With the HDMI port
     facing you, connection 0 (first pin) is the far left. Conection 3 is 
     the fourth screw terminal. 
