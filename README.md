# NXColorsetMaker
NXColorsetMaker can make colorsets for Xcode from Excel file.


# Purpose
I needed to apply iOS / tvOS dark mode. but there were so many things to do and should communicate with designers about the way to let the developers know the color sets. It was so hard to understand to each other. so I gave designer an Excel file and we did it easily.


# How it works
When you make a colorset on Xcode, JSON file and directory is generated. so __NXColorsetMaker__ makes same directory and JSON file from an Excel file.  

I chose HEX format for color values, but you can change to float value format.
```ruby
HEX: getFormattedHexValue()
Float: getFormattedFloatValue()
```


# Install component
## openpyxl
 You should install *openpyxl* to read an Excel file. I assume that you are using python3.
```ruby
$ sudo pip3 install openpyxl
```

# Usage
## Options
```swift
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