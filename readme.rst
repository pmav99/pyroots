.. image:: https://travis-ci.org/pmav99/pyroots.svg?branch=master
    :target: https://travis-ci.org/pmav99/pyroots

pyroots
=======

Abstract
--------

A Python library implementing various root finding methods for single-variable
functions.

Currently the following methods have been implemented::

* The `bisect <http://en.wikipedia.org/wiki/Bisection_method>`_ method.
* The `ridder <http://en.wikipedia.org/wiki/Ridders%27_method>`_ method.
* The `brent <http://en.wikipedia.org/wiki/Brent%27s_method>`_ method.

With regard to ``Brent``'s method, there are two implementations, the first one
uses inverse quadratic extrapolation (``Brentq``) while the other ones uses
hyperbolic extrapolation (``Brenth``).

If you don't know which method to use, you should probably use ``Brentq``.  That
being said, ``Bisect`` method is safe and slow.

Example
-------

::

    # define the function whose root you are searching
    def f(x, a):
        return x ** 2 - a + 1

    # Create the Solver object (instead of Brentq you could also import Brenth/Ridder/Bisect)
    from pyroots import Brentq
    brent = Brentq(epsilon=1e-5)

    # solve the function in `[-3, 0]` while `a` is equal to 2
    result = brent(f, -3, 0, a=2)
    print(result)

will output::

         converged : True
           message : Solution converged.
         iteration :   6
        func calls :   9
                x0 :    -1.0000000748530762
              xtol :     0.0000000000000002
             f(x0) :     0.0000001497061579
           epsilon :     0.0000100000000000

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
Moreover, in ``scipy`` there is no reliable way to define how many digits of
accuracy you want in the obtained root.  For example, you may ask for 6 digits,
but scipy may calculate up to 14 (or 12 or whatever) digits.  The main
implication of this "glitch" is that scipy's method may evaluate the function
more times than those really needed. If the function calculates something
trivial like the functions in the following examples, then these extra function
calls are no big deal, but if your functions take significant time to evaluate
,e.g. more than seconds, then this can quickly become annoying, or even, simply
unacceptable, e.g. the function takes some minutes to return a value.

Installation
------------

with pip::

    pip install pyroots

or from source::

    python setup.py install

Usage
-----

All the solvers share the same API, so you can easily switch between the
various methods.

Function
++++++++

The function whose root you are searching must take at least a single argument
and return a single number.  This first argument is also the dependent variable
and, apart from that, the function can also take any number of
positional/keyword arguments. For example the following functions are totally
valid ones::

    def f(x, a):
        return x ** 2 - a + 1

    def g(x, a, b, c=3):
        return x ** 2 + a ** b - c

Solver Objects
--------------

The first thing you have to do is to create a ``Solver`` object for the method
you want to use::

    from pyroots import Brentq

    brent = Brentq()

When you create the ``Solver`` object, you can specify several parameters
that will affect the convergence. The most important are:

* `epsilon` which specifies the number of digits that will be taken under
  consideration when checking for convergence. It defaults to `1e-6`.
* `raise_on_fail` which will raise an exception if convergence failed. It
  defaults to `True`.

Using the above function definitions, in order to find the root of ``f`` you
must first define an interval that contains the root. Let's say that this
interval is defined as ``[xa, xb]``.  In this case you will call the solver
like this::

    def f(x, a):
        return x ** 2 - a + 1

    solver = Brentq()
    result = solver(f, xa, xb, a=3)

Result Objects
--------------

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
    print(result)

API
---

Each solver factory has the following signature::

    SolverFactory(epsilon=1e-6, xtol=EPS, max_iter=500, raise_on_fail=True, debug_precision=10)

where:

* ``epsilon`` is the required precision of the solution, i.e. a solution is
  achieved when ``|f(x0)|`` is smaller than ``epsilon``.
* ``max_iter`` is the maximum allowed number of iterations.
* ``raise_on_fail`` is a boolean flag indicating whether or not an exception
  should be raised if convergence fails. It defaults to True

Each solver object has the following signature::

    solver_object(f, xa, xb, *args, **kwargs)

where:

* ``f`` is the function whose root we are searching.
* ``xa`` is the lower bracket of the interval of the solution we search.
* ``xb`` is the upper bracket of the interval of the solution we search.
* ``*args`` are passed as positional arguments when ``f`` is evaluated.
* ``**kwargs`` are passed as keyword arguments when ``f`` is evaluated.

Documentation
-------------

For the time being documentation is not yet ready, but the examples in the
README should be enough to get your feet wet.

The source code repository of pyroots can be found at: https://github.com/pmav99/pyroots

Feedback and contributions are greatly appreciated.

pmav99 <gmail>
