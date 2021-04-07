# hvac_controller.py
# By: Adam Kraft

class HVAC_Controller:

    def __init__(self, rx, tx):
        self._rx = rx
        self._tx = tx
        self.mode = None
        self._temp = None
        self.fan  = None
        self._modes = {
            "OFF"    :  0,
            "COOL"   :  1,
            "DRY"    :  2,
            "HEAT"   :  3,
            "RESEND" : -1
        }
        self._fan_speeds = {
            "AUTO" : 0,
            "LOW"  : 1,
            "HIGH" : 2
        }

    def send(self, temp, mode, fan):
        """ Send command to slave """
        # Check for updated commands
        if temp != self._temp or mode != self.mode or fan != self.fan or mode == "RESEND":
            # Send the command
            if mode == "RESEND":
                self._send(self._temp, self.mode, self.fan)
            else:
                self._send(temp, mode, fan)

    def _send(self):
        pass
