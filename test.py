from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import FileResponse
import soundfile as sf
import numpy as np
from kokoro import KPipeline
import uuid
import os

app = FastAPI()

class TTSRequest(BaseModel):
    text: str
    lang_code: str = 'a'
    voice: str = 'af_heart'
    speed: float = 1.0

@app.post("/text-to-speech/")
async def text_to_speech(request: TTSRequest):
    try:
        pipeline = KPipeline(lang_code=request.lang_code)
        generator = pipeline(request.text, voice=request.voice, speed=request.speed, split_pattern=r'\n\n\n\n\+')
        
        all_audio = []
        for _, _, audio in generator:
            all_audio.append(audio)
        
        combined_audio = np.concatenate(all_audio)
        
        output_file = f"output_{uuid.uuid4().hex}.wav"
        sf.write(output_file, combined_audio, 24000)
        
        return FileResponse(output_file, media_type="audio/wav", filename=output_file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))