#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""سرور دانلود مستقیم NEXUS HQ — اندروید + ویندوز، با هدرهای صحیح."""
import http.server
import socketserver
import os
import hashlib

DIR = '/home/user/dl'
APK = 'application/vnd.android.package-archive'
EXE = 'application/vnd.microsoft.portable-executable'

FILES = {
    '/NexusHQ.apk':          (APK,               'NexusHQ.apk'),
    '/NexusHQ-Android.zip':  ('application/zip',  'NexusHQ-Android.zip'),
    '/NexusHQ-Setup.exe':    (EXE,               'NexusHQ-Setup.exe'),
    '/NexusHQ-Portable.exe': (EXE,               'NexusHQ-Portable.exe'),
}

_cache = {}


def info(name):
    if name not in _cache:
        p = os.path.join(DIR, name)
        with open(p, 'rb') as f:
            d = f.read()
        _cache[name] = (len(d), hashlib.sha256(d).hexdigest())
    return _cache[name]


def mb(n):
    return f'{n / 1048576:.1f} MB'


CSS = """
*{box-sizing:border-box}
body{margin:0;background:#08090c;color:#e8eaf0;
font-family:system-ui,'Segoe UI',Tahoma,sans-serif;line-height:1.9;padding:26px 16px 70px}
.w{max-width:640px;margin:0 auto}
h1{font-size:22px;margin:0 0 4px}
h2{font-size:15px;margin:30px 0 8px;color:#fff}
.s{color:#8b93a7;font-size:13.5px;margin-bottom:22px}
a.btn{display:block;text-decoration:none;background:linear-gradient(135deg,#6366f1,#8b5cf6);
color:#fff;border-radius:14px;padding:16px 20px;margin:12px 0;box-shadow:0 8px 26px rgba(99,102,241,.28)}
a.btn.alt{background:#171b24;border:1px solid #2a2f3c;box-shadow:none}
.t{font-size:16px;font-weight:700}
.d{font-size:12.5px;opacity:.85;margin-top:3px}
.card{background:#11141b;border:1px solid #1e2330;border-radius:14px;padding:14px 16px;margin:16px 0}
.k{font-size:12px;color:#8b93a7}
.v{font-family:ui-monospace,monospace;font-size:11px;direction:ltr;text-align:left;
word-break:break-all;color:#a5b0ff;background:#0d1017;border:1px solid #1e2330;
border-radius:8px;padding:8px 10px;margin-top:5px}
ol{padding-inline-start:20px;font-size:14px;color:#cdd2de}
li{margin:7px 0}
.warn{border-inline-start:3px solid #f59e0b;background:rgba(245,158,11,.08);
border-radius:0 10px 10px 0;padding:11px 15px;font-size:13.5px;margin:14px 0}
.new{display:inline-block;background:rgba(34,197,94,.15);color:#4ade80;border:1px solid rgba(34,197,94,.35);
border-radius:999px;padding:1px 9px;font-size:11px;margin-inline-start:6px;vertical-align:middle}
"""


