# -*- coding: utf-8 -*-
"""Persian (Jalali) calendar functions for LibreOffice Calc."""
from datetime import date, timedelta
import uno
import unohelper
from com.sun.star.sheet import XAddIn
from org.afshin.jalali import XJalaliFunctions
from com.sun.star.lang import XLocalizable
from com.sun.star.lang import IllegalArgumentException

_IMPL = "org.afshin.jalali.JalaliCalcAddIn"
_EPOCH = date(1899, 12, 30)  # LibreOffice Calc's date serial epoch
_FIRST_NOWRUZ = date(622, 3, 21)  # 1 Farvardin of year 1, proleptic Gregorian
# 33-year rule plus this correction table, the same algorithm as ICU 77.1+ and ICU4X.
# It matches the astronomical calendar (52.5 E meridian) for 1178-3000 AP and
# extrapolates arithmetically outside that range.
# Years the 33-year rule calls leap but are not; the next year is leap instead.
_NON_LEAP_CORRECTION = frozenset((
    1502, 1601, 1634, 1667, 1700, 1733, 1766, 1799, 1832, 1865, 1898, 1931,
    1964, 1997, 2030, 2059, 2063, 2096, 2129, 2158, 2162, 2191, 2195, 2224,
    2228, 2257, 2261, 2290, 2294, 2323, 2327, 2356, 2360, 2389, 2393, 2422,
    2426, 2455, 2459, 2488, 2492, 2521, 2525, 2554, 2558, 2587, 2591, 2620,
    2624, 2653, 2657, 2686, 2690, 2719, 2723, 2748, 2752, 2756, 2781, 2785,
    2789, 2818, 2822, 2847, 2851, 2855, 2880, 2884, 2888, 2913, 2917, 2921,
    2946, 2950, 2954, 2979, 2983, 2987,
))


def _is_leap(year):
    if year in _NON_LEAP_CORRECTION:
        return False
    if year - 1 in _NON_LEAP_CORRECTION:
        return True
    return (25 * year + 11) % 33 < 8


def _nowruz(year):
    days = 365 * (year - 1) + (8 * year + 21) // 33
    if year - 1 in _NON_LEAP_CORRECTION:
        days -= 1
    return _FIRST_NOWRUZ + timedelta(days=days)


_LAST_DATE = _nowruz(3178) - timedelta(days=1)


def _parts(value):
    n = _integer(value, "date")
    return n // 10000, (n // 100) % 100, n % 100


def _argument_error(message, position=0):
    raise IllegalArgumentException(message, None, position)


def _integer(value, label, position=0):
    try:
        number = float(value)
        integer = int(number)
        if number != integer:
            raise ValueError
        return integer
    except (TypeError, ValueError, OverflowError):
        _argument_error("آرگومان «%s» باید عدد صحیح باشد." % label, position)


def _require_date(value, label="تاریخ شمسی", position=0):
    number = _integer(value, label, position)
    if not _valid(number):
        _argument_error("«%s» تاریخ شمسی معتبر YYYYMMDD نیست." % label, position)
    return number


def _require_year(value, label="سال", position=0):
    year = _integer(value, label, position)
    if not 1 <= year <= 3177:
        _argument_error("«%s» باید در بازهٔ ۱ تا ۳۱۷۷ باشد." % label, position)
    return year


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
            mdays = 30 if _is_leap(y) else 29
        return d <= mdays
    except Exception:
        return False


def _to_gregorian(value):
    if not _valid(value):
        raise ValueError("Invalid Jalali date")
    y, m, d = _parts(value)
    offset = (m - 1) * 31 + d - 1 if m <= 6 else 186 + (m - 7) * 30 + d - 1
    return _nowruz(y) + timedelta(days=offset)


