import requests, time
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from jnius import autoclass, cast
from plyer import vibrator

# 📌 Türkiye 81 İl ve Diyanet location_id
TURKIYE_ILLER = {
    "Adana": 9201, "Adıyaman": 9202, "Afyonkarahisar": 9203, "Ağrı": 9204, "Amasya": 9205,
    "Ankara": 9206, "Antalya": 9207, "Artvin": 9208, "Aydın": 9209, "Balıkesir": 9210,
    "Bilecik": 9211, "Bingöl": 9212, "Bitlis": 9213, "Bolu": 9214, "Burdur": 9215,
    "Bursa": 9216, "Çanakkale": 9217, "Çankırı": 9218, "Çorum": 9219, "Denizli": 9220,
    "Diyarbakır": 9221, "Edirne": 9222, "Elazığ": 9223, "Erzincan": 9224, "Erzurum": 9225,
    "Eskişehir": 9226, "Gaziantep": 9227, "Giresun": 9228, "Gümüşhane": 9229, "Hakkari": 9230,
    "Hatay": 9231, "Isparta": 9232, "Mersin": 9233, "İstanbul": 9541, "İzmir": 9877,
    "Kars": 9236, "Kastamonu": 9237, "Kayseri": 9238, "Kırklareli": 9239, "Kırşehir": 9240,
    "Kocaeli": 9241, "Konya": 9242, "Kütahya": 9243, "Malatya": 9244, "Manisa": 9245,
    "Kahramanmaraş": 9246, "Mardin": 9247, "Muğla": 9248, "Muş": 9789, "Nevşehir": 9250,
    "Niğde": 9770, "Ordu": 9252, "Rize": 9253, "Sakarya": 9254, "Samsun": 9255,
    "Siirt": 9256, "Sinop": 9257, "Sivas": 9258, "Tekirdağ": 9259, "Tokat": 9260,
    "Trabzon": 9261, "Tunceli": 9262, "Şanlıurfa": 9263, "Uşak": 9264, "Van": 9265,
    "Yozgat": 9266, "Zonguldak": 9267, "Aksaray": 9898, "Bayburt": 9899, "Karaman": 9900,
    "Kırıkkale": 9901, "Batman": 9902, "Şırnak": 9932, "Bartın": 9904, "Ardahan": 9905,
    "Iğdır": 9906, "Yalova": 9907, "Karabük": 9908, "Kilis": 9909, "Osmaniye": 9910, "Düzce": 9911
}

# 📌 Ülke & Şehir listeleri
COUNTRIES = {
    "Türkiye": TURKIYE_ILLER,
    "Almanya": {
        "Berlin": "Berlin,DE", "Hamburg": "Hamburg,DE", "Münih": "Munich,DE", "Köln": "Cologne,DE",
        "Frankfurt": "Frankfurt,DE", "Stuttgart": "Stuttgart,DE"
    },
    "Amerika": {
        "New York": "New York,US", "Los Angeles": "Los Angeles,US",
        "Chicago": "Chicago,US", "Washington": "Washington,US"
    },
    "İngiltere": {
        "Londra": "London,GB", "Manchester": "Manchester,GB", "Birmingham": "Birmingham,GB"
    },
    "Avusturya": {
        "Viyana": "Vienna,AT", "Salzburg": "Salzburg,AT", "Linz": "Linz,AT"
    },
    "Hollanda": {
        "Amsterdam": "Amsterdam,NL", "Rotterdam": "Rotterdam,NL", "Lahey": "The Hague,NL"
    }
}

# 📐 Dinamik font
screen_w, screen_h = Window.size
TITLE_FONT = int(screen_h * 0.04)   # saat küçültüldü
SPINNER_FONT = int(screen_h * 0.04)
BIG_FONT   = int(screen_h * 0.04)

# ✅ Android Bildirim
def android_notify(title, message):
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    NotificationBuilder = autoclass('android.app.Notification$Builder')
    NotificationManager = autoclass('android.app.NotificationManager')
    Context = autoclass('android.content.Context')

    app_context = PythonActivity.mActivity.getApplicationContext()
    builder = NotificationBuilder(app_context)
    builder.setContentTitle(title)
    builder.setContentText(message)
    builder.setSmallIcon(0x1080093)

    nm = cast(NotificationManager, app_context.getSystemService(Context.NOTIFICATION_SERVICE))

    BuildVersion = autoclass("android.os.Build$VERSION")
    if int(BuildVersion.SDK_INT) >= 26:
        NotificationChannel = autoclass("android.app.NotificationChannel")
        channel_id = "ezan_channel"
        importance = NotificationManager.IMPORTANCE_DEFAULT
        channel = NotificationChannel(channel_id, "Ezan Bildirimleri", importance)
        nm.createNotificationChannel(channel)
        builder.setChannelId(channel_id)

    notification = builder.build()
    nm.notify(1, notification)

    try:
        vibrator.vibrate(0.3)
    except:
        pass

