# Copyright (c) 2018 luozhouyang
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import unittest

from .cosine import Cosine


class TestCosine(unittest.TestCase):

    def test_cosine(self):
        cos = Cosine(1)
        s = ['', ' ', 'Shanghai', 'ShangHai', 'Shang Hai']
        for i in range(len(s)):
            for j in range(i, len(s)):
                print('dis between \'%s\' and \'%s\': %.4f' % (s[i], s[j], cos.distance(s[i], s[j])))
                print('sim between \'%s\' and \'%s\': %.4f' % (s[i], s[j], cos.similarity(s[i], s[j])))


if __name__ == "__main__":
    unittest.main()
