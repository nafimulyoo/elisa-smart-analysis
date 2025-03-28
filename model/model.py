from pydantic import BaseModel
from typing import List, Dict, Any


class AnalysisResultWeb(BaseModel):
    data: Dict[str, Any]
    visualization_type: str
    explanation: str

class AnalysisResultLINE(BaseModel):
    image_url: str
    explanation: str

class AnalysisResultWhatsApp(BaseModel):
    image_url: str
    explanation: str

class InitialPromptHandlerResult(BaseModel):
    type: str
    message: str
 
