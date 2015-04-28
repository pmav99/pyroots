#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# file tests/test_boundaries.py
#
#############################################################################
# Copyright (c) 2014 by Panagiotis Mavrogiorgos
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# * Neither the name(s) of the copyright holders nor the names of its
#   contributors may be used to endorse or promote products derived from this
#   software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AS IS AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO
# EVENT SHALL THE COPYRIGHT HOLDERS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
# OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#############################################################################
#
# @license: http://opensource.org/licenses/BSD-3-Clause
# @authors: see AUTHORS.txt

"""
Tests checking the boundary conditions of the pyroots functions.
"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

from math import pi, tan

import pytest

import pyroots
from pyroots.utils import EPS, ConvergenceError, nearly_equal


def test_tolerance_values(Solver):
    with pytest.raises(ArithmeticError):
        Solver(xtol=EPS / 2)

    with pytest.raises(ArithmeticError):
        Solver(xtol=-1)

    with pytest.raises(ArithmeticError):
        Solver(epsilon=EPS / 2)

    with pytest.raises(ArithmeticError):
        Solver(epsilon=-1)



def test_small_bracket_initial_values(Solver):
    f = lambda x: x
    a, b = (-1e-8, -2e-8)
    xtol = 1e-4
    # without raising exceptions
    solver = Solver(xtol=xtol, raise_on_fail=False)
    result = solver(f, a, b)
    assert result.converged is False
    assert result.msg == Solver.messages["small bracket"]
    # while raising exceptions
    solver = Solver(xtol=xtol, raise_on_fail=True)
    with pytest.raises(ConvergenceError):
        solver(f, a, b)


def test_small_bracket_during_iterations(Solver):
    f = lambda x: tan(x)
    a = pi / 2 + 0.1
    b = pi / 2 - 0.1
    xtol = EPS * 20
    # without raising exceptions
    solver = Solver(xtol=xtol, raise_on_fail=False)
    result = solver(f, a, b)
    assert result.converged is False
    assert result.msg == Solver.messages["small bracket"]
    # while raising exceptions
    solver = Solver(xtol=xtol, raise_on_fail=True)
    with pytest.raises(ConvergenceError):
        solver(f, a, b)

def test_root_is_on_the_lower_bracket(Solver):
    f = lambda x: x
    a, b = (-1e-4, 1)
    epsilon = 1e-2
    solver = Solver(epsilon=epsilon)
    result = solver(f, a, b)
    assert result.converged
    assert result.x0 == a
    assert abs(result.fx0) < epsilon
    assert result.func_calls == 1
    assert result.msg == Solver.messages["lower bracket"]

def test_root_is_on_the_upper_bracket(Solver):
    # input
    f = lambda x: x
    a, b = (-1, 1e-4)
    epsilon = 1e-2
    solver = Solver(epsilon=epsilon)
    result = solver(f, a, b)
    assert result.converged
    assert result.x0 == b
    assert abs(result.fx0) < epsilon
    assert result.func_calls == 2
    assert result.msg == Solver.messages["upper bracket"]

def test_root_is_not_bracketed(Solver):
    # input
    f = lambda x: x
    a, b = (1, 2)
    # while not raising
    solver = Solver(raise_on_fail=False)
    result = solver(f, a, b)
    assert result.converged is False
    assert result.func_calls == 2
    assert result.msg == Solver.messages["no bracket"]
    # while raising on errors
    solver = Solver(raise_on_fail=True)
    with pytest.raises(ConvergenceError):
        solver(f, a, b)

def test_linear_equation(Solver):
    f = lambda x: x
    a, b = (-1, 1)
    solver = Solver()
    result = solver(f, a, b)
    assert result.converged is True
    assert result.x0 == 0
    assert result.fx0 == 0
    assert result.func_calls == 3
    assert result.msg == Solver.messages["convergence"]

def test_max_iterations(Solver):
    # http://en.wikipedia.org/wiki/Bisection_method#Example:_Finding_the_root_of_a_polynomial
    f = lambda x: x**3 - x - 2
    a, b = (1, 2)
    max_iter = 1
    # while not raising
    solver = Solver(max_iter=max_iter, raise_on_fail=False)
    result = solver(f, a, b)
    assert result.converged is False
    # The ridder method does two function calls per iteration.
    if isinstance(solver, pyroots.Ridder):
        assert result.func_calls == 4
    else:
        assert result.func_calls == 3
    assert result.iterations == max_iter
    assert result.msg == Solver.messages["iterations"]
    # while raising on errors
    solver = Solver(max_iter=max_iter, raise_on_fail=True)
    with pytest.raises(ConvergenceError):
        solver(f, a, b)

def test_root_is_found(Solver):
    f = lambda x: x**2 - 3 * x + 2
    a, b = (0.5, 1.5)
    epsilon=1e-5
    solver = Solver(epsilon=epsilon)
    result = solver(f, a, b)
    assert result.converged
    assert nearly_equal(result.x0, 1, epsilon)
    assert nearly_equal(result.fx0, 0, epsilon)
    assert result.msg == Solver.messages["convergence"]

@pytest.mark.parametrize("a, b, root", [(-2.5, 0, -1.618), (0, 1, 0.618), (1, 2.5, 2)])
def test_root_is_found2(Solver, a, b, root):
    epsilon = 1e-3
    solver = Solver(epsilon=epsilon)
    f = lambda x: x**3 - x**2 - 3 * x + 2       # three roots: -1.618, 0.618, 2
    result = solver(f, a, b)
    assert result.converged
    assert nearly_equal(result.x0, root, epsilon)
    assert nearly_equal(result.fx0, 0, epsilon)
    assert result.msg == Solver.messages["convergence"]

def test_root_is_found3(Solver):
    # http://en.wikipedia.org/wiki/Bisection_method#Example:_Finding_the_root_of_a_polynomial
    f = lambda x: x**3 - x - 2
    a, b = (1, 2)
    epsilon = 1e-3
    solver = Solver(epsilon=epsilon)
    result = solver(f, a, b)
    assert result.converged
    assert nearly_equal(result.x0, 1.521, epsilon)
    assert nearly_equal(result.fx0, 0, epsilon)
    assert result.msg == Solver.messages["convergence"]