class EzanApp(App):
    def build(self):
        root = FloatLayout()

        # 🌄 Arka plan
        bg = Image(source="Namazvakit.jpg", allow_stretch=True, keep_ratio=False)
        root.add_widget(bg)

        # 📌 Ana düzen
        main_layout = BoxLayout(orientation="vertical", spacing=10, padding=20)

        # 🔹 Dinamik saat
        self.clock_label = Label(
            text=time.strftime("%d.%m.%Y - %H:%M:%S"),
            font_size=TITLE_FONT,
            color=(1,1,0.8,1),
            bold=True,
            size_hint_y=0.12,
            halign="center",
            valign="middle"
        )
        self.clock_label.bind(size=self.clock_label.setter("text_size"))
        Clock.schedule_interval(self.update_clock, 1)

        # 🔹 Ülke seçici
        self.country_spinner = Spinner(
            text="Ülke Seçiniz",
            values=list(COUNTRIES.keys()),
            size_hint_y=0.12,
            background_color=(0.1,0.1,0.1,0.7),
            color=(1,1,1,1),
            font_size=SPINNER_FONT
        )
        self.country_spinner.bind(text=self.on_country_select)

        # 🔹 Şehir seçici
        self.city_spinner = Spinner(
            text="Önce Ülke Seçiniz",
            values=[],
            size_hint_y=0.12,
            background_color=(0.1,0.1,0.1,0.7),
            color=(1,1,1,1),
            font_size=SPINNER_FONT
        )
        self.city_spinner.bind(text=self.on_city_select)

        # 🔹 Namaz vakitleri grid
        self.grid = GridLayout(cols=2, spacing=10, padding=10, size_hint_y=0.7)
        self.labels = {}
        for vakit in ["İmsak", "Güneş", "Öğle", "İkindi", "Akşam", "Yatsı"]:
            box = BoxLayout(orientation="vertical", padding=5, spacing=5)
            lbl_name = Label(text=vakit, font_size=BIG_FONT, color=(1,0.9,0.4,1), bold=True)
            lbl_time = Label(text="--:--", font_size=BIG_FONT, color=(1,1,1,1))
            box.add_widget(lbl_name)
            box.add_widget(lbl_time)
            self.grid.add_widget(box)
            self.labels[vakit] = lbl_time

        # 📌 Elemanları ekle
        main_layout.add_widget(self.clock_label)
        main_layout.add_widget(self.country_spinner)
        main_layout.add_widget(self.city_spinner)
        main_layout.add_widget(self.grid)
        root.add_widget(main_layout)

        return root

    def update_clock(self, dt):
        self.clock_label.text = time.strftime("%d.%m.%Y - %H:%M:%S")

    def on_country_select(self, spinner, text):
        self.city_spinner.values = list(COUNTRIES[text].keys())
        self.city_spinner.text = "Şehir Seçiniz"

    def on_city_select(self, spinner, text):
        country = self.country_spinner.text
        if country not in COUNTRIES: return
        cities = COUNTRIES[country]
        if text not in cities: return
        loc_id = cities[text]

        if country == "Türkiye":
            url = f"https://prayertimes.api.abdus.dev/api/diyanet/prayertimes?location_id={loc_id}"
            try:
                resp = requests.get(url, timeout=5)
                if resp.status_code == 200:
                    times = resp.json()[0]
                    self.labels["İmsak"].text  = times['fajr']
                    self.labels["Güneş"].text  = times['sun']
                    self.labels["Öğle"].text   = times['dhuhr']
                    self.labels["İkindi"].text = times['asr']
                    self.labels["Akşam"].text  = times['maghrib']
                    self.labels["Yatsı"].text  = times['isha']
                    android_notify("Ezan Vakitleri", f"{text} için vakitler güncellendi.")
            except Exception as e:
                print("API hatası:", e)
        else:
            try:
                city_name, country_code = loc_id.split(",")
                url = f"http://api.aladhan.com/v1/timingsByCity?city={city_name}&country={country_code}&method=13"
                resp = requests.get(url, timeout=5)
                if resp.status_code == 200:
                    data = resp.json()["data"]["timings"]
                    self.labels["İmsak"].text  = data['Fajr']
                    self.labels["Güneş"].text  = data['Sunrise']
                    self.labels["Öğle"].text   = data['Dhuhr']
                    self.labels["İkindi"].text = data['Asr']
                    self.labels["Akşam"].text  = data['Maghrib']
                    self.labels["Yatsı"].text  = data['Isha']
                    android_notify("Ezan Vakitleri", f"{text} için vakitler güncellendi.")
            except Exception as e:
                print("Aladhan API hatası:", e)

if __name__ == "__main__":
    EzanApp().run()