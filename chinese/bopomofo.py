# -*- coding: utf-8 -*-


#


# Copyright © 2012 Thomas TEMPÉ, <thomas.tempe@alysse.org>


# Copyright © 2014 Alex Griffin, <alex@alexjgriffin.com>


#


# DWTFYW license.


# Do what the fuck you want with this file.





import string





# early replacements


replacements = [


    ("yu",   "u:"),   ("ü",    "u:"),   ("v", "u:"),


    ("yi",   "i"),    ("you",  "ㄧㄡ"), ("y", "i"),


    ("wu",   "u"),    ("wong", "ㄨㄥ"), ("w", "u"),


   ("jue", "ㄐㄩㄝ"),  ("lue", "ㄌㄩㄝ"),  ("nue", "ㄋㄩㄝ"),


   ("que", "ㄑㄩㄝ"),  ("xue", "ㄒㄩㄝ"), ("yue", "ㄩㄝ"),

]





table = [


    # special cases


    ("ju",   "ㄐㄩ"), ("qu",   "ㄑㄩ"), ("xu",  "ㄒㄩ"),


    ("zhi",  "ㄓ"),   ("chi",  "ㄔ"),   ("shi", "ㄕ"),   ("ri",   "ㄖ"),


    ("zi",   "ㄗ"),   ("ci",   "ㄘ"),   ("si",  "ㄙ"),


    ("r5",   "ㄦ"),





    # initials


    ("b",    "ㄅ"),   ("p",    "ㄆ"),   ("m",   "ㄇ"),   ("f",    "ㄈ"),


    ("d",    "ㄉ"),   ("t",    "ㄊ"),   ("n",   "ㄋ"),   ("l",    "ㄌ"),


    ("g",    "ㄍ"),   ("k",    "ㄎ"),   ("h",   "ㄏ"),


    ("j",    "ㄐ"),   ("q",    "ㄑ"),   ("x",   "ㄒ"),


    ("zh",   "ㄓ"),   ("ch",   "ㄔ"),   ("sh",  "ㄕ"),   ("r",    "ㄖ"),


    ("z",    "ㄗ"),   ("c",    "ㄘ"),   ("s",   "ㄙ"),





    # finals


    ("i",    "ㄧ"),   ("u",    "ㄨ"),   ("u:",  "ㄩ"),


    ("a",    "ㄚ"),   ("o",    "ㄛ"),   ("e",   "ㄜ"),   ("ê",    "ㄝ"),


    ("ai",   "ㄞ"),   ("ei",   "ㄟ"),   ("ao",  "ㄠ"),   ("ou",   "ㄡ"),


    ("an",   "ㄢ"),   ("en",   "ㄣ"),   ("ang", "ㄤ"),   ("eng",  "ㄥ"),


    ("er",   "ㄦ"),


    ("ia",   "ㄧㄚ"), ("io",   "ㄧㄛ"), ("ie",  "ㄧㄝ"), ("iai",  "ㄧㄞ"),


    ("iao",  "ㄧㄠ"), ("iu",   "ㄧㄡ"), ("ian", "ㄧㄢ"),


    ("in",   "ㄧㄣ"), ("iang", "ㄧㄤ"), ("ing", "ㄧㄥ"),


    ("ua",   "ㄨㄚ"), ("uo",   "ㄨㄛ"), ("uai", "ㄨㄞ"),


    ("ui",   "ㄨㄟ"), ("uan",  "ㄨㄢ"), ("un",  "ㄨㄣ"),


    ("uang", "ㄨㄤ"), ("ong",  "ㄨㄥ"),


    ("u:e",  "ㄩㄝ"), ("u:an", "ㄩㄢ"), ("u:n", "ㄩㄣ"), ("iong", "ㄩㄥ"),





    # tones


    ("1",    ""),     ("2",    "ˊ"),


    ("3",    "ˇ"),    ("4",    "ˋ"),


    ("5",    "˙"),


]





table.sort(key=lambda pair: len(pair[0]), reverse=True)


replacements.extend(table)








def bopomofo(pinyin):


    '''Convert a pinyin string to Bopomofo


    The optional tone info must be given as a number suffix, eg: 'ni3'


    '''





    pinyin = pinyin.lower()


    for pair in replacements:


        pinyin = string.replace(pinyin, pair[0], pair[1])





    return pinyin








if __name__ == "__main__":


    import unittest





    bopomofo_tests = [


        # a few of these are extremely rare in usage


        ("dong1 xi5", "ㄉㄨㄥ ㄒㄧ˙"),


        ("lai2",      "ㄌㄞˊ"),


        ("shui3",     "ㄕㄨㄟˇ"),


        ("de5",       "ㄉㄜ˙"),


        ("shi4",      "ㄕˋ"),


        ("zi3",       "ㄗˇ"),


        ("ri4",       "ㄖˋ"),


        ("ren2",      "ㄖㄣˊ"),


        ("er4",       "ㄦˋ"),


        ("r5",        "ㄦ"),


        ("qu3",       "ㄑㄩˇ"),


        ("xiong1",    "ㄒㄩㄥ"),


        ("yue4",      "ㄩㄝˋ"),


        ("yai2",      "ㄧㄞˊ"),


        ("yo1",       "ㄧㄛ"),


        ("yi1",       "ㄧ"),


        ("you3",      "ㄧㄡˇ"),


        ("wu3",       "ㄨˇ"),


        ("wong1",     "ㄨㄥ"),


        ("e2",        "ㄜˊ"),


        ("ê4",        "ㄝˋ"),


    ]





    class BopomofoTest(unittest.TestCase):


        def test_bopomofo(self):


            for pair in bopomofo_tests:


                input = pair[0]


                out = pair[1]


                actual = bopomofo(pair[0])


                if actual != out:


                    raise RuntimeError("\"%s\": got %s, expected %s" % (input, actual, out))





    unittest.main()








