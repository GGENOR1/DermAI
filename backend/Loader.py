from uuid import uuid4
import os

import yadisk
y = yadisk.YaDisk(token="y0_AgAAAABf461CAAr5XAAAAAD0hzz6kBx5h3TjSFGCTFzcjQs4GVieusU")
class LoaderImage:
    @staticmethod
    async def generate_unique_filename( file):
        unique_filename = str(uuid4())
        file_extension = file.filename.split(".")[-1]
        unique_filename_with_extension = f"{unique_filename}.{file_extension}"
        return unique_filename_with_extension

    @staticmethod
    async def save_and_upload_file( file, prediction_key, unique_filename_with_extension):
        if prediction_key is None:
            prediction_key = "None"
        save_path = f"D:/DERMAI/{str(prediction_key)}/{unique_filename_with_extension}"
        with open(save_path, "wb") as f:
            f.write(await file.read())
        y.upload(f"D:/DERMAI/{str(prediction_key)}/{unique_filename_with_extension}",
                 f"DermAI/TEST/{str(prediction_key)}/{unique_filename_with_extension}")
