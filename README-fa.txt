افزونهٔ توابع تاریخ هجری شمسی برای LibreOffice Calc
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
