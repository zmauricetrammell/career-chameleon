# Career Chameleon

**Career Chameleon** is a multi-agent resume-generation system that turns a reusable body of professional evidence into a targeted, truthful resume for a specific job.

The core idea is simple: **people are more complex than a resume**. A strong resume should not flatten a career into a chronological inventory. It should select the candidate's strongest, most relevant attributes and combine them into a coherent professional narrative for the role being pursued—without inventing experience or overstating evidence.

Career Chameleon is the executable successor to the earlier **Rapid Resume System (RRS)**. It keeps the strongest ideas from RRS—specialized agents, evidence-grounded writing, explicit authority boundaries, idempotency, and independent evaluation—but replaces the older manually coordinated architecture with a working Python runtime and leaner data structures.

> **Current status:** working local Python MVP. Analyst, Custodian, Interviewer, Writer, OpenAI integration, structured runtime, and DOCX rendering are implemented. Evaluator integration and Supervisor-driven revision/reuse are the next major milestones.

---

# Why This Exists

Writing a strong targeted resume requires several different kinds of reasoning:

1. Understanding what an employer actually needs.
2. Searching a large career history for relevant evidence.
3. Determining how strongly that evidence supports each requirement.
4. Recognizing when the professional corpus already contains enough evidence.
5. Identifying the small number of factual gaps that could materially improve the application.
6. Asking useful questions without turning the process into an interrogation.
7. Translating military, technical, specialized, or unconventional experience into recognizable civilian professional functions.
8. Deciding where evidence belongs in the resume based on what it proves professionally.
9. Selecting only the strongest evidence that fits within limited resume space.
10. Evaluating the finished product from ATS, recruiter, and hiring-manager perspectives.

Trying to perform all of these functions inside one AI role creates conflicting objectives.

A Writer should make the strongest truthful presentation possible. A Custodian should protect evidence integrity. An Interviewer should establish facts without interpreting them. An Evaluator should be free to criticize the final product without defending the decisions that created it.

Career Chameleon separates those responsibilities.

---

# What Changed From Rapid Resume System

Career Chameleon keeps the best architectural ideas from RRS but changes the implementation substantially.

## 1. The system now has a real runtime

The earlier project primarily defined manually operated conversational agents and artifact contracts.

Career Chameleon is an executable Python workflow using:

- Python dataclasses for workflow state.
- Pydantic models for artifacts that need machine-readable structure.
- OpenAI structured responses for agent outputs.
- Local professional-evidence files.
- Discord for human interview interaction.
- `python-docx` for resume rendering.

## 2. Structure is used only where software needs structure

A major lesson from the earlier design was that over-structuring semantic reasoning creates large schemas, brittle bookkeeping, and weaker model outputs.

Career Chameleon uses a simpler rule:

> **If code must inspect, route, validate, or render a field, structure it. If an artifact only needs to communicate rich reasoning to another agent, prefer dense prose.**

Examples:

- `JobAnalysis` is mostly prose because another agent consumes its meaning.
- `EvidenceAuthorization` contains prose evidence plus structured information requests because code must know whether to invoke the Interviewer.
- `InterviewerOutput` is structured because runtime logic must distinguish a question from a completed response.
- `ResumeContentManifest` is structured because Python must render it into a DOCX.
- `ResumeEvaluation` contains prose assessment plus a literal decision because runtime logic only needs the final `pass`, `fail`, or `error` state.

## 3. Evidence authorization is separate from candidate analysis

The current architecture separates three different questions:

- **What does the employer require?** — Analyst
- **What candidate evidence is authorized to support those requirements?** — Custodian
- **What story does that evidence tell for this particular job?** — Analyst

That keeps evidence integrity distinct from presentation strategy.

## 4. Resume placement is functional, not mechanically chronological

The evidence corpus preserves factual provenance. The resume is a presentation layer.

An accomplishment may appear under the resume section whose **professional function** it best demonstrates, provided the presentation does not falsify the underlying employer, client, ownership, scope, or nature of the work.

For example:

- Help-desk transformation and incident command can reinforce an IT Service / Operations narrative.
- Enterprise modernization and audit-control work can reinforce a Technical Project Manager narrative.
- Broad people, vendor, budget, compliance, and operational ownership can reinforce an IT Operations Manager narrative.

The result is effectively a **functional resume presented in a familiar chronological format**.

