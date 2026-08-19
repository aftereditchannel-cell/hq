#!/bin/bash
# بازسازی ابزارهای ساخت پس از پاک‌شدن اسنپ‌شات
set -x
export DEBIAN_FRONTEND=noninteractive

echo "=== [1/4] electron binary ==="
cd /home/user/hq
node node_modules/electron/install.js && echo "ELECTRON_OK" || echo "ELECTRON_FAIL"

echo "=== [2/4] android sdk ==="
export JAVA_HOME=/home/user/tools/jdk-21.0.12+8
export ANDROID_HOME=/home/user/tools/android-sdk
export PATH=$JAVA_HOME/bin:$PATH
if [ ! -x "$JAVA_HOME/bin/java" ]; then
  echo "JDK MISSING - redownloading"
  mkdir -p /home/user/tools && cd /home/user/tools
  curl -sL -o jdk.tgz "https://api.adoptium.net/v3/binary/latest/21/ga/linux/x64/jdk/hotspot/normal/eclipse"
  tar xzf jdk.tgz && rm jdk.tgz
  ls -d /home/user/tools/jdk-21* 
fi
"$JAVA_HOME/bin/java" -version 2>&1 | head -2

mkdir -p "$ANDROID_HOME"
if [ ! -x "$ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager" ]; then
  cd /tmp && rm -rf cltools && mkdir cltools && cd cltools
  curl -sL -o cl.zip https://dl.google.com/android/repository/commandlinetools-linux-11076708_latest.zip
  python3 -c "import zipfile;zipfile.ZipFile('cl.zip').extractall('.')"
  mkdir -p "$ANDROID_HOME/cmdline-tools"
  rm -rf "$ANDROID_HOME/cmdline-tools/latest"
  mv cmdline-tools "$ANDROID_HOME/cmdline-tools/latest"
fi
chmod +x "$ANDROID_HOME/cmdline-tools/latest/bin/"* 2>/dev/null
yes | "$ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager" --licenses > /dev/null 2>&1
"$ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager" "platform-tools" "platforms;android-35" "build-tools;35.0.0" "build-tools;34.0.0" 2>&1 | tail -5
ls "$ANDROID_HOME/build-tools/35.0.0/" | head -20
echo "ANDROID_DONE"

echo "=== [3/4] wine ==="
sudo apt-get update -qq 2>&1 | tail -2
sudo apt-get install -y -qq --no-install-recommends wine wine64 xvfb 2>&1 | tail -5
which wine && wine --version && echo "WINE_OK" || echo "WINE_FAIL"

echo "=== [4/4] done ==="
echo "ALL_SETUP_COMPLETE"

# === [5/5] وابستگی‌های افزوده‌شده در دور بازطراحی ===
# کتابخانه‌های سیستمی که الکترون برای اجرای بدون‌سر لازم دارد
sudo apt-get install -y -qq --no-install-recommends \
  libnspr4 libnss3 libgbm1 libasound2t64 libatk1.0-0t64 libatk-bridge2.0-0t64 \
  libcups2t64 libxdamage1 libxkbcommon0 libpango-1.0-0 libcairo2 \
  libgtk-3-0t64 libnotify4 libxss1 libxtst6 xdg-utils libsecret-1-0 2>&1 | tail -2

# NSIS به لایه‌ی ۳۲ بیتی wine نیاز دارد؛ بدون آن بسته‌بندی ویندوز شکست می‌خورد
sudo dpkg --add-architecture i386
sudo apt-get update -qq
sudo apt-get install -y -qq --no-install-recommends wine32:i386 2>&1 | tail -2
rm -rf "$HOME/.wine"
XDG_RUNTIME_DIR=/tmp/xdgrt WINEDEBUG=-all DISPLAY=:99 wineboot -u 2>&1 | tail -2
ls "$HOME/.wine/drive_c/windows/syswow64/ntdll.dll" >/dev/null 2>&1 && echo "WINE32_OK" || echo "WINE32_FAIL"

# /dev/shm برای رندر الکترون لازم است (در برخی سندباکس‌ها وجود ندارد)
[ -d /dev/shm ] || sudo mkdir -p /dev/shm
mountpoint -q /dev/shm || sudo mount -t tmpfs -o size=512m tmpfs /dev/shm
sudo chmod 1777 /dev/shm

# سواپ — گریدل با افزونه‌ی Kotlin روی ۲ گیگ رم بدون سواپ کشته می‌شود
if ! swapon --show | grep -q swapfile; then
  sudo fallocate -l 4G /swapfile || sudo dd if=/dev/zero of=/swapfile bs=1M count=4096 status=none
  sudo chmod 600 /swapfile && sudo mkswap /swapfile >/dev/null && sudo swapon /swapfile
fi
free -m | head -3
echo "ALL_SETUP_COMPLETE_V2"
