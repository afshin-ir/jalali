# افزونهٔ تاریخ جلالی برای LibreOffice Calc

این مخزن منبع افزونه و فرایند ساخت بستهٔ نصب‌پذیر OXT است.

## ساخت محلی

به LibreOffice SDK، فایل `types.rdb` همان نسخه و Python 3 نیاز است:

```sh
unoidl-write /path/to/program/types.rdb idl/org/afshin/jalali/XJalaliFunctions.idl JalaliFunctions.rdb
python3 build_package.py
```

بسته در `JalaliCalc.oxt` ساخته می‌شود. راهنمای نصب و فهرست توابع در [README-fa.txt](README-fa.txt) آمده است.

## توابع روز کاری

امضای توابع با Calc هم‌راستا شده است:

```text
JALALI_WORKDAY(startDate; days; [weekend]; [holidays])
JALALI_NETWORKDAYS(startDate; endDate; [weekend]; [holidays])
```

برای `weekend` می‌توان از ماسک هفت‌نویسه‌ای دوشنبه تا یکشنبه یا کدهای عددی Calc استفاده کرد. حذف آرگومان‌ها، آخرهفتهٔ شنبه و یکشنبه و بدون تعطیلات را به‌کار می‌برد.

## خطاها

توابع محاسباتی برای تاریخ یا آرگومان نامعتبر، خطای UNO از نوع `IllegalArgumentException` می‌دهند تا Calc آن را به خطای فرمول تبدیل کند. `JALALI_ISVALIDDATE` استثناست و برای تاریخ نامعتبر `FALSE` می‌دهد.

## انتشار

GitHub Actions برای pull request و هر push به `main`، کتابخانهٔ UNO را می‌سازد، بستهٔ OXT را تولید و ساختار ZIP آن را بررسی می‌کند. با push کردن برچسبی مانند `v1.3.0` که با نسخهٔ `description.xml` یکی باشد، همان بسته در GitHub Releases منتشر می‌شود.
