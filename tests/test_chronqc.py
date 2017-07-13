#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_chronqc
----------------------------------

Tests for `chronqc` module.
"""

import unittest

import chronqc


class TestChronqc(unittest.TestCase):

    def setUp(self):
        pass

    def test_something(self):
        assert(chronqc.__version__)

    def tearDown(self):
        pass
