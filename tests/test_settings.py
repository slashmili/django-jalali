from django.test import TestCase, override_settings

from django_jalali.settings import DEFAULTS, jalali_settings


class TestJalaliSettings(TestCase):
    def test_default_settings_loaded(self):
        for key, value in DEFAULTS.items():
            self.assertEqual(getattr(jalali_settings, key), value)

    def test_override_settings(self):
        js = ["admin/scripts/custom.js"]
        with override_settings(JALALI_SETTINGS={"ADMIN_JS_STATIC_FILES": js}):
            self.assertEqual(jalali_settings.ADMIN_JS_STATIC_FILES, js)

        self.assertEqual(
            jalali_settings.ADMIN_JS_STATIC_FILES, DEFAULTS["ADMIN_JS_STATIC_FILES"]
        )

    def test_invalid_setting_access_raise_attribute_error(self):
        with self.assertRaises(AttributeError):
            jalali_settings.INVALID_SETTING
