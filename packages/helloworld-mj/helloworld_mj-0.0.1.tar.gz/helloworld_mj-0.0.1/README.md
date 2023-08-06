# Hello world

This is an example of a python project demonstrating how to publish a python module to PyPI.

``` python
from hello import say_hello
#generate > hello, world!
say_hello()


#generate> hello, cool!
say_hello("cool")

```

# Developing Hello World

To install hellow word, along with the tools you need to develop and run tests, run the following in your virtualenv :
```
bash
$ pip install -e .[dev]
```
