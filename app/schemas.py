from pydantic import BaseModel

class InteractionCreate(BaseModel):
    hcp_name: str
    specialty: str
    hospital: str
    notes: str
    follow_up_date: str

class InteractionResponse(BaseModel):
    message: str
    summary: str
    sentiment: str
    opportunity_score: int