from typing import Literal
from pydantic import BaseModel, ConfigDict, Field

#ANALYST TO CUSTODIAN DATA STRUCTURES
class JobAnalysis(BaseModel):
    model_config = ConfigDict(extra="forbid")
    schema_version: Literal["1.0"]
    analysis: str

#CUSTODIAN TO INTERVIEWER DATA STRUCTURES
class InformationRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    request_id: str
    objective: str
    facts_requested: list[str] = Field(min_length=1)

#CUSTODIAN TO ANALYST DATA STRUCTUES
class EvidenceAuthorization(BaseModel):
    model_config = ConfigDict(extra="forbid")
    evidence: str 
    information_requests: list[InformationRequest]

#INTERVIEWER TO CUSTODIAN DATA STRUCTURES
class InformationResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    request_id: str 
    response: str 

class InterviewerOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    output_type: Literal[
        "question",
        "information_response",
    ]
    question: str | None = None
    information_response: InformationResponse | None = None

#ANALYST TO WRITER DATA STRUCTURES
class CandidateJobAnalysis(BaseModel):
    analysis: str

#WRITER DATA STRUCTURES
class ResumeBullet(BaseModel):
    text: str

class ResumeExperienceContent(BaseModel):
    selected_title: str
    description: str
    bullets: list[ResumeBullet]

class ResumeContentManifest(BaseModel):
    professional_summary: str
    core_skills: list[str]
    certifications: list[str]
    experiences: list[ResumeExperienceContent]

#EVALUATOR DATA STRUCTURES
class ResumeEvaluation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    overall_assessment: str
    requirement_coverage: str
    strengths: str
    weaknesses: str
    recommended_improvements: str
    claim_safety: str
    decision: Literal[
        "pass",
        "fail",
        "error",
    ]