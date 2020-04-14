#!/usr/bin/python

# RPiHUB-75E - Driving a HUB-75E 64x32 LED Matrix Animation
# Copyright (C) 2016 Jason Birch
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

#/****************************************************************************/
#/* RPiHUB-75E - Driving a HUB-75E 64x32 LED Matrix Animation.               */
#/* ------------------------------------------------------------------------ */
#/* V1.00 - 2020-04-14 - Jason Birch                                         */
#/* ------------------------------------------------------------------------ */
#/* Python example to directly drive a HUB-75E 64x32 LED Matrix and display  */
#/* an animated image.                                                       */
#/****************************************************************************/


import time
import random
import pygame
import RPi.GPIO


# GPIO pin assignments.
HUB75E_R1 = 14
HUB75E_G1 = 15
HUB75E_B1 = 18
HUB75E_R2 = 23
HUB75E_G2 = 24
HUB75E_B2 = 25
# HUB75E_E = 8
HUB75E_A = 7
HUB75E_B = 12
HUB75E_C = 16
HUB75E_D = 20
HUB75E_CLK = 21
HUB75E_LAT = 26
HUB75E_OE = 19

# Display properties.
RED = 0
GREEN = 1
BLUE = 2
FRAME_REPEAT = 5
DISPLAY_FRAMES = 4
DISPLAY_COLS = 64
DISPLAY_ROWS = 32


# PyGame used to read image files from storage.
pygame.init()

# Configure GPIO pins.
RPi.GPIO.setwarnings(False)
RPi.GPIO.setmode(RPi.GPIO.BCM)
RPi.GPIO.setup(HUB75E_R1, RPi.GPIO.OUT, initial=0)
RPi.GPIO.setup(HUB75E_G1, RPi.GPIO.OUT, initial=0)
RPi.GPIO.setup(HUB75E_B1, RPi.GPIO.OUT, initial=0)
RPi.GPIO.setup(HUB75E_R2, RPi.GPIO.OUT, initial=0)
RPi.GPIO.setup(HUB75E_G2, RPi.GPIO.OUT, initial=0)
RPi.GPIO.setup(HUB75E_B2, RPi.GPIO.OUT, initial=0)
# RPi.GPIO.setup(HUB75E_E, RPi.GPIO.OUT, initial=0)
RPi.GPIO.setup(HUB75E_A, RPi.GPIO.OUT, initial=0)
RPi.GPIO.setup(HUB75E_B, RPi.GPIO.OUT, initial=0)
RPi.GPIO.setup(HUB75E_C, RPi.GPIO.OUT, initial=0)
RPi.GPIO.setup(HUB75E_D, RPi.GPIO.OUT, initial=0)
RPi.GPIO.setup(HUB75E_CLK, RPi.GPIO.OUT, initial=0)
RPi.GPIO.setup(HUB75E_LAT, RPi.GPIO.OUT, initial=0)
RPi.GPIO.setup(HUB75E_OE, RPi.GPIO.OUT, initial=1)

# Load animation image files.
FrameImage = []
FrameImage.append(pygame.image.load("FrameImage1.png"))
FrameImage.append(pygame.image.load("FrameImage2.png"))
FrameImage.append(pygame.image.load("FrameImage3.png"))
FrameImage.append(pygame.image.load("FrameImage4.png"))

# Load a display frames from images.
DisplayImage = []
for Frame in range(DISPLAY_FRAMES):
   DisplayImage.append([])
   for Row in range(DISPLAY_ROWS):
      DisplayImage[Frame].append([])
      for Col in range(DISPLAY_COLS):
         DisplayImage[Frame][Row].append([])
         ColourValue = FrameImage[Frame].get_at((Col, Row))
         DisplayImage[Frame][Row][Col].append(ColourValue[0] & 0x80)
         DisplayImage[Frame][Row][Col].append(ColourValue[1] & 0x80)
         DisplayImage[Frame][Row][Col].append(ColourValue[2] & 0x80)

# Loop forever.
Frame = 0
FrameDirection = 1
FrameRepeat = FRAME_REPEAT
while True:
   # Animate display frames.
   FrameRepeat -= 1
   if FrameRepeat < 1:
      FrameRepeat = FRAME_REPEAT
      Frame += FrameDirection
      if Frame < 1 or Frame >= DISPLAY_FRAMES - 1:
         FrameDirection *= -1

   # Update LED Matrix.
   for Row in range(DISPLAY_ROWS / 2):
      # Select row to dispaly.
      RPi.GPIO.output(HUB75E_A, Row & 1)
      RPi.GPIO.output(HUB75E_B, Row & 2)
      RPi.GPIO.output(HUB75E_C, Row & 4)
      RPi.GPIO.output(HUB75E_D, Row & 8)
#      RPi.GPIO.output(HUB75E_E, Row & 16)

      SelRow = Row + 1
      if SelRow > (DISPLAY_ROWS / 2) - 1:
         SelRow = 0
      for Col in range(DISPLAY_COLS):
         # Load bits into top row set.
         RPi.GPIO.output(HUB75E_R1, DisplayImage[Frame][SelRow][Col][RED])
         RPi.GPIO.output(HUB75E_G1, DisplayImage[Frame][SelRow][Col][GREEN])
         RPi.GPIO.output(HUB75E_B1, DisplayImage[Frame][SelRow][Col][BLUE])

         # Load bits into bottom row set.
         RPi.GPIO.output(HUB75E_R2, DisplayImage[Frame][SelRow + 16][Col][RED])
         RPi.GPIO.output(HUB75E_G2, DisplayImage[Frame][SelRow + 16][Col][GREEN])
         RPi.GPIO.output(HUB75E_B2, DisplayImage[Frame][SelRow + 16][Col][BLUE])

         # While clocking in new bit data.
         # Refresh existing display data on the current output row.
         RPi.GPIO.output(HUB75E_OE, 0)
         RPi.GPIO.output(HUB75E_CLK, 1)
         RPi.GPIO.output(HUB75E_OE, 1)
         RPi.GPIO.output(HUB75E_CLK, 0)

      # When a pair of rows of display bits has been loaded.
      # Latch the data into the output buffer.
      RPi.GPIO.output(HUB75E_LAT, 1)
      RPi.GPIO.output(HUB75E_LAT, 0)

