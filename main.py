from fastapi import FastAPI, File, UploadFile, Form
import io
import json
from fastapi.responses import JSONResponse
import whisper
from google import genai

app = FastAPI()
model = whisper.load_model("base")

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
async def summarize_text(text: str = Form(...), key: str = Form(...), language: str = Form(...)):
    try:
        client = genai.Client(api_key=key)

        if language == 'en':
          prompt = 'You are an expert in medical summarisation and report creation,\
                    vital for doctors who depend on you to accurately condense conversations with patients into concise,\
                    structured summaries in british english. Strive for excellence to meet their needs,\
                    as your work is crucial to their careers.'
        elif language == 'ja':
          prompt = 'You are an expert in medical summarisation and report creation in japaneese,\
                    vital for doctors who depend on you to accurately condense conversations with patients into concise,\
                    structured summaries in japaneese. Strive for excellence to meet their needs,\
                    as your work is crucial to their careers.'
        else:
          prompt = 'You are an expert in medical summarisation and report creation,\
                    vital for doctors who depend on you to accurately condense conversations with patients into concise,\
                    structured summaries in british english. Strive for excellence to meet their needs,\
                    as your work is crucial to their careers.'
        
        response = client.models.generate_content(
            model="gemini-2.0-flash",
        
            contents=f"{prompt} Summerize {text} to key points",
        )

        print(response.text)
        return JSONResponse(content={ "summary": response.text })
    except ValueError:
        return JSONResponse(content={"summary": "Could not generate summary"})

# Run using: uvicorn filename:app --reload
