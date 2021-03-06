import RPi.GPIO as GPIO
import time

SPI_CLK = 11
SPI_MOSI = 10
SPI_MISO = 9
SPI_SS = 8

CLK = SPI_CLK
Din = SPI_MOSI
Dout = SPI_MISO
CS = SPI_SS

CS_IN = GPIO.LOW
CS_OUT = GPIO.HIGH
CLK_IN = GPIO.LOW
CLK_OUT = GPIO.HIGH

def MCP3208(ch, clk=SPI_CLK, mosi=SPI_MOSI, miso=SPI_MISO, cs=SPI_SS):
  if (ch>7 or ch<0):
    return -1

  t_conv = 0
  t_data = 0

  channel = ch
  channel |= 0x18
  channel <<= 3

  GPIO.output(CS, CS_OUT)  # CS in
  GPIO.output(CLK, CLK_IN)  # CLK SGL/DIFF
  GPIO.output(CS, CS_IN)  # CS in

  for i in range(5):
    if channel & 0x80:
      GPIO.output(mosi, GPIO.HIGH)
    else:
      GPIO.output(mosi, GPIO.LOW)
    channel <<= 1

    GPIO.output(CLK, CLK_OUT) # CLK out
    GPIO.output(CLK, CLK_IN) # CLK in

  str = ""
  value = 0
  for i in range(13):
    GPIO.output(CLK, CLK_OUT)  # CLK B11 Tconv
    GPIO.output(CLK, CLK_IN)  # CLK B11 Tconv
    value <<= 1
    if i>0 and GPIO.input(miso)==GPIO.LOW:
      value |= 0x1
  GPIO.output(CS, CS_OUT) # CLK out

  return value

