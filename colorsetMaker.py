# Copyright (c) 2019 Jinwook Jeon. All rights reserved.

# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:

# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


import argparse
from collections import OrderedDict
from libs.idiomType import IdiomType
from libs.excelParser import ExcelParser
from libs.fileManager import FileManager


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


def makeColorsetJSON(allDataDict: OrderedDict):
    for key in allDataDict:
        printHeader(f' \'{key}\' folder is creating')
        fileManager.createContainerDirAndInfoFile(f'{rootDir}/{key}')
        allColors = allDataDict[key]
        for color in allColors:
            parsed = excelParser.getJSONDict(color, idioms=deviceTypes, needMacCatalyst=macCatalyst)
            path = f'{rootDir}/{key}/{color.name}.colorset'
            fileManager.createDir(path)
            fileManager.saveJSONToFile(parsed, filePath=path)
            print(f'{path}/{fileManager.jsonFileName} file is created')


def makeColorExtension(allDataDict: OrderedDict):
    fileManager.saveColorExtensionToFile(allDataDict, extensionFileName)


def start():
    allDataDict = excelParser.colorComponentsFromFiles(excelFileNames)

    printHeader(f' {excelParser.numberOfColors} colors are loaded')
    printHeader(' Container folder is creating')

    fileManager.createContainerDirAndInfoFile(rootDir)
    print(f'{rootDir}/{fileManager.jsonFileName} file is created')

    printHeader(' Colorsets are creating')
    makeColorsetJSON(allDataDict)

    printHeader(f' {extensionFileName} is creating')
    makeColorExtension(allDataDict)

    print(f'{rootDir}/{extensionFileName} file is created')
    printHeader(f' DONE: {excelParser.numberOfColors} colorsets are all created')


def updateArgs(args):
    global rootDir
    global excelFileNames
    global deviceTypes
    global macCatalyst

    excelFileNamesStr = args.files
    deviceTypeStr = args.types
    macCatalyst = args.catalyst
    rootDir = args.directory

    if type(excelFileNamesStr) == str:
        excelFileNames = [excelFileNamesStr]
    elif type(excelFileNamesStr) == list:
        excelFileNames = excelFileNamesStr

    if type(deviceTypeStr) == str:
        deviceTypes = [IdiomType[deviceTypeStr.upper()]]
    elif type(deviceTypeStr) == list:
        deviceTypeList = []
        for deviceType in deviceTypeStr:
            deviceTypeList.append(IdiomType[deviceType.upper()])
        deviceTypes = deviceTypeList


rootDir = './ColorSets'
excelFileNames = []
# excelFileNamesStr = './colorSheet.csv'
excelFileNamesStr = './colorSheet.xlsx'
extensionFileName = 'UIColor+DarkMode.swift'
deviceTypeStr = 'universal'
deviceTypes = [IdiomType.UNIVERSAL]
macCatalyst = False
excelParser = ExcelParser()
fileManager = FileManager()
numberOfColors = 0


def main():
    global rootDir
    global excelFileNamesStr
    global deviceTypeStr
    global macCatalyst

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', metavar="EXCEL_FILE_NAMES", dest="files", nargs='*', default=excelFileNamesStr, help=f"excel or csv file name. default: {excelFileNamesStr}")
    parser.add_argument('-t', '--type', metavar="TYPE", dest="types", nargs='*', default=deviceTypeStr, help=f"target device types. default: {deviceTypeStr} / all types: [ universal, iphone, ipad, carplay, watch, tv, mac ] / ex) -t iphone ipad")
    parser.add_argument('-d', '--dir', metavar="DESTINATION_DIR", dest="directory", type=str, default=rootDir, help=f"target directory. default: {rootDir}")
    parser.add_argument('-c', '--catalyst', dest="catalyst", action='store_true', help="add colorset for mac-catalyst ex) -t ipad -c")
 
    updateArgs(parser.parse_args())

    start()


if __name__ == "__main__":
    main()
