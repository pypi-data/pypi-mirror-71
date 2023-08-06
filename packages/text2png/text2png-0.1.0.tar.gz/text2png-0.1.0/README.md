# Text to Image (Text to PNG)

<badges>[![version](https://img.shields.io/pypi/v/text2png.svg)](https://pypi.org/project/text2png/)
[![license](https://img.shields.io/pypi/l/text2png.svg)](https://pypi.org/project/text2png/)
[![pyversions](https://img.shields.io/pypi/pyversions/text2png.svg)](https://pypi.org/project/text2png/)  
[![donate](https://img.shields.io/badge/Donate-Paypal-0070ba.svg)](https://paypal.me/foxe6)
[![powered](https://img.shields.io/badge/Powered%20by-UTF8-red.svg)](https://paypal.me/foxe6)
[![made](https://img.shields.io/badge/Made%20with-PyCharm-red.svg)](https://paypal.me/foxe6)
</badges>

<i>Easiest way to create text thumbnail.</i>

# Hierarchy

```
text2png
'---- TextToPng()
    '---- create()
```

# Example

## python
```python
from text2png import *


t2p = TextToPng(
    # absolute path to font file
    font_file="C:\\Windows\\Fonts\\msgothic.ttc",
    # font size, integer    
    font_size=64,
    # background color, RGB value
    background_color=(0, 0, 0),
    # text color, RGB value
    text_color=(255, 255, 255),
    # png file save directory
    save_dir="C:\\Temp"
)
print(
    t2p.create(
        # what text
        text="HELLO",
        # text padding, in pixels
        padding=15,
        # file name
        filename="hello.png"
    )
)
# C:\\Temp\\hello.png
```
