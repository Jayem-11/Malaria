import uvicorn
import numpy as np
from io import BytesIO
from fastapi import FastAPI, File, UploadFile
from PIL import Image
import tensorflow as tf
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

CHANNELS = 3
IMAGE_SIZE = 256

origins = [
    "http://localhost",
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL = tf.keras.models.load_model("malaria.h5")

CLASS_NAMES = ['uninfected', 'parasitized']

@app.get("/ping")
async def ping():
    return "Hello, I am alive"

if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=8000)

def read_file_as_image(data) -> np.ndarray:
    image = np.array(Image.open(BytesIO(data)))
    image = tf.image.resize_with_crop_or_pad(image,IMAGE_SIZE,IMAGE_SIZE)
    image = tf.reshape(image, (-1,IMAGE_SIZE, IMAGE_SIZE, CHANNELS))

    return image

@app.post("/predict")
async def predict(file: UploadFile):
    image = read_file_as_image(await file.read())

    # image_batch = np.expand_dims(image, 0)
    predictions = MODEL.predict(image)

    predicted_class = CLASS_NAMES[predictions]
    confidence = predictions

    return {
        'class': predicted_class,
        "confidence": float(confidence)
    }
