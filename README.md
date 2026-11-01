<h1 dir="rtl" align="right">توابع تاریخ هجری شمسی برای LibreOffice Calc</h1>

<p dir="rtl" align="right">این افزونه ۲۵ تابع برای خواندن، تبدیل و محاسبهٔ تاریخ‌های هجری شمسی در Calc فراهم می‌کند.</p>
<p dir="rtl" align="right"><a href="https://github.com/afshin-ir/jalali/releases/latest">دریافت آخرین نسخهٔ نصب‌پذیر</a> · <a href="https://github.com/afshin-ir/jalali/releases">دیدن همهٔ نسخه‌ها</a></p>

<h2 dir="rtl" align="right">نصب افزونه</h2>
<ol dir="rtl" align="right">
  <li>فایل <code dir="ltr">JalaliCalc.oxt</code> را از صفحهٔ Releases دریافت کنید.</li>
  <li>در LibreOffice به <bdi dir="ltr">Tools → Extension Manager</bdi> بروید و <bdi dir="ltr">Add</bdi> را بزنید.</li>
  <li>فایل OXT را انتخاب کنید و LibreOffice را ببندید و دوباره باز کنید.</li>
</ol>
<p dir="rtl" align="right">برای ارتقا، نسخهٔ قبلی افزونه را از Extension Manager حذف کنید، نسخهٔ تازه را نصب کنید و LibreOffice را دوباره راه‌اندازی کنید.</p>

<h2 dir="rtl" align="right">شیوهٔ واردکردن تاریخ شمسی</h2>
<p dir="rtl" align="right">بیشتر توابع، تاریخ شمسی را به صورت عدد <code dir="ltr">YYYYMMDD</code> می‌گیرند؛ برای نمونه <code dir="ltr">14050810</code> یعنی ۱۰ آبان ۱۴۰۵. این عدد، تاریخ سریالی Calc نیست.</p>
<p dir="rtl" align="right">در فرمول‌های چندآرگومانی، جداکننده معمولاً نقطه‌ویرگول است؛ اگر تنظیمات منطقه‌ای Calc شما ویرگول می‌خواهد، همان جداکننده را به کار ببرید.</p>
<p dir="rtl" align="right"><code dir="ltr">JALALI_TOGREGORIAN</code> تاریخ شمسی را به شماره‌تاریخ میلادی Calc تبدیل می‌کند؛ قالب سلول نتیجه را روی تاریخ بگذارید. <code dir="ltr">JALALI_FROMGREGORIAN</code> تاریخ واقعی Calc را می‌گیرد، نه متنی مانند <code dir="ltr">2026-11-01</code>.</p>

<h2 dir="rtl" align="right">فهرست همهٔ توابع</h2>

<h3 dir="rtl" align="right">اجزای تاریخ و اعتبارسنجی</h3>
<table dir="rtl" align="right">
  <thead><tr><th align="right">تابع و نمونه</th><th align="right">کاربرد و نتیجه</th></tr></thead>
  <tbody>
    <tr><td dir="ltr" align="left"><code>=JALALI_DAY(14050810)</code></td><td dir="rtl" align="right">روز ماه را می‌دهد؛ نتیجه <code dir="ltr">10</code> است.</td></tr>
    <tr><td dir="ltr" align="left"><code>=JALALI_MONTH(14050810)</code></td><td dir="rtl" align="right">شمارهٔ ماه را می‌دهد؛ نتیجه <code dir="ltr">8</code> است.</td></tr>
    <tr><td dir="ltr" align="left"><code>=JALALI_YEAR(14050810)</code></td><td dir="rtl" align="right">سال را می‌دهد؛ نتیجه <code dir="ltr">1405</code> است.</td></tr>
    <tr><td dir="ltr" align="left"><code>=JALALI_ISLEAPYEAR(1405)</code></td><td dir="rtl" align="right">کبیسه‌بودن سال شمسی را می‌سنجد؛ <code dir="ltr">1</code> یعنی کبیسه و <code dir="ltr">0</code> یعنی عادی. ورودی، سال است.</td></tr>
    <tr><td dir="ltr" align="left"><code>=JALALI_DAYSINMONTH(1405;8)</code></td><td dir="rtl" align="right">تعداد روزهای ماه را می‌دهد؛ آبان ۳۰ روز دارد. آرگومان‌ها سال و شمارهٔ ماه‌اند.</td></tr>
    <tr><td dir="ltr" align="left"><code>=JALALI_ISVALIDDATE(14050810)</code></td><td dir="rtl" align="right">اعتبار تاریخ را می‌سنجد؛ برای تاریخ معتبر <code dir="ltr">TRUE</code> و برای نامعتبر <code dir="ltr">FALSE</code> می‌دهد.</td></tr>
  </tbody>
