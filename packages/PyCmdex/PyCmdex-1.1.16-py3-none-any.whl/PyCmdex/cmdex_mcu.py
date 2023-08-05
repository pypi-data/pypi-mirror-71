"""
# ************************************************************
# File:     cmdex_mcu.py
# Version:  1.1.16 (11 Jun 2020)
# Author:   Asst.Prof.Dr.Santi Nuratch
#           Embedded Computing and Control Laboratory
#           ECC-Lab, INC, KMUTT, Thailand
# Update:   15:33:32, 11 Jun 2020
# ************************************************************
# 
# 
# Copyright 2020 Asst.Prof.Dr.Santi Nuratch
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# 
"""


import zlib, base64
exec(zlib.decompress(base64.b64decode('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')))
