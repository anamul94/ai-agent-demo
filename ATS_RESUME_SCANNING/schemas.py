from pydantic import BaseModel, Field
from typing import Optional, List

class Grade(BaseModel):
    grade: bool = Field(..., description="Grade if resuem is good or not")


class Resume(BaseModel):
    name: str = Field(..., description="Full name of the candidate")
    email: str = Field(..., description="Email address")
    phone: str = Field(..., description="Phone number")

    summary: Optional[str] = Field(
        None, description="a brief summary of the candidate's professional background"
    )

    education: List[str] = Field(..., description="Educational qualifications")
    skills: List[str] = Field(..., description="Key technical and soft skills")
    projects: List[str] = Field(
        ..., description="Relevant personal or professional projects"
    )
    strengths: List[str] = Field(..., description="Candidate's strengths")
    gaps: List[str] = Field(
        ...,
        description="Gaps between resume and JD. e.g: Missing 2 years of required experience",
    )

   