def _from_gregorian(gdate):
    if not _FIRST_NOWRUZ <= gdate <= _LAST_DATE:
        raise ValueError("Jalali year outside supported range")
    jy = gdate.year - 621
    first = _nowruz(jy)
    if gdate < first:
        jy -= 1
        first = _nowruz(jy)
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
    return 30 if _is_leap(year) else 29


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
        if value is None or value == "":
            continue
        try:
            numeric = float(value)
        except (TypeError, ValueError, OverflowError):
            # Match Calc's date functions: text cells in a holiday range are ignored.
            continue
        if numeric == 0:
            continue
        number = _integer(numeric, "تاریخ تعطیل", 3)
        if not _valid(number):
            _argument_error("محدودهٔ تعطیلات شامل تاریخ شمسی نامعتبر است.", 3)
        result.add(_to_gregorian(number))
    return result


def _weekend_mask(value):
    if value is None or value == "":
        return "0000011"
    if isinstance(value, (int, float)):
        code = _integer(value, "آخرهفته", 2)
        weekend_codes = {
            1: "0000011", 2: "1000001", 3: "1100000", 4: "0110000",
            5: "0011000", 6: "0001100", 7: "0000110", 11: "0000001",
            12: "1000000", 13: "0100000", 14: "0010000", 15: "0001000",
            16: "0000100", 17: "0000010",
        }
        if code not in weekend_codes:
            _argument_error("کد آخرهفته باید از ۱ تا ۷ یا ۱۱ تا ۱۷ باشد.", 2)
        return weekend_codes[code]
    mask = str(value)
    if len(mask) != 7 or any(char not in "01" for char in mask) or all(c == "1" for c in mask):
        _argument_error("ماسک آخرهفته باید ۷ نویسهٔ ۰/۱ داشته باشد و دست‌کم یک روز کاری بگذارد.", 2)
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

    # Public Calc functions. Invalid arguments raise IllegalArgumentException,
    # which Calc reports as a formula error instead of a plausible-looking 0.
    def JalaliDay(self, f_date):
        return _parts(_require_date(f_date))[2]

    def JalaliMonth(self, f_date):
        return _parts(_require_date(f_date))[1]

    def JalaliYear(self, f_date):
        return _parts(_require_date(f_date))[0]

    def JalaliIsLeapYear(self, only_sal):
        year = _require_year(only_sal)
        return 1 if _is_leap(year) else 0

    def JalaliDaysInMonth(self, year_no, month_no):
        year = _require_year(year_no, "سال", 0)
        month = _integer(month_no, "ماه", 1)
        if not 1 <= month <= 12:
            _argument_error("ماه باید بین ۱ تا ۱۲ باشد.", 1)
        return _month_length(year, month)

    def JalaliIsValidDate(self, f_date):
        return 1 if _valid(f_date) else 0

    def JalaliToGregorian(self, f_date):
        return _serial(_to_gregorian(_require_date(f_date)))

    def JalaliFromGregorian(self, m_date):
        try:
            return _from_gregorian(_serial_date(m_date))
        except (TypeError, ValueError, OverflowError):
            _argument_error("ورودی باید شماره‌تاریخ معتبر Calc باشد.", 0)

    def JalaliToday(self):
        return _from_gregorian(date.today())

    def JalaliAddDays(self, f_date, add):
        current = _to_gregorian(_require_date(f_date))
        days = _integer(add, "تعداد روز", 1)
        try:
            return _from_gregorian(current + timedelta(days=days))
        except (ValueError, OverflowError):
            _argument_error("نتیجه خارج از محدودهٔ تاریخ‌های پشتیبانی‌شده است.", 1)

    def JalaliSubtractDays(self, f_date, subtract):
        current = _to_gregorian(_require_date(f_date))
        days = _integer(subtract, "تعداد روز", 1)
        try:
            return _from_gregorian(current - timedelta(days=days))
        except (ValueError, OverflowError):
            _argument_error("نتیجه خارج از محدودهٔ تاریخ‌های پشتیبانی‌شده است.", 1)

    def JalaliDaysDiff(self, from_date, to_date):
        start = _to_gregorian(_require_date(from_date, "تاریخ آغاز", 0))
        end = _to_gregorian(_require_date(to_date, "تاریخ پایان", 1))
        return (end - start).days

    def JalaliWeekday(self, f_date):
        return (_to_gregorian(_require_date(f_date)).weekday() + 2) % 7

    def JalaliWeekdayName(self, f_date):
        names = ("شنبه", "یکشنبه", "دوشنبه", "سه‌شنبه", "چهارشنبه", "پنج‌شنبه", "جمعه")
        return names[self.JalaliWeekday(f_date)]

    def JalaliMonthName(self, mah_no):
        names = ("فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور", "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند")
        month = _integer(mah_no, "ماه", 0)
        if not 1 <= month <= 12:
            _argument_error("ماه باید بین ۱ تا ۱۲ باشد.", 0)
        return names[month - 1]

    def JalaliTodayText(self):
        today = self.JalaliToday()
        return self.JalaliWeekdayName(today) + " " + self.JalaliDate(today)

    def JalaliDate(self, f_date):
        year, month, day = _parts(_require_date(f_date))
        return "%04d/%02d/%02d" % (year, month, day)

    def JalaliYearMonth(self, f_date):
        year, month, _ = _parts(_require_date(f_date))
        return year * 100 + month

    def JalaliNextMonth(self, sal_mah):
        value = _integer(sal_mah, "سال‌وماه", 0)
        year, month = divmod(value, 100)
        _require_year(year)
        if not 1 <= month <= 12:
            _argument_error("ماه باید بین ۱ تا ۱۲ باشد.", 0)
        if month == 12:
            if year == 3177:
                _argument_error("نتیجه خارج از محدودهٔ سال‌های پشتیبانی‌شده است.", 0)
            return (year + 1) * 100 + 1
        return year * 100 + month + 1

    def JalaliPreviousMonth(self, sal_mah):
        value = _integer(sal_mah, "سال‌وماه", 0)
        year, month = divmod(value, 100)
        _require_year(year)
        if not 1 <= month <= 12:
            _argument_error("ماه باید بین ۱ تا ۱۲ باشد.", 0)
        if month == 1:
            if year == 1:
                _argument_error("نتیجه خارج از محدودهٔ سال‌های پشتیبانی‌شده است.", 0)
            return (year - 1) * 100 + 12
        return year * 100 + month - 1

    def JalaliFirstWeekday(self, year_no, month_no):
        year = _require_year(year_no, "سال", 0)
        month = _integer(month_no, "ماه", 1)
        if not 1 <= month <= 12:
            _argument_error("ماه باید بین ۱ تا ۱۲ باشد.", 1)
        fdate = year * 10000 + month * 100 + 1
        return self.JalaliWeekday(fdate)

    def JalaliEDate(self, f_date, months):
        year, month, day = _parts(_require_date(f_date))
        offset = _integer(months, "ماه‌ها", 1)
        index = year * 12 + month - 1 + offset
        target_year, target_month0 = divmod(index, 12)
        target_month = target_month0 + 1
        if not 1 <= target_year <= 3177:
            _argument_error("نتیجه خارج از محدودهٔ سال‌های پشتیبانی‌شده است.", 1)
        target_day = min(day, _month_length(target_year, target_month))
        return target_year * 10000 + target_month * 100 + target_day

    def JalaliEOMonth(self, f_date, months):
        year, month, _ = _parts(_require_date(f_date))
        offset = _integer(months, "ماه‌ها", 1)
        index = year * 12 + month - 1 + offset
        target_year, target_month0 = divmod(index, 12)
        target_month = target_month0 + 1
        if not 1 <= target_year <= 3177:
            _argument_error("نتیجه خارج از محدودهٔ سال‌های پشتیبانی‌شده است.", 1)
        return target_year * 10000 + target_month * 100 + _month_length(target_year, target_month)

    def JalaliWorkday(self, start_date, days, weekend_mask=None, holidays=None):
        current = _to_gregorian(_require_date(start_date, "تاریخ آغاز", 0))
        count = _integer(days, "روزهای کاری", 1)
        holiday_dates = _holiday_set(holidays)
        mask = _weekend_mask(weekend_mask)
        step = 1 if count >= 0 else -1
        remaining = abs(count)
        if count == 0:
            return _from_gregorian(current)
        current += timedelta(days=step)
        while remaining:
            if _is_workday(current, holiday_dates, mask):
                remaining -= 1
                if remaining == 0:
                    break
            current += timedelta(days=step)
        try:
            return _from_gregorian(current)
        except ValueError:
            _argument_error("نتیجه خارج از محدودهٔ تاریخ‌های پشتیبانی‌شده است.", 1)

    def JalaliNetworkdays(self, start_date, end_date, weekend_mask=None, holidays=None):
        start = _to_gregorian(_require_date(start_date, "تاریخ آغاز", 0))
        end = _to_gregorian(_require_date(end_date, "تاریخ پایان", 1))
        mask = _weekend_mask(weekend_mask)
        holiday_dates = _holiday_set(holidays)
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


