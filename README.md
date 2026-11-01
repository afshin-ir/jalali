# افزونهٔ تاریخ جلالی برای LibreOffice Calc

منبع و بستهٔ نصب‌پذیر افزونهٔ توابع تاریخ هجری شمسی.

## ساخت بسته

برای ساخت کتابخانهٔ رابط UNO به LibreOffice SDK و فایل `types.rdb` همان نسخه نیاز است:

```sh
unoidl-write /path/to/program/types.rdb idl/org/afshin/jalali/XJalaliFunctions.idl JalaliFunctions.rdb
python3 build_package.py
```

اسکریپت، فایل `JalaliCalc.oxt` را در ریشهٔ پروژه می‌سازد. راهنمای فارسی توابع و نصب در [README-fa.txt](README-fa.txt) است.

## توابع روز کاری

`JALALI_WORKDAY` و `JALALI_NETWORKDAYS` چهار آرگومان می‌گیرند: تاریخ(های) شمسی به شکل `YYYYMMDD`، محدودهٔ تعطیلات، و ماسک آخرهفته. ماسک هفت نویسه‌ای از دوشنبه تا یکشنبه است؛ `1` یعنی روز تعطیل. نمونه‌ها: `0000011` برای شنبه و یکشنبه، `0000100` برای جمعه. برای نبود تعطیلات یک محدوده از خانه‌های خالی بدهید.
