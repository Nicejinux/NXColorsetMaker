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


import io
import os
import json
from templateManager import SwiftTemplate
from templateManager import JSONTemplate
from colorManager import ColorComponent
from colorManager import ColorExtensionModel
from collections import OrderedDict


class FileManager():
    # Initializer
    def __init__(self):
        self.jsonFileName = 'Contents.json'


    # Public Methods
    def saveJSONToFile(self, jsonInfoDict: OrderedDict, filePath='./'):
        fileName = f'{filePath}/{self.jsonFileName}'
        with io.open(fileName, 'w+', encoding='utf-8') as file:
            file.write(json.dumps(jsonInfoDict, ensure_ascii=False, indent=2, separators=(',', ' : ')))


    def saveColorExtensionToFile(self, allColorDict: OrderedDict, fileName: str, filePath='./'):
        template = SwiftTemplate()
        headComment = template.getHeaderComment(fileName)
        fileName = f'{filePath}/{fileName}'
        with io.open(fileName, 'w+', encoding='utf-8') as file:
            file.write(headComment)
            file.write('import UIKit\n\n\n')
            file.write('extension UIColor {')
            for key in allColorDict:
                allColors = allColorDict[key]
                for color in allColors:
                    file.write(template.getColorExtensionCodes(color.extension))
                    file.write('\n')
            file.write('}\n')


    def createContainerDirAndInfoFile(self, dirName: str):
        template = JSONTemplate()
        self.createDir(dirName)
        colorSetDic = OrderedDict()
        colorSetDic["info"] = template.getInfo()
        self.saveJSONToFile(colorSetDic, filePath=dirName)


    def createDir(self, filePath: str):
        if not os.path.exists(filePath):
            os.makedirs(filePath)
