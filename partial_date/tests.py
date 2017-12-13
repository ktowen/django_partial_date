# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import date
from django.test import TestCase
from partial_date import PartialDate, PartialDateField


class PartialDateTestCase(TestCase):
    def test_init_with_string(self):
        self.assertEqual(PartialDate("2000").date, date(year=2000, month=1, day=1))
        self.assertEqual(PartialDate("2000-02").date, date(year=2000, month=2, day=1))
        self.assertEqual(PartialDate("2000-03-04").date, date(year=2000, month=3, day=4))

        self.assertEqual(PartialDate("2000").precision, PartialDate.YEAR)
        self.assertEqual(PartialDate("2000-02").precision, PartialDate.MONTH)
        self.assertEqual(PartialDate("2000-03-04").precision, PartialDate.DAY)

    def test_init_with_date(self):
        self.assertEqual(PartialDate(date(year=2000, month=3, day=4), precision=PartialDate.DAY).__repr__(), "2000-03-04")
        self.assertEqual(PartialDate(date(year=2000, month=3, day=4), precision=PartialDate.MONTH).__repr__(), "2000-03")
        self.assertEqual(PartialDate(date(year=2000, month=3, day=4), precision=PartialDate.YEAR).__repr__(), "2000")

    def test_eq(self):
        self.assertTrue(PartialDate("2000") == PartialDate("2000"))
        self.assertFalse(PartialDate("2001") == PartialDate("2000"))
        self.assertFalse(PartialDate("2000-01") == PartialDate("2000"))
        self.assertFalse(PartialDate("2000-01") == PartialDate("2000-01-01"))

    def test_ne(self):
        self.assertFalse(PartialDate("2000") != PartialDate("2000"))
        self.assertTrue(PartialDate("2001") != PartialDate("2000"))
        self.assertTrue(PartialDate("2000-01") != PartialDate("2000"))
        self.assertTrue(PartialDate("2000-01") != PartialDate("2000-01-01"))

    def test_gt(self):
        self.assertFalse(PartialDate("2000") > PartialDate("2000"))
        self.assertTrue(PartialDate("2001") > PartialDate("2000"))
        self.assertTrue(PartialDate("2000-01") > PartialDate("2000"))
        self.assertFalse(PartialDate("2000-01") > PartialDate("2000-01-01"))

    def test_lt(self):
        self.assertFalse(PartialDate("2000") < PartialDate("2000"))
        self.assertFalse(PartialDate("2001") < PartialDate("2000"))
        self.assertFalse(PartialDate("2000-01") < PartialDate("2000"))
        self.assertTrue(PartialDate("2000-01") < PartialDate("2000-01-01"))

    def test_ge(self):
        self.assertTrue(PartialDate("2000") >= PartialDate("2000"))
        self.assertTrue(PartialDate("2001") >= PartialDate("2000"))
        self.assertTrue(PartialDate("2000-01") >= PartialDate("2000"))
        self.assertFalse(PartialDate("2000-01") >= PartialDate("2000-01-01"))

    def test_le(self):
        self.assertTrue(PartialDate("2000") <= PartialDate("2000"))
        self.assertFalse(PartialDate("2001") <= PartialDate("2000"))
        self.assertFalse(PartialDate("2000-01") <= PartialDate("2000"))
        self.assertTrue(PartialDate("2000-01") <= PartialDate("2000-01-01"))

    def test_format(self):
        format = ('%Y', '%m/%Y', '%m/%d/%Y')
        self.assertEqual(PartialDate("2000-03-04").format(*format), "03/04/2000")
        self.assertEqual(PartialDate("2000-03").format(*format), "03/2000")
        self.assertEqual(PartialDate("2000").format(*format), "2000")
