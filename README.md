Bug
---

Bug is a simple, toy programming language. The compiler for Bug is written in Python, and translates
bug code into C code (so more accurately it is a *transpiler*).

Currently Bug is very, very minimal, and can only recognize a few simple statements:

```
int x = 3
int y = 4
int z = x
int w = y
```

No recognition of functions, classes, or expressions. Though it's currently not a very practical programming language,
I plan on continuing to develop Bug until I'm able to *boostrap* the Bug compiler, meaning I can write the complete 
compiler for Bug, in the Bug language itself. That's the first major goal, and will mark the release of Bug 1.0.0.

Beyond that, I'm not entirely sure what direction I'll take the project. I'll likely continue adding more advance
features to Bug, and maintaing and optimizing the code.

A quick overview of the project structure:
* ```bug/bug``` contains the code for the Bug compiler, written entirely in Python.
* ```bug/grammar/grammar.txt``` is the grammar that describes the syntax of the Bug language,
      written in [Extended Backus-Naur Form](https://en.wikipedia.org/wiki/Extended_Backus%E2%80%93Naur_form) (EBNF for short).
* ```bug/tests``` contains source code examples for Bug that help to test the compiler is working correctly.

Installation
------------

To test out Bug, you'll need a Python interpreter installed. The easiest and most popular intepreter is 
[CPython](https://www.python.org/). Any version above Python 3.5 will work fine, since the source code
for the compiler uses [type annotations](https://docs.python.org/3/library/typing.html) throughout.

Once you have Python installed, you can install Bug using pip:

```
python -m pip install git+https://github.com/algerbrex/bug.git
```

Which will install Bug as a command line program. You can then test bug by running:

```
bug path/to/source/code/file.bug
```

And pointing it to an appropriate file. If Bug compiles the program correctly, it should display a 
confirmation messsage, and a file with the same name but with the C extension will be put in the
same directory. You'll then need to find a suitable C compiler to compile the C code to ane exectuable
that can be run. The C code Bug generate does aim to be fairly human readable however, so you can also
feel free to poke around in the file generated.

Why the name "Bug"?
-------------------

As many might be aware of, a *bug* in software engineering is a mistake in the logic of a program that
causes it to work unexpectedly. So the name "Bug" is meant to be a little ironic, since I hope Bug will
eventually have a compiler that has very few bugs.

If you do find any bugs will playing with Bug, feel free to leave an issue with the Bug code that's
producing the error.

License
-------

Bug is licensed under the [MIT license](https://opensource.org/licenses/MIT).