</table>

<h3 dir="rtl" align="right">تبدیل تاریخ و تاریخ امروز</h3>
<table dir="rtl" align="right">
  <thead><tr><th align="right">تابع و نمونه</th><th align="right">کاربرد و نتیجه</th></tr></thead>
  <tbody>
    <tr><td dir="ltr" align="left"><code>=JALALI_TOGREGORIAN(14050810)</code></td><td dir="rtl" align="right">تاریخ شمسی را به شماره‌تاریخ میلادی Calc تبدیل می‌کند. قالب سلول را روی تاریخ بگذارید.</td></tr>
    <tr><td dir="ltr" align="left"><code>=JALALI_FROMGREGORIAN(A1)</code></td><td dir="rtl" align="right">تاریخ واقعی Calc در <code dir="ltr">A1</code> را به عدد شمسی <code dir="ltr">YYYYMMDD</code> تبدیل می‌کند.</td></tr>
    <tr><td dir="ltr" align="left"><code>=JALALI_TODAY()</code></td><td dir="rtl" align="right">تاریخ امروز را به شکل عدد شمسی <code dir="ltr">YYYYMMDD</code> می‌دهد.</td></tr>
    <tr><td dir="ltr" align="left"><code>=JALALI_TODAYTEXT()</code></td><td dir="rtl" align="right">تاریخ امروز را همراه با نام روز هفته و به شکل متن می‌دهد؛ مانند «یکشنبه ۱۴۰۵/۰۸/۱۰».</td></tr>
  </tbody>
</table>

<h3 dir="rtl" align="right">جابه‌جایی و فاصلهٔ روزها</h3>
<table dir="rtl" align="right">
  <thead><tr><th align="right">تابع و نمونه</th><th align="right">کاربرد و نتیجه</th></tr></thead>
  <tbody>
    <tr><td dir="ltr" align="left"><code>=JALALI_ADDDAYS(14050810;1)</code></td><td dir="rtl" align="right">یک روز به تاریخ می‌افزاید؛ نتیجه <code dir="ltr">14050811</code> است. عدد منفی روزها را کم می‌کند.</td></tr>
    <tr><td dir="ltr" align="left"><code>=JALALI_SUBTRACTDAYS(14050810;1)</code></td><td dir="rtl" align="right">یک روز از تاریخ کم می‌کند؛ نتیجه <code dir="ltr">14050809</code> است.</td></tr>
    <tr><td dir="ltr" align="left"><code>=JALALI_DAYSDIFF(14050810;14050820)</code></td><td dir="rtl" align="right">فاصلهٔ روزی «تاریخ پایان منهای تاریخ آغاز» را می‌دهد؛ نتیجه <code dir="ltr">10</code> است.</td></tr>
    <tr><td dir="ltr" align="left"><code>=JALALI_WORKDAY(14050810;5)</code></td><td dir="rtl" align="right">تاریخ ۵ روز کاری پس از تاریخ آغاز را می‌دهد؛ روز آغاز شمرده نمی‌شود. پیش‌فرض آخرهفته شنبه و یکشنبه است.</td></tr>
    <tr><td dir="ltr" align="left"><code>=JALALI_NETWORKDAYS(14050810;14050820)</code></td><td dir="rtl" align="right">تعداد روزهای کاری بازه را می‌شمارد و دو سر بازه را هم در نظر می‌گیرد. آخرهفتهٔ پیش‌فرض شنبه و یکشنبه است.</td></tr>
  </tbody>
