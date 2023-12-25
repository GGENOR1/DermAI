import io
import os
import cv2
from PIL import Image
from io import BytesIO
import tensorflow as tf
from fastapi import UploadFile
import numpy as np
import tkinter as tk
import tensorflow as tf
from tkinter import filedialog
from PIL import Image, ImageTk
from keras.src.saving.saving_api import load_model
from starlette.responses import JSONResponse
from tensorflow.keras.applications.efficientnet import preprocess_input











    # print(type(image))
    # processed_img = cv2.resize(image, (224, 224))
    # processed_img = preprocess_input(processed_img)
    # processed_img = np.expand_dims(processed_img, axis=0)
    # print(processed_img.size)
    # return processed_img

class FileChecker:
    ALLOWED_EXTENSIONS = {'jpeg', 'png', 'jpg'}

    @staticmethod
    def get_file_extension(file_name):
        return file_name.split(".")[-1].lower()

    @staticmethod
    def is_allowed_file(file_name):
        return '.' in file_name and FileChecker.get_file_extension(file_name) in FileChecker.ALLOWED_EXTENSIONS

    @staticmethod
    async def is_image(file: UploadFile):
        extension = FileChecker.get_file_extension(file.filename)
        return extension in FileChecker.ALLOWED_EXTENSIONS
    @staticmethod
    async def render_photo(image: UploadFile):
        contents = await image.read()
        # Путь для сохранения файла на ПК

        # Сохранение файла на ПК



        img = Image.open(io.BytesIO(contents))
        img = np.array(img)
        processed_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        processed_img = cv2.resize(processed_img, (224, 224))
        processed_img = np.expand_dims(processed_img, axis=0)
        # nparr = np.frombuffer(contents, np.uint8)
        # cv_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        # processed_img = cv2.resize(cv_img, (224, 224))
        # # processed_img = image.img_to_array(processed_img)
        # p
        # processed_img = np.expand_dims(processed_img, axis=0)
        return processed_img

    @staticmethod
    async def load_my_model():
        global loaded_model
        model = tf.keras.models.load_model('backend/DERM_AI_11_25.h5')
        # if not loaded_model:
        #     try:
        #         loaded_model = tf.compat.v1.losses.sparse_softmax_cross_entropy('./DERM_AI_11_25.h5')  # Поменяйте 'your_model.h5' на путь к вашей модели
        #     except:
        #         return JSONResponse(status_code=400, content={"message": "Invalid model file"})

        # return JSONResponse(status_code=200, content={"message": "wsdadadad"})
        return model
