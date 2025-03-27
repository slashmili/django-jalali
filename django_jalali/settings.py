from django.conf import settings
from django.core.signals import setting_changed

DEFAULTS = {
    # JavaScript static files for the admin Jalali date widget
    "ADMIN_JS_STATIC_FILES": [
        "admin/jquery.ui.datepicker.jalali/scripts/jquery-1.10.2.min.js",
        "admin/jquery.ui.datepicker.jalali/scripts/jquery.ui.core.js",
        "admin/jquery.ui.datepicker.jalali/scripts/jquery.ui.datepicker-cc.js",
        "admin/jquery.ui.datepicker.jalali/scripts/calendar.all.js",
        "admin/jquery.ui.datepicker.jalali/scripts/calendar.js",
        "admin/jquery.ui.datepicker.jalali/scripts/jquery.ui.datepicker-cc-fa.js",
        "admin/main.js",
    ],
    # CSS static files for the admin Jalali date widget
    "ADMIN_CSS_STATIC_FILES": {
        "all": [
            "admin/jquery.ui.datepicker.jalali/themes/base/jquery-ui.min.css",
            "admin/css/main.css",
        ]
    },
}


class JalaliSetting:
    def __init__(self, defaults=None):
        self._defaults = defaults or DEFAULTS
        self._attrs = set()

    @property
    def user_settings(self):
        if not hasattr(self, "_user_settings"):
            self._user_settings = getattr(settings, "JALALI_SETTINGS", {})

        return self._user_settings

    def __getattr__(self, attr):
        if attr not in self._defaults:
            raise AttributeError(f"Invalid Jalali setting: {attr}")

        try:
            val = self.user_settings[attr]
        except KeyError:
            val = self._defaults[attr]

        # Cache the result
        self._attrs.add(attr)
        setattr(self, attr, val)

        return val

    def reload(self):
        for attr in self._attrs:
            delattr(self, attr)

        self._attrs.clear()
        if hasattr(self, "_user_settings"):
            delattr(self, "_user_settings")


jalali_settings = JalaliSetting()


def reload_jalali_settings(*args, **kwargs):
    setting = kwargs["setting"]
    if setting == "JALALI_SETTINGS":
        jalali_settings.reload()


setting_changed.connect(reload_jalali_settings)
