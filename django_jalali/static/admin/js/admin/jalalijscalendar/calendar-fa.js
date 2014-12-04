// ** I18N

// Calendar FA language
// Author: Ali Farhadi, <a.farhadi@gmail.com>
// Encoding: UTF-8
// Distributed under the same terms as the calendar itself.

// For translators: please use UTF-8 if possible.  We strongly believe that
// Unicode is the answer to a real internationalized world.  Also please
// include your contact information in the header, as can be seen above.

// full day names
JCalendar._DN = new Array
("یکشنبه",
 "دوشنبه",
 "سه شنبه",
 "چهارشنبه",
 "پنجشنبه",
 "جمعه",
 "شنبه",
 "یکشنبه");

// Please note that the following array of short day names (and the same goes
// for short month names, _SMN) isn't absolutely necessary.  We give it here
// for exemplification on how one can customize the short day names, but if
// they are simply the first N letters of the full name you can simply say:
//
//   JCalendar._SDN_len = N; // short day name length
//   JCalendar._SMN_len = N; // short month name length
//
// If N = 3 then this is not needed either since we assume a value of 3 if not
// present, to be compatible with translation files that were written before
// this feature.

// short day names
JCalendar._SDN = new Array
("یک",
 "دو",
 "سه",
 "چهار",
 "پنج",
 "جمعه",
 "شنبه",
 "یک");

// First day of the week. "0" means display Sunday first, "1" means display
// Monday first, etc.
JCalendar._FD = 6;

// full month names
JCalendar._MN = new Array
("ژانویه",
 "فوریه",
 "مارس",
 "آوریل",
 "می",
 "جون",
 "جولای",
 "آگوست",
 "سپتامبر",
 "اکتبر",
 "نوامبر",
 "دسامبر");

// short month names
JCalendar._SMN = new Array
("Jan",
 "Feb",
 "Mar",
 "Apr",
 "May",
 "Jun",
 "Jul",
 "Aug",
 "Sep",
 "Oct",
 "Nov",
 "Dec");

 // full month names
JCalendar._JMN = new Array
("فروردین",
 "اردیبهشت",
 "خرداد",
 "تیر",
 "مرداد",
 "شهریور",
 "مهر",
 "آبان",
 "آذر",
 "دی",
 "بهمن",
 "اسفند");

// short month names
JCalendar._JSMN = new Array
("فروردین",
 "اردیبهشت",
 "خرداد",
 "تیر",
 "مرداد",
 "شهریور",
 "مهر",
 "آبان",
 "آذر",
 "دی",
 "بهمن",
 "اسفند");


// tooltips
JCalendar._TT = {};
JCalendar._TT["INFO"] = "درباره تقویم";

JCalendar._TT["ABOUT"] =
"JalaliJSCalendar\n" +
"Copyright (c) 2008 Ali Farhadi (http://farhadi.ir/)\n" + // don't translate this this ;-)
"Distributed under GNU GPL. See http://gnu.org/licenses/gpl.html for details.\n\n" +

"Based on The DHTML Calendar developed by Dynarch.com.\n" +
"(c) dynarch.com 2002-2005 / Author: Mihai Bazon\n" + // don't translate this this ;-)

"\n\n" +
"Date selection:\n" +
"- Use the \xab, \xbb buttons to select year\n" +
"- Use the " + String.fromCharCode(0x2039) + ", " + String.fromCharCode(0x203a) + " buttons to select month\n" +
"- Hold mouse button on any of the above buttons for faster selection.";
JCalendar._TT["ABOUT_TIME"] = "\n\n" +
"Time selection:\n" +
"- Click on any of the time parts to increase it\n" +
"- or Shift-click to decrease it\n" +
"- or click and drag for faster selection.";

JCalendar._TT["PREV_YEAR"] = "سال قبل (hold for menu)";
JCalendar._TT["PREV_MONTH"] = "ماه قبل (hold for menu)";
JCalendar._TT["GO_TODAY"] = "رفتن به امروز";
JCalendar._TT["NEXT_MONTH"] = "ماه بعد (hold for menu)";
JCalendar._TT["NEXT_YEAR"] = "سال بعد (hold for menu)";
JCalendar._TT["SEL_DATE"] = "انتخاب تاریخ";
JCalendar._TT["DRAG_TO_MOVE"] = "Drag to move";
JCalendar._TT["PART_TODAY"] = " (امروز)";

// the following is to inform that "%s" is to be the first day of week
// %s will be replaced with the day name.
JCalendar._TT["DAY_FIRST"] = "ابتدا %s نمایش داده شود";

JCalendar._TT["SELECT_COLUMN"] = "انتخاب تمام %s‌های این ماه";
JCalendar._TT["SELECT_ROW"] = "انتخاب روزهای این هفته";

// This may be locale-dependent.  It specifies the week-end days, as an array
// of comma-separated numbers.  The numbers are from 0 to 6: 0 means Sunday, 1
// means Monday, etc.
JCalendar._TT["WEEKEND"] = "5";

JCalendar._TT["CLOSE"] = "بستن";
JCalendar._TT["TODAY"] = "امروز";
JCalendar._TT["TIME_PART"] = "(Shift-)Click or drag to change value";

// date formats
JCalendar._TT["DEF_DATE_FORMAT"] = "%Y-%m-%d";
JCalendar._TT["TT_DATE_FORMAT"] = "%A, %e %b";

JCalendar._TT["WK"] = "هفته";
JCalendar._TT["TIME"] = "زمان :";

JCalendar._TT["LAM"] = "ق.ظ.";
JCalendar._TT["AM"] = "ق.ظ.";
JCalendar._TT["LPM"] = "ب.ظ.";
JCalendar._TT["PM"] = "ب.ظ.";

JCalendar._NUMBERS = ['۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹'];

JCalendar._DIR = 'rtl';