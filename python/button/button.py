"""
--------------------------------------------------------------------------
Button Driver
--------------------------------------------------------------------------
License:   
Copyright 2025 - Daniel Gutierrez

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this 
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, 
this list of conditions and the following disclaimer in the documentation 
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors 
may be used to endorse or promote products derived from this software without 
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE 
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, 
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
--------------------------------------------------------------------------

Button Driver

  This driver can support buttons that have either a pull up resistor between the
button and the processor pin (i.e. the input is "High" / "1" when the button is
not pressed) and will be connected to ground when the button is pressed (i.e. 
the input is "Low" / "0" when the button is pressed), or a pull down resistor 
between the button and the processor pin (i.e. the input is "Low" / "0" when the 
button is not pressed) and will be connected to power when the button is pressed
(i.e. the input is "High" / "1" when the button is pressed).

  To select the pull up configuration, press_low=True.  To select the pull down
configuration, press_low=False.
"""

import time
import Adafruit_BBIO.GPIO as GPIO

# ------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------

HIGH = GPIO.HIGH
LOW  = GPIO.LOW

# ------------------------------------------------------------------------
# Button Class
# ------------------------------------------------------------------------

class Button():
    """ Button Class """

    def __init__(self, pin=None, press_low=True, sleep_time=0.1):
        """ Initialize variables and set up the button """
        if (pin == None):
            raise ValueError("Pin not provided for Button()")
        else:
            self.pin = pin
        
        # For pull up resistor configuration:    press_low = True
        # For pull down resistor configuration:  press_low = False
        if press_low:
            self.unpressed_value = HIGH
            self.pressed_value   = LOW
        else:
            self.unpressed_value = LOW
            self.pressed_value   = HIGH
        
        self.sleep_time      = sleep_time
        self.press_duration  = 0.0        

        # Callback functions and their stored return values
        self.pressed_callback          = None
        self.pressed_callback_value    = None
        self.unpressed_callback        = None
        self.unpressed_callback_value  = None
        self.on_press_callback         = None
        self.on_press_callback_value   = None
        self.on_release_callback       = None
        self.on_release_callback_value = None

        # Initialize the hardware components        
        self._setup()
    
    # -------------------------------------------------------------------
    # Hardware Setup
    # -------------------------------------------------------------------
    def _setup(self):
        """ Setup the hardware components. """
        GPIO.setup(self.pin, GPIO.IN)
    # End def

    # -------------------------------------------------------------------
    # Button State
    # -------------------------------------------------------------------
    def is_pressed(self):
        """ Return True if button is pressed, False otherwise. """
        return GPIO.input(self.pin) == self.pressed_value
    # End def

    # -------------------------------------------------------------------
    # Wait for Press
    # -------------------------------------------------------------------
    def wait_for_press(self):
        """ Wait for the button to be pressed and released. """
        button_press_time = None
        
        # Wait while button is NOT pressed
        while(GPIO.input(self.pin) == self.unpressed_value):
            if self.unpressed_callback is not None:
                self.unpressed_callback_value = self.unpressed_callback()
            time.sleep(self.sleep_time)
            
        # Button pressed
        button_press_time = time.time()
        if self.on_press_callback is not None:
            self.on_press_callback_value = self.on_press_callback()
        
        # Wait while button IS pressed
        while(GPIO.input(self.pin) == self.pressed_value):
            if self.pressed_callback is not None:
                self.pressed_callback_value = self.pressed_callback()
            time.sleep(self.sleep_time)
        
        # Button released
        self.press_duration = time.time() - button_press_time
        if self.on_release_callback is not None:
            self.on_release_callback_value = self.on_release_callback()
    # End def
    
    # -------------------------------------------------------------------
    # Helper Functions
    # -------------------------------------------------------------------
    def get_last_press_duration(self):
        """ Return the last press duration """
        return self.press_duration
    
    def cleanup(self):
        """ Clean up the button hardware. """
        GPIO.cleanup()
    # End def
    
    # -------------------------------------------------------------------
    # Callback Functions
    # -------------------------------------------------------------------
    def set_pressed_callback(self, function):
        self.pressed_callback = function
    
    def get_pressed_callback_value(self):
        return self.pressed_callback_value
    
    def set_unpressed_callback(self, function):
        self.unpressed_callback = function
    
    def get_unpressed_callback_value(self):
        return self.unpressed_callback_value
    
    def set_on_press_callback(self, function):
        self.on_press_callback = function
    
    def get_on_press_callback_value(self):
        return self.on_press_callback_value
    
    def set_on_release_callback(self, function):
        self.on_release_callback = function
    
    def get_on_release_callback_value(self):
        return self.on_release_callback_value
# End class


# ------------------------------------------------------------------------
# Main Script
# ------------------------------------------------------------------------
if __name__ == '__main__':

    print("Button Test")

    # Create instance for button on P2_2
    button = Button("P2_2", press_low=True)
    
    # Define callback test functions
    def pressed():
        print("  Button pressed")
    
    def unpressed():
        print("  Button not pressed")
    
    def on_press():
        print("  On Button press")
        return 3
    
    def on_release():
        print("  On Button release")
        return 4

    # Test
    try:
        print("Is the button pressed?")
        print("    {0}".format(button.is_pressed()))

        print("Press and hold the button.")
        time.sleep(4)
        
        print("Is the button pressed?")
        print("    {0}".format(button.is_pressed()))
        
        print("Release the button.")
        time.sleep(4)
        
        print("Waiting for button press ...")
        button.wait_for_press()
        print("    Button pressed for {0} seconds.".format(button.get_last_press_duration()))        
        time.sleep(4)

        print("Setting callback functions ... ")
        button.set_pressed_callback(pressed)
        button.set_unpressed_callback(unpressed)
        button.set_on_press_callback(on_press)
        button.set_on_release_callback(on_release)
        
        print("Waiting for button press with callback functions ...")
        value = button.wait_for_press()
        print("    Button pressed for {0} seconds.".format(button.get_last_press_duration()))
        print("    Button pressed callback return value    = {0}".format(button.get_pressed_callback_value()))
        print("    Button unpressed callback return value  = {0}".format(button.get_unpressed_callback_value()))
        print("    Button on press callback return value   = {0}".format(button.get_on_press_callback_value()))
        print("    Button on release callback return value = {0}".format(button.get_on_release_callback_value()))
        
    except KeyboardInterrupt:
        pass

    button.cleanup()
    print("Test Complete")
