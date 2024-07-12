from urllib.parse import unquote

import jdatetime
from django.contrib.admin import site
from django.contrib.admin.views.main import ChangeList
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory, TestCase
from django.utils.encoding import force_str

from tests.admin import BarTimeAdmin
from tests.models import BarTime


def select_by(dictlist, key, value):
    return [x for x in dictlist if x[key] == value][0]


class ListFiltersTests(TestCase):
    def setUp(self):
        self.request_factory = RequestFactory()
        self.today = jdatetime.date.today()
        self.tomorrow = self.today + jdatetime.timedelta(days=1)
        self.one_week_ago = self.today - jdatetime.timedelta(days=7)
        if self.today.month == 12:
            self.next_month = self.today.replace(
                year=self.today.year + 1, month=1, day=1
            )
        else:
            self.next_month = self.today.replace(month=self.today.month + 1, day=1)
        self.next_year = self.today.replace(year=self.today.year + 1, month=1, day=1)

        # Bars
        self.mybartime = BarTime.objects.create(name="foo", datetime=self.today)

    def test_jdatefieldlistfilter(self):
        modeladmin = BarTimeAdmin(BarTime, site)

        request = self.request_factory.get("/")
        request.user = AnonymousUser()
        changelist = self.get_changelist(request, BarTime, modeladmin)
        request = self.request_factory.get(
            "/",
            {
                "datetime__gte": self.today.strftime("%Y-%m-%d %H:%M:%S"),
                "datetime__lt": self.tomorrow.strftime("%Y-%m-%d %H:%M:%S"),
            },
        )
        request.user = AnonymousUser()
        changelist = self.get_changelist(request, BarTime, modeladmin)

        # Make sure the correct queryset is returned
        queryset = changelist.get_queryset(request)
        self.assertEqual(list(queryset), [self.mybartime])

        # Make sure the correct choice is selected
        filterspec = changelist.get_filters(request)[0][0]
        self.assertEqual(force_str(filterspec.title), "datetime")
        choice = select_by(filterspec.choices(changelist), "display", "Today")
        self.assertEqual(choice["selected"], True)

        self.assertEqual(
            unquote(choice["query_string"]).replace("+", " "),
            "?datetime__gte=%s&datetime__lt=%s"
            % (
                self.today.strftime("%Y-%m-%d %H:%M:%S"),
                self.tomorrow.strftime("%Y-%m-%d %H:%M:%S"),
            ),
        )

        request = self.request_factory.get(
            "/",
            {
                "datetime__gte": self.today.replace(day=1),
                "datetime__lt": self.next_month,
            },
        )
        request.user = AnonymousUser()
        changelist = self.get_changelist(request, BarTime, modeladmin)

    def get_changelist(self, request, model, modeladmin):
        args = [
            request,
            model,
            modeladmin.list_display,
            modeladmin.list_display_links,
            modeladmin.list_filter,
            modeladmin.date_hierarchy,
            modeladmin.search_fields,
            modeladmin.list_select_related,
            modeladmin.list_per_page,
            modeladmin.list_max_show_all,
            modeladmin.list_editable,
            modeladmin,
            modeladmin.sortable_by,
            modeladmin.search_help_text,
        ]
        return ChangeList(*args)
