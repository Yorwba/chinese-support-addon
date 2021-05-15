# -*- mode: python; coding: utf-8 -*-
#
# Copyright © 2012 Roland Sieker, ospalh@gmail.com
# Inspiration and source of the URL: Tymon Warecki
# Adapted by Thomas TEMPE, thomas.tempe@alysse.org
#
# License: GNU AGPL, version 3 or later; http://www.gnu.org/copyleft/agpl.html


'''
Download Chinese pronunciations from BaiduTTS
'''

import urllib.request, urllib.parse, urllib.error
import urllib.request, urllib.error, urllib.parse
import os
import re

from aqt import mw


download_file_extension = '.mp3'
url_gtts = 'http://fanyi.baidu.com/gettts?'
user_agent_string = 'Mozilla/5.0'

# was: http://tts.baidu.com/text2audio?lan=zh&ie=UTF-8&text=%E4%BD%A0%E5%9C%A8%E5%B9%B2%E4%BB%80%E4%B9%88
# then: http://fanyi.baidu.com/gettts?lan=zh&text=%E4%BD%A0%E5%9C%A8%E5%B9%B2%E4%BB%80%E4%B9%88
# now: http://fanyi.baidu.com/gettts?lan=zh&text=%E4%BD%A0%E5%9C%A8%E5%B9%B2%E4%BB%80%E4%B9%88&spd=3&source=web



def get_word_from_baidu(source, lang="zh"):
    filename, fullpath = get_filename("_".join([source, "B", lang]), download_file_extension)
    if os.path.exists(fullpath):
        return filename
    get_url = build_query_url(source, lang)
    # This may throw an exception
    request = urllib.request.Request(get_url)
    request.add_header('User-agent', user_agent_string)
    response = urllib.request.urlopen(request, timeout=5)
    if 200 != response.code:
        raise ValueError(str(response.code) + ': ' + response.msg)
    content = response.read()
    if not content:
        raise ValueError('Did not get anything from Baidu.')
    if content.startswith(b'<!DOCTYPE html>'):
        raise ValueError('Got HTML instead of MP3 from Baidu.')
    with open(fullpath, 'wb') as audio_file:
        audio_file.write(content)
    return filename


def build_query_url(source, lang):
    qdict = dict(lan=lang, text=source.encode('utf-8'), spd='3', source='web')
    return url_gtts + urllib.parse.urlencode(qdict)


def get_filename(base, end):
    """Return the media filename for the given title. """
    # Basically stripping the 'invalidFilenameChars'. (Not tested too much).
    base = re.sub('[\\/:\*?"<>\|]', '', base)
    mdir = mw.col.media.dir()
    return base + end, os.path.join(mdir, base + end)
