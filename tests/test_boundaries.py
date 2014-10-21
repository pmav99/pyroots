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
import unittest

import pytest

from pyroots import Bisect
from pyroots.base import BaseSolver
from pyroots.utils import EPS, ConvergenceError, nearly_equal


class BoundariesTest(object):
    def test_tolerance_values(self):
        with pytest.raises(ArithmeticError):
            self.SolverClass(xtol=EPS / 2)

        with pytest.raises(ArithmeticError):
            self.SolverClass(xtol=-1)

        with pytest.raises(ArithmeticError):
            self.SolverClass(epsilon=EPS / 2)

        with pytest.raises(ArithmeticError):
            self.SolverClass(epsilon=-1)

    def test_small_bracket_for_initial_values(self):
        f = lambda x: x
        a, b = (-1e-8, -2e-8)
        xtol = 1e-4
        # without raising exceptions
        solver = self.SolverClass(xtol=xtol, raise_on_fail=False)
        result = solver(f, a, b)
        assert result.converged is False
        assert result.msg == BaseSolver.messages["small bracket"]
        # while raising exceptions
        solver = self.SolverClass(xtol=xtol, raise_on_fail=True)
        with pytest.raises(ConvergenceError):
            solver(f, a, b)

    def test_small_bracket_during_iterations(self):
        # input
        f = lambda x: tan(x)
        a = pi / 2 + 0.1
        b = pi / 2 - 0.1
        xtol = EPS * 20
        # without raising exceptions
        solver = self.SolverClass(xtol=xtol, raise_on_fail=False)
        result = solver(f, a, b)
        assert result.converged is False
        assert result.msg == BaseSolver.messages["small bracket"]
        # while raising exceptions
        solver = self.SolverClass(xtol=xtol, raise_on_fail=True)
        with pytest.raises(ConvergenceError):
            solver(f, a, b)

    def test_root_is_on_the_lower_bracket(self):
        # input
        f = lambda x: x
        a, b = (-1e-4, 1)
        epsilon = 1e-2
        solver = self.SolverClass(epsilon=epsilon)
        result = solver(f, a, b)

        assert result.converged
        assert result.x0 == a
        assert abs(result.fx0) < epsilon
        assert result.func_calls == 1
        assert result.msg == BaseSolver.messages["lower bracket"]

    def test_root_is_on_the_upper_bracket(self):
        # input
        f = lambda x: x
        a, b = (-1, 1e-4)
        epsilon = 1e-2
        solver = self.SolverClass(epsilon=epsilon)
        result = solver(f, a, b)

        assert result.converged
        assert result.x0 == b
        assert abs(result.fx0) < epsilon
        assert result.func_calls == 2
        assert result.msg == BaseSolver.messages["upper bracket"]

    def test_root_is_not_bracketed(self):
        # input
        f = lambda x: x
        a, b = (1, 2)
        # while not raising
        solver = self.SolverClass(raise_on_fail=False)
        result = solver(f, a, b)
        assert result.converged is False
        assert result.func_calls == 2
        assert result.msg == BaseSolver.messages["no bracket"]
        # while raising on errors
        solver = self.SolverClass(raise_on_fail=True)
        with pytest.raises(ConvergenceError):
            solver(f, a, b)

    def test_linear_equation(self):
        f = lambda x: x
        a, b = (-1, 1)
        solver = self.SolverClass()
        result = solver(f, a, b)
        assert result.converged is True
        assert result.x0 == 0
        assert result.fx0 == 0
        assert result.func_calls == 3
        assert result.msg == BaseSolver.messages["convergence"]

    def test_max_iterations(self):
        # http://en.wikipedia.org/wiki/Bisection_method#Example:_Finding_the_root_of_a_polynomial
        f = lambda x: x**3 - x - 2
        a, b = (1, 2)
        max_iter = 2
        # while not raising
        solver = self.SolverClass(max_iter=max_iter, raise_on_fail=False)
        result = solver(f, a, b)
        assert result.converged is False
        assert result.func_calls == 4
        assert result.iterations == max_iter
        assert result.msg == BaseSolver.messages["iterations"]
        # while raising on errors
        solver = self.SolverClass(max_iter=max_iter, raise_on_fail=True)
        with pytest.raises(ConvergenceError):
            solver(f, a, b)

    def test_root_is_found(self):
        f = lambda x: x**2 - 3 * x + 2
        a, b = (0.5, 1.5)
        epsilon=1e-5
        solver = self.SolverClass(epsilon=epsilon)
        result = solver(f, a, b)
        assert result.converged
        assert result.x0 == 1
        assert result.fx0 == 0
        assert result.msg == BaseSolver.messages["convergence"]

    def test_root_is_found2(self):
        f = lambda x: x**3 - x**2 - 3 * x + 2       # root is -1.618
        a, b = (-2.5, 2.5)
        epsilon = 1e-3
        solver = self.SolverClass(epsilon=epsilon)
        result = solver(f, a, b)
        assert result.converged
        assert nearly_equal(result.x0, -1.618, epsilon)
        assert nearly_equal(result.fx0, 0, epsilon)
        assert result.msg == BaseSolver.messages["convergence"]

    def test_root_is_found3(self):
        # http://en.wikipedia.org/wiki/Bisection_method#Example:_Finding_the_root_of_a_polynomial
        f = lambda x: x**3 - x - 2
        a, b = (1, 2)
        epsilon = 1e-3
        solver = self.SolverClass(epsilon=epsilon)
        result = solver(f, a, b)
        assert result.converged
        assert nearly_equal(result.x0, 1.521, epsilon)
        assert nearly_equal(result.fx0, 0, epsilon)
        assert result.msg == BaseSolver.messages["convergence"]


class TestBisectBoundaries(BoundariesTest):
    def setup_class(self):
        self.SolverClass = Bisect
        self.solver = Bisect()
