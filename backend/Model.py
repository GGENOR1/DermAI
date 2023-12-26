import tensorflow as tf


classes = ['Инфекционные заболевания', 'Экзема', 'Акне (Угри)', 'Пигментные изменения', 'Доброкачественные опухоли', 'Злокачественные опухоли']

class MyModelLoader:
    def __init__(self):
        self.loaded_model = None

    async def load_my_model(self):
        if not self.loaded_model:
            try:
                self.loaded_model = tf.keras.models.load_model('backend/DERM_AI_11_25.h5')

                return {"message": "Model loaded successfully"}
            except Exception as e:
                return {"message": f"Failed to load model. Error: {str(e)}"}
        else:
            return {"message": "Model already loaded"}

    async def prediction(self, image):
        if self.loaded_model:
            prediction = self.loaded_model.predict(image) * 100
            prediction_list = prediction.tolist()[0]
            result = {class_name: value for class_name, value in zip(classes, prediction_list)}
            result = {k: v for k, v in sorted(result.items(), key=lambda item: item[1], reverse=True)}
            return result
        else:
            return {"message": "Model not loaded yet"}