---

# System Overview

The system contains six professional agents/functions:

```text
Analyst
    Understand employer demand
    Match authorized evidence to the target

Custodian
    Protect and authorize professional evidence
    Identify material information gaps

Interviewer
    Resolve factual information requests with the human

Writer
    Build targeted resume content
    Render the current resume

Evaluator
    Judge the final resume as a hiring product

Supervisor
    Govern execution, revision, reuse, and system feedback
```

---

# The Agents

## Analyst

The **Analyst** owns interpretation of employer demand and target-to-candidate fit.

It performs two operations.

### Analyze the target job

The Analyst converts a raw job description into a `JobAnalysis` that explains:

- The employer's central mandate.
- Material professional requirements.
- Practical meaning of those requirements.
- Expected ownership and scope.
- Evidence that would demonstrate each requirement.
- Important interpretation boundaries.

This analysis is intentionally candidate-independent.

### Match candidate evidence

After the Custodian authorizes evidence, the Analyst produces a `CandidateJobAnalysis` describing:

- Overall candidate fit.
- Requirement-by-requirement alignment.
- Strongest professional evidence.
- Candidate differentiators.
- Claim boundaries.
- Functional resume narrative allocation.
- Which accomplishments should anchor each section.
- Which evidence should remain secondary or be excluded to prevent redundancy.

The goal is for the Writer to make limited presentation choices rather than rediscover the candidate's entire story.

---

## Custodian

The **Custodian** owns evidence integrity.

It receives the target `JobAnalysis` and searches the candidate's professional evidence corpus.

Its responsibilities include:

- Finding evidence relevant to employer requirements.
- Preserving factual scope, ownership, limitations, and provenance.
- Distinguishing adequate evidence from genuine evidence gaps.
- Avoiding unnecessary interviews when the corpus is already sufficient.
- Producing an `EvidenceAuthorization` containing the evidence the Analyst may use.
- Producing `InformationRequest` objects only when additional facts could materially improve the application.

The Custodian does not write the resume and does not decide how evidence should be presented.

---

## Interviewer

The **Interviewer** resolves one factual information request at a time.

Its output can be either:

```text
question
```

or:

```text
information_response
```

This supports a natural multi-turn investigation without confusing runtime state with professional evidence.

The Interviewer is intentionally constrained to resume-relevant factual investigation. It should not ask for exhaustive technical inventories when a smaller amount of information is sufficient to establish professional scope, ownership, or result.

The current runtime uses Discord as the human interaction channel and preserves OpenAI conversation state across follow-up questions.

---

## Writer

The **Writer** owns resume presentation.

It receives the `CandidateJobAnalysis` and produces a structured `ResumeContentManifest` containing:

- Professional summary.
- Core skills.
- Certifications.
- Experience titles.
- Experience descriptions.
- Achievement bullets.

The Writer does not search the professional evidence corpus.

### Functional career narratives

The current Writer architecture uses functional career narratives inside familiar chronological-looking experience containers.

Evidence is allocated according to the professional identity it best demonstrates rather than being trapped inside the literal date range of the original episode.

This is not permission to fabricate chronology. The Writer must preserve the factual nature of each accomplishment and may not create false employers, clients, authority, scope, or outcomes.

### Compression over completeness

The evidence available upstream is intentionally richer than the final resume.

The Writer therefore optimizes for:

- Strongest evidence first.
- Quantified impact.
- Distinct professional narratives.
- Minimal redundancy.
- Concise descriptions.
- Limited bullet counts.
- A two-page target when practical.

A shorter resume containing stronger evidence is preferable to a longer resume that reproduces every useful fact.

---

## Evaluator

The **Evaluator** judges the final rendered resume against the target job description.

It evaluates:

- Requirement coverage.
- Visible evidence strength.
- ATS alignment.
- Recruiter readability.
- Hiring-manager credibility.
- Claim safety.
- Resume density and prioritization.
- Highest-value remaining improvements.

The Evaluator returns a `ResumeEvaluation` with prose assessment and one literal decision:

```text
pass
fail
error
```

The Evaluator does **not** decide which upstream agent should rerun or which artifact should be reused.

> **Implementation status:** model, contract, and task instruction exist; file-input runtime integration is in progress.

---

## Supervisor

The **Supervisor** owns workflow governance and revision orchestration.

