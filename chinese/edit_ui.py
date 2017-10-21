# -*- coding: utf-8 -*-
# Copyright 2013 Thomas TEMPE <thomas.tempe@alysse.org>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

from anki.hooks import addHook, wrap
from aqt.editor import Editor
from .config import chinese_support_config as config

toggleButton = None
config_file_key = None
enable = None #enable editor UI enhancements for the current note type?

def setupToggleButton(buttons, editor):
    global toggleButton
    toggleButton = "toggle_chinese_support"
    buttons.append(editor.addButton(None, toggleButton, toggleButtonClick, id=toggleButton, label="汉字", tip="Enable/disable <b>Chinese Support Add-on</b> input fill-up", toggleable=True))
    return buttons

def toggleButtonClick(editor):
    global enable
    enable = not enable
    config.set_option(config_file_key, enable)
    updateToggleButton(editor)

def updateToggleButton(editor, *args, **kwargs):
    global config_file_key
    global enable
    try:
        model_name = editor.note.model()['name']
        model_id = editor.note.model()['id']
    except:
        return
    try:
        model_type = editor.note.model()['addon']
    except:
        model_type = None
    config_file_key = "enable_for_model_"+str(model_id)

    if config_file_key in config.options:
        enable = config.options[config_file_key]
    elif "Chinese (compatibility)" == model_type:
        enable = True
    else:
        enable = False

    if enable:
#        toggleButton.setChecked(True)
        editor.web.eval('$("#%s .blabel").text("✓ 汉字")' % toggleButton)
    else:
#        toggleButton.setChecked(False)
        editor.web.eval('$("#%s .blabel").text("✕ 汉字")' % toggleButton)
   

    
addHook("setupEditorButtons", setupToggleButton)
Editor.loadNote=wrap(Editor.loadNote, updateToggleButton)
