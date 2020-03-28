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


class ColorModel():
    # Initializer
    def __init__(self, name: str, lightColor='#ffffff', lightColorAlpha=1.0, darkColor='#000000', darkColorAlpha=1.0):
        self.name = name
        self.lightColor = lightColor
        self.lightColorAlpha = lightColorAlpha
        self.darkColor = darkColor
        self.darkColorAlpha = darkColorAlpha


class ColorExtensionModel():
    # Initializer
    def __init__(self, name: str, lightStr: str, darkStr: str):
        self.name = name
        self.lightUIColorText = lightStr
        self.darkUIColorText = darkStr


class ColorComponent():
    # Initializer
    def __init__(self, model: ColorModel):
        # self.model = model
        self.name = model.name
        self.lightColor = model.lightColor
        self.lightColorAlpha = model.lightColorAlpha
        self.darkColor = model.darkColor
        self.darkColorAlpha = model.darkColorAlpha
        self.extension = ColorExtensionModel(self.name,
                                             self.__getExtensionStr(),
                                             self.__getExtensionStr(isDark=True))

    # Public Methods
    def getLightComponent(self, isHex=True):
        return self.__getComponent(isHex=isHex)

    def getDarkComponent(self, isHex=True):
        return self.__getComponent(isHex=isHex, isDark=True)


    # Private Methods
    def __getExtensionStr(self, isDark=False):
        color = isDark and self.darkColor or self.lightColor
        alpha = isDark and self.darkColorAlpha or self.lightColorAlpha

        red = self.__getFloat(color[1:3])
        green = self.__getFloat(color[3:5])
        blue = self.__getFloat(color[5:7])
        return f'UIColor(red: {red}, green: {green}, blue: {blue}, alpha: {alpha})'

    def __getComponent(self, isHex=True, isDark=False):
        color = OrderedDict()
        color["color-space"] = "srgb"
        components = OrderedDict()
        targetColor = isDark and self.darkColor or self.lightColor
        alpha = isDark and self.darkColorAlpha or self.lightColorAlpha

        components["red"] = isHex and self.__getHex(targetColor[1:3]) or self.__getFloat(targetColor[1:3])
        components["green"] = isHex and self.__getHex(targetColor[3:5]) or self.__getFloat(targetColor[3:5])
        components["blue"] = isHex and self.__getHex(targetColor[5:7]) or self.__getFloat(targetColor[5:7])
        components["alpha"] = '{0:1.3f}'.format(float(alpha))
        color["components"] = components
        return color

    def __getHex(self, s: str):
        if len(s) == 0:
            return '0x00'
        return f'0x{s.upper()}'

    def __getFloat(self, s: str):
        if len(s) == 0:
            return '0.000'
        return '{0:1.3f}'.format(float.fromhex(s) / 255.0)
