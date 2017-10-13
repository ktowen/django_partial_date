import datetime
import re

from django.core import  exceptions
from django.db import models
from django.utils import six
from django.utils.translation import ugettext_lazy as _

partial_date_re = re.compile(
    r'(?P<year>\d{4})(?:-(?P<month>\d{1,2}))?(?:-(?P<day>\d{1,2}))?$'
)

class PartialDate(object):
    YEAR = 0
    MONTH = 1
    DAY = 2

    _date = None
    _precision = None

    DATE_FORMATS = {
        YEAR: '%Y',
        MONTH: '%Y-%m',
        DAY: '%Y-%m-%d'
    }

    def __init__(self, date, precision=DAY):
        self.date = date
        self.precision = precision

    def __repr__(self):
        return "" if not self._date else self._date.strftime(self.DATE_FORMATS[self._precision])

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        if not isinstance(value, datetime.date):
            raise exceptions.ValidationError(
                _("%(value)s is not datetime.date instance"),
                params={'value': value},
            )
        self._date = value

    @property
    def precision(self):
        return self._precision

    @precision.setter
    def precision(self, value):
        self._precision = value if value in (self.YEAR, self.MONTH, self.DAY) else self.DAY

    def precisionYear(self):
        return self.precision == self.YEAR

    def precisionMonth(self):
        return self.precision == self.MONTH

    def precisionDay(self):
        return self.precision == self.DAY

    @staticmethod
    def fromString(value):
        """
        Returns a PartialDate object from a string formatted as YYYY, YYYY-MM, YYYY-MM-DD.
        """
        match = partial_date_re.match(value)

        try:
            match_dict = match.groupdict()
            kw = {k: int(v) if v else 1 for k, v in six.iteritems(match_dict)}

            precision = PartialDate.DAY if match_dict["day"] else \
                        PartialDate.MONTH if match_dict["month"] else \
                        PartialDate.YEAR
            return PartialDate(datetime.date(**kw), precision)
        except (AttributeError, ValueError):
            raise exceptions.ValidationError(
                _("'%(value)s' is not a valid date string (YYYY, YYYY-MM, YYYY-MM-DD)"),
                params={'value': value}
            )


class PartialDateField(models.Field):
    """
    A django model field for storing partial dates.
    Accepts None, a partial_date.PartialDate object,
    or a formatted string such as YYYY, YYYY-MM, YYYY-MM-DD.
    In the database it saves the date in a column of type DateTimeField
    and uses the seconds to save the level of precision.
    """

    def get_internal_type(self):
        return "DateTimeField"

    def from_db_value(self, value, expression, connection, context):
        if value is None:
            return value
        return PartialDate(value.date(), value.second)

    def to_python(self, value):
        if value is None:
            return value

        if isinstance(value, PartialDate):
            return value

        if isinstance(value, str):
            return PartialDate.fromString(value)

        raise exceptions.ValidationError(
            _("'%(name)s' value must be a PartialDate instance, "
                "a valid partial date string (YYYY, YYYY-MM, YYYY-MM-DD) "
                "or None, not '%(value)s'"),
            params={'name': self.name, 'value': value},
        )

    def get_prep_value(self, value):
        partial_date = self.to_python(value)
        date = partial_date.date
        return datetime.datetime(date.year, date.month, date.day, second=partial_date.precision)
