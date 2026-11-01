# -*- coding: utf-8 -*-
"""Persian (Jalali) calendar functions for LibreOffice Calc."""
from datetime import date, timedelta
import uno
import unohelper
from com.sun.star.sheet import XAddIn
from org.afshin.jalali import XJalaliFunctions
from com.sun.star.lang import XLocalizable

_IMPL = "org.afshin.jalali.JalaliCalcAddIn"
_BREAKS = (-61, 9, 38, 199, 426, 686, 756, 818, 1111, 1181, 1210,
           1635, 2060, 2097, 2192, 2262, 2324, 2394, 2456, 3178)
_EPOCH = date(1899, 12, 30)  # LibreOffice Calc's date serial epoch


def _jal_cal(jy):
    jy = int(jy)
    if jy < _BREAKS[0] or jy >= _BREAKS[-1]:
        raise ValueError("Jalali year outside supported range")
    gy = jy + 621
    leap_j, jp, jump = -14, _BREAKS[0], 0
    for jm in _BREAKS[1:]:
        jump = jm - jp
        if jy < jm:
            break
        leap_j += (jump // 33) * 8 + ((jump % 33) // 4)
        jp = jm
    n = jy - jp
    leap_j += (n // 33) * 8 + (((n % 33) + 3) // 4)
    if (jump % 33) == 4 and (jump - n) == 4:
        leap_j += 1
    leap_g = (gy // 4) - ((((gy // 100) + 1) * 3) // 4) - 150
    march = 20 + leap_j - leap_g
    if (jump - n) < 6:
        n = n - jump + ((jump + 4) // 33) * 33
    leap = ((n + 1) % 33 - 1) % 4
    if leap == -1:
        leap = 4
    return leap, gy, march


def _parts(value):
    n = int(value)
    return n // 10000, (n // 100) % 100, n % 100


def _valid(value):
    try:
        y, m, d = _parts(value)
        if y < 1 or y > 3177 or m < 1 or m > 12 or d < 1:
            return False
        if m <= 6:
            mdays = 31
        elif m <= 11:
            mdays = 30
        else:
            mdays = 30 if _jal_cal(y)[0] == 0 else 29
        return d <= mdays
    except Exception:
        return False


def _to_gregorian(value):
    if not _valid(value):
        raise ValueError("Invalid Jalali date")
    y, m, d = _parts(value)
    _, gy, march = _jal_cal(y)
    first = date(gy, 3, march)
    offset = (m - 1) * 31 + d - 1 if m <= 6 else 186 + (m - 7) * 30 + d - 1
    return first + timedelta(days=offset)


def _from_gregorian(gdate):
    jy = gdate.year - 621
    _, jgy, march = _jal_cal(jy)
    first = date(jgy, 3, march)
    if gdate < first:
        jy -= 1
        _, jgy, march = _jal_cal(jy)
        first = date(jgy, 3, march)
    k = (gdate - first).days
    if k <= 185:
        jm, jd = 1 + k // 31, k % 31 + 1
    else:
        k -= 186
        jm, jd = 7 + k // 30, k % 30 + 1
    return jy * 10000 + jm * 100 + jd


def _serial_date(serial):
    return _EPOCH + timedelta(days=int(float(serial)))


def _serial(gdate):
    return (gdate - _EPOCH).days


def _month_length(year, month):
    if month <= 6:
        return 31
    if month <= 11:
        return 30
    return 30 if _jal_cal(year)[0] == 0 else 29


def _flatten_values(value):
    if value is None:
        return
    if isinstance(value, (tuple, list)):
        for item in value:
            yield from _flatten_values(item)
    else:
        yield value


def _holiday_set(values):
    result = set()
    for value in _flatten_values(values):
        try:
            number = int(value)
        except (TypeError, ValueError, OverflowError):
            continue
        if number and _valid(number):
            result.add(_to_gregorian(number))
    return result


def _weekend_mask(value):
    mask = str(value or "0000011")
    if len(mask) != 7 or any(char not in "01" for char in mask) or all(c == "1" for c in mask):
        raise ValueError("Weekend mask must be seven 0/1 characters with at least one workday")
    return mask


def _is_workday(day, holidays, mask):
    return mask[day.weekday()] == "0" and day not in holidays


class JalaliCalcAddIn(unohelper.Base, XAddIn, XLocalizable, XJalaliFunctions):
    def __init__(self, ctx):
        self.ctx = ctx
        self.locale = uno.createUnoStruct("com.sun.star.lang.Locale")
        self.locale.Language = "fa"
        self.locale.Country = "IR"

    # XLocalizable
    def setLocale(self, locale):
        self.locale = locale

    def getLocale(self):
        return self.locale

    # XAddIn metadata
    def getProgrammaticFuntionName(self, display_name):
        token = str(display_name).split(".")[-1].casefold()
        for function_name, public_name in _FUNCTION_NAMES.items():
            if public_name.casefold() == token:
                return function_name
        return token

    def getDisplayFunctionName(self, programmatic_name):
        return _FUNCTION_NAMES.get(str(programmatic_name), "JALALI_" + str(programmatic_name).upper())

    def getFunctionDescription(self, programmatic_name):
        return _META.get(str(programmatic_name), ("تابع تقویم هجری شمسی", []))[0]

    def getProgrammaticCategoryName(self, programmatic_name):
        return "Add-In"

    def getDisplayCategoryName(self, programmatic_name):
        return "تقویم هجری شمسی"

    def getProgrammaticArgumentName(self, programmatic_name, argument):
        args = _META.get(str(programmatic_name), ("", []))[1]
        return args[argument] if 0 <= argument < len(args) else "arg" + str(argument + 1)

    def getDisplayArgumentName(self, programmatic_name, argument):
        return self.getProgrammaticArgumentName(programmatic_name, argument)

    def getArgumentDescription(self, programmatic_name, argument):
        return self.getDisplayArgumentName(programmatic_name, argument)

    # Public Calc functions. Dates are Calc serials; Jalali dates use YYYYMMDD.
    def JalaliDay(self, f_date): return int(f_date) % 100
    def JalaliMonth(self, f_date): return (int(f_date) % 10000) // 100
    def JalaliYear(self, f_date): return int(f_date) // 10000
    def JalaliIsLeapYear(self, only_sal): return 1 if _jal_cal(int(only_sal))[0] == 0 else 0
    def JalaliDaysInMonth(self, year_no, month_no):
        y, m = int(year_no), int(month_no)
        if 1 <= m <= 6: return 31
        if 7 <= m <= 11: return 30
        if m == 12: return 30 if self.JalaliIsLeapYear(y) else 29
        return 0
    def JalaliIsValidDate(self, f_date): return _valid(f_date)
    def JalaliToGregorian(self, f_date):
        try: return _serial(_to_gregorian(f_date))
        except Exception: return 0
    def JalaliFromGregorian(self, m_date):
        try: return _from_gregorian(_serial_date(m_date))
        except Exception: return 0
    def JalaliToday(self): return _from_gregorian(date.today())
    def JalaliAddDays(self, f_date, add):
        try: return _from_gregorian(_to_gregorian(f_date) + timedelta(days=int(add)))
        except Exception: return 0
    def JalaliSubtractDays(self, f_date, subtract):
        try: return _from_gregorian(_to_gregorian(f_date) - timedelta(days=int(subtract)))
        except Exception: return 0
    def JalaliDaysDiff(self, from_date, to_date):
        try: return (_to_gregorian(to_date) - _to_gregorian(from_date)).days
        except Exception: return 0
    def JalaliWeekday(self, f_date):
        try: return (_to_gregorian(f_date).weekday() + 2) % 7
        except Exception: return 0
    def JalaliWeekdayName(self, f_date):
        names = ("شنبه", "یکشنبه", "دوشنبه", "سه‌شنبه", "چهارشنبه", "پنج‌شنبه", "جمعه")
        try: return names[self.JalaliWeekday(f_date)]
        except Exception: return ""
    def JalaliMonthName(self, mah_no):
        names = ("فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور", "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند")
        m = int(mah_no)
        return names[m - 1] if 1 <= m <= 12 else ""
    def JalaliTodayText(self):
        d = self.JalaliToday()
        return self.JalaliWeekdayName(d) + " " + self.JalaliDate(d) if d else ""
    def JalaliDate(self, f_date):
        if not _valid(f_date): return ""
        y, m, d = _parts(f_date)
        return "%04d/%02d/%02d" % (y, m, d)
    def JalaliYearMonth(self, f_date):
        if not _valid(f_date): return 0
        y, m, _ = _parts(f_date)
        return y * 100 + m
    def JalaliNextMonth(self, sal_mah):
        y, m = divmod(int(sal_mah), 100)
        if not 1 <= m <= 12: return 0
        return (y + 1) * 100 + 1 if m == 12 else y * 100 + m + 1
    def JalaliPreviousMonth(self, sal_mah):
        y, m = divmod(int(sal_mah), 100)
        if not 1 <= m <= 12: return 0
        return (y - 1) * 100 + 12 if m == 1 else y * 100 + m - 1
    def JalaliFirstWeekday(self, year_no, month_no):
        fdate = int(year_no) * 10000 + int(month_no) * 100 + 1
        if not _valid(fdate): return 0
        return self.JalaliWeekday(fdate)

    def JalaliEDate(self, f_date, months):
        try:
            _to_gregorian(f_date)
            year, month, day = _parts(f_date)
            index = year * 12 + month - 1 + int(months)
            target_year, target_month0 = divmod(index, 12)
            target_month = target_month0 + 1
            target_day = min(day, _month_length(target_year, target_month))
            target = target_year * 10000 + target_month * 100 + target_day
            return target if _valid(target) else 0
        except Exception: return 0

    def JalaliEOMonth(self, f_date, months):
        try:
            _to_gregorian(f_date)
            year, month, _ = _parts(f_date)
            index = year * 12 + month - 1 + int(months)
            target_year, target_month0 = divmod(index, 12)
            target_month = target_month0 + 1
            target = target_year * 10000 + target_month * 100 + _month_length(target_year, target_month)
            return target if _valid(target) else 0
        except Exception: return 0

    def JalaliWorkday(self, start_date, days, holidays, weekend_mask):
        try:
            current = _to_gregorian(start_date)
            count = int(days)
            holiday_dates = _holiday_set(holidays)
            mask = _weekend_mask(weekend_mask)
            step = 1 if count >= 0 else -1
            remaining = abs(count)
            if count < 0:
                current += timedelta(days=step)
            while remaining:
                if _is_workday(current, holiday_dates, mask):
                    remaining -= 1
                    if remaining == 0:
                        break
                current += timedelta(days=step)
            return _from_gregorian(current)
        except Exception: return 0

    def JalaliNetworkdays(self, start_date, end_date, holidays, weekend_mask):
        try:
            start = _to_gregorian(start_date)
            end = _to_gregorian(end_date)
            holiday_dates = _holiday_set(holidays)
            mask = _weekend_mask(weekend_mask)
            sign = 1
            if end < start:
                start, end = end, start
                sign = -1
            total = 0
            current = start
            while current <= end:
                if _is_workday(current, holiday_dates, mask):
                    total += 1
                current += timedelta(days=1)
            return sign * total
        except Exception: return 0


_FUNCTION_NAMES = {'JalaliDay': 'JALALI_DAY', 'JalaliMonth': 'JALALI_MONTH', 'JalaliYear': 'JALALI_YEAR', 'JalaliIsLeapYear': 'JALALI_ISLEAPYEAR', 'JalaliDaysInMonth': 'JALALI_DAYSINMONTH', 'JalaliIsValidDate': 'JALALI_ISVALIDDATE', 'JalaliToGregorian': 'JALALI_TOGREGORIAN', 'JalaliFromGregorian': 'JALALI_FROMGREGORIAN', 'JalaliToday': 'JALALI_TODAY', 'JalaliAddDays': 'JALALI_ADDDAYS', 'JalaliSubtractDays': 'JALALI_SUBTRACTDAYS', 'JalaliDaysDiff': 'JALALI_DAYSDIFF', 'JalaliWeekday': 'JALALI_WEEKDAY', 'JalaliWeekdayName': 'JALALI_WEEKDAYNAME', 'JalaliMonthName': 'JALALI_MONTHNAME', 'JalaliTodayText': 'JALALI_TODAYTEXT', 'JalaliDate': 'JALALI_DATE', 'JalaliYearMonth': 'JALALI_YEARMONTH', 'JalaliNextMonth': 'JALALI_NEXTMONTH', 'JalaliPreviousMonth': 'JALALI_PREVIOUSMONTH', 'JalaliFirstWeekday': 'JALALI_FIRSTWEEKDAY', 'JalaliEDate': 'JALALI_EDATE', 'JalaliEOMonth': 'JALALI_EOMONTH', 'JalaliWorkday': 'JALALI_WORKDAY', 'JalaliNetworkdays': 'JALALI_NETWORKDAYS'}

_META = {
    "JalaliDay": ("روز تاریخ شمسی با قالب YYYYMMDD", ["تاریخ"]),
    "JalaliMonth": ("ماه تاریخ شمسی با قالب YYYYMMDD", ["تاریخ"]),
    "JalaliYear": ("سال تاریخ شمسی با قالب YYYYMMDD", ["تاریخ"]),
    "JalaliIsLeapYear": ("اگر سال شمسی کبیسه باشد ۱ و در غیر این صورت ۰ برمی‌گرداند", ["سال"]),
    "JalaliDaysInMonth": ("تعداد روزهای ماه شمسی", ["سال", "ماه"]),
    "JalaliIsValidDate": ("اعتبار تاریخ شمسی YYYYMMDD را بررسی می‌کند", ["تاریخ"]),
    "JalaliToGregorian": ("تاریخ شمسی YYYYMMDD را به شماره‌تاریخ میلادی Calc تبدیل می‌کند", ["تاریخ شمسی"]),
    "JalaliFromGregorian": ("شماره‌تاریخ میلادی Calc را به YYYYMMDD شمسی تبدیل می‌کند", ["تاریخ میلادی"]),
    "JalaliToday": ("تاریخ شمسی امروز را به شکل YYYYMMDD برمی‌گرداند", []),
    "JalaliAddDays": ("تعداد روز مشخصی به تاریخ شمسی می‌افزاید", ["تاریخ شمسی", "تعداد روز"]),
    "JalaliSubtractDays": ("تعداد روز مشخصی از تاریخ شمسی کم می‌کند", ["تاریخ شمسی", "تعداد روز"]),
    "JalaliDaysDiff": ("فاصلهٔ روزی تاریخ دوم نسبت به تاریخ اول", ["از تاریخ", "تا تاریخ"]),
    "JalaliWeekday": ("شمارهٔ روز هفته؛ شنبه ۰ و جمعه ۶", ["تاریخ شمسی"]),
    "JalaliWeekdayName": ("نام روز هفتهٔ تاریخ شمسی", ["تاریخ شمسی"]),
    "JalaliMonthName": ("نام ماه شمسی", ["ماه"]),
    "JalaliTodayText": ("تاریخ امروز همراه با نام روز هفته", []),
    "JalaliDate": ("تاریخ شمسی را به صورت YYYY/MM/DD می‌سازد", ["تاریخ شمسی"]),
    "JalaliYearMonth": ("سال و ماه تاریخ شمسی را به صورت YYYYMM برمی‌گرداند", ["تاریخ شمسی"]),
    "JalaliNextMonth": ("ماه بعد را از ورودی YYYYMM محاسبه می‌کند", ["سال و ماه YYYYMM"]),
    "JalaliPreviousMonth": ("ماه قبل را از ورودی YYYYMM محاسبه می‌کند", ["سال و ماه YYYYMM"]),
    "JalaliFirstWeekday": ("شمارهٔ روز هفتهٔ نخستین روز ماه؛ شنبه ۰ و جمعه ۶", ["سال", "ماه"]),
    "JalaliEDate": ("تاریخ شمسی پس از جابه‌جایی تعداد ماه؛ روز ناموجود به آخر ماه محدود می‌شود", ["تاریخ شمسی", "ماه‌ها"]),
    "JalaliEOMonth": ("آخرین روز ماه شمسی پس از جابه‌جایی تعداد ماه", ["تاریخ شمسی", "ماه‌ها"]),
    "JalaliWorkday": ("تاریخ کاری شمسی پس از افزودن روزهای کاری؛ تعطیلات یک محدودهٔ YYYYMMDD و آخرهفته ماسک ۷ رقمی دوشنبه تا یکشنبه است", ["تاریخ آغاز", "روزهای کاری", "تعطیلات", "ماسک آخرهفته"]),
    "JalaliNetworkdays": ("تعداد روزهای کاری شمسی بین دو تاریخ با احتساب دو سر بازه؛ تعطیلات یک محدودهٔ YYYYMMDD و آخرهفته ماسک ۷ رقمی دوشنبه تا یکشنبه است", ["تاریخ آغاز", "تاریخ پایان", "تعطیلات", "ماسک آخرهفته"]),
}


def createInstance(ctx):
    return JalaliCalcAddIn(ctx)


g_ImplementationHelper = unohelper.ImplementationHelper()
g_ImplementationHelper.addImplementation(createInstance, _IMPL, ("com.sun.star.sheet.AddIn",))
