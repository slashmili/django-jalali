"""
To add filtering to your admin interface you need to
import django_jalali.admin.filterspecs in to your admin.py
"""

import jdatetime
from django.contrib.admin.filterspecs import FilterSpec
from django.utils.translation import gettext as _

from django_jalali.db.models import jDateField


class jDateFieldFilterSpec(FilterSpec):
    def __init__(self, f, request, params, model, model_admin, field_path=None):
        super().__init__(f, request, params, model, model_admin, field_path=field_path)
        self.field_generic = "%s__" % self.field_path

        self.date_params = {
            k: v for k, v in params.items() if k.startswith(self.field_generic)
        }

        today = jdatetime.date.today()
        one_week_ago = today - jdatetime.timedelta(days=7)
        # today_str = isinstance(self.field, jmodels.DateTimeField) \
        #            and today.strftime('%Y-%m-%d 23:59:59') \
        #            or today.strftime('%Y-%m-%d')
        today_str = today.strftime("%Y-%m-%d")

        last_day_this_month = 29
        if today.month == 12 and today.isleap():
            last_day_this_month = 30
        else:
            last_day_this_month = jdatetime.j_days_in_month[today.month - 1]

        last_day_this_year = 29
        if today.isleap():
            last_day_this_year = 30

        self.links = (
            (_("Any date"), {}),
            (_("Today"), {"%s" % self.field_path: today.strftime("%Y-%m-%d")}),
            (
                _("Past 7 days"),
                {
                    "%s__gte" % self.field_path: one_week_ago.strftime("%Y-%m-%d"),
                    "%s__lte" % self.field_path: today_str,
                },
            ),
            (
                _("This month"),
                {
                    "%s__gte"
                    % self.field_path: today.replace(day=1).strftime("%Y-%m-%d"),
                    "%s__lte"
                    % self.field_path: today.replace(day=last_day_this_month).strftime(
                        "%Y-%m-%d"
                    ),
                },
            ),
            (
                _("This year"),
                {
                    "%s__gte"
                    % self.field_path: today.replace(day=1, month=1).strftime(
                        "%Y-%m-%d"
                    ),
                    "%s__lte"
                    % self.field_path: today.replace(
                        day=last_day_this_year,
                        month=12,
                    ).strftime("%Y-%m-%d"),
                },
            ),
        )

    def title(self):
        return self.field.verbose_name

    def choices(self, cl):
        for title, param_dict in self.links:
            yield {
                "selected": self.date_params == param_dict,
                "query_string": cl.get_query_string(param_dict, [self.field_generic]),
                "display": title,
            }


register_jdate = True
register_jdatetime = False
for f in FilterSpec.filter_specs:
    if f[0] == type(jDateFieldFilterSpec):
        register_jdate = False

if register_jdate is True:
    FilterSpec.filter_specs.insert(
        0, (lambda f: isinstance(f, jDateField), jDateFieldFilterSpec)
    )
