#!/usr/bin/env python
# encoding: utf-8

# The MIT License (MIT)

# Copyright (c) 2014 CNRS

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Authors
# Hervé BREDIN (http://herve.niderb.fr)

from __future__ import unicode_literals

"""
SRT (SubRip Text) is a file format to specify subtitles for a recorded video.

References
----------
http://en.wikipedia.org/wiki/SubRip
"""


import pysrt
from pyannote.core import Transcription


class SRTParser(object):

    def _timeInSeconds(self, t):
        h = t.hours
        m = t.minutes
        s = t.seconds
        u = t.milliseconds
        return 3600. * h + 60. * m + s + 1e-3 * u

    def read(self, path, uri=None):

        transcription = Transcription(uri=uri)
        subtitles = pysrt.open(path)

        prev_end = None
        for subtitle in subtitles:

            start = self._timeInSeconds(subtitle.start)
            end = self._timeInSeconds(subtitle.end)

            if prev_end and start > prev_end:
                transcription.add_edge(prev_end, start)

            text = subtitle.text
            transcription.add_edge(start, end, subtitle=text)

            prev_end = end

        return transcription
