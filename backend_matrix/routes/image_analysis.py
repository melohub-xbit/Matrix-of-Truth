from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
import PIL.Image
import io
import os

image_router = APIRouter()

@image_router.post("/analyze-image")
async def analyze_image_endpoint(file: UploadFile = File(...)):
    try:
        if not file:
            raise HTTPException(status_code=400, detail="No file uploaded")
            
        # Check if GEMINI_API_KEY is set
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise HTTPException(status_code=500, detail="GEMINI_API_KEY not configured")
            
        # Read image content
        content = await file.read()
        image = PIL.Image.open(io.BytesIO(content))
        
        # Configure Gemini
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Prepare prompt
        prompt = "Analyze the content in this image and detect if it contains misinformation or bias. First state if the content is real or fake. Then give a short summary regarding the content. Then Summarize key points."

        response = model.generate_content([prompt, image])
        
        return {"analysis": response.text}
        
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        error_detail = f"Error analyzing image: {str(e)}\n{traceback.format_exc()}"
        print(error_detail)
        raise HTTPException(status_code=500, detail=str(e))