_FUNCTION_NAMES = {'JalaliDay': 'JALALI_DAY', 'JalaliMonth': 'JALALI_MONTH', 'JalaliYear': 'JALALI_YEAR', 'JalaliIsLeapYear': 'JALALI_ISLEAPYEAR', 'JalaliDaysInMonth': 'JALALI_DAYSINMONTH', 'JalaliIsValidDate': 'JALALI_ISVALIDDATE', 'JalaliToGregorian': 'JALALI_TOGREGORIAN', 'JalaliFromGregorian': 'JALALI_FROMGREGORIAN', 'JalaliToday': 'JALALI_TODAY', 'JalaliAddDays': 'JALALI_ADDDAYS', 'JalaliSubtractDays': 'JALALI_SUBTRACTDAYS', 'JalaliDaysDiff': 'JALALI_DAYSDIFF', 'JalaliWeekday': 'JALALI_WEEKDAY', 'JalaliWeekdayName': 'JALALI_WEEKDAYNAME', 'JalaliMonthName': 'JALALI_MONTHNAME', 'JalaliTodayText': 'JALALI_TODAYTEXT', 'JalaliDate': 'JALALI_DATE', 'JalaliYearMonth': 'JALALI_YEARMONTH', 'JalaliNextMonth': 'JALALI_NEXTMONTH', 'JalaliPreviousMonth': 'JALALI_PREVIOUSMONTH', 'JalaliFirstWeekday': 'JALALI_FIRSTWEEKDAY', 'JalaliEDate': 'JALALI_EDATE', 'JalaliEOMonth': 'JALALI_EOMONTH', 'JalaliWorkday': 'JALALI_WORKDAY', 'JalaliNetworkdays': 'JALALI_NETWORKDAYS'}