</table>

<h3 dir="rtl" align="right">روز هفته، نام ماه و نمایش تاریخ</h3>
<table dir="rtl" align="right">
  <thead><tr><th align="right">تابع و نمونه</th><th align="right">کاربرد و نتیجه</th></tr></thead>
  <tbody>
    <tr><td dir="ltr" align="left"><code>=JALALI_WEEKDAY(14050810)</code></td><td dir="rtl" align="right">شمارهٔ روز هفته را می‌دهد: شنبه <code dir="ltr">0</code>، یکشنبه <code dir="ltr">1</code>، …، جمعه <code dir="ltr">6</code>.</td></tr>
    <tr><td dir="ltr" align="left"><code>=JALALI_WEEKDAYNAME(14050810)</code></td><td dir="rtl" align="right">نام فارسی روز هفتهٔ تاریخ را می‌دهد.</td></tr>
    <tr><td dir="ltr" align="left"><code>=JALALI_MONTHNAME(8)</code></td><td dir="rtl" align="right">نام ماه را می‌دهد؛ نتیجه «آبان» است. ورودی، شمارهٔ ماه از ۱ تا ۱۲ است.</td></tr>
    <tr><td dir="ltr" align="left"><code>=JALALI_DATE(14050810)</code></td><td dir="rtl" align="right">تاریخ را به صورت متن <code dir="ltr">YYYY/MM/DD</code> می‌دهد؛ نتیجه <code dir="ltr">1405/08/10</code> است.</td></tr>
    <tr><td dir="ltr" align="left"><code>=JALALI_YEARMONTH(14050810)</code></td><td dir="rtl" align="right">سال و ماه را به صورت عدد <code dir="ltr">YYYYMM</code> می‌دهد؛ نتیجه <code dir="ltr">140508</code> است.</td></tr>
    <tr><td dir="ltr" align="left"><code>=JALALI_FIRSTWEEKDAY(1405;8)</code></td><td dir="rtl" align="right">شمارهٔ روز هفتهٔ نخستین روز ماه را می‌دهد؛ شنبه <code dir="ltr">0</code> و جمعه <code dir="ltr">6</code> است. ورودی‌ها سال و ماه‌اند.</td></tr>
  </tbody>
</table>

<h3 dir="rtl" align="right">جابه‌جایی ماه‌ها و پایان ماه</h3>
<table dir="rtl" align="right">
  <thead><tr><th align="right">تابع و نمونه</th><th align="right">کاربرد و نتیجه</th></tr></thead>
  <tbody>
    <tr><td dir="ltr" align="left"><code>=JALALI_NEXTMONTH(140508)</code></td><td dir="rtl" align="right">ماه بعد از ورودی <code dir="ltr">YYYYMM</code> را می‌دهد؛ نتیجه <code dir="ltr">140509</code> است.</td></tr>
    <tr><td dir="ltr" align="left"><code>=JALALI_PREVIOUSMONTH(140508)</code></td><td dir="rtl" align="right">ماه پیش از ورودی <code dir="ltr">YYYYMM</code> را می‌دهد؛ نتیجه <code dir="ltr">140507</code> است.</td></tr>
    <tr><td dir="ltr" align="left"><code>=JALALI_EDATE(14050810;3)</code></td><td dir="rtl" align="right">سه ماه به تاریخ می‌افزاید؛ نتیجه <code dir="ltr">14051110</code> است. اگر روز متناظر در ماه مقصد وجود نداشته باشد، آخرین روز آن ماه را می‌دهد. عدد منفی ماه‌ها را کم می‌کند.</td></tr>
    <tr><td dir="ltr" align="left"><code>=JALALI_EOMONTH(14050810;0)</code></td><td dir="rtl" align="right">آخرین روز ماه شمسی تاریخ ورودی را می‌دهد؛ نتیجه <code dir="ltr">14050830</code> است. عدد مثبت یا منفی، ماه مقصد را جابه‌جا می‌کند.</td></tr>
  </tbody>
</table>

