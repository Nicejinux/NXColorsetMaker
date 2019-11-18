![License](https://img.shields.io/badge/license-MIT-yellow.svg)
![Python](https://img.shields.io/badge/Python-3.7-green.svg)
![Xcode](https://img.shields.io/badge/Xcode-9%20or%20higher-blue.svg)
![Platform](https://img.shields.io/badge/Platform-iOS%20|%20tvOS%20|%20watchOS%20|%20macOS-red.svg)

# NXColorsetMaker
NXColorsetMaker can make colorsets for Xcode from Excel file.


# Purpose
I needed to apply iOS / tvOS dark mode. but there were so many things to do and should communicate with designers about the way to let the developers know the color sets. It was so hard to understand to each other. so I gave designer an Excel file and we did it easily.


# How it works
When you make a colorset on Xcode, JSON file and directory is generated. so __NXColorsetMaker__ makes same directory and JSON file from an Excel file.  

![Alt text](xcode_json_screen.png?raw=true)

And, __NXColorsetMaker__ output color values are HEX format, but you can change to float value format.

```ruby
HEX: getFormattedHexValue() # default
Float: getFormattedFloatValue()
```


# Install component
## openpyxl
 You should install __*openpyxl*__ to read an Excel file. I assume that you are using python3.
```ruby
$ sudo pip3 install openpyxl
```

# Usage
## Options
```swift
  -h, --help            show this help message and exit
  -f EXCEL_FILE_NAME, --file EXCEL_FILE_NAME
                        excel file name.
                        default: ./colorSheet.xlsx
  -s EXCEL_SHEET_NAME, --sheet EXCEL_SHEET_NAME
                        excel sheet name.
                        default: Sheet1
  -t [TYPE [TYPE ...]], --type [TYPE [TYPE ...]]
                        target device types.
                        default: universal
                        supporting types: [ universal, iphone, ipad, carplay, watch, tv, mac ]
                        ex) -t iphone ipad
  -d DESTINATION_DIR, --dir DESTINATION_DIR
                        target directory.
                        default: ./ColorSets
  -c, --catalyst        add colorset for mac-catalyst.
                        if type doesn't have ipad, this option will be ignored
                        ex) -t ipad -c
```

## Excute
All options have default value. so you don't have to add any option if you can use default values.
```swift
$ python3 makeColorSet.py
or
$ python3 makeColorSet.py -f ~/colors.xlsx -t universal iphone ipad -c -d ~/repository/myproject/image.xcassets/colorSets
```

# Author
This is [Jinwook Jeon](http://Nicejinux.NET).   
I've been working as an iOS developer in Korea.  
This is my first Python script, so there can be lots of weird things in this source.  
I'm waiting for your comments, suggestions, fixes, everything what you want to say.  
Feel free to contact me.

 - email : nicejinux@gmail.com
 - facebook : http://facebook.com/Nicejinux
 - homepage : http://Nicejinux.NET


# MIT License

	Copyright (c) 2019 Jinwook Jeon. All rights reserved.

	Permission is hereby granted, free of charge, to any person obtaining a
	copy of this software and associated documentation files (the "Software"),
	to deal in the Software without restriction, including
	without limitation the rights to use, copy, modify, merge, publish,
	distribute, sublicense, and/or sell copies of the Software, and to
	permit persons to whom the Software is furnished to do so, subject to
	the following conditions:

	The above copyright notice and this permission notice shall be included
	in all copies or substantial portions of the Software.

	THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
	OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
	MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
	IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
	CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
	TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
	SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
	
