import jdatetime
from django.contrib import admin
from django.contrib.admin.options import IncorrectLookupParameters
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from django_jalali.db import models


class JDateFieldListFilter(admin.FieldListFilter):

    def __init__(self, field, request, params, model, model_admin, field_path):
        self.field_generic = '%s__' % field_path
        self.date_params = {k: v for k, v in params.items()
                            if k.startswith(self.field_generic)}

        now = jdatetime.datetime.fromgregorian(datetime=timezone.now())
        if timezone.is_aware(now):
            now = timezone.localtime(now)

        if isinstance(field, models.jDateTimeField):
            today = now.replace(hour=0, minute=0, second=0, microsecond=0)
        else:
            today = now.date()

        tomorrow = today + jdatetime.timedelta(days=1)

        if today.month == 12:
            next_month = today.replace(year=today.year + 1, month=1, day=1)
        else:
            next_month = today.replace(month=today.month + 1, day=1)
        next_year = today.replace(year=today.year + 1, month=1, day=1)

        self.lookup_kwarg_since = '%s__gte' % field_path
        self.lookup_kwarg_until = '%s__lt' % field_path
        self.links = (
            (_('Any date'), {}),
            (_('Today'), {
                self.lookup_kwarg_since: today.strftime('%Y-%m-%d %H:%M:%S'),
                self.lookup_kwarg_until: tomorrow.strftime('%Y-%m-%d %H:%M:%S'),
            }),
            (_('Past 7 days'), {
                self.lookup_kwarg_since: (today - jdatetime.timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S'),
                self.lookup_kwarg_until: tomorrow.strftime('%Y-%m-%d %H:%M:%S'),
            }),
            (_('This month'), {
                self.lookup_kwarg_since: (today.replace(day=1)).strftime('%Y-%m-%d %H:%M:%S'),
                self.lookup_kwarg_until: next_month.strftime('%Y-%m-%d %H:%M:%S'),
            }),
            (_('This year'), {
                self.lookup_kwarg_since: (today.replace(month=1, day=1)).strftime('%Y-%m-%d %H:%M:%S'),
                self.lookup_kwarg_until: next_year.strftime('%Y-%m-%d %H:%M:%S'),
            }),
        )

        super().__init__(field, request, params, model, model_admin, field_path)

    def queryset(self, request, queryset):
        try:
            return queryset.filter(**self.used_parameters)
        except ValidationError as e:
            raise IncorrectLookupParameters(e)

    def expected_parameters(self):
        return [self.lookup_kwarg_since, self.lookup_kwarg_until]

    def choices(self, cl):
        for title, param_dict in self.links:
            yield {
                'selected': self.date_params == param_dict,
                'query_string': cl.get_query_string(
                    param_dict, [self.field_generic]),
                'display': title,
            }

    def has_output(self):
        return True