The intended revision model is idempotent:

> **An artifact should only be regenerated when its inputs materially change or evaluation feedback identifies a defect within that artifact's responsibility.**

When evaluation fails, the Supervisor will inspect the completed artifact chain, determine the earliest stage requiring correction, and publish agent-specific feedback and reuse instructions.

Conceptually:

```text
Resume Evaluation: FAIL
        ↓
Supervisor After-Action Review
        ↓
JobAnalysis              REUSE / REGENERATE
EvidenceAuthorization    REUSE / REGENERATE
CandidateJobAnalysis     REUSE / REGENERATE
ResumeContentManifest    REUSE / REGENERATE
        ↓
Render
        ↓
Evaluate Again
```

This prevents a small Writer issue from causing unnecessary evidence searches or interviews and reduces both model drift and API cost.

> **Implementation status:** Supervisor after-action and reuse orchestration are the next major runtime features.

---

# Current Workflow

```text
Target Job Description
        ↓
Analyst: analyze job
        ↓
JobAnalysis
        ↓
Custodian: authorize evidence
        ↓
EvidenceAuthorization
        │
        ├── information gap? ──→ Interviewer
        │                         ↓
        │                    InformationResponse
        │                         ↓
        └────────────────── Custodian re-evaluates
        ↓
Analyst: match candidate evidence
        ↓
CandidateJobAnalysis
        ↓
Writer: draft resume content
        ↓
ResumeContentManifest
        ↓
Python DOCX renderer
        ↓
Targeted Resume
        ↓
Evaluator
        ↓
ResumeEvaluation
```

The runtime stores current artifacts in `WorkflowContext`, allowing later stages—and eventually the Supervisor—to inspect complete application state.

---

# Data Model Philosophy

Career Chameleon intentionally avoids turning every piece of professional reasoning into deeply nested Python objects.

The design rule is:

```text
Agent-to-agent semantic reasoning
        → dense prose when possible

Runtime decision or renderer dependency
        → minimal structured field
```

Current shared models include:

```text
JobAnalysis
InformationRequest
EvidenceAuthorization
InformationResponse
InterviewerOutput
CandidateJobAnalysis
ResumeBullet
ResumeExperienceContent
ResumeContentManifest
ResumeEvaluation
```

This keeps models small, reduces bookkeeping, and preserves semantic nuance.

---

# Professional Evidence Corpus

Career Chameleon operates from a reusable corpus of professional evidence rather than rebuilding the candidate's history for each application.

The current implementation loads YAML evidence records from:

```text
resume_system/experience_corpus/
```

The corpus is intentionally **not committed to this public repository** because it contains candidate-specific professional history.

Evidence records should preserve enough information to support truthful downstream claims, including where relevant:

- Professional context.
- Candidate ownership.
- Scope.
- Technologies or methods.
- Quantified results.
- Attribution.
- Limitations.
- Known unknowns.

The Custodian converts that larger corpus into a target-specific `EvidenceAuthorization` so downstream agents do not need direct corpus access.

---

# Core Artifacts

| Artifact | Purpose |
|---|---|
| `JobAnalysis` | Employer-demand analysis |
| `EvidenceAuthorization` | Target-relevant candidate evidence authorized by the Custodian |
| `InformationRequest` | Material factual question requiring human input |
| `InformationResponse` | Human-supplied factual response |
| `CandidateJobAnalysis` | Candidate-fit and functional resume strategy |
| `ResumeContentManifest` | Structured semantic content for rendering |
| Targeted Resume | Final DOCX hiring product |
| `ResumeEvaluation` | Independent product assessment |

Artifacts are structured only to the degree required by runtime logic or rendering.

---

# Idempotency and Revision

Idempotency remains a core design principle inherited from Rapid Resume System, but Career Chameleon moves it into the runtime architecture.

Repeated execution with materially unchanged inputs should preserve strong existing decisions rather than generate novelty for its own sake.

The planned Supervisor revision process follows one rule:

> **Invalidate only the earliest defective artifact and the downstream artifacts that depend on it. Reuse everything earlier that remains valid.**

Examples:

```text
Writer selection problem
JobAnalysis              REUSE
EvidenceAuthorization    REUSE
CandidateJobAnalysis     REUSE or REGENERATE
ResumeContentManifest    REGENERATE
```

