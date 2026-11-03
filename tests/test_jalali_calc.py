"""Tests for JalaliCalc.py. UNO is stubbed, so LibreOffice is not needed."""
import csv
import importlib.util
import sys
import types
import unittest
import zipfile
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = Path(__file__).resolve().parent / "data"


class IllegalArgumentException(Exception):
    def __init__(self, message, context=None, position=0):
        super().__init__(message)
        self.position = position


def _stub(name, **attributes):
    module = types.ModuleType(name)
    module.__dict__.update(attributes)
    sys.modules[name] = module


def _load_addin():
    class Helper:
        def addImplementation(self, *args):
            pass

    _stub("uno", createUnoStruct=lambda name: types.SimpleNamespace())
    _stub("unohelper", Base=type("Base", (), {}), ImplementationHelper=Helper)
    _stub("com")
    _stub("com.sun")
    _stub("com.sun.star")
    _stub("com.sun.star.sheet", XAddIn=type("XAddIn", (), {}))
    _stub(
        "com.sun.star.lang",
        XLocalizable=type("XLocalizable", (), {}),
        IllegalArgumentException=IllegalArgumentException,
    )
    _stub("org")
    _stub("org.afshin")
    _stub("org.afshin.jalali", XJalaliFunctions=type("XJalaliFunctions", (), {}))
    spec = importlib.util.spec_from_file_location("JalaliCalc", ROOT / "JalaliCalc.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


JALALI = _load_addin()
ADDIN = JALALI.JalaliCalcAddIn(None)
EPOCH = date(1899, 12, 30)


def serial(gdate):
    return (gdate - EPOCH).days


def years_csv():
    with open(DATA / "years.csv", encoding="utf-8", newline="") as source:
        return list(csv.DictReader(source))


def official_rows():
    rows = []
    for line in (DATA / "kabise-1206-1498.txt").read_text(encoding="utf-8").splitlines():
        if line.strip() and not line.startswith("#"):
            year, nowruz = line.split()
            rows.append((int(year.rstrip("*")), year.endswith("*"), date.fromisoformat(nowruz)))
    return rows


class ReferenceData(unittest.TestCase):
    def test_official_table_1206_1498(self):
        rows = official_rows()
        self.assertEqual(len(rows), 293)
        for year, leap, nowruz in rows:
            self.assertEqual(ADDIN.JalaliIsLeapYear(year), int(leap), year)
            self.assertEqual(ADDIN.JalaliToGregorian(year * 10000 + 101), serial(nowruz), year)

    def test_astronomical_years_1178_3000(self):
        rows = years_csv()
        self.assertEqual(len(rows), 1823)
        for row in rows:
            year = int(row["year"])
            nowruz = date.fromisoformat(row["nowruz_gregorian"])
            self.assertEqual(ADDIN.JalaliIsLeapYear(year), int(row["is_leap"]), year)
            self.assertEqual(ADDIN.JalaliToGregorian(year * 10000 + 101), serial(nowruz), year)
            self.assertEqual(ADDIN.JalaliFromGregorian(serial(nowruz)), year * 10000 + 101, year)
            self.assertEqual(ADDIN.JalaliWeekday(year * 10000 + 101), int(row["nowruz_weekday"]), year)

    def test_correction_years(self):
        self.assertEqual(ADDIN.JalaliIsLeapYear(1502), 0)
        self.assertEqual(ADDIN.JalaliIsLeapYear(1503), 1)
        self.assertFalse(ADDIN.JalaliIsValidDate(15021230))
        self.assertTrue(ADDIN.JalaliIsValidDate(15031230))
        self.assertEqual(ADDIN.JalaliToGregorian(15030101), serial(date(2124, 3, 20)))
        self.assertEqual(ADDIN.JalaliFromGregorian(serial(date(2124, 3, 20))), 15030101)


class FullRange(unittest.TestCase):
    def test_every_day_is_continuous_and_round_trips(self):
        current = date(622, 3, 21)
        for year in range(1, 3178):
            for month in range(1, 13):
                for day in range(1, ADDIN.JalaliDaysInMonth(year, month) + 1):
                    value = year * 10000 + month * 100 + day
                    number = serial(current)
                    if ADDIN.JalaliToGregorian(value) != number or ADDIN.JalaliFromGregorian(number) != value:
                        self.fail("mismatch at %d / %s" % (value, current))
                    current += timedelta(days=1)
        self.assertEqual(current, date(3799, 3, 21))

    def test_first_and_last_supported_days(self):
        self.assertEqual(ADDIN.JalaliFromGregorian(serial(date(622, 3, 21))), 10101)
        self.assertEqual(ADDIN.JalaliFromGregorian(serial(date(3799, 1, 1))), 31771012)
        self.assertEqual(ADDIN.JalaliFromGregorian(serial(date(3799, 3, 20))), 31771230)

    def test_results_outside_range_are_errors(self):
        for gdate in (date(622, 3, 20), date(622, 1, 1), date(600, 6, 1), date(1, 1, 1), date(3799, 3, 21)):
            with self.assertRaises(IllegalArgumentException, msg=gdate):
                ADDIN.JalaliFromGregorian(serial(gdate))
        with self.assertRaises(IllegalArgumentException):
            ADDIN.JalaliAddDays(10101, -1)
        with self.assertRaises(IllegalArgumentException):
            ADDIN.JalaliSubtractDays(10101, 1)
        with self.assertRaises(IllegalArgumentException):
            ADDIN.JalaliAddDays(31771230, 1)
        with self.assertRaises(IllegalArgumentException):
            ADDIN.JalaliWorkday(10101, -1)


class Functions(unittest.TestCase):
    def test_readme_examples(self):
        self.assertEqual(ADDIN.JalaliDay(14050810), 10)
        self.assertEqual(ADDIN.JalaliMonth(14050810), 8)
        self.assertEqual(ADDIN.JalaliYear(14050810), 1405)
        self.assertEqual(ADDIN.JalaliDaysInMonth(1405, 8), 30)
        self.assertEqual(ADDIN.JalaliToGregorian(14050810), serial(date(2026, 11, 1)))
        self.assertEqual(ADDIN.JalaliAddDays(14050810, 1), 14050811)
        self.assertEqual(ADDIN.JalaliSubtractDays(14050810, 1), 14050809)
        self.assertEqual(ADDIN.JalaliDaysDiff(14050810, 14050820), 10)
        self.assertEqual(ADDIN.JalaliWeekday(14050810), 1)
        self.assertEqual(ADDIN.JalaliWeekdayName(14050810), "یکشنبه")
        self.assertEqual(ADDIN.JalaliMonthName(8), "آبان")
        self.assertEqual(ADDIN.JalaliDate(14050810), "1405/08/10")
        self.assertEqual(ADDIN.JalaliYearMonth(14050810), 140508)
        self.assertEqual(ADDIN.JalaliNextMonth(140508), 140509)
        self.assertEqual(ADDIN.JalaliPreviousMonth(140508), 140507)
        self.assertEqual(ADDIN.JalaliEDate(14050810, 3), 14051110)
        self.assertEqual(ADDIN.JalaliEOMonth(14050810, 0), 14050830)

    def test_weekend_codes_match_calc(self):
        names = ("mon", "tue", "wed", "thu", "fri", "sat", "sun")
        expected = {
            1: {"sat", "sun"}, 2: {"sun", "mon"}, 3: {"mon", "tue"}, 4: {"tue", "wed"},
            5: {"wed", "thu"}, 6: {"thu", "fri"}, 7: {"fri", "sat"},
            11: {"sun"}, 12: {"mon"}, 13: {"tue"}, 14: {"wed"}, 15: {"thu"}, 16: {"fri"}, 17: {"sat"},
        }
        for code, days in expected.items():
            mask = JALALI._weekend_mask(float(code))
            self.assertEqual({names[i] for i, flag in enumerate(mask) if flag == "1"}, days, code)

    def test_networkdays_with_weekend_code_2(self):
        # 14050810 is a Sunday; the week through Saturday has Sunday and Monday as weekend.
        self.assertEqual(ADDIN.JalaliNetworkdays(14050810, 14050816, 2.0), 5)

    def test_workdays_with_mask_and_holidays(self):
        self.assertEqual(ADDIN.JalaliWorkday(14050810, 5, 16.0, ((14050811.0,), (0.0,), ("text",))), 14050817)
        self.assertEqual(ADDIN.JalaliNetworkdays(14050810, 14050820), 8)
        self.assertEqual(ADDIN.JalaliNetworkdays(14050820, 14050810), -8)


class Boundaries(unittest.TestCase):
    def test_serial_with_time_stays_on_the_same_day(self):
        for gdate in (date(2026, 11, 1), date(1800, 1, 1)):
            self.assertEqual(
                ADDIN.JalaliFromGregorian(serial(gdate) + 0.5),
                ADDIN.JalaliFromGregorian(serial(gdate)),
            )

    def test_workday_outside_range_is_an_error(self):
        with self.assertRaises(IllegalArgumentException):
            ADDIN.JalaliWorkday(14050810, 1e9, "0000000")
        with self.assertRaises(IllegalArgumentException):
            ADDIN.JalaliWorkday(14050810, -1e9, "0000000")
        self.assertEqual(ADDIN.JalaliWorkday(14050810, 0), 14050810)
        self.assertEqual(ADDIN.JalaliWorkday(14050810, -1), 14050808)

    def test_month_shifts_at_range_ends(self):
        self.assertEqual(ADDIN.JalaliNextMonth(140512), 140601)
        self.assertEqual(ADDIN.JalaliPreviousMonth(140501), 140412)
        self.assertEqual(ADDIN.JalaliEDate(14031230, 12), 14041229)
        self.assertEqual(ADDIN.JalaliEOMonth(14030101, 11), 14031230)
        for call, args in (
            (ADDIN.JalaliNextMonth, (317712,)),
            (ADDIN.JalaliPreviousMonth, (101,)),
            (ADDIN.JalaliEDate, (10101, -1)),
            (ADDIN.JalaliEOMonth, (31771201, 1)),
            (ADDIN.JalaliNextMonth, (140513,)),
            (ADDIN.JalaliDaysInMonth, (1405, 13)),
            (ADDIN.JalaliMonthName, (0,)),
            (ADDIN.JalaliWorkday, (14050810, 1, 16.0, 14051301.0)),
        ):
            with self.assertRaises(IllegalArgumentException, msg=(call.__name__, args)):
                call(*args)


class Package(unittest.TestCase):
    def test_no_function_returns_boolean(self):
        # Calc reads a boolean add-in result as 0, so true results would be lost.
        idl = (ROOT / "idl/org/afshin/jalali/XJalaliFunctions.idl").read_text(encoding="utf-8")
        self.assertNotRegex(idl, r"(?m)^\s*boolean\s")
        self.assertIs(type(ADDIN.JalaliIsValidDate(14050810)), int)
        self.assertEqual(ADDIN.JalaliIsValidDate(14050810), 1)
        self.assertEqual(ADDIN.JalaliIsValidDate(14051301), 0)

    def test_tracked_package_contains_current_source(self):
        with zipfile.ZipFile(ROOT / "JalaliCalc.oxt") as package:
            self.assertEqual(package.read("JalaliCalc.py"), (ROOT / "JalaliCalc.py").read_bytes())


if __name__ == "__main__":
    unittest.main()
