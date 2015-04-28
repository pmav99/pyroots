#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Panagiotis Mavrogiorgos
# email: gmail, pmav99

"""
tests/conftest.py

"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import


import pytest

from pyroots import Bisect, Ridder, Brentq, Brenth


@pytest.fixture(params=[Bisect, Ridder, Brenth, Brentq])
def Solver(request):
    return request.param
