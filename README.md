
Latex to text (help to translation)
===================================

Thanks to [arnbod](https://github.com/arnbod) for the Latex parsing.

Let's translate
---------------

Do you need to translate your work in LaTeX into a foreign language? Don't have the time or skills to do it? Why not let a computer do it for you?

Machine translation has made huge progress and the text produced is quite good.

Issue with maths
----------------

However automatic translators don't like mathematics and LaTeX file. We provide here a tool to hide mathematics to the machine so that you can translate any scientific text from one language to another.

It works!
---------

These tools have been used to translate the book *Python au lycée* to *Python in high school*, more than 200 pages, in 15 workdays. See [GitHub Exo7](https://github.com/exo7math).

Requirements
------------

* Your original LaTeX file,

* a Python3 installation and all the Python files you will find in the `bin/` directory.

* Use `pip3 install deepl` to install the deepl python API.

Operations
----------

* Use `python3 translator.py -i toto.tex -o toto-en.tex -f DE -t EN-GB` to translate the `toto.tex` Latex file from german to english.
* You can add `-d <Deepl API Key>` or use the `DEEPL_AUTH_KEY` environment variable to set your deepl api key.

* You certainly need to check and correct the translation, if certain Latex commands are incorrectly processed please try to add them inside
the constants_perso.py file and retry.
