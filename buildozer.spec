[app]
# Uygulama bilgileri
title = Namaz Vakitleri
package.name = ezanvakit
package.domain = org.suayip
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

# Gereken Python kütüphaneleri
requirements = python3,kivy,requests,plyer,pyjnius

# APK ikonun
icon.filename = namazicon.png

# Ekran ayarları
orientation = portrait
fullscreen = 1

# Android sürüm ayarları
android.api = 30
android.minapi = 21
android.ndk = 21b
android.sdk = 30
android.ndk_path = $ANDROID_HOME/ndk/21.4.7075529
android.sdk_path = $ANDROID_HOME

# İzinler (uygulaman gerektiğinde açabilirsin)
android.permissions = INTERNET,VIBRATE

[buildozer]
log_level = 2
warn_on_root = 1

[publishing]
# Eğer Google Play’e yüklemek istersen burayı dolduracaksın
# android.keystore = my-release-key.keystore
# android.keyalias = myalias
# android.keypassword = %(env:KEY_PASSWORD)s
# android.storepassword = %(env:STORE_PASSWORD)s

[clean]
# Özel ayar gerekmez
