# -*- coding: utf-8 -*-
"""
The MIT License

Copyright (c) 2009 Cedric RICARD

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

try:
    from configparser import RawConfigParser
except ImportError:
    from ConfigParser import RawConfigParser


class Config(RawConfigParser):
    def get(self, section, option, default=None, *args, **kwargs):
        if self.has_option(section, option) or default is None:
            return RawConfigParser.get(self, section, option)
        else:
            return default

    def getint(self, section, option, default=None, *args, **kwargs):
        if self.has_option(section, option) or not isinstance(default, int):
            return RawConfigParser.getint(self, section, option)
        else:
            return default

    def getfloat(self, section, option, default=None, *args, **kwargs):
        if self.has_option(section, option) or not isinstance(default, float):
            return RawConfigParser.getfloat(self, section, option)
        else:
            return default

    def getboolean(self, section, option, default=None, *args, **kwargs):
        if self.has_option(section, option) or not isinstance(default, bool):
            return RawConfigParser.getboolean(self, section, option)
        else:
            return default

    def set(self, section, option, value=None):
        if not self.has_section(section):
            self.add_section(section)
        RawConfigParser.set(self, section, option, value)

    def getlist(self, section, option, default=None):
        if self.has_option(section, option) or default is None:
            return RawConfigParser.get(self, section, option).split(',')
        else:
            return default
