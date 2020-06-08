from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


def validate_more_then_zero(value):
    if value < 0:
        raise ValidationError(
            _('%(value)s is less then 0'),
            params={'value': value},
        )
