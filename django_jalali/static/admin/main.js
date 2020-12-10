$(function () {
    if (!$.datepicker){$ = django.jQuery;}
    $('.vjDateField').datepicker({
        dateFormat: 'yy-mm-dd',
        changeMonth: true,
        changeYear: true,
        showOn: 'button',
        buttonImage: '/static/admin/jquery.ui.datepicker.jalali/themes/base/images/icon-calendar.svg',
        buttonImageOnly: true
    });
});
