# Vögelroboter quiz 

- 2024-11-24 A python-flask app to display the Vögelroboter quiz

## To Start

- click 'start_vogel.sh' on the Desktop to start the quiz server
- <a href="http://127.0.0.1:5001">Click here to run the quiz</a>
- <a href="http://127.0.0.1:5001">Click here to run the quiz</a>
- [Click here to run the quiz](http://127.0.0.1:5000)

## Installation

### Software
1. check out of github
a. Copy the SSH URL/String from the green "Code" button on top on the start page of the repository.

b. Open a terminal on your computer in the directory where you want to place the repo.
* On Linux/Mac OS: Open your Terminal app and navigate to the directory using `cd`.
* On windows: right-click inside the directory on a blank area and select "Open Git Bash here".

c. Type this command and replace `REPO` with the URL you copied in step `a`.
`git clone REPO`

2. Install python dependencies
a. In this terminal navigate into the downloaded repository into the quiz directory:
`cd vogelroboter/quiz`
b. Now run the setup script here:
`source install_python_dependencies.sh`
c. Now you have all required python modules (libraries) installed in a virtual environment inside this directory.

3. Now you can start the server:
* In development mode: `./run_server_dev.sh`
* In production mode: `./run_server_prod.sh`

### Hardware
- The quiz uses a Raspberry Pi and AdaFruit motor hat to dispense liquids.

- You need a 5 and 12 volt power supplies.
  - 5 volt 2.5 amp micro usb power supply for the Raspberry Pi 3b+
  - 12 volt 1 amp or better with a barrel connector for the pumps.
 
## Debugging

- Make sure the green light on the top of the motor hat is on. It is 
  near the network and USB ports. It is pretty obvious.

- A red light, with intermittant green, should be lit on the opposite
  side. On the Raspberry Pi near the Micro USB power connection.

- Make sure the USB power has enough current. You might get by with less
  than 2.5 Amps, but it can lead to weird issues.

- If one pump works, but not the other one, use the pump_test and use
  a multimeter to measure the voltage on the pump. Put the leads of the
  multimeter on the two connection points on the pump.

  And then test the working pump. If you get voltage on one, but not the
  other pump than consider the wiring. I am, sadly, not great with wiring, 
  and my crimps can fail and my connectors fail, and my screw terminal 
  joints fail. Not every time, but often enough to keep that in mind.


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

   - currently Chromium and start_vogel.sh auto start because of the 
     entries in this file:

     sudo vi /etc/xdg/lxsession/LXDE-pi/autostart  

   - Desktop/start_vogel.sh is a script on the desktop which you can
     click to run to restart the quiz program if something goes wrong.
     Select the first option 'Execute', not 'Execute in terminal'


## How to run manually

- The quiz is in app.py
   python -m flask run
   flask run --host=0.0.0.0 --port=5000 --reload

- in browser go to: http://127.0.0.0:5000

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
