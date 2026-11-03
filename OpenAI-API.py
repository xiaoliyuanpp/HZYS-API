from huoZiYinShua import *
from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel
import random
import os

ttsApi = FastAPI()
class TTSRequest(BaseModel):
    model:str = "HZYS"
    input:str = "大家好啊,我是说的道理"
    voice:str = "otto"
    speed:float = 1.0

@ttsApi.post("/audio/speech")
def genAudio(request:TTSRequest):
    if(request.model=="HZYS"):
        # try:
            HZYS = huoZiYinShua("./settings.json")
            exportFile="./tmp/"+str(random.randint(0,10000))+".wav"
            HZYS.export(request.input,filePath=exportFile,inYsddMode=True,pitchMult=1,speedMult=request.speed,reverse=False,norm=False)
            audioFile=os.open(exportFile,os.O_RDONLY)
            audio=os.read(audioFile,os.path.getsize(exportFile))
            os.close(audioFile)
            os.remove(exportFile)
            return Response(content=audio,media_type="audio/wav")
        # except Exception as e:
        #     print(e)
        #     raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(ttsApi, host="0.0.0.0", port=1145)