```text
Candidate evidence was poorly allocated
JobAnalysis              REUSE
EvidenceAuthorization    REUSE
CandidateJobAnalysis     REGENERATE
ResumeContentManifest    REGENERATE
```

```text
Custodian missed evidence
JobAnalysis              REUSE
EvidenceAuthorization    REGENERATE
CandidateJobAnalysis     REGENERATE
ResumeContentManifest    REGENERATE
```

```text
Employer requirement was misunderstood
JobAnalysis              REGENERATE
Everything downstream    REGENERATE
```

Reuse is not only a token-saving mechanism. It also reduces stochastic drift and makes revisions easier to debug.

---

# Separation of Authority

| Domain | Authority |
|---|---|
| Employer requirement analysis | Analyst |
| Evidence authorization and factual sufficiency | Custodian |
| Human factual investigation | Interviewer |
| Candidate-fit interpretation and functional allocation | Analyst |
| Resume presentation | Writer |
| Final product evaluation | Evaluator |
| Workflow revision and artifact reuse | Supervisor |
| Architecture approval | Human System Owner |

This separation is intentional.

---

# Repository Structure

```text
career-chameleon/
│
├── docs/
│   └── pseudocode.txt
│
├── resume_system/
│   ├── __init__.py
│   ├── main.py
│   ├── workflow.py
│   ├── context.py
│   ├── clients.py
│   ├── models_reduced.py
│   │
│   ├── contracts/
│   │   ├── analyst.txt
│   │   ├── custodian.txt
│   │   ├── interviewer.txt
│   │   ├── writer.txt
│   │   ├── evaluator.txt
│   │   └── supervisor.txt
│   │
│   ├── instructions/
│   │   ├── job_analysis.txt
│   │   ├── authorize_evidence.txt
│   │   ├── resolve_information_request.txt
│   │   ├── candidate_job_analysis.txt
│   │   ├── generate_resume_content_manifest.txt
│   │   └── evaluate_resume.txt
│   │
│   ├── fixtures/
│   │   └── job_description.txt
│   │
│   └── experience_corpus/
│       └── candidate-specific YAML files (local / ignored)
│
├── .gitignore
└── README.md
```

---

# Runtime Components

## `WorkflowContext`

`WorkflowContext` holds the current application state, including:

- Job description.
- Current `JobAnalysis`.
- Current `EvidenceAuthorization`.
- Open information requests.
- Information responses.
- Current `CandidateJobAnalysis`.
- Current `ResumeContentManifest`.
- Current rendered resume path.
- Current `ResumeEvaluation`.

## `AgentClient`

`AgentClient` wraps OpenAI model calls and structured-response parsing.

The current implementation uses the OpenAI Responses API with Pydantic structured outputs.

## `FileClient`

`FileClient` creates per-job working directories, stores artifacts and logs, and assembles the local professional evidence corpus for Custodian use.

## `DiscordClient`

`DiscordClient` supplies the human-in-the-loop interview channel when evidence requests require clarification.

## Renderer

The current renderer uses `python-docx` to convert the semantic `ResumeContentManifest` into a DOCX resume.

The renderer owns document layout. The Writer owns semantic content.

---

# Running the Current MVP

The repository is still a development build rather than a packaged application.

## Requirements

The runtime currently depends on Python packages including:

```text
openai
pydantic
python-dotenv
discord.py
requests
beautifulsoup4
python-docx
```

A pinned dependency file and cross-platform setup flow are planned as part of portability work.

## Environment variables

Create a local `.env` file in the repository root.

Do **not** commit it.

```text
OPENAI_API_KEY=your_openai_api_key
DISCORD_BOT_TOKEN=your_discord_bot_token
```

## Professional evidence

Create:

```text
resume_system/experience_corpus/
```

and place the candidate's YAML professional-evidence files there.

The corpus is local candidate data and should not be committed to a public repository.

## Target job

The current development entry point reads:

```text
resume_system/fixtures/job_description.txt
```

Replace that fixture with the target job description during local testing.

Website ingestion code exists in `WebsiteClient`, but the fixture path is the active development path.

## Run

From the repository root:

```bash
python -m resume_system.main
```

The runtime creates a directory named from the target job title and writes job artifacts, logs, and the rendered resume there.

---

# Current Limitations

Career Chameleon is a working MVP and still contains candidate-specific development assumptions.

Known limitations include:

