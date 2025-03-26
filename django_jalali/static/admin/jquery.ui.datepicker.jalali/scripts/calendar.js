function mod(a, b) {return a - (b * Math.floor(a / b));}
/*
       JavaScript functions for the Fourmilab Calendar Converter

                  by John Walker  --  September, MIM
              http://www.fourmilab.ch/documents/calendar/

                This program is in the public domain.
*/

//  LEAP_GREGORIAN  --  Is a given year in the Gregorian calendar a leap year ?

function leap_gregorian(year)
{
    return ((year % 4) == 0) &&
            (!(((year % 100) == 0) && ((year % 400) != 0)));
}

//  GREGORIAN_TO_JD  --  Determine Julian day number from Gregorian calendar date

var GREGORIAN_EPOCH = 1721425.5;

function gregorian_to_jd(year, month, day)
{
    return (GREGORIAN_EPOCH - 1) +
           (365 * (year - 1)) +
           Math.floor((year - 1) / 4) +
           (-Math.floor((year - 1) / 100)) +
           Math.floor((year - 1) / 400) +
           Math.floor((((367 * month) - 362) / 12) +
           ((month <= 2) ? 0 :
                               (leap_gregorian(year) ? -1 : -2)
           ) +
           day);
}


//  JD_TO_GREGORIAN  --  Calculate Gregorian calendar date from Julian day

function jd_to_gregorian(jd) {
    var wjd, depoch, quadricent, dqc, cent, dcent, quad, dquad,
        yindex, dyindex, year, yearday, leapadj;

    wjd = Math.floor(jd) + 0.5;
    depoch = wjd - GREGORIAN_EPOCH;
    quadricent = Math.floor(depoch / 146097);
    dqc = mod(depoch, 146097);
    cent = Math.floor(dqc / 36524);
    dcent = mod(dqc, 36524);
    quad = Math.floor(dcent / 1461);
    dquad = mod(dcent, 1461);
    yindex = Math.floor(dquad / 365);
    year = (quadricent * 400) + (cent * 100) + (quad * 4) + yindex;
    if (!((cent == 4) || (yindex == 4))) {
        year++;
    }
    yearday = wjd - gregorian_to_jd(year, 1, 1);
    leapadj = ((wjd < gregorian_to_jd(year, 3, 1)) ? 0
                                                  :
                  (leap_gregorian(year) ? 1 : 2)
              );
    month = Math.floor((((yearday + leapadj) * 12) + 373) / 367);
    day = (wjd - gregorian_to_jd(year, month, 1)) + 1;

    return new Array(year, month, day);
}

/*  TEHRAN_EQUINOX  --  Determine Julian day and fraction of the
                        March equinox at the Tehran meridian in
                        a given Gregorian year.  */

function tehran_equinox(year)
{
    var equJED, equJD, equAPP, equTehran, dtTehran;

    //  March equinox in dynamical time
    equJED = equinox(year, 0);

    //  Correct for delta T to obtain Universal time
    equJD = equJED - (deltat(year) / (24 * 60 * 60));

    //  Apply the equation of time to yield the apparent time at Greenwich
    equAPP = equJD + equationOfTime(equJED);

    /*  Finally, we must correct for the constant difference between
        the Greenwich meridian andthe time zone standard for
    Iran Standard time, 52°30' to the East.  */

    dtTehran = (52 + (30 / 60.0) + (0 / (60.0 * 60.0))) / 360;
    equTehran = equAPP + dtTehran;

    return equTehran;
}


/*  TEHRAN_EQUINOX_JD  --  Calculate Julian day during which the
                           March equinox, reckoned from the Tehran
                           meridian, occurred for a given Gregorian
                           year.  */

function tehran_equinox_jd(year)
{
    var ep, epg;

    ep = tehran_equinox(year);
    epg = Math.floor(ep);

    return epg;
}

/*  PERSIANA_YEAR  --  Determine the year in the Persian
                       astronomical calendar in which a
                       given Julian day falls.  Returns an
             	       array of two elements:

                            [0]  Persian year
                            [1]  Julian day number containing
                                 equinox for this year.
*/

var PERSIAN_EPOCH = 1948320.5;
var PERSIAN_WEEKDAYS = new Array("Yekshanbeh", "Doshanbeh",
                                 "Seshhanbeh", "Chaharshanbeh",
                                 "Panjshanbeh", "Jomeh", "Shanbeh");
function persiana_year(jd)
{
    var guess = jd_to_gregorian(jd)[0] - 2,
        lasteq, nexteq, adr;

    lasteq = tehran_equinox_jd(guess);
    while (lasteq > jd) {
        guess--;
        lasteq = tehran_equinox_jd(guess);
    }
    nexteq = lasteq - 1;
    while (!((lasteq <= jd) && (jd < nexteq))) {
        lasteq = nexteq;
        guess++;
        nexteq = tehran_equinox_jd(guess);
    }
    adr = Math.round((lasteq - PERSIAN_EPOCH) / TropicalYear) + 1;

    return new Array(adr, lasteq);
}


/*  PERSIANA_TO_JD  --  Obtain Julian day from a given Persian
                    	astronomical calendar date.  */

function persiana_to_jd(year, month, day)
{
    var adr, equinox, guess, jd;

    guess = (PERSIAN_EPOCH - 1) + (TropicalYear * ((year - 1) - 1));
    adr = new Array(year - 1, 0);

    while (adr[0] < year) {
        adr = persiana_year(guess);
        guess = adr[1] + (TropicalYear + 2);
    }
    equinox = adr[1];

    jd = equinox +
            ((month <= 7) ?
                ((month - 1) * 31) :
                (((month - 1) * 30) + 6)
            ) +
            (day - 1);
    return jd;
}

/*  JD_TO_PERSIANA  --  Calculate date in the Persian astronomical
                        calendar from Julian day.  */

function jd_to_persiana(jd)
{
    var year, month, day,
        adr, equinox, yday;

    jd = Math.floor(jd) + 0.5;
    adr = persiana_year(jd);
    year = adr[0];
    equinox = adr[1];
    day = Math.floor((jd - equinox) / 30) + 1;
    
    yday = (Math.floor(jd) - persiana_to_jd(year, 1, 1)) + 1;
    month = (yday <= 186) ? Math.ceil(yday / 31) : Math.ceil((yday - 6) / 30);
    day = (Math.floor(jd) - persiana_to_jd(year, month, 1)) + 1;

    return new Array(year, month, day);
}

/*  LEAP_PERSIANA  --  Is a given year a leap year in the Persian
    	    	       astronomical calendar ?  */

function leap_persiana(year)
{
    return (persiana_to_jd(year + 1, 1, 1) -
            persiana_to_jd(year, 1, 1)) > 365;
}
