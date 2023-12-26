import os
import cv2
import webbrowser
import numpy as np
import tkinter as tk
import tensorflow as tf
import customtkinter as CTk
from tkinter import filedialog
from PIL import Image, ImageTk
from tensorflow.keras.applications.efficientnet import preprocess_input

# загрузка модели и имена классов
model = tf.keras.models.load_model('Resources/DERM_AI_11_25.h5')
classes = ['Инфекционные', 'Экзема', 'Акне (Угри)', 'Пигментные изменения', 'Доброкачественные', 'Злокачественные']

# GUI
CTk.set_appearance_mode("dark")
CTk.set_default_color_theme("green")

root = CTk.CTk()
root.title("DermAI")
root.iconbitmap('Resources/DermAI.ico')
root.resizable(False, False)
root.geometry('820x600+50+50')

top_left_frame = CTk.CTkFrame(root, fg_color='black', width=20, height=20, border_width=0)
top_left_frame.grid(row=0, column=0, rowspan=1, sticky="ns", pady=15, padx=15)

# переменная для вероятности диагноза
probability = tk.DoubleVar()
probability.set(0.5)

# фото заглушки
stub = "Resources/zaglushka_prod.jpg"

# отображение заглушки
image = cv2.imread(stub)
if image is None:
    print("""Ошибка: Невозможно загрузить изображение.""")
else:
    if len(image.shape) == 2: 
        resized_img = cv2.resize(image, (500, 500), interpolation=cv2.INTER_NEAREST)
    else:
        resized_img = cv2.resize(image, (500, 500), interpolation=cv2.INTER_AREA)

    # BGR в RGB
    if len(resized_img.shape) == 3 and resized_img.shape[2] == 3:
        resized_img = cv2.cvtColor(resized_img, cv2.COLOR_BGR2RGB)

    image = Image.fromarray(resized_img)
    image = ImageTk.PhotoImage(image)

    # вывод фото на панель
    panel = tk.Label(root, image=image, background='#242424')
    panel.grid(row=0, column=2, columnspan=2, pady=10, padx=10)




# функция для отображения ошибок
def error_msg(title, message):
    error_window = CTk.CTkToplevel(root)
    error_window.title(title)
    error_label = CTk.CTkLabel(error_window, text=message, padx=10, pady=10)
    error_label.pack()

# очистка данных
def clear_data():
    other_probability.configure(text="")

    for widget in root.winfo_children():
        if isinstance(widget, CTk.CTkLabel) and widget.grid_info()["row"] >= 6:
            widget.destroy()

    more_button.grid_forget()
    more_button.configure(fg_color="transparent", state="disabled", text=" ")

# загрузка фото и предсказание
def load_predict():
    clear_data()
    try:
        file_path = filedialog.askopenfilename()
        if file_path:
            img = cv2.imread(file_path)
            if img is not None:
                skin_disease(img)

                more_button.grid(row=13, column=0, pady=1, padx=1, sticky='s')
                more_button.configure(fg_color="green", state="enable", text="Узнать больше")
                other_probability.configure(text="Вероятности диагнозов:")
            else:
                error_msg("Ошибка", """Невозможно загрузить изображение.
    Проверьте формат фото.""")
    except Exception as e:
        error_msg("Ошибка", f"Произошла ошибка: {str(e)}")

# фото с вебки и предсказание
def web_predict():
    clear_data()
    try:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Ошибка: Невозможно открыть веб-камеру.")
            error_msg("Ошибка", "Невозможно открыть веб-камеру.")
            return

        ret, frame = cap.read()
        cap.release()

        if ret:
            skin_disease(frame)
            more_button.grid(row=13, column=0, pady=1, padx=1, sticky='s')
            more_button.configure(fg_color="green", state="enable", text="Узнать больше")
            other_probability.configure(text="Вероятности диагнозов:")
        else:
            print("Ошибка: Невозможно получить кадр с веб-камеры.")
            error_msg("Ошибка", "Невозможно получить кадр с веб-камеры.")
    except Exception as e:
        error_msg("Ошибка", f"Произошла ошибка: {str(e)}")


