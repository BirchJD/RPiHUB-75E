RPiHUB-75E
==========

YouTube Video: https://www.youtube.com/watch?v=mw-ZLyynL9E

This Python script will directly drive a 64x32 LED Matrix board which has a HUB-75E communication connector. The power for the LEDs on the matrix board is supplied on a seperate connecter, on the board I am using the LED power supply is 5V. The HUB-75E communication connector is a standard and layed out as follows:

  Pin 1
    |
    v--
 R1|o o|G1
 B1|o o|GND
 R2|o o|G2
 B2|o o|E
  A|o o|B
  C|o o|D
CLK|o o|LAT
 OE|o o|GND
    ---


                                COL 0-63
              <------------------------------------------>

              --------------------------------------------
           A |............................................|
ROW 0-15   | |............................................|
ADDR: DCBA | |............................................|
[R1,G1,B1] | |............................................|
           V |............................................|
           A |............................................|
ROW 16-31  | |............................................|
ADDR: DCBA | |............................................|
[R2,G2,B2] | |............................................|
           v |............................................|
              --------------------------------------------


The display is split into upper and lower halves. The pins [R1,G1,B1] provide the red, green and blue colour for the upper half of the display. The pins [R2,G2,B2] provide the red, green and blue colour for the lower half of the display. The colour bits are shifted into the currently selected row with each clock pulse on CLK. The currently selected row is addressed with pins, E, D, C, B and A. When a complete row has been shifted in, the data is then latched into the output buffer with a clock pulse on the LAT pin. The output buffer for the currently selected row can be displayed by taking the output enable pin, OE, low and providing a clock pulse each side of raising the output enable pin again.

The display can display upto eight colours by arranging the R, G and B pins high or low for each pixel.


