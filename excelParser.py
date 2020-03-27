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

import csv
import openpyxl
from idiomType import IdiomType
from collections import OrderedDict
from colorManager import ColorComponent
from templateManager import JSONTemplate
from templateManager import SwiftTemplate


class ExcelParser():
    # Initializer
    def __init__(self):
        self.numberOfColors = 0


    # Public Methods
    def colorComponentsFromExcel(self, fileName: str):
        workBook = openpyxl.load_workbook(fileName, data_only=True)
        sheetNames = workBook.sheetnames
        colorDict = OrderedDict()

        for sheetName in sheetNames:
            workSheet = workBook[sheetName]
            allColors = []
            for row in workSheet.rows:
                if row[0].value is None or row[0].value == 'name':
                    continue
                allColors.append(ColorComponent(row))
            colorDict[sheetName] = allColors
            self.numberOfColors += len(allColors)

        return colorDict


    def colorComponentsFromCSV(self, fileName: str):
        colorDict = OrderedDict()


    # Private Methods
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