_META = {
    "JalaliDay": ("روز تاریخ شمسی با قالب YYYYMMDD", ["تاریخ"]),
    "JalaliMonth": ("ماه تاریخ شمسی با قالب YYYYMMDD", ["تاریخ"]),
    "JalaliYear": ("سال تاریخ شمسی با قالب YYYYMMDD", ["تاریخ"]),
    "JalaliIsLeapYear": ("اگر سال شمسی کبیسه باشد ۱ و در غیر این صورت ۰ برمی‌گرداند", ["سال"]),
    "JalaliDaysInMonth": ("تعداد روزهای ماه شمسی", ["سال", "ماه"]),
    "JalaliIsValidDate": ("اگر تاریخ شمسی YYYYMMDD معتبر باشد ۱ و در غیر این صورت ۰ برمی‌گرداند", ["تاریخ"]),
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
    "JalaliWorkday": ("تاریخ کاری شمسی پس از افزودن روزهای کاری؛ آخرهفته و تعطیلات اختیاری‌اند", ["تاریخ آغاز", "روزهای کاری", "آخرهفته (اختیاری)", "تعطیلات (اختیاری)"]),
    "JalaliNetworkdays": ("تعداد روزهای کاری شمسی بین دو تاریخ با احتساب دو سر بازه؛ آخرهفته و تعطیلات اختیاری‌اند", ["تاریخ آغاز", "تاریخ پایان", "آخرهفته (اختیاری)", "تعطیلات (اختیاری)"]),
}


def createInstance(ctx):
    return JalaliCalcAddIn(ctx)


g_ImplementationHelper = unohelper.ImplementationHelper()
g_ImplementationHelper.addImplementation(createInstance, _IMPL, ("com.sun.star.sheet.AddIn",))
