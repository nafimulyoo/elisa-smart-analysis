from pydantic import BaseModel
from typing import List, Dict, Any


class AnalysisResultWeb(BaseModel):
    data: Dict[str, Any]
    visualization_type: str
    explanation: str

class AnalysisResultLINE(BaseModel):
    image_url: str
    explanation: str

# TODO: Pelajarin response whatsapp gimana
class AnalysisResultWhatsApp(BaseModel):
    image_url: str
    explanation: str

class PromptRequest(BaseModel):
    prompt: str


from pydantic import BaseModel
from typing import List, Dict, Any


class InitialPromptHandlerResult(BaseModel):
    type: str
    message: str
 
