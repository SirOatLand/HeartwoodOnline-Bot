# Heartwood Online Farming Bot
## Overview

#### This project is a farming bot designed for the game Heartwood Online. It automates the resource gathering process by scanning screenshots, processing images, and performing in-game actions accordingly.

## Features

* Resource Gathering: The bot gathers resources like coal and tin by scanning screenshots of the game environment.
* Image Processing: Utilizes the **Win32** library to capture screenshots and **OpenCV2** for image processing. Implements HSV filtering and needle image matching techniques.
* Target Identification: Identifies targets by scanning for matching images and calculates the nearest target for gathering.
* Character Movement: Uses the **Keyboard** library to move the character towards the identified target.
* Distance Calculation: Determines the distance between the character and the target, initiating resource gathering when in close enough proximity.

**P.S.** This project is not intended for abusive and exploitative purposes. It is just a proof of concept and therefore the effectiveness of the bot is limited.  

## Basic Usages

* Run the game in 1024x768 resolution.
* With the game running, executes main.py.
* A window of the program's vision should popup and your keyboard and/or mouse will be controlled.

## Basic Configurations

#### Unfortunately this project does not include UI for the bot's behavior configuration nor am I planning to include one, so the editing the code directly is the only way.

### These are the changes you can make inside main.py

* needles - This is the image that the program uses to search for ingame, in this project it includes:
    * coal_needles
    * tin_needles
    * copper_needles
    * hp_needles (for mob detections)
* hsvfilter - This is a filter that makes the detection more accurate and the needle and hsv selected should match. For example, "needles = coal_needles" then "hsvfilter = hsvfilter_coal". (for mob detection use hsvfilter_none)
* threshold - This is the change to the how accurate the detected object should match the needle to be recognized. Try increasing this value if unrelated objects are being detected, or decrease it if targeted objects are not being recognized.

#### NOTE - To use a mob detector, equip a range weapon and stands in the middle of the spawning area (preferably but not mandatory somewhere with an object on top of your head such as ores or trees, to prevent mob from hiding behind your own health bar and become undetectable).    
