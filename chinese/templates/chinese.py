# -*- coding: utf-8 -*-
# Copyright: Damien Elmes <anki@ichi2.net>, Thomas TEMPE <thomas.tempe@alysse.org>
# Copyright 2012, Thomas TEMPE <thomas.tempe@alysse.org>
# # Copyright: Ankitects Pty Ltd and contributors
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
# Based off Kieran Clancy's initial implementation.

# These templates complement the ruby.py module, and provide
# chinese-specific services. They should be used on fields containing
# chinese characters, with transcription formatted as in 吗[ma3].


import re
from anki.hooks import addHook
from anki.utils import stripHTML
from .ruby import ruby_top, ruby_top_text, ruby_bottom, ruby_bottom_text
from .ruby import no_sound
from functools import reduce

r = r' ?([^ >]+?)\[(.+?)\]'
ruby_re = r'<ruby><rb>\1</rb><rt>\2</rt></ruby>'

tone_info= [
['[ɑ̄āĀáɑ́ǎɑ̌ÁǍàɑ̀À]', 'a'],
['[ēĒéÉěĚèÈ]', 'e'],
['[īĪíÍǐǏìÌ]', 'i'],
['[ōŌóÓǒǑòÒ]', 'o'],
['[ūŪúÚǔǓùÙ]', 'u'],
['[ǖǕǘǗǚǙǜǛ]', 'v']
]



def transcription_no_tones(txt, *args):
    '''Returns only the transcription, with tone information removed, whether
    it is in the form 'nǐ' or 'ni2'.
    '''
    txt = ruby_top_text(txt)
    for a, b in tone_info:
        txt = re.sub(a, b, txt)
    txt = re.sub(r'(\[\s*[a-z]+?)[0-9]', r'\1 ', txt, flags=re.IGNORECASE)
    txt = re.sub(r'¹²³⁴', r' ', txt)
    return txt

def hanzi_silhouette(txt, *args):
    ''' Hides the chinese characters, ruby annotations and tone colorization.
    Eg: '又[you4]A又B' returns '_ A _ B'.
    '''
    if len(txt)<10:
        return re.sub('[\u4e00-\u9fff]', '_ ', ruby_bottom_text(txt))
    else:
        return ""

def hanzi_context(txt, extra, context, tag, fullname):
    '''
    For use on a Hanzi field.
    Return a list of all the other Hanzi synonyms, with the common characters hidden,
    to allow the user to identify the correct hanzi from a note.
    '''
    other_hanzi = []
    for k, v in context.items():
        if re.match(r'Hanzi.*', k, flags=re.IGNORECASE) and v != txt :
            other_hanzi += [k]
    if len(other_hanzi)<1:
        return ""
    other_hanzi.sort()
    other_hanzi_values = []
    for v in other_hanzi:
        value = stripHTML(re.sub(r, r'\1', no_sound(context[v]))) 
        if len(value)>0:
            other_hanzi_values += [value]
    if len(other_hanzi_values)<1:
        return ""
    def concat(a, b):
        return a + " / " + b
    context_string = reduce(concat, other_hanzi_values)
    for h in txt:
        if  h >= '\u4e00' and h <= '\u9fff':
            context_string = re.sub(h, " _ ", context_string)
    context_string = re.sub("  ", " ", context_string)
    return context_string

def hint(txt: str, args, context, tag: str, fullname) -> str:
    # From https://github.com/ankitects/anki/blob/31ceb5d7300c74a1d2315a2a4a79d33e6cce6013/pylib/anki/template_legacy.py#L147
    if not txt.strip():
        return ""
    # random id
    domid = "hint%d" % id(txt)
    return """
<a class=hint href="#"
onclick="this.style.display='none';document.getElementById('%s').style.display='block';return false;">
%s</a><div id="%s" class=hint style="display: none">%s</div>
""" % (
        domid,
        _("Show %s") % tag,
        domid,
        txt,
    )

def hint_transcription(txt, extra, context, tag, fullname):
    return hint(ruby_top(txt), extra, context, 'Transcription', fullname)

def hint_transcription_no_tones(txt, extra, context, tag, fullname):
    return hint(transcription_no_tones(txt), extra, context, 'Transcription', fullname)

def install():
    addHook('fmod_transcription_no_tones', transcription_no_tones)
    addHook('fmod_hanzi_silhouette', hanzi_silhouette)
    addHook('fmod_hanzi_context', hanzi_context)
    addHook('fmod_hint_transcription', hint_transcription)
    addHook('fmod_hint_transcription_no_tones', hint_transcription_no_tones)
