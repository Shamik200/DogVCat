import gradio as gr
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np
import io

app = FastAPI()
model = load_model("cat_dog_classifier.keras", compile=False)

def preprocess_image(image):
    image = image.resize((256, 256))
    image = np.array(image) / 255.0
    image = np.expand_dims(image, axis=0)
    return image

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes))
    image = preprocess_image(image)
    prediction = model.predict(image)
    result = "Dog" if prediction[0] > 0.5 else "Cat"
    return JSONResponse({"prediction": result})

# Mount Gradio as UI (Optional)
gr_interface = gr.Interface(fn=predict, inputs=gr.File(type="binary"), outputs="text")
app = gr.mount_gradio_app(app, gr_interface, path="/")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)