<h2 dir="rtl" align="right">آخرهفته و تعطیلات در محاسبهٔ روزهای کاری</h2>
<p dir="rtl" align="right">امضای این دو تابع از الگوی <code dir="ltr">WORKDAY.INTL</code> و <code dir="ltr">NETWORKDAYS.INTL</code> پیروی می‌کند:</p>
<pre dir="ltr"><code>JALALI_WORKDAY(startDate; days; [weekend]; [holidays])
JALALI_NETWORKDAYS(startDate; endDate; [weekend]; [holidays])</code></pre>
<p dir="rtl" align="right"><code dir="ltr">weekend</code> اختیاری است و می‌تواند کد عددی Calc یا ماسک هفت‌نویسه‌ای از دوشنبه تا یکشنبه باشد. در ماسک، <code dir="ltr">0</code> یعنی روز کاری و <code dir="ltr">1</code> یعنی آخرهفته. کد <code dir="ltr">1</code> یعنی شنبه و یکشنبه، <code dir="ltr">7</code> یعنی جمعه و شنبه، و <code dir="ltr">16</code> یعنی جمعهٔ تنها. نمونهٔ ماسک شنبه و یکشنبه <code dir="ltr">"0000011"</code> و نمونهٔ جمعهٔ تنها <code dir="ltr">"0000100"</code> است.</p>
<p dir="rtl" align="right"><code dir="ltr">holidays</code> هم اختیاری است و محدوده‌ای از تاریخ‌های شمسی <code dir="ltr">YYYYMMDD</code> می‌گیرد. خانه‌های خالی و متن در این محدوده نادیده گرفته می‌شوند.</p>
<pre dir="ltr"><code>=JALALI_WORKDAY(14050810;5;16;A2:A4)
=JALALI_NETWORKDAYS(14050810;14050820;"0000100";A2:A4)
=JALALI_WORKDAY(14050810;5;;A2:A4)</code></pre>
<p dir="rtl" align="right">در نمونهٔ سوم، آرگومان آخرهفته خالی است تا آخرهفتهٔ پیش‌فرض بماند و محدودهٔ تعطیلات از <code dir="ltr">A2:A4</code> خوانده شود. اگر هیچ‌کدام را نمی‌خواهید، هر دو آرگومان اختیاری را حذف کنید.</p>

<h2 dir="rtl" align="right">خطاها و محدودهٔ پشتیبانی</h2>
<p dir="rtl" align="right">تاریخ یا آرگومان نامعتبر در توابع محاسباتی خطای فرمول ایجاد می‌کند؛ نتیجهٔ نامعتبر به صورت <code dir="ltr">0</code> یا متن خالی پنهان نمی‌شود. <code dir="ltr">JALALI_ISVALIDDATE</code> استثناست و برای تاریخ نامعتبر <code dir="ltr">FALSE</code> می‌دهد. محدودهٔ محاسباتی تاریخ شمسی سال‌های ۱ تا ۳۱۷۷ است.</p>
<p dir="rtl" align="right">تبدیل سریال میلادی در نسخهٔ کنونی بر پایهٔ مبدأ پیش‌فرض Calc، یعنی <code dir="ltr">1899-12-30</code>، است. سندهایی که مبدأ تاریخ دیگری دارند ممکن است به تبدیل ویژه نیاز داشته باشند.</p>

<h2 dir="rtl" align="right">ساخت بسته از منبع</h2>
<p dir="rtl" align="right">برای توسعه به LibreOffice SDK، فایل <code dir="ltr">types.rdb</code> همان نسخه و Python 3 نیاز است:</p>
<pre dir="ltr"><code>unoidl-write /path/to/program/types.rdb idl/org/afshin/jalali/XJalaliFunctions.idl JalaliFunctions.rdb
python3 build_package.py</code></pre>
<p dir="rtl" align="right">GitHub Actions با ادغام نسخهٔ تازه در <code dir="ltr">main</code> بستهٔ OXT را می‌سازد و در Releases منتشر می‌کند. شمارهٔ نسخه در <code dir="ltr">build_package.py</code> باید به‌روز شود.</p>
