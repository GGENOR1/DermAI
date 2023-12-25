from fastapi import UploadFile, File, APIRouter
from starlette.responses import JSONResponse
from uuid import uuid4
from backend.ImageRender import FileChecker

import yadisk
router = APIRouter()
y = yadisk.YaDisk(token="y0_AgAAAABf461CAAr5XAAAAAD0hzz6kBx5h3TjSFGCTFzcjQs4GVieusU")

classes = ['Инфекционные', 'Экзема', 'Акне (Угри)', 'Пигментные изменения', 'Доброкачественные', 'Злокачественные']
loaded_model = None

model = None

@router.on_event("startup")
async def on_startup():
    global model
    model = await FileChecker.load_my_model()
    print(model.summary())
    return model




@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    checker = FileChecker()
    if not checker.is_allowed_file(file.filename):
        return JSONResponse(status_code=400, content={"message": "Invalid file extension."})
    if not await checker.is_image(file):
        return JSONResponse(status_code=400, content={"message": "Invalid file extension."})

    if model is not None:
        photo = await checker.render_photo(file)
        prediction = model.predict(photo) * 100
        prediction_list = prediction.tolist()[0]
        print(prediction_list)
        result = {class_name: value for class_name, value in zip(classes, prediction_list)}

        sorted_result = {k: v for k, v in sorted(result.items(), key=lambda item: item[1], reverse=True)}

        return sorted_result
    return JSONResponse(status_code=200, content={"message": "File uploaded successfully."})


@router.post("/saveToStorage/")
async def save_file(file: UploadFile = File(...), path_name="None",  predictionKey=None):
    print(path_name)
    print(file)
    print(predictionKey)
    contents = await file.read()
    unique_filename = str(uuid4())
    file_extension = file.filename.split(".")[-1]
    if predictionKey is None:
        predictionKey = "None"
    unique_filename_with_extension = f"{unique_filename}.{file_extension}"
    save_path = f"D:/DERMAI/{str(predictionKey)}/{unique_filename_with_extension}"
    with open(save_path, "wb") as f:
        f.write(contents)
    y.upload(f"D:/DERMAI/{str(predictionKey)}/{unique_filename_with_extension}", f"DermAI/TEST/{str(predictionKey)}/{unique_filename_with_extension}")
    return JSONResponse(status_code=200, content={"message": "File save successfully."})
