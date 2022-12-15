from enum import Enum

class Power(Enum):
    Off = False
    On = True

class OperationMode(Enum):
    Auto = "Auto"
    Dry = "CoolDehumidifying"
    Cool = "Cooling"
    Heat = "Heating"
    Fan = "Blast"
    Nanoe = "Nanoe"
    Off = "Stop"

class AirSwingUD(Enum):
    Auto = 0
    Up = 1
    UpMid = 2
    Mid = 3
    DownMid = 4
    Down = 5

class AirSwingLR(Enum):
    Auto = -1
    Left = 0
    LeftMid = 4
    Mid = 2
    RightMid = 3
    Right = 1

# class EcoMode(Enum):
#     Auto = 0
#     Powerful = 1
#     Quiet = 2

class AirSwingAutoMode(Enum):
    Disabled = 1
    Both = 0
    AirSwingLR = 3
    AirSwingUD = 2

class FanSpeed(Enum):
    Auto = 0
    Low = 1
    LowMid = 2
    Mid = 3
    HighMid = 4
    High = 5

class dataMode(Enum):
    Day = 0
    Week = 1
    Month = 2
    Year = 4
