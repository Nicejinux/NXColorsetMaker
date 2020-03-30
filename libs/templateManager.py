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


from collections import OrderedDict
from libs.idiomType import IdiomType
from libs.colorManager import ColorComponent, ColorExtensionModel


class SwiftTemplate():
    # Public Methods
    def getHeaderComment(self, fileName: str):
        comment = f'''//
//  {fileName}
//
//  WARNING!!
//
//  PLEASE DO NOT CHANGE THIS FILE MANUALLY. 
//  All CHANGES WILL BE IGNORED WHEN THE FILE IS REGENERATED BY THE SCRIPT.
//  IF YOU WANT TO CHANGE SOMETHING, PLEASE UPDATE YOUR EXCEL FILE AND REGENERATE THIS FILE.
//
//  https://github.com/Nicejinux/NXColorsetMaker
//  Copyright © 2019 JINWOOK JEON. All rights reserved.
//


'''
        return comment


    def getColorExtensionCodes(self, extensionModel: ColorExtensionModel):
        extensionStr = f'''
    static var {extensionModel.name}: UIColor {{
        if #available(iOS 13, *) {{
            return UIColor {{ (traitCollection: UITraitCollection) -> UIColor in
                if traitCollection.userInterfaceStyle == .dark {{
                    return {extensionModel.darkUIColorText}
                }} else {{
                    return {extensionModel.lightUIColorText}
                }}
            }}
        }} else {{
            return {extensionModel.lightUIColorText}
        }}
    }}'''
        return extensionStr


class JSONTemplate():
    # Public Methods
    def getInfo(self):
        infoDic = OrderedDict()
        infoDic["version"] = 1
        infoDic["author"] = "xcode"
        return infoDic


    def getAppearances(self):
        appearances = []
        appearanceModel = OrderedDict()
        appearanceModel["appearance"] = "luminosity"
        appearanceModel["value"] = "dark"
        appearances.append(appearanceModel)
        return appearances


    def getColorInfo(self, color: ColorComponent, idiom=IdiomType.UNIVERSAL, isDarkMode=False, isMacCatalyst=False):
        colorInfo = OrderedDict()
        colorInfo["idiom"] = idiom.value

        if idiom.value == 'ipad' and isMacCatalyst:
            colorInfo["subtype"] = "mac-catalyst"

        if isDarkMode:
            colorInfo["appearances"] = self.getAppearances()
            colorInfo["color"] = color.getDarkComponent()
        else:
            colorInfo["color"] = color.getLightComponent()

        return colorInfo