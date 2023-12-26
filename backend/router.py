from fastapi import UploadFile, File, APIRouter
from starlette.responses import JSONResponse
from uuid import uuid4
from backend.ImageRender import FileChecker
from backend.Loader import LoaderImage
from backend.Model import MyModelLoader

router = APIRouter()
# @router.on_event("startup")
# async def startup_event():
#     print('hellow')
model = MyModelLoader()

@router.on_event("startup")
async def startup_event():
    await model.load_my_model()

@router.post("/uploadImage")
async def upload_file(file: UploadFile = File(...)):
    checker = FileChecker()
    if not checker.is_allowed_file(file.filename):
        return JSONResponse(status_code=400, content={"message": "Invalid file extension."})
    if not await checker.is_image(file):
        return JSONResponse(status_code=400, content={"message": "Invalid file extension."})
    photo = await checker.render_photo(file)
    prediction = await model.prediction(photo)
    return prediction


@router.post("/saveToStorage/")
async def save_file(file: UploadFile = File(...), path_name="None",  predictionKey=None):

    name = await LoaderImage.generate_unique_filename(file)
    await LoaderImage.save_and_upload_file(file,predictionKey,name)
    # contents = await file.read()
    # unique_filename = str(uuid4())
    # file_extension = file.filename.split(".")[-1]
    # if predictionKey is None:
    #     predictionKey = "None"
    # unique_filename_with_extension = f"{unique_filename}.{file_extension}"
    # save_path = f"D:/DERMAI/{str(predictionKey)}/{unique_filename_with_extension}"
    # with open(save_path, "wb") as f:
    #     f.write(contents)
    # y.upload(f"D:/DERMAI/{str(predictionKey)}/{unique_filename_with_extension}", f"DermAI/TEST/{str(predictionKey)}/{unique_filename_with_extension}")
    return JSONResponse(status_code=200, content={"message": "File save successfully."})
