from __future__ import print_function
import os
import io
import json
import enum
import argparse
from openpyxl import load_workbook
from collections import OrderedDict

class IdiomType(enum.Enum):
    UNIVERSAL = 'universal'
    IPHONE = 'iphone'
    IPAD = 'ipad'
    CARPLAY = 'car'
    WATCH = 'watch'
    TV = 'tv'
    MAC = 'mac'

def getFormattedFloatValue(s):
    return '{0:1.3f}'.format(float.fromhex(s) / 255.0)

def getFormattedHexValue(s):
    return '0x{}'.format(s.upper())

def getInfo():
    infoDic = OrderedDict()
    infoDic["version"] = 1
    infoDic["author"] = "xcode"
    return infoDic

def getColor(colorValue, colorAlpha="1.0"):
    color = OrderedDict()
    color["color-space"] = "srgb"
    components = OrderedDict()
    components["red"] = getFormattedHexValue(colorValue[1:3])
    components["green"] = getFormattedHexValue(colorValue[3:5])
    components["blue"] = getFormattedHexValue(colorValue[5:7])
    components["alpha"] = '{0:1.3f}'.format(float(colorAlpha))
    color["components"] = components
    return color

def getAppearances():
    appearances = []
    appearanceModel = OrderedDict()
    appearanceModel["appearance"] = "luminosity"
    appearanceModel["value"] = "dark"
    appearances.append(appearanceModel)
    return appearances

def getColorInfo(row, idiom=IdiomType.UNIVERSAL, isDarkMode=False, isMacCatalyst=False):
    colorInfo = OrderedDict()
    colorInfo["idiom"] = idiom.value
    if idiom.value == 'ipad' and isMacCatalyst:
        colorInfo["subtype"] = "mac-catalyst"
    if isDarkMode:
        colorInfo["appearances"] = getAppearances()
    colorInfo["color"] = getColor(str(row[3].value), colorAlpha=str(row[4].value))
    return colorInfo

def getAllRows():
    wookBook = load_workbook(excelFileName, data_only=True)
    workSheet = wookBook[excelSheetName]
    allRows = []
    for row in workSheet.rows:
        allRows.append(row)
    del allRows[0]
    return allRows

def parse(row, idioms=[IdiomType.UNIVERSAL], needMacCatalyst=False):
    colorList = []
    for idiom in idioms:
        colorList.append(getColorInfo(row, idiom, isDarkMode=False))
        colorList.append(getColorInfo(row, idiom, isDarkMode=True))
        # 'mac-catalyst' is a subType of 'ipad'
        if idiom.value == 'ipad' and needMacCatalyst:
            colorList.append(getColorInfo(row, idiom, isDarkMode=False, isMacCatalyst=True))
            colorList.append(getColorInfo(row, idiom, isDarkMode=True, isMacCatalyst=True))

    colorSetDic = OrderedDict()
    colorSetDic["info"] = getInfo()
    colorSetDic["colors"] = colorList

    return colorSetDic

def createDir(filePath):
    if not os.path.exists(filePath):
        os.makedirs(filePath)

def saveToFile(data, filePath='./'):
    fileName = '{}/{}'.format(filePath, jsonFile)
    with io.open(fileName, 'w+', encoding='utf-8') as file:
        file.write(json.dumps(data, ensure_ascii=False, indent=2, separators=(',', ' : ')))

    print('{} file is created'.format(fileName))

def createContainerDir(dirName):
    createDir(dirName)
    colorSetDic = OrderedDict()
    colorSetDic["info"] = getInfo()
    saveToFile(colorSetDic, filePath=dirName)

def printSeparator(count):
    for _ in range(0, count):
        print('=', end="")
    print()    

def printHeader(title):
    print()
    printSeparator(len(title) + 1)
    print(title)
    printSeparator(len(title) + 1)
    print()

def extract():
    allRows = getAllRows()
    printHeader(' {} colors are loaded'.format(len(allRows)))

    printHeader(' Container folder is creating')
    createContainerDir(rootDir)

    printHeader(' Colorsets are creating')
    for row in allRows:
        parsed = parse(row, idioms=deviceTypes, needMacCatalyst=macCatalyst)
        path = '{}/{}.colorset'.format(rootDir, row[0].value)
        createDir(path)
        saveToFile(parsed, filePath=path)
        # print(json.dumps(parsed, ensure_ascii=False, indent="  "))

    printHeader(' {} colorsets are created'.format(len(allRows)))


rootDir = './ColorSets'
jsonFile = 'Contents.json'
excelFileName = './colorSheet.xlsx'
excelSheetName = 'Sheet1'
deviceTypeStr = 'universal'
deviceTypes = [IdiomType.UNIVERSAL]
macCatalyst = False

def main():
    global rootDir
    global jsonFile
    global excelFileName
    global excelSheetName
    global deviceTypeStr
    global deviceTypes
    global macCatalyst

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', metavar="EXCEL_FILE_NAME", dest="file", type=str, default=excelFileName, help="excel file name. default: {}".format(excelFileName))
    parser.add_argument('-s', '--sheet', metavar="EXCEL_SHEET_NAME", dest="sheet", type=str, default=excelSheetName, help="excel sheet name. default: {}".format(excelSheetName))
    parser.add_argument('-t', '--type', metavar="TYPE", dest="types", nargs='*', default=deviceTypeStr, help="target device types. default: {} / all types: [ universal, iphone, ipad, carplay, watch, tv, mac ] / ex) -t iphone ipad".format(deviceTypeStr))
    parser.add_argument('-d', '--dir', metavar="DESTINATION_DIR", dest="directory", type=str, default=rootDir, help="target directory. default: {}".format(rootDir))
    parser.add_argument('-c', '--catalyst', dest="catalyst", action='store_true', help="add colorset for mac-catalyst ex) -t ipad -c")

    args = parser.parse_args()
    excelFileName = args.file
    excelSheetName = args.sheet
    deviceTypeStr = args.types
    macCatalyst = args.catalyst
    rootDir = args.directory

    typeList = []
    deviceTypeList = deviceTypeStr.split()
    for deviceType in deviceTypeList:
        typeList.append(IdiomType[deviceType.upper().strip()])
    deviceTypes = typeList

    extract()

if __name__=="__main__":
    main()