def page():
    a_sz, a_sha = info('NexusHQ.apk')
    z_sz, _ = info('NexusHQ-Android.zip')
    s_sz, s_sha = info('NexusHQ-Setup.exe')
    p_sz, _ = info('NexusHQ-Portable.exe')
    return f"""<!doctype html><html lang="fa" dir="rtl"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>دانلود NEXUS HQ</title><style>{CSS}</style></head><body><div class="w">
<h1>NEXUS HQ</h1>
<div class="s">مرکز فرماندهی شخصی — نسخه‌ی ۱٫۰٫۰ <span class="new">به‌روزرسانی جدید</span></div>

<div class="card" style="border-color:#2a3550">
<b>تازه‌ها در این نسخه</b>
<ol style="margin:8px 0 0">
<li>قفل برنامه با رمز عبور و اثر انگشت (مثل تلگرام)</li>
<li>پوسته‌ی روشن و تیره + پیروی خودکار از تنظیم گوشی/ویندوز</li>
<li>طراحی شیشه‌ای و نوار ناوبری پایین مخصوص گوشی</li>
<li>رفع بریدگی فرم‌های بلند در پنجره‌های کوچک</li>
<li>آیکون برنامه با لوگوی خودتان</li>
</ol></div>

<h2>گوشی اندروید</h2>
<a class="btn" href="/NexusHQ.apk" download>
  <div class="t">دانلود مستقیم APK</div>
  <div class="d">{mb(a_sz)} — روی همین دکمه بزنید، بعد فایل را باز کنید</div></a>
<a class="btn alt" href="/NexusHQ-Android.zip" download>
  <div class="t">اگر دانلود APK مسدود شد → ZIP</div>
  <div class="d">{mb(z_sz)} — از حالت فشرده خارج کنید و APK داخلش را نصب کنید</div></a>

<div class="warn"><b>هنگام نصب:</b> اندروید می‌پرسد «نصب از منبع ناشناس».
تنظیمات ← «اجازه از این منبع» را روشن کنید ← بازگشت ← نصب.
اگر Play Protect هشدار داد، «به‌هرحال نصب کن» را بزنید.</div>

<h2>ویندوز</h2>
<a class="btn" href="/NexusHQ-Setup.exe" download>
  <div class="t">نصب‌کننده‌ی ویندوز</div>
  <div class="d">{mb(s_sz)} — نصب عادی با میان‌بر دسکتاپ و منوی استارت</div></a>
<a class="btn alt" href="/NexusHQ-Portable.exe" download>
  <div class="t">نسخه‌ی قابل حمل (بدون نصب)</div>
  <div class="d">{mb(p_sz)} — یک فایل، مستقیم اجرا می‌شود</div></a>

<div class="warn">ویندوز ممکن است «Windows protected your PC» نشان دهد
(چون گواهی امضای کد پولی است و ما رایگان کار می‌کنیم).
روی <b>More info</b> ← <b>Run anyway</b> بزنید.</div>

<div class="card">
<div class="k">SHA-256 — فایل APK</div><div class="v">{a_sha}</div>
<div class="k" style="margin-top:10px">SHA-256 — نصب‌کننده‌ی ویندوز</div><div class="v">{s_sha}</div>
</div>

<div class="card">
<b>همگام‌سازی بین ویندوز و گوشی</b>
<ol style="margin:8px 0 0">
<li>در ویندوز: تنظیمات ← همگام‌سازی ابری ← توکن گیت‌هاب را بچسبانید ← «اتصال و آزمایش»</li>
<li>«کپی شناسه» را بزنید تا Gist ID کپی شود</li>
<li>در گوشی: همان توکن + شناسه را وارد کنید ← «دریافت از ابر»</li>
</ol></div>
</div></body></html>"""


class H(http.server.BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'

    def log_message(self, fmt, *args):
        print(f'{self.address_string()} — {fmt % args}', flush=True)

    def _send(self, code, body, ctype, extra=None):
        self.send_response(code)
        self.send_header('Content-Type', ctype)
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Cache-Control', 'no-store')
        for k, v in (extra or {}).items():
            self.send_header(k, v)
        self.end_headers()
        if self.command != 'HEAD':
            self.wfile.write(body)

    def do_HEAD(self):
        self.do_GET()

    def do_GET(self):
        path = self.path.split('?')[0]
        if path in ('/', '/index.html'):
            self._send(200, page().encode('utf-8'), 'text/html; charset=utf-8')
            return
        if path in FILES:
            ctype, name = FILES[path]
            full = os.path.join(DIR, name)
            size = os.path.getsize(full)
            # پشتیبانی از Range تا دانلود نیمه‌کاره ادامه پیدا کند
            rng = self.headers.get('Range')
            start, end = 0, size - 1
            code = 200
            if rng and rng.startswith('bytes='):
                try:
                    s, _, e = rng[6:].partition('-')
                    start = int(s) if s else 0
                    end = int(e) if e else size - 1
                    code = 206
                except ValueError:
                    code = 200
            length = end - start + 1
            self.send_response(code)
            self.send_header('Content-Type', ctype)
            self.send_header('Content-Length', str(length))
            self.send_header('Content-Disposition', f'attachment; filename="{name}"')
            self.send_header('Accept-Ranges', 'bytes')
            if code == 206:
                self.send_header('Content-Range', f'bytes {start}-{end}/{size}')
            self.end_headers()
            if self.command == 'HEAD':
                return
            with open(full, 'rb') as f:
                f.seek(start)
                left = length
                while left > 0:
                    chunk = f.read(min(262144, left))
                    if not chunk:
                        break
                    try:
                        self.wfile.write(chunk)
                    except (BrokenPipeError, ConnectionResetError):
                        return
                    left -= len(chunk)
            return
        self._send(404, b'not found', 'text/plain; charset=utf-8')


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


if __name__ == '__main__':
    for n in ('NexusHQ.apk', 'NexusHQ-Android.zip', 'NexusHQ-Setup.exe', 'NexusHQ-Portable.exe'):
        sz, sha = info(n)
        print(f'{n:24} {mb(sz):>10}  {sha[:16]}…', flush=True)
    with Server(('0.0.0.0', 3000), H) as httpd:
        print('serving on 0.0.0.0:3000', flush=True)
        httpd.serve_forever()
