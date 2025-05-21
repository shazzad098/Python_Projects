import tkinter as tk
from tkinter import ttk
from utils.weather_utils import get_weather_data
from config import API_KEY
from PIL import Image, ImageTk

if 'get_weather_data' not in globals():
    def get_weather_data(city, api_key):
        print(f"Mock fetch for {city} with {api_key}")
        if city.lower() == "error": return None
        return {
            "city": city.title(), "temp": 25.99, "feels_like": 25.99,
            "humidity": 83, "description": "Haze", "emoji": "🌫️",
            "sunrise": "05:14", "sunset": "18:36",
            "weather_main": "Haze", "icon": "50d"
        }
    API_KEY = "e1775046fa012eecb8da967ec7b4aafc"

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather App")
        self.root.geometry("600x400")
        self.root.resizable(True, True)
        self.is_night_mode = False

        self.icon_images = {}
        self.load_icons()

        self.create_widgets()
        self.update_theme()

    def load_icons(self):
        icon_names = {
            "Clear": "sun.png", "Clouds": "cloud.png", "Rain": "rain.png",
            "Drizzle": "drizzle.png", "Thunderstorm": "thunderstorm.png",
            "Snow": "snow.png", "Mist": "mist.png", "Smoke": "smoke.png",
            "Haze": "haze.png", "Dust": "dust.png", "Fog": "fog.png",
            "Sand": "sand.png", "Ash": "ash.png", "Squall": "squall.png",
            "Tornado": "tornado.png"
        }
        for condition, filename in icon_names.items():
            try:
                img = Image.open(f"assets/icons/{filename}")
                img = img.resize((50, 50), Image.LANCZOS)
                self.icon_images[condition] = ImageTk.PhotoImage(img)
            except FileNotFoundError:
                print(f"Error loading icon: assets/icons/{filename} not found.")
            except Exception as e:
                print(f"Error loading icon for {condition}: {e}")

    def create_widgets(self):
        self.style = ttk.Style(self.root)

        self.header_frame = ttk.Frame(self.root)
        self.header_frame.pack(pady=10, padx=10, fill='x')

        city_label = ttk.Label(self.header_frame, text="Enter City:", font=("Arial", 14))
        city_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')

        self.city_entry = ttk.Entry(self.header_frame, width=30, font=("Arial", 12))
        self.city_entry.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        self.city_entry.bind("<Return>", self.fetch_weather_event)

        self.header_frame.grid_columnconfigure(1, weight=1)

        self.search_button = ttk.Button(self.header_frame, text="Search", command=self.fetch_weather_event)
        self.search_button.grid(row=0, column=2, padx=5, pady=5)

        self.result_frame = ttk.Frame(self.root)
        self.result_frame.pack(pady=10, padx=10, fill='both', expand=True)

        self.output_label_placeholder = ttk.Label(self.result_frame, text="Enter a city to see the weather.",
                                                 font=("Arial", 16), wraplength=550, anchor="center")
        self.output_label_placeholder.pack(expand=True, fill='both')


        self.toggle_button_frame = ttk.Frame(self.root)
        self.toggle_button_frame.pack(pady=10, padx=10, fill='x')

        self.toggle_button = ttk.Button(self.toggle_button_frame, text="Toggle Day/Night Mode", command=self.toggle_mode) # Store
        self.toggle_button.pack(expand=False)

    def update_theme(self):
        night_bg = "#1e1e2f"
        night_fg = "white"
        night_entry_bg = "#2a2a3f"
        night_button_bg = "#33334c"

        light_bg = "SystemButtonFace"
        light_fg = "SystemWindowText"
        light_entry_bg = "SystemWindow"
        light_button_bg = "SystemButtonFace"

        button_padding = (10, 5, 10, 5)
        button_borderwidth = 1

        if self.is_night_mode:
            current_bg = night_bg
            current_fg = night_fg
            current_entry_bg = night_entry_bg
            current_entry_fg = night_fg
            current_button_bg = night_button_bg
            current_button_fg = night_fg
            self.style.theme_use('clam')
        else:
            current_bg = light_bg
            current_fg = light_fg
            current_entry_bg = light_entry_bg
            current_entry_fg = light_fg
            current_button_bg = light_button_bg
            current_button_fg = light_fg
            self.style.theme_use('default')

        self.root.configure(background=current_bg)

        self.style.configure('.', background=current_bg, foreground=current_fg,
                             font=("Arial", 11))

        self.style.configure('TFrame', background=current_bg)
        self.style.configure('TLabel', background=current_bg, foreground=current_fg,
                             font=("Arial", 14))
        self.style.configure('TButton',
                             background=current_button_bg,
                             foreground=current_button_fg,
                             font=("Arial", 10),
                             padding=button_padding,
                             borderwidth=button_borderwidth,
                             relief=tk.FLAT if self.is_night_mode else tk.RAISED)

        self.style.configure('TEntry',
                             fieldbackground=current_entry_bg,
                             foreground=current_entry_fg,
                             insertcolor=current_entry_fg,
                             font=("Arial", 12))

        self.header_frame.configure(style='TFrame')
        self.result_frame.configure(style='TFrame')
        self.toggle_button_frame.configure(style='TFrame')

        if hasattr(self, 'output_label_placeholder') and self.output_label_placeholder.winfo_exists():
            self.output_label_placeholder.configure(font=("Arial", 16))


    def toggle_mode(self):
        self.is_night_mode = not self.is_night_mode
        self.update_theme()

        if hasattr(self, 'last_city_searched') and self.last_city_searched:
            self.fetch_weather_data(self.last_city_searched)


    def fetch_weather_event(self, event=None):
        city = self.city_entry.get().strip()
        if not city:
            self.display_message("Please enter a city name.")
            return
        self.last_city_searched = city
        self.fetch_weather_data(city)

    def fetch_weather_data(self, city):
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        data = get_weather_data(city, API_KEY)

        if not data:
            self.display_message(f"Error fetching weather data for {city.title()}.\nCity not found or API error.")
            return

        details_container = ttk.Frame(self.result_frame, padding=(20, 10))
        details_container.pack(expand=True, fill='both')


        if "weather_main" in data and data["weather_main"] in self.icon_images:
            icon_label = ttk.Label(details_container, image=self.icon_images[data["weather_main"]])
            icon_label.image = self.icon_images[data["weather_main"]]
            icon_label.pack(pady=(0,10))
        else:
            print(f"Icon for condition '{data.get('weather_main', 'N/A')}' not found.")

        city_name = data.get('city', 'N/A')
        city_label = ttk.Label(details_container, text=f"{city_name}", font=("Arial", 24, "bold")) # Larger city name
        city_label.pack(pady=(0, 10))

        temp_text = f"Temperature: {data.get('temp', 'N/A')}°C"
        temp_label = ttk.Label(details_container, text=temp_text, font=("Arial", 16))
        temp_label.pack(pady=3)

        feels_like_text = f"Feels Like: {data.get('feels_like', 'N/A')}°C"
        feels_like_label = ttk.Label(details_container, text=feels_like_text, font=("Arial", 16))
        feels_like_label.pack(pady=3)

        humidity_text = f"Humidity: {data.get('humidity', 'N/A')}%"
        humidity_label = ttk.Label(details_container, text=humidity_text, font=("Arial", 16))
        humidity_label.pack(pady=3)

        condition_text = f"Condition: {data.get('description', 'N/A').title()}"
        condition_label = ttk.Label(details_container, text=condition_text, font=("Arial", 16))
        condition_label.pack(pady=3)

        sunrise_text = f"Sunrise: {data.get('sunrise', 'N/A')}"
        sunrise_label = ttk.Label(details_container, text=sunrise_text, font=("Arial", 16))
        sunrise_label.pack(pady=3)

        sunset_text = f"Sunset: {data.get('sunset', 'N/A')}"
        sunset_label = ttk.Label(details_container, text=sunset_text, font=("Arial", 16))
        sunset_label.pack(pady=3)

    def display_message(self, message_text):
        for widget in self.result_frame.winfo_children():
            widget.destroy()
        msg_label = ttk.Label(self.result_frame, text=message_text,
                              font=("Arial", 16), wraplength=550, anchor="center", justify="center")
        msg_label.pack(expand=True, fill='both', padx=20, pady=20)


if __name__ == '__main__':
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()