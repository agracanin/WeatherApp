from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
from configparser import ConfigParser
import requests


config_file = 'config.ini'
config = ConfigParser()
config.read(config_file)
api_key = config['api_key']['key']

def get_weather(city):
    result = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=imperial&APPID={api_key}")
    if result:
        json = result.json()
        # (City, country, temp, temp_farenheight, icon, weather
        city = json['name']
        country = json ['sys']['country']
        temp = round(json['main']['temp'])
        icon = json ['weather'][0]['icon']
        weather = json['weather'][0]['description']
        final =(city, country, temp, icon, weather)
        return final
    else:
        return None

def search():
    city = city_text.get()
    weather = get_weather(city)
    if weather:
        location_label['text'] = '{}, {}'.format(weather[0].upper(), weather[1])
        icon_path = 'weather_icons/{}.png'.format(weather[3])
        icon_image = Image.open(icon_path)
        icon_photo = ImageTk.PhotoImage(icon_image)
        image.config(image=icon_photo)
        image.image = icon_photo
        temp_label['text'] = '{}°F'.format(weather[2])
        weather_label['text'] = weather[4].upper()
    else:
        messagebox.showerror("Error", "City {} was not found".format(city))

app = Tk()
app.configure(background='#e5e5e5')

app.title ("Weather App")
app.geometry('450x350')

heading_title = Label(app, text='THE WEATHER WIZARD', font=("Impact", 18), fg="#14213d", bg="#e5e5e5")
heading_title.pack(pady=(5,5))

city_text = StringVar()
city_entry = Entry(app, textvariable=city_text, width=25, bg="#ffffff")
city_entry.pack()

search_btn = Button(app, text="Search Weather", width=12, command=search, fg="#e5e5e5", bg="#14213d")
search_btn.pack(pady=(5,10))

location_label = Label(app, text="", font=('arial',20, 'bold','underline'), bg="#e5e5e5", fg="#14213d")
location_label.pack(pady=(5,5))

image = Label(app, bitmap='', bg="#e5e5e5")
image.pack()

temp_label = Label (app, text='', font=('bold'), bg="#e5e5e5", fg="#fca311")
temp_label.pack()

weather_label = Label(app,text="", fg="#14213d", bg="#e5e5e5")
weather_label.pack()

app.mainloop()