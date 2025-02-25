from fastapi import FastAPI, File, UploadFile, Form
import io
import json
from fastapi.responses import JSONResponse
import whisper

app = FastAPI()
model = whisper.get_model("base")

@app.post("/transcribe/")
async def transcribe_audio(file: UploadFile = File(...), key: str = Form(...)):
    
    try:
        result = model.transcribe(file)
        return JSONResponse(content={"key": key, "transcription": result})
    except ValueError:
        return JSONResponse(content={"key": key, "transcription": "Could not transcribe audio"})
    except Exception as e:
        return JSONResponse(content={"key": key, "transcription": str(e)})
    # Read file content into memory
    # audio_content = await file.read()
    # audio_file = io.BytesIO(audio_content)
    
    # with sr.AudioFile(audio_file) as source:
    #     audio_data = recognizer.record(source)  # Convert audio file to recognizable format
        
    #     try:
    #         text = recognizer.recognize_google(audio_data)  # Convert speech to text
    #         return JSONResponse(content={"key": key, "transcription": text})
    #     except sr.UnknownValueError:
    #         return JSONResponse(content={"key": key, "transcription": "Could not understand audio"})
    #     except sr.RequestError:
    #         return JSONResponse(content={"key": key, "transcription": "API unavailable"})

@app.post("/summarize/")
async def summarize_text(text: str = Form(...), key: str = Form(...)):
    try:
        summary = summarize(text)
        return JSONResponse(content={"key": key, "summary": summary})
    except ValueError:
        return JSONResponse(content={"key": key, "summary": "Could not generate summary"})

# Run using: uvicorn filename:app --reload