- Resume identity, education, dates, and some experience-container metadata are currently hard-coded in the renderer.
- Certification content is currently embedded in Writer instructions for the active candidate configuration.
- Experience-container architecture is currently tailored to the development candidate.
- Candidate profile/configuration has not yet been externalized.
- Evaluator API/file-attachment integration is still being completed.
- Supervisor after-action and artifact-reuse logic is not yet implemented.
- Dependency installation is not yet packaged for Windows/Linux portability.
- Discord is currently the only implemented human interview transport.

The next portability milestone is to move candidate-specific static content into a profile/configuration layer so the same engine can operate against different candidates without editing source code or prompt instructions.

---

# Design Philosophy

### Separate professional responsibilities

Job analysis, evidence custody, interviewing, candidate analysis, writing, evaluation, and workflow governance are different professional functions.

### Preserve factual provenance

Professional translation and functional placement are encouraged.

Historical fabrication is not.

### Separate evidence from presentation

The professional evidence corpus answers **what happened**.

The resume answers **which truthful aspects of that history best communicate fit for this role**.

### Structure only what software needs

Do not create elaborate schemas merely because data can be structured.

Use structure for routing, validation, rendering, and explicit runtime decisions. Use prose for rich semantic reasoning between agents.

### Keep agents within authority

A Custodian should not write the resume. A Writer should not search the corpus. An Evaluator should not decide runtime routing.

### Prefer strong existing evidence over unnecessary interviews

Missing detail is not automatically a missing capability.

The Interviewer should be invoked only when additional factual information could materially improve the application.

### Build functional professional narratives

A resume is not an archival transcript of a career.

Evidence should be arranged around the professional function it demonstrates while remaining truthful about the underlying work.

### Optimize for evidence strength, not evidence volume

The strongest quantified and distinctive accomplishments should survive to the final product.

Not every valid fact belongs on the resume.

### Optimize for convergence, not novelty

Repeated execution should preserve good decisions unless new information or product feedback gives a reason to change them.

### Keep cognition separate from runtime

Contracts define professional authority. Task instructions define repeatable reasoning operations. Python implements orchestration and transport.

The runtime should serve the reasoning architecture rather than redefine it.

---

# Roadmap

Near-term development priorities:

1. Complete Evaluator file-input integration and structured evaluation.
2. Implement Supervisor after-action analysis.
3. Add artifact-specific reuse/regeneration controls for idempotent revision cycles.
4. Externalize candidate identity, education, certifications, and experience containers into candidate profiles.
5. Package dependencies and setup for Linux and Windows.
6. Add portable candidate-corpus initialization and validation.
7. Continue regression testing against known successful job applications.

Longer-term possibilities include passive job discovery, application tracking, Kanban-style workflow management, and broader career-application automation.

---

# Relationship to Rapid Resume System

The original **Rapid Resume System** remains useful as an architecture and design-history repository.

Career Chameleon is the executable successor focused on:

- Smaller runtime-friendly data models.
- Explicit Python orchestration.
- Functional resume construction.
- Evidence authorization separated from candidate analysis.
- Human-in-the-loop evidence recovery.
- Independent evaluation.
- Idempotent revision and artifact reuse.

The project changed names because the vision is larger than rapid resume generation:

> **A candidate is more complex than a resume. Career Chameleon selects the strongest truthful attributes of that candidate and adapts their presentation to the professional environment they are trying to enter.**

The goal is not to pretend to be someone else.

The goal is to make the most relevant parts of who the candidate already is impossible to miss.

---

# Security and Privacy

Professional evidence, resumes, interview responses, logs, and API credentials may contain sensitive information.

Recommended practices:

- Never commit `.env` files or API tokens.
- Keep candidate evidence corpora out of public repositories.
- Keep generated resumes and logs out of source control unless intentionally sanitized.
- Use `.gitignore` before the first commit.
- Rotate credentials immediately if they are accidentally committed.
- Review staged files before pushing to a remote repository.

The public repository should contain the engine, contracts, instructions, models, and safe fixtures—not a candidate's private professional corpus.

---

# Project Status

Career Chameleon is under active development.

The current MVP has already demonstrated end-to-end generation of strong, evidence-backed targeted resumes. The next phase focuses on making evaluation and revision idempotent, then separating candidate-specific configuration from the engine so the system can be safely transplanted to other users.
