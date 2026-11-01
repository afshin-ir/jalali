from pathlib import Path
import zipfile

root = Path(__file__).parent
functions = [
    ("JalaliDay", "JALALI_DAY", "روز تاریخ شمسی با قالب YYYYMMDD", [("fDate", "تاریخ")]),
    ("JalaliMonth", "JALALI_MONTH", "ماه تاریخ شمسی با قالب YYYYMMDD", [("fDate", "تاریخ")]),
    ("JalaliYear", "JALALI_YEAR", "سال تاریخ شمسی با قالب YYYYMMDD", [("fDate", "تاریخ")]),
    ("JalaliIsLeapYear", "JALALI_ISLEAPYEAR", "اگر سال شمسی کبیسه باشد ۱ و در غیر این صورت ۰ برمی‌گرداند", [("onlySal", "سال")]),
    ("JalaliDaysInMonth", "JALALI_DAYSINMONTH", "تعداد روزهای ماه شمسی", [("yearNo", "سال"), ("monthNo", "ماه")]),
    ("JalaliIsValidDate", "JALALI_ISVALIDDATE", "اعتبار تاریخ شمسی YYYYMMDD را بررسی می‌کند", [("fDate", "تاریخ")]),
    ("JalaliToGregorian", "JALALI_TOGREGORIAN", "تاریخ شمسی YYYYMMDD را به شماره‌تاریخ میلادی Calc تبدیل می‌کند", [("fDate", "تاریخ شمسی")]),
    ("JalaliFromGregorian", "JALALI_FROMGREGORIAN", "شماره‌تاریخ میلادی Calc را به YYYYMMDD شمسی تبدیل می‌کند", [("mDate", "تاریخ میلادی")]),
    ("JalaliToday", "JALALI_TODAY", "تاریخ شمسی امروز را به شکل YYYYMMDD برمی‌گرداند", []),
    ("JalaliAddDays", "JALALI_ADDDAYS", "تعداد روز مشخصی به تاریخ شمسی می‌افزاید", [("fDate", "تاریخ شمسی"), ("add", "تعداد روز")]),
    ("JalaliSubtractDays", "JALALI_SUBTRACTDAYS", "تعداد روز مشخصی از تاریخ شمسی کم می‌کند", [("fDate", "تاریخ شمسی"), ("subtract", "تعداد روز")]),
    ("JalaliDaysDiff", "JALALI_DAYSDIFF", "فاصلهٔ روزی تاریخ دوم نسبت به تاریخ اول", [("fromDate", "از تاریخ"), ("toDate", "تا تاریخ")]),
    ("JalaliWeekday", "JALALI_WEEKDAY", "شمارهٔ روز هفته؛ شنبه ۰ و جمعه ۶", [("fDate", "تاریخ شمسی")]),
    ("JalaliWeekdayName", "JALALI_WEEKDAYNAME", "نام روز هفتهٔ تاریخ شمسی", [("fDate", "تاریخ شمسی")]),
    ("JalaliMonthName", "JALALI_MONTHNAME", "نام ماه شمسی", [("mahNo", "ماه")]),
    ("JalaliTodayText", "JALALI_TODAYTEXT", "تاریخ امروز همراه با نام روز هفته", []),
    ("JalaliDate", "JALALI_DATE", "تاریخ شمسی را به صورت YYYY/MM/DD می‌سازد", [("fDate", "تاریخ شمسی")]),
    ("JalaliYearMonth", "JALALI_YEARMONTH", "سال و ماه تاریخ شمسی را به صورت YYYYMM برمی‌گرداند", [("fDate", "تاریخ شمسی")]),
    ("JalaliNextMonth", "JALALI_NEXTMONTH", "ماه بعد را از ورودی YYYYMM محاسبه می‌کند", [("salMah", "سال و ماه YYYYMM")]),
    ("JalaliPreviousMonth", "JALALI_PREVIOUSMONTH", "ماه قبل را از ورودی YYYYMM محاسبه می‌کند", [("salMah", "سال و ماه YYYYMM")]),
    ("JalaliFirstWeekday", "JALALI_FIRSTWEEKDAY", "شمارهٔ روز هفتهٔ نخستین روز ماه؛ شنبه ۰ و جمعه ۶", [("yearNo", "سال"), ("monthNo", "ماه")]),
    ("JalaliEDate", "JALALI_EDATE", "تاریخ شمسی پس از جابه‌جایی تعداد ماه؛ روز ناموجود به آخر ماه محدود می‌شود", [("fDate", "تاریخ شمسی"), ("months", "ماه‌ها")]),
    ("JalaliEOMonth", "JALALI_EOMONTH", "آخرین روز ماه شمسی پس از جابه‌جایی تعداد ماه", [("fDate", "تاریخ شمسی"), ("months", "ماه‌ها")]),
    ("JalaliWorkday", "JALALI_WORKDAY", "تاریخ کاری شمسی پس از افزودن روزهای کاری؛ آخرهفته و تعطیلات اختیاری‌اند", [("startDate", "تاریخ آغاز"), ("days", "روزهای کاری"), ("weekend", "آخرهفته (اختیاری)"), ("holidays", "تعطیلات (اختیاری)")]),
    ("JalaliNetworkdays", "JALALI_NETWORKDAYS", "تعداد روزهای کاری شمسی بین دو تاریخ با احتساب دو سر بازه؛ آخرهفته و تعطیلات اختیاری‌اند", [("startDate", "تاریخ آغاز"), ("endDate", "تاریخ پایان"), ("weekend", "آخرهفته (اختیاری)"), ("holidays", "تعطیلات (اختیاری)")]),
]

