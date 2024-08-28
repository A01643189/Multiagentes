from ultralytics import YOLO
import logging
import cv2
import numpy as np
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
import io

# Create FastAPI app instance
app = FastAPI()

# Initialize the YOLO model
model = YOLO('yolov8s.pt')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("upload_image")

@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        logger.info(f"Received file: {file.filename}")

        # Convert the received bytes into a numpy array
        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Process the image using YOLOv8
        results = model.track(img, persist=True)
        annotated_frame = results[0].plot()

        # Encode the image to JPEG format
        _, img_encoded = cv2.imencode('.jpg', annotated_frame)
        img_bytes = img_encoded.tobytes()

        # Return the processed image as a response
        return StreamingResponse(io.BytesIO(img_bytes), media_type="image/jpeg")

    except Exception as e:
        logger.error(f"Error processing image: {str(e)}")
        raise HTTPException(status_code=500, detail="Error processing image")

@app.get("/")
def root():
    return {"message": "FastAPI server is running"}

# Run the FastAPI application
if _name_ == "_main_":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)