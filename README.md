# RockPro64 Cooling Fan Controller

Python script to control fan on a Pine64 RockPro64 single board computer. Useful on LibreELEC.

## Installation

```mkdir fan_controller```
```wget https://raw.githubusercontent.com/kromsam/FanControlerRockPro64/master/fan_controller.py -O fan_controller/fan_controller.py```
```python fan_controller/fan_controller.py```

## Usage

### Automatic mode

Enables fan if temperature is between tempMax = 70 and tempMin = 35 where tempMax is 100% fan speed and tempMin is 23%.

#### Configuration

Set up a cronjob (updates every minute in this example).
```
*/1 * * * * python fan_controller/fan_controller.py
```

### Static mode

Static fan speed to desired strengh 0-100:

```
python fan_controller/fan_controller.py force 90
```