xml = ['''<?xml version="1.0" encoding="UTF-8"?>
<oor:component-data xmlns:oor="http://openoffice.org/2001/registry" xmlns:xs="http://www.w3.org/2001/XMLSchema" oor:name="CalcAddIns" oor:package="org.openoffice.Office">
  <node oor:name="AddInInfo"><node oor:name="org.afshin.jalali.JalaliCalcAddIn" oor:op="replace"><node oor:name="AddInFunctions">''']
for method, display, description, params in functions:
    param_xml = "".join(
        f'<node oor:name="{internal}" oor:op="replace"><prop oor:name="DisplayName"><value xml:lang="fa">{label}</value></prop><prop oor:name="Description"><value xml:lang="fa">{label}</value></prop></node>'
        for internal, label in params
    )
    xml.append(
        f'<node oor:name="{method}" oor:op="replace">'
        f'<prop oor:name="DisplayName"><value xml:lang="en">{display}</value></prop>'
        f'<prop oor:name="CompatibilityName"><value xml:lang="en">{display}</value></prop>'
        f'<prop oor:name="Description"><value xml:lang="fa">{description}</value></prop>'
        f'<prop oor:name="Category"><value>Add-In</value></prop>'
        f'<node oor:name="Parameters">{param_xml}</node></node>'
    )
