# Write your code here :-) SLAAAAAAAAAAAAVEEEEEEE
import board
import busio
import time
import digitalio
import adafruit_ssd1306

# CONSTANTS

TIMEOUT = 1.005


# set up hc05 module
slave_hc05 = busio.UART(board.GP16, board.GP17, baudrate=9600)

# set up internal led
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

# set up oled display
i2c = busio.I2C(board.GP19, board.GP18)
oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)


def sendCMD_waitResp(cmd, uart=slave_hc05, timeout=TIMEOUT):
    print("CMD: " + cmd)
    uart.write(cmd)
    waitResp(uart, timeout)
    print()



def waitResp(uart = slave_hc05, timeout=TIMEOUT):
    """
    Waits for a response from the UART device within a specified timeout.

    Args:
        uart (object): The UART object to read from. Default is `slave_hc05`.
        timeout (int): The timeout value in milliseconds. Default is 2000.

    Returns:
        bytes: The response received from the UART device.

    """
    prvMills = time.monotonic()
    
    resp = b""

    while (time.monotonic() - prvMills) < timeout:
        # print(time.monotonic() - prvMills)
        res = uart.read(11)  
        if len(res) >0:
            resp = b"".join([resp, res])
        return resp  
    
    

while True:
    bef = None
    res = waitResp(slave_hc05, timeout=TIMEOUT)
    print(f'response:{res}')

    # clear oled if different resp from before
    if len(str(res)[2:-5:]) != bef:
        bef = len(str(res)[2:-5:])
        # oled.fill(0)
        # oled.show()
    # show text if text
    if len(str(res)[2:-5:]) > 0:
        print(str(res)[2:-5:])
        # oled.text(str(res)[2:-5:], 10, 10, 1)
        # oled.show()
