from dataclasses import dataclass, field
from resume_system.models_reduced import JobAnalysis, EvidenceAuthorization, InformationRequest, CandidateJobAnalysis, InformationResponse, ResumeContentManifest, ResumeEvaluation
from resume_system.clients import FileClient, LoggerClient, DiscordClient, AgentClient
from pathlib import Path

@dataclass
class WorkflowContext:
    job_title: str
    file_client: FileClient
    logger_client: LoggerClient
    message_client: DiscordClient
    agent_client: AgentClient
    job_description: str
    current_job_analysis: JobAnalysis| None=None
    current_evidence_authorization: EvidenceAuthorization | None=None
    open_information_requests: list[InformationRequest] = field(
        default_factory=list
    )
    current_information_responses: list[InformationResponse] = field(
        default_factory=list
    )
    current_candidate_job_analysis: CandidateJobAnalysis| None=None
    current_resume_content_manifest: ResumeContentManifest | None = None
    current_resume_path: Path | None=None
    current_resume_evaluation: ResumeEvaluation | None = None