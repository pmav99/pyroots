pyroots
=======

Abstract
--------

A Python 3 library implementing various root finding methods for single-variable
functions.

Currently the following methods have been implemented:

* The `bisect <http://en.wikipedia.org/wiki/Bisection_method>`_ method.
* The `ridder <http://en.wikipedia.org/wiki/Ridders%27_method>`_ method.
* The `brent <http://en.wikipedia.org/wiki/Brent%27s_method>`_ method (there are
  2 implementations, one following the Wikipedia article and one following the
  scipy implementation. The latter seems to converge faster).

Rationale
---------

The functionality of ``pyroots`` is already implemented in ``scipy``, so the
natural question is why rediscover the wheel?

Well, the main reason is that ``scipy`` is a huge dependency.  ``Pyroots`` on
the other hand is just a single package that is easily installed and that you
can easily bundle with ``py2exe`` or similar projects.  It doesn't even need to
get installed, just throw the ``pyroots`` folder in your project and you are
ready to go.

Apart from that, the API used by ``scipy``'s functions is not very
user-friendly. For example you can't use keyword arguments for your functions.
Finally, in ``scipy`` there is no reliable way to define how many digits of
accuracy you want in the obtained root.  For example, you may ask for 6 digits,
but scipy may calculate up to 14 (or 12 or whatever) digits.  The main
implication of this "glitch" is that scipy's method may evaluate the function
more times than those really needed. If the function calculates something
trivial like the functions in the following examples, then these extra function
calls are no big deal, but if your functions take significant time to evaluate
(e.g. more than seconds), then this can quickly become annoying, or even, simply
unacceptable (e.g. the function takes some minutes to return a value).

Usage
-----

All the functions share the same API, so you can easily switch between the,
methods, although, it should be noted that the method you probably want to use
is ``brent``.

Anyway, the function whose root you are searching must take at least a single
argument and return a single number.  This first argument is also the dependent
variable and, apart from that, the function can also take any number of
positional/keyword arguments. For example the following functions are totally
valid ones::

    def f(x, a):
        return x ** 2 - a + 1

    def g(x, a, b, c=3):
        # calculations
        return x ** 2 + a ** b - c

In order to find the root of ``f`` you must first define an interval that
contains the root. Let's say that this interval is defined as ``[xa, xb]``.  In
that case you call the methods of ``pyroots`` like this::

    result = brent(f, xa, xb, a)

All the methods return a ``Result`` object that has the following attributes::

    result.x0               # the root
    result.fx0              # the value of ``f(x0)`
    result.convergence      # True/False
    result.iterations       # the number of iterations
    result.func_calls       # the number of function evaluations.
    result.msg              # a descriptive message regarding the convergence (or the failure of convergence)

If, for some reason, convergence cannot be achieved, then a ``ConvergenceError``
is raised.  If you don't want that to happen, then you have to pass ``False`` as
the value of ``raise_on_fail`` argument::

    def f(x):
        return x ** 2 - 1

    result = brent(f, xa=-10, xb=-5, raise_on_fail=False):
    print(result)    # Outputs the following line
    # iter=  0, func_calls=  2, convergence=False, x0=None, f(x0)=None, msg=Root is not bracketed.

API
---

The definition of each root-finding function is the following one::

    brent(f, xa, xb, *args, ftol=1e-6, xtol=EPS, max_iter=500, raise_on_fail=True, **kwargs)

We have already covered ``f``, ``xa`` and ``xb``. At first, let's examine the
arguments that regard the function that we want to solve:

* ``f`` is the function whose root we are searching.
* ``xa`` is the lower bracket of the interval of the solution we search.
* ``xb`` is the upper bracket of the interval of the solution we search.
* ``*args`` are passed as positional arguments when ``f`` is evaluated.
* ``**kwargs`` are passed as keyword arguments when ``f`` is evaluated.

The remaining arguments are "keyword only arguments" (a feature unique in Python
3) and they are the following ones:

* ``ftol`` is the required precision of the solution, i.e. a solution is
  achieved when ``|f(x0)|`` is smaller than ``ftol``.
* ``xtol`` is
* ``max_iter`` is the maximum allowed number of iterations.
* ``raise_on_fail`` is a boolean flag indicating whether or not an exception
  should be raised if convergence fails. It defaults to True


Example
-------

A simple example::

    from pyroots import brent

    # define a function ``f(x)`` that returns a single variable.
    def f(x, y, z):
        return x**y + z

    # solve using the brent method
    result = brent(f, -10, 10, y=23, z=0.3, ftol=1e-5)

Installation
------------

with pip::

    pip install pyroots

or from source::

    python setup.py install

Documentation
-------------

For the time being documentation is not yet ready, but when it is prepared, it
will be uploaded at:

http://pyroots.readthedocs.org

The source code repository of pyroots can be found at bitbucket.org:

http://bitbucket.org/pmav99/pyroots/

Feedback is greatly appreciated.

pmav99 <gmail>