xml.append("</node></node></node></oor:component-data>")
(root / "CalcAddIns.xcu").write_text("\n".join(xml), encoding="utf-8")
(root / "description.xml").write_text('''<?xml version="1.0" encoding="UTF-8"?>
<description xmlns="http://openoffice.org/extensions/description/2006" xmlns:xlink="http://www.w3.org/1999/xlink">
  <identifier value="org.afshin.jalali.calc"/>
  <version value="1.3.1"/>
  <dependencies><lo:LibreOffice-minimal-version value="4.1" d:name="LibreOffice 4.1" xmlns:lo="http://libreoffice.org/extensions/description/2011" xmlns:d="http://openoffice.org/extensions/description/2006"/></dependencies>
  <display-name><name lang="fa">توابع تاریخ هجری شمسی برای Calc</name><name lang="en">Jalali Calendar Functions for Calc</name></display-name>
  <publisher><name lang="fa">افشین</name></publisher>
  <extension-description><src lang="fa" xlink:href="description-fa.txt"/></extension-description>
</description>
''', encoding="utf-8")
(root / "description-fa.txt").write_text(
    "افزونهٔ توابع تقویم هجری شمسی برای LibreOffice Calc. نام توابع با پیشوند JALALI_ آغاز می‌شود.\n",
    encoding="utf-8",
)
(root / "META-INF").mkdir(exist_ok=True)
(root / "META-INF" / "manifest.xml").write_text('''<?xml version="1.0" encoding="UTF-8"?>
<manifest:manifest xmlns:manifest="http://openoffice.org/2001/manifest">
  <manifest:file-entry manifest:media-type="application/vnd.sun.star.configuration-data" manifest:full-path="CalcAddIns.xcu"/>
  <manifest:file-entry manifest:media-type="application/vnd.sun.star.uno-typelibrary;type=RDB" manifest:full-path="JalaliFunctions.rdb"/>
  <manifest:file-entry manifest:media-type="application/vnd.sun.star.uno-component;type=Python" manifest:full-path="JalaliCalc.py"/>
</manifest:manifest>
''', encoding="utf-8")
(root / "README-fa.txt").write_text('''افزونهٔ توابع تاریخ هجری شمسی برای LibreOffice Calc
نسخهٔ ۱٫۳٫۱

نصب
۱. در LibreOffice از منوی ابزارها ← مدیر افزونه‌ها (Tools → Extension Manager) را باز کنید.
۲. افزودن (Add) را بزنید و فایل JalaliCalc.oxt را انتخاب کنید.
۳. نسخهٔ قبلی افزونه را ابتدا حذف کنید، سپس LibreOffice را یک‌بار ببندید و دوباره باز کنید.

استفاده
نام توابع با پیشوند JALALI_ آغاز می‌شود. نمونه:
=JALALI_DATE(14050810)           نتیجه: 1405/08/10
=JALALI_WEEKDAYNAME(14050810)    نام روز هفته
=JALALI_FROMGREGORIAN(A1)        تبدیل تاریخ میلادی Calc به YYYYMMDD شمسی
=JALALI_TOGREGORIAN(14050810)    تبدیل تاریخ شمسی به شماره‌تاریخ میلادی Calc

اگر زبان Calc جداکنندهٔ آرگومان را نقطه‌ویرگول می‌خواهد، برای توابع چندآرگومانی از ; استفاده کنید.
تاریخ شمسی در توابعی که YYYYMMDD می‌گیرند، یک عدد مانند 14050810 است. تاریخ میلادی در ورودی JALALI_FROMGREGORIAN باید مقدار تاریخ واقعی Calc باشد (نه متن تاریخ).
JALALI_TOGREGORIAN یک شماره‌تاریخ میلادی Calc برمی‌گرداند؛ قالب سلول خروجی را در صورت نیاز روی تاریخ بگذارید.

فهرست توابع
JALALI_DAY, JALALI_MONTH, JALALI_YEAR, JALALI_ISLEAPYEAR,
JALALI_DAYSINMONTH, JALALI_ISVALIDDATE, JALALI_TOGREGORIAN,
JALALI_FROMGREGORIAN, JALALI_TODAY, JALALI_ADDDAYS,
JALALI_SUBTRACTDAYS, JALALI_DAYSDIFF, JALALI_WEEKDAY,
JALALI_WEEKDAYNAME, JALALI_MONTHNAME, JALALI_TODAYTEXT,
JALALI_DATE, JALALI_YEARMONTH, JALALI_NEXTMONTH,
JALALI_PREVIOUSMONTH, JALALI_FIRSTWEEKDAY, JALALI_EDATE,
JALALI_EOMONTH, JALALI_WORKDAY, JALALI_NETWORKDAYS

توابع افزوده‌شده در نسخهٔ ۱٫۲٫۰
=JALALI_EDATE(14050810;3)                         نتیجه: 14051110
=JALALI_EOMONTH(14050810;0)                       نتیجه: 14050830
=JALALI_WORKDAY(14050810;5;"0000100";A2:A5)     نمونه با جمعه به‌عنوان آخرهفته
=JALALI_NETWORKDAYS(14050810;14050820;"0000100";A2:A5)

در دو تابع روز کاری، آرگومان سوم آخرهفته و آرگومان چهارم تعطیلات است؛ هر دو اختیاری‌اند. ماسک هفت‌نویسه‌ای از دوشنبه تا یکشنبه است: ۱ یعنی تعطیل و ۰ یعنی کاری. کدهای عددی Calc نیز پذیرفته می‌شوند: ۱ تا ۷ برای جفت‌روزهای آخرهفته و ۱۱ تا ۱۷ برای یک روز آخرهفته. برای نبود آخرهفتهٔ سفارشی یا تعطیلات، آرگومان را حذف کنید؛ برای تعطیلات بدون تغییر آخرهفته بنویسید: =JALALI_WORKDAY(14050810;5;;A2:A5). خانه‌های خالی و متن در محدودهٔ تعطیلات نادیده گرفته می‌شوند.

الگوریتم جلالی مطابق منطق ماکروی مبنا و با محدودهٔ محاسباتی سال‌های ۱ تا ۳۱۷۷ هجری شمسی است. تاریخ یا آرگومان عددی نامعتبر در توابع محاسباتی به‌صورت خطای فرمول گزارش می‌شود؛ JALALI_ISVALIDDATE برای تاریخ نامعتبر مقدار FALSE می‌دهد.
''', encoding="utf-8")

output = root / "JalaliCalc.oxt"
if output.exists():
    output.unlink()
package_files = [
    "CalcAddIns.xcu", "JalaliFunctions.rdb", "JalaliCalc.py",
    "META-INF/manifest.xml", "README-fa.txt", "description.xml",
    "description-fa.txt",
]
with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as archive:
    for relative_path in package_files:
        archive.write(root / relative_path, relative_path)
print(output)
