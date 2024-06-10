#!/usr/bin/env python3

# Convert a LaTeX file to txt file
# Usage : 'python3 latextotext.py toto.tex'
# Output : create a file toto.txt and a file toto.dic


# Author: Arnaud Bodin. Thanks to Kroum Tzanev
# Idea from Mr.Sh4nnon https://codereview.stackexchange.com/questions/209049
# Licence CC-BY-SA 4.0

import argparse
import re
import sys
import os
import yaml
from constants import *    # Definition of the tag symbol and special commands/environnments
from constants_perso import *  # Personnal customization
import deepl

#--------------------------------------------------
#--------------------------------------------------

# Arguments 
parser = argparse.ArgumentParser(description='Translate latex file with minimal destruction')
parser.add_argument("-i", dest='inputfile', help='input file to translate')
parser.add_argument("-o", dest='outputfile', nargs='?', help='output translated file')
parser.add_argument("-d", dest="DEEPL_AUTH_KEY", required=False, help="Deepl API key")
parser.add_argument("-f", dest="FROM", default="DE", required=True, help="Language of the source document(s) e.g. DE")
parser.add_argument("-t", dest="TO", default="EN", required=True, help="Language of the target document e.g EN-GB")
options = parser.parse_args()

DEEPL_AUTH_KEY = os.environ.get("DEEPL_AUTH_KEY")
    if DEEPL_AUTH_KEY == None :
        if args.DEEPL_AUTH_KEY == None:
            print('Specify a Deepl API key.')
            sys.exit(0)
        else:
           DEEPL_AUTH_KEY = options.DEEPL_AUTH_KEY

tex_file = options.inputfile
output_file = options.outputfile
dic_file = tex_file + '.dic'
txt_file = tex_file + '.txt'


# Read file object to string
fic_tex = open(tex_file, 'r')
text_all = fic_tex.read()
fic_tex.close()

# Real stuff start there!
# Replacement function pass as the replacement pattern in re.sub()

count = 0           # counter for tags
dictionnary = {}    # memorize tag: key=nb -> value=replacement

def func_repl(m):
    """ Function called by sub as replacement pattern given by output
    Input: the pattern to be replaced
    Ouput: the new pattern
    Action: also update the dictionnary of tags/replacement
    and increment the counter
    https://stackoverflow.com/questions/33962371"""
    global count
    dictionnary[count] = m.group(0)  # Add old string found to the dic
    tag_str = tag+str(count)+tag     # tag = '€' is defined in 'constants.py'
    count += 1   
    return tag_str                   # New string for pattern replacement


# Now we replace case by case math and command by tags
text_new = text_all

### PART 1 - Replacement of maths ###

# $$ ... $$
text_new = re.sub(r'\$\$(.+?)\$\$',func_repl,text_new, flags=re.MULTILINE|re.DOTALL)
# $ ... $
text_new = re.sub(r'\$(.+?)\$',func_repl,text_new, flags=re.MULTILINE|re.DOTALL)
# \( ... \)
text_new = re.sub(r'\\\((.+?)\\\)',func_repl,text_new, flags=re.MULTILINE|re.DOTALL)
# \[ ... \]
text_new = re.sub(r'\\\[(.+?)\\\]',func_repl,text_new, flags=re.MULTILINE|re.DOTALL)


### PART 2 - Replace \begin{env} and \end{env} but not its contents

for env in list_env_discard + list_env_discard_perso:
    str_env = r'\\begin\{' + env + r'\}(.+?)\\end\{' + env + r'\}'
    text_new = re.sub(str_env,func_repl,text_new, flags=re.MULTILINE|re.DOTALL)


### PART 3 - Discards contents of some environnments ###

text_new = re.sub(r'\\begin\{(.+?)\}',func_repl,text_new, flags=re.MULTILINE|re.DOTALL)
text_new = re.sub(r'\\end\{(.+?)\}',func_repl,text_new, flags=re.MULTILINE|re.DOTALL)


### PART 4 - Replacement of LaTeX commands with their argument ###

for cmd in list_cmd_arg_discard + list_cmd_arg_discard_perso:
    # Without opt arg, ex. \cmd{arg}
    str_env = r'\\' + cmd + r'\{(.+?)\}'
    text_new = re.sub(str_env,func_repl,text_new, flags=re.MULTILINE|re.DOTALL)
    # With opt arg, ex. \cmd[opt]{arg}
    str_env = r'\\' + cmd + r'\[(.*?)\]\{(.+?)\}'
    text_new = re.sub(str_env,func_repl,text_new, flags=re.MULTILINE|re.DOTALL)


### PART 5 - Replacement of LaTeX remaining commands (but not their argument) ###

text_new = re.sub(r'\\[a-zA-Z]+',func_repl,text_new, flags=re.MULTILINE|re.DOTALL)


### Translation

translator = deepl.Translator(DEEPL_AUTH_KEY)
result = translator.translate_text(text_new, source_lang=options.FROM, target_lang=options.TO, preserve_formatting=True)
resultText = result.text

# Replacement to latex file

for i,val in dictionnary.items():
    tag_str = tag+str(i)+tag
    val = val.replace('\\','\\\\')    # double \\ for correct write
    # val = re.escape(val)
    resultText = re.sub(tag_str,val,resultText, flags=re.MULTILINE|re.DOTALL)


# Write the result
with open(output_file, 'w') as out_tex:
    out_tex.write(resultText)

