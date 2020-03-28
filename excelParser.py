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

import pandas
from pathlib import Path
from idiomType import IdiomType
from collections import OrderedDict
from colorManager import ColorModel
from colorManager import ColorComponent
from templateManager import JSONTemplate
from templateManager import SwiftTemplate


class ExcelParser():
    # Initializer
    def __init__(self):
        self.numberOfColors = 0


    # Public Methods
    def colorComponentsFromFiles(self, fileNames: [str]):
        colorDict = OrderedDict()

        for fileName in fileNames:
            if fileName.endswith('.csv'):
                cvsDict = self.colorComponentsFromCSV(fileName)
                self.__mergeDict(colorDict, cvsDict)
            elif fileName.endswith('.xlsx') or fileName.endswith('.xls'):
                excelDict = self.colorComponentsFromExcel(fileName)
                self.__mergeDict(colorDict, excelDict)
            else:
                continue

        return colorDict


    def colorComponentsFromExcel(self, fileName: str):
        book = pandas.ExcelFile(fileName)
        sheetNames = book.sheet_names
        colorDict = OrderedDict()

        for sheetName in sheetNames:
            sheet = book.parse(sheetName)
            allColors = []
            for _, row in sheet.iterrows():
                if row[0] is None or row[0] == 'name':
                    continue
                model = self.__getColorModelFromExcelRow(row)
                allColors.append(ColorComponent(model))
            colorDict[sheetName] = allColors
            self.numberOfColors += len(allColors)

        return colorDict


    def colorComponentsFromCSV(self, fileName: str):
        colorDict = OrderedDict()

        book = pandas.read_csv(fileName)
        allColors = []
        for _, row in book.iterrows():
            if row[0] is None or row[0] == 'name':
                continue
            model = self.__getColorModelFromExcelRow(row)
            allColors.append(ColorComponent(model))
        colorDict[Path(fileName).stem] = allColors
        self.numberOfColors += len(allColors)

        return colorDict


    def getJSONDict(self, color: ColorComponent, idioms=[IdiomType.UNIVERSAL], needMacCatalyst=False):
        colorList = []
        template = JSONTemplate()

        for idiom in idioms:
            colorList.append(template.getColorInfo(color=color, idiom=idiom, isDarkMode=False))
            colorList.append(template.getColorInfo(color=color, idiom=idiom, isDarkMode=True))

            # 'mac-catalyst' is a subType of 'ipad'
            if idiom.value == 'ipad' and needMacCatalyst:
                colorList.append(template.getColorInfo(color=color, idiom=idiom, isDarkMode=False, isMacCatalyst=True))
                colorList.append(template.getColorInfo(color=color, idiom=idiom, isDarkMode=True, isMacCatalyst=True))

        colorSetDic = OrderedDict()
        colorSetDic["info"] = template.getInfo()
        colorSetDic["colors"] = colorList

        return colorSetDic


    # Private Methods
    def __mergeDict(self, mainDict: OrderedDict, targetDict: OrderedDict):
        # if main dict has same key, it will be overwrited.
        for key in targetDict.keys():
            mainDict[key] = targetDict[key]

    def __getColorModelFromExcelRow(self, row):
        return ColorModel(name=row[0], lightColor=row[1], lightColorAlpha=row[2], darkColor=row[3], darkColorAlpha=row[4])
