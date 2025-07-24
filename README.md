# GOAL
The goal of this project is to build my own ipod classic style mp3 player. UI is heavily based on ipod ver. 1.3 for the ipod classic 5th gen, with some nice quality of life updates and features from later classics. 

## Base parts needed for this project
  - Raspberry Pi Zero 2 (Any seller)
  - [240x320 SPI display](https://www.pishop.us/product/240-320-general-2inch-ips-lcd-display-module/) - I used this one
  - [Cirque TM040040 Trackpad](https://www.mouser.com/c/?marcom=118816186) - Be careful to buy the correct one, 40mm flat overlay

## Parts for the future
  - DAC (Yet to decide)
  - Battery (Yet to decide on capacity)
  - Connector Port (USB-C)
  - Likely other parts I have not thought of yet

### [Building Guide](https://docs.google.com/document/d/1XwhfeOkbN93wCHk-AwTpOQk8uyo2gPRMQpYmsx6mDbI/edit?usp=sharing)

## Development Stages

Step 0: <-- Currently here
  - Functional UI
  - Get Pi Zero connected to screen and trackpad

Step 1:
  - Get UI working on Pi Zero
  - Temporary development case
    
Step 2:
  - Find way get into memory of Pi Zero from USB-C Connector

Step 3:
  - Battery
  - Battery charge controller
  - Battery level sensor
    
Step 4:
  - DAC

Step 5:
  - Proper Case

### Future Propects
  - Video Player
    - Composite video out like 5th gen classic
  - Refactor Code to C++

## Special Thanks
- Apple for the original ipod
- Rockbox team for the insperation for a lot of features
