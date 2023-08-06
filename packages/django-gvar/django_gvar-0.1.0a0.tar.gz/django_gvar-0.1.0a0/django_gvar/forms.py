"""Input converter for db field."""
from typing import Union, Optional

from json import JSONDecodeError

from numpy import ndarray

from django.core.exceptions import ValidationError
from django.core.validators import EMPTY_VALUES
from django.forms import Textarea
from django.forms.fields import JSONField
from django.utils.translation import gettext_lazy as _

from gvar._gvarcore import GVar

from django_gvar.testing import allclose
from django_gvar.parser import parse_str_to_gvar, parse_gvar_to_str


class EmptyValuesWrapper:
    """Wrapper which allows empty value checks on arrays.

    In the validation process of fields (from forms), Djagno checks if the value
    is in EMPTY_VALUES.
    But since GVars can be arrays, the check `value in list` potentially fails.
    This class wrapps the `in` operator such that elements of value are checked if
    value is an array.
    """

    empty_values = EMPTY_VALUES

    def __contains__(self, value):
        """Wrap contains to allow empty checks."""
        if isinstance(value, ndarray):
            out = any([val in self for val in value])
        else:
            out = value in self.empty_values

        return out


EMPTY_VALUES_WRAPPED = EmptyValuesWrapper()


class InvalidGVarInput(str):
    """Wrap input which is not convertable."""


class GVarFormField(JSONField):
    """Class which parses input from string to gvar and vice versa.

    The implementation follows Djangos JSONField implementation:
    https://github.com/django/django/blob/926148ef019abcac3a9988c78734d9336d69f24e/django/forms/fields.py#L1226
    """

    default_error_messages = {
        "invalid": _("Enter a valid conversion string."),
    }
    widget = Textarea
    empty_values = EMPTY_VALUES_WRAPPED

    def to_python(self, value: Union[GVar, str, None]) -> Optional[GVar]:
        """Tries to convert value to GVar."""
        if self.disabled:
            return value
        elif value in self.empty_values:
            return None
        elif isinstance(value, (GVar, ndarray)):  # Not sure if this can actually happen
            return value

        try:
            return parse_str_to_gvar(value)
        except (JSONDecodeError, ValueError) as e:
            raise ValidationError(
                self.error_messages["invalid"] + "\n" + str(e),
                code="invalid",
                params={"value": value, "exception": e},
            )

    def bound_data(self, data: str, initial: GVar) -> Union[GVar, InvalidGVarInput]:
        """Parses string to GVar if possible. Else keeps invalid string input."""
        if self.disabled:
            return initial
        try:
            return parse_str_to_gvar(data)
        except (JSONDecodeError, ValueError):
            return InvalidGVarInput(data)

    def prepare_value(self, value: GVar) -> str:
        """Parses GVar to string if string is not invalid."""
        try:
            return parse_gvar_to_str(value)
        except (ValueError, TypeError):
            return value

    def has_changed(self, initial: GVar, data):
        """Checks if input and initial gvars differ using asser allclose."""
        return False if self.disabled else not allclose(initial, self.to_python(data))
