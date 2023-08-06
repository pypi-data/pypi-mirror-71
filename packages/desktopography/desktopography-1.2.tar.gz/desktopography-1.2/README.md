Desktopography command line
===========================

see http://www.desktopography.net

Usage
-----

``` console
$ pip install desktopography
$ desktopography -h
```

TODO
----

- Add more verbose documentation and docstrings
- Add tests
- Setup CI
- Auto-detect screen size
- Fix XDG support

Development
-----------

``` console
$ git clone https://gitlab.com/fbochu/desktopography.git
$ cd desktopography
$ python -m venv venv
$ . venv/bin/activate
$ flit install --deps=develop
```

Tests
-----

``` console
$ prospector src/
```

Publishing
----------

Change `__version__` in `src/desktopography/__init__.py` then

``` console
$ flit build
$ flit publish
```
