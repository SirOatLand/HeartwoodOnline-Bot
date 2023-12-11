# Heartwood Online Farming Bot
## Overview

#### This project is a farming bot designed for the game Heartwood Online. It automates the resource gathering process by scanning screenshots, processing images, and performing in-game actions accordingly.

## Features

* Resource Gathering: The bot gathers resources like coal and tin by scanning screenshots of the game environment.
* Image Processing: Utilizes the **Win32** library to capture screenshots and **OpenCV2** for image processing. Implements HSV filtering and needle image matching techniques.
* Target Identification: Identifies targets by scanning for matching images and calculates the nearest target for gathering.
* Character Movement: Uses the **Keyboard** library to move the character towards the identified target.
* Distance Calculation: Determines the distance between the character and the target, initiating resource gathering when in close enough proximity.
