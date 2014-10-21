#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# file tests/test_nearly_equal.py
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

""" Test `nearly_equal()` """

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

import sys
import itertools

import pytest

from pyroots.utils import nearly_equal


# Python's floats have up to 16 digits of accuracy, so we choose the
# fixture's parameters in such a way that in no case we need more than
# 16 digits are needed.
EPSILONS = [1e10, 1e6, 1e3, 1e0, 1e-1, 1e-3, 1e-6, 1e-10]
NUMBERS = [
    -10032, -1093, -104, -11, -1, -0.032, -2.3e-7, -3.2e-15, -9.2e-40,      # negative
     10032,  1093,  104,  11,  1,  0.032,  2.3e-7,  3.2e-15,  9.2e-40,      # positive
     0
]


@pytest.mark.parametrize(["num", "epsilon"], itertools.product(NUMBERS, EPSILONS))
def test_same_sign(num, epsilon):
    """ Test big numbers (i.e. number >> 1). """
    # Define two "big" numbers
    n1 = num
    n2 = num + 9 * epsilon      # if we change "9" to "10" tests will fail!!!

    # epsilon >= diff(n1, n2)
    assert nearly_equal(n1, n2, epsilon=epsilon * 1e+1)
    assert nearly_equal(n2, n1, epsilon=epsilon * 1e+1)
    assert nearly_equal(n1, n2, epsilon=epsilon * 1e+3)
    assert nearly_equal(n2, n1, epsilon=epsilon * 1e+3)
    assert nearly_equal(n1, n2, epsilon=epsilon * 1e+6)
    assert nearly_equal(n2, n1, epsilon=epsilon * 1e+6)
    # epsilon < diff(n1, n2)
    assert not nearly_equal(n1, n2, epsilon=epsilon * 1e-1)
    assert not nearly_equal(n2, n1, epsilon=epsilon * 1e-1)
    assert not nearly_equal(n1, n2, epsilon=epsilon * 1e-3)
    assert not nearly_equal(n2, n1, epsilon=epsilon * 1e-3)
    assert not nearly_equal(n1, n2, epsilon=epsilon * 1e-6)
    assert not nearly_equal(n2, n1, epsilon=epsilon * 1e-6)
    # we don't check that epsilon == diff(n1, n2)
    # because the result is case specific.


@pytest.mark.parametrize(["num", "epsilon"], itertools.product(NUMBERS, EPSILONS))
def test_opposite_sign(num, epsilon):
    """ Test opposite numbers. """
    # mpf is a very small value. Something in the order of 1e-300
    # The following compraisons are valid for epsilons > sys.float_info.epsilon
    mpf = sys.float_info.min

    # Comparing very small numbers should evaluate to True even if the numbers
    # have opposite signs.
    assert nearly_equal(mpf, mpf, epsilon=epsilon)
    assert nearly_equal(mpf, -mpf, epsilon=epsilon)
    assert nearly_equal(-mpf, -mpf, epsilon=epsilon)

    # comparing very big numbers with opposite sings should evaluate to False
    num = 1e40
    assert not nearly_equal(num, -num, epsilon=epsilon)
    assert not nearly_equal(-num, num, epsilon=epsilon)


def test_opposite_sign2():
    """ Test opposite numbers. """
    mpf = sys.float_info.min
    epsilon = 1e-5
    assert not nearly_equal(-1.0, 1.0, epsilon=epsilon)
    assert not nearly_equal(1.0, -1.0, epsilon=epsilon)
    assert not nearly_equal(1.000000001, -1.0, epsilon=epsilon)
    assert not nearly_equal(-1.0, 1.000000001, epsilon=epsilon)
    assert not nearly_equal(-1.000000001, 1.0, epsilon=epsilon)
    assert not nearly_equal(1.0, -1.000000001, epsilon=epsilon)
    assert not nearly_equal(1e-3, -1e-3, epsilon=epsilon)
    assert nearly_equal(1e-7, -1e-7, epsilon=epsilon)
    assert nearly_equal(10 * mpf, 10 * -mpf, epsilon=epsilon)
    assert nearly_equal(1e6 * mpf, 1e7 * -mpf, epsilon=epsilon)


@pytest.mark.parametrize("epsilon", EPSILONS)
def test_ulp(epsilon):
    # mpf is a very small value. Something in the order of 1e-300
    # The following compraisons are valid for epsilons > sys.float_info.epsilon
    mpf = sys.float_info.min
    assert nearly_equal(mpf, -mpf, epsilon)
    assert nearly_equal(mpf, 0, epsilon)
    assert nearly_equal(0, mpf, epsilon)
    assert nearly_equal(-mpf, 0, epsilon)
    assert nearly_equal(0, -mpf, epsilon)

    assert nearly_equal(1e-40, -mpf, epsilon)
    assert nearly_equal(1e-40, mpf, epsilon)
    assert nearly_equal(mpf, 1e-40, epsilon)
    assert nearly_equal(-mpf, 1e-40, epsilon)


@pytest.mark.parametrize("epsilon", EPSILONS)
def test_zero(epsilon):
    """ Test comparisons involving zero. """
    # zero equals itself... (duh)
    assert nearly_equal(0.0, 0.0, epsilon=epsilon)
    assert nearly_equal(0.0, -0.0, epsilon=epsilon)
    assert nearly_equal(-0.0, -0.0, epsilon=epsilon)


@pytest.mark.parametrize("epsilon", EPSILONS)
def test_nan(epsilon):
    pos = float("inf")
    neg = -float("inf")
    nan = float("nan")
    max_float = sys.float_info.max
    min_float = -max_float

    assert not nearly_equal(nan, nan, epsilon=epsilon)
    assert not nearly_equal(nan, 0.0, epsilon=epsilon)
    assert not nearly_equal(-0.0, nan, epsilon=epsilon)
    assert not nearly_equal(nan, -0.0, epsilon=epsilon)
    assert not nearly_equal(0.0, nan, epsilon=epsilon)
    assert not nearly_equal(nan, pos, epsilon=epsilon)
    assert not nearly_equal(pos, nan, epsilon=epsilon)
    assert not nearly_equal(nan, neg, epsilon=epsilon)
    assert not nearly_equal(neg, nan, epsilon=epsilon)
    assert not nearly_equal(nan, max_float, epsilon=epsilon)
    assert not nearly_equal(max_float, nan, epsilon=epsilon)
    assert not nearly_equal(nan, min_float, epsilon=epsilon)
    assert not nearly_equal(min_float, nan, epsilon=epsilon)
    assert not nearly_equal(nan, min_float, epsilon=epsilon)
    assert not nearly_equal(min_float, nan, epsilon=epsilon)
    assert not nearly_equal(nan, -min_float, epsilon=epsilon)
    assert not nearly_equal(-min_float, nan, epsilon=epsilon)


@pytest.mark.parametrize("epsilon", EPSILONS)
def test_infinities(epsilon):
    pinf = float("inf")
    ninf = -pinf
    max_float = sys.float_info.max
    min_float = -max_float

    # infinite is equal to itself no matter the epsilon value used.
    assert nearly_equal(pinf, pinf, epsilon)
    assert nearly_equal(ninf, ninf, epsilon)
    # but the two infs compare as unequal
    assert not nearly_equal(pinf, ninf, epsilon)
    # infinite is not equal to the extreme allowed float values.
    assert not nearly_equal(ninf, min_float, epsilon)
    assert not nearly_equal(pinf, max_float, epsilon)
