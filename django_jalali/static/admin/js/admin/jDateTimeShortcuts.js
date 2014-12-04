// Inserts shortcut buttons after all of the following:
//     <input type="text" class="vjDateField">

var jDateTimeShortcuts = {
    timezoneWarningClass: 'timezonewarning', // class of the warning for timezone mismatch
    timezoneOffset: 0,
    admin_media_prefix: '',
    init: function () {
        // Get admin_media_prefix by grabbing it off the window object. It's
        // set in the admin/base.html template, so if it's not there, someone's
        // overridden the template. In that case, we'll set a clearly-invalid
        // value in the hopes that someone will examine HTTP requests and see it.
        if (window.__admin_media_prefix__ != undefined) {
            jDateTimeShortcuts.admin_media_prefix = window.__admin_media_prefix__;
        } else {
            jDateTimeShortcuts.admin_media_prefix = '/missing-admin-media-prefix/';
        }

        if (window.__admin_utc_offset__ != undefined) {
            var serverOffset = window.__admin_utc_offset__;
            var localOffset = new Date().getTimezoneOffset() * -60;
            jDateTimeShortcuts.timezoneOffset = localOffset - serverOffset;
        }

        var inputs = document.getElementsByTagName('input');
        for (i = 0; i < inputs.length; i++) {
            var inp = inputs[i];
            if (inp.getAttribute('type') == 'text' && inp.className.match(/vjDateField/)) {
                jDateTimeShortcuts.addCalendar(inp);
                jDateTimeShortcuts.addTimezoneWarning(inp);
            }
        }
    },
    // Add a warning when the time zone in the browser and backend do not match.
    addTimezoneWarning: function (inp) {
        var $ = django.jQuery;
        var warningClass = jDateTimeShortcuts.timezoneWarningClass;
        var timezoneOffset = jDateTimeShortcuts.timezoneOffset / 3600;

        // Only warn if there is a time zone mismatch.
        if (!timezoneOffset)
            return;

        // Check if warning is already there.
        if ($(inp).siblings('.' + warningClass).length)
            return;

        var message;
        if (timezoneOffset > 0) {
            message = ngettext(
                'Note: You are %s hour ahead of server time.',
                'Note: You are %s hours ahead of server time.',
                timezoneOffset
            );
        }
        else {
            timezoneOffset *= -1
            message = ngettext(
                'Note: You are %s hour behind server time.',
                'Note: You are %s hours behind server time.',
                timezoneOffset
            );
        }
        message = interpolate(message, [timezoneOffset]);

        var $warning = $('<span>');
        $warning.attr('class', warningClass);
        $warning.text(message);

        $(inp).parent()
            .append($('<br>'))
            .append($warning)
    },
    // Add calendar widget to a given field.
    addCalendar: function (inp) {
        // Shortcut links (calendar icon and "Today" link)
        var shortcuts_span = document.createElement('a');
        shortcuts_span.setAttribute('href', 'javascript:void(0)');
        inp.parentNode.insertBefore(shortcuts_span, inp.nextSibling);
        img_id = inp.id + '_calendar';
        quickElement('img', shortcuts_span, '', 'id', img_id, 'src', jDateTimeShortcuts.admin_media_prefix + 'img/icon_calendar.gif', 'alt', gettext('Calendar'));
        JCalendar.setup({
            inputField: inp.id,
            button: img_id,
            ifFormat: '%Y-%m-%d',
            dateType: 'jalali',
            weekNumbers: false
        });
    },
}

addEvent(window, 'load', jDateTimeShortcuts.init);