# преобразование фото и предсказание
def skin_disease(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(img)
    resized_img = pil_image.resize((224, 224))
    img = np.array(resized_img)
    display_resized_img(img)
    predict_disease(img)

# ф-я предсказания диагноза
def predict_disease(frame):
    processed_img = preproc_img(frame)
    prediction = model.predict(processed_img)
    clear_data()
    disease_class = np.argmax(prediction)
    confidence = prediction[0][disease_class]
    disease_name = classes[disease_class]
    disease_label.configure(text=f"Прогноз: {disease_name}, Точность: {confidence * 100:.2f}%")
    probability.set(confidence * 100)
    display_probabilities(prediction)

# обработка фото перед подачей на вход модели
def preproc_img(image):
    processed_img = cv2.resize(image, (224, 224))
    processed_img = preprocess_input(processed_img)
    processed_img = np.expand_dims(processed_img, axis=0)
    return processed_img

# отображаем фото
def display_resized_img(image):
    image = np.array(image)
    resized_img = cv2.resize(image, (500, 500), interpolation=cv2.INTER_AREA)
    resized_img = cv2.cvtColor(resized_img, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(resized_img)
    image = ImageTk.PhotoImage(image)
    panel.config(image=image)
    panel.image = image

# вероятности диагнозов
def display_probabilities(prediction):
    for widget in top_left_frame.winfo_children():
        if isinstance(widget, CTk.CTkLabel) and widget.grid_info()["row"] >= 6:
            widget.destroy()
    sorted_indices = np.argsort(prediction[0])[::-1]
    for i, idx in enumerate(sorted_indices[1:]):
        probability = prediction[0][idx]
        disease_name = classes[idx]
        label_text = f"{disease_name}: {probability * 100:.2f}%"
        other_probability = CTk.CTkLabel(top_left_frame, text=label_text)
        other_probability.grid(row=6 + i, column=0, columnspan=1, sticky='nw', pady=2, padx=3)

# открывем доп.инф. по диагнозу в браузере
def open_link():
    disease_name = disease_label.cget("text").split(": ")[1].split(",")[0]
    links = {
        'Инфекционные': 'https://www.msdmanuals.com/ru/%D0%B4%D0%BE%D0%BC%D0%B0/%D0%BA%D0%BE%D0%B6%D0%BD%D1%8B%D0%B5-%D0%B7%D0%B0%D0%B1%D0%BE%D0%BB%D0%B5%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F/%D0%B1%D0%B0%D0%BA%D1%82%D0%B5%D1%80%D0%B8%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D0%B5-%D0%BA%D0%BE%D0%B6%D0%BD%D1%8B%D0%B5-%D0%B8%D0%BD%D1%84%D0%B5%D0%BA%D1%86%D0%B8%D0%B8/%D1%84%D0%BB%D0%B5%D0%B3%D0%BC%D0%BE%D0%BD%D0%B0',
        'Экзема': 'https://www.msdmanuals.com/ru/%D0%B4%D0%BE%D0%BC%D0%B0/%D0%BA%D0%BE%D0%B6%D0%BD%D1%8B%D0%B5-%D0%B7%D0%B0%D0%B1%D0%BE%D0%BB%D0%B5%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F/%D0%B7%D1%83%D0%B4-%D0%B8-%D0%B4%D0%B5%D1%80%D0%BC%D0%B0%D1%82%D0%B8%D1%82/%D0%B0%D1%82%D0%BE%D0%BF%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D0%B9-%D0%B4%D0%B5%D1%80%D0%BC%D0%B0%D1%82%D0%B8%D1%82-%D1%8D%D0%BA%D0%B7%D0%B5%D0%BC%D0%B0?query=%D1%8D%D0%BA%D0%B7%D0%B5%D0%BC%D0%B0',
        'Акне (Угри)': 'https://www.msdmanuals.com/ru/%D0%B4%D0%BE%D0%BC%D0%B0/%D0%BA%D0%BE%D0%B6%D0%BD%D1%8B%D0%B5-%D0%B7%D0%B0%D0%B1%D0%BE%D0%BB%D0%B5%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F/%D1%83%D0%B3%D1%80%D0%B5%D0%B2%D0%B0%D1%8F-%D1%81%D1%8B%D0%BF%D1%8C-%D0%B8-%D1%80%D0%BE%D0%B4%D1%81%D1%82%D0%B2%D0%B5%D0%BD%D0%BD%D1%8B%D0%B5-%D0%B7%D0%B0%D0%B1%D0%BE%D0%BB%D0%B5%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F/%D1%83%D0%B3%D1%80%D0%B5%D0%B2%D0%B0%D1%8F-%D1%81%D1%8B%D0%BF%D1%8C?query=%D0%B0%D0%BA%D0%BD%D0%B5',
        'Пигментные изменения': 'https://www.pharmacosmetica.ru/information/pigmentaciya-kozhi-osnovnye-prichiny-vidy-i-osobennosti-uhoda.html',
        'Доброкачественные': 'https://sovamed.ru/zabolevaniya/dobrokachestvennye-novoobrazovaniya-kozhi/',
        'Злокачественные': 'http://www.kvd74.ru/novoobraz_kozhi.html'
    }
    if disease_name in links:
        webbrowser.open(links[disease_name])
    else:
        error_msg("Ошибка", f"Нет доступной ссылки на {disease_name}")

# элементы интерфейса
load_label = CTk.CTkLabel(top_left_frame, text="Выберете фото для анализа")
load_label.grid(row=0, column=0, pady=1, padx=3, sticky='s')

load_button = CTk.CTkButton(top_left_frame, text="Загрузить фото", command=load_predict)
load_button.grid(row=1, column=0, pady=1, padx=1, sticky='s')

web_label = CTk.CTkLabel(top_left_frame, text="Фото с web камеры")
web_label.grid(row=2, column=0, pady=1, padx=3, sticky='s')

web_button = CTk.CTkButton(top_left_frame, text="Web фото", command=web_predict)
web_button.grid(row=3, column=0, pady=1, padx=1, sticky='s')

web_label = CTk.CTkLabel(top_left_frame, text=" ")
web_label.grid(row=4, column=0, pady=10, padx=1, sticky='w')

disease_label = CTk.CTkLabel(root, text="Прогноз: ")
disease_label.grid(row=2, column=1, columnspan=3)

probability_slider = CTk.CTkSlider(root, from_=0, to=100, variable=probability, state="disabled", progress_color='orange', button_color='red')
probability_slider.grid(row=3, column=1, columnspan=3)

other_probability = CTk.CTkLabel(top_left_frame, text=" ")
other_probability.grid(row=5, column=0, columnspan=1, pady=10, padx=3, sticky='s')

cap_label = CTk.CTkLabel(top_left_frame, text=" ")
cap_label.grid(row=12, column=0, pady=20, padx=1, sticky='w')

more_button = CTk.CTkButton(top_left_frame, text=" ", command=open_link, state="disabled", fg_color="transparent")
more_button.grid(row=13, column=0, pady=1, padx=1, sticky='s')

root.mainloop()
