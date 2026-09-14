from resume_system.models_reduced import JobAnalysis, EvidenceAuthorization, ResumeContentManifest, InterviewerOutput, CandidateJobAnalysis
from resume_system.context import WorkflowContext
from pydantic import ValidationError

from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

from pathlib import Path

def run_supervisor(context):
    context.logger_client.log("supervisor started")
    
    #call evaluator
    run_evaluator(context)
    return

def run_evaluator(context):
    context.logger_client.log("evaluator started")

    run_writer(context)

    # get current resume docx object and call the evaluator agent

    # Agent inputs
    file_path = Path(__file__).parent/"contracts"/"evaluator.txt"

    with open(file_path,"r") as file:
        contract = file.read()

    file_path = Path(__file__).parent/"instructions"/"evaluate_resume.txt"

    with open(file_path,"r") as file:
        instructions = file.read()

    #TODO: call agent, give resume and job description, get resume evaluation
    #current_resume_json = context.current_candidate_job_analysis.model_dump_json(indent=2)
    #resume_content_manifest = context.agent_client.get_structured_response(contract + instructions, current_candidate_job_analysis_json, ResumeContentManifest, context)
    return

def add_section_heading(document, text):
    paragraph = document.add_paragraph()
    paragraph.paragraph_format.space_before = Pt(10)
    paragraph.paragraph_format.space_after = Pt(3)

    run = paragraph.add_run(text)

    run.bold = True
    run.font.size = Pt(13)

def add_experience_content(document,title_info,resume_experience_content):

    #experience  title
    experience_title = document.add_paragraph()
    experience_title_run = experience_title.add_run(resume_experience_content.selected_title)
    experience_title_run.bold = True

    #static experience one location and time
    experience_title_info_run = experience_title.add_run(title_info)
    experience_title.paragraph_format.space_before = Pt(6)
    experience_title.paragraph_format.space_after = Pt(0)

    # description
    description = document.add_paragraph(resume_experience_content.description)
    description.paragraph_format.space_before = Pt(3)
    description.paragraph_format.space_after = Pt(3)

    # key results header
    key_results_header = document.add_paragraph()
    key_results_header_run = key_results_header.add_run("Key Results")
    key_results_header_run.bold = True
    key_results_header.paragraph_format.space_after = Pt(3)

    # result bullets
    for bullet in resume_experience_content.bullets:
        paragraph = document.add_paragraph(style="List Bullet")
        paragraph.paragraph_format.space_after = Pt(1)
        paragraph.add_run(bullet.text)
    
def render_resume(content_manifest,output_path):
    document = Document()

    # Page margins
    section = document.sections[0]

    section.top_margin = Inches(0.5)
    section.bottom_margin = Inches(0.5)
    section.left_margin = Inches(0.6)
    section.right_margin = Inches(0.6)

    # Default font
    styles = document.styles

    normal_style = styles["Normal"]
    normal_style.font.name = "Arial"
    normal_style.font.size = Pt(10)

    # Header
    name = document.add_paragraph()
    name.alignment = WD_ALIGN_PARAGRAPH.LEFT

    name_run = name.add_run("MAURICE TRAMMELL")
    name_run.bold = True 
    name_run.font.size = Pt(26)

    contact = document.add_paragraph()

    email_header_run = contact.add_run("Email: ")
    email_header_run.bold = True
    email_run = contact.add_run("z.maurice.trammell@gmail.com | ")

    linkedIn_header_run = contact.add_run("LinkedIn: ")
    linkedIn_header_run.bold = True
    linkedIn_run = contact.add_run("www.linkedin.com/in/maurice-trammell | ")

    phone_header_run = contact.add_run("Phone: ")
    phone_header_run.bold = True
    phone_run = contact.add_run("425.500.8778")

    # Professional Summary
    add_section_heading(document,"PROFESSIONAL SUMMARY")
    professional_summary = document.add_paragraph()
    professional_summary.add_run(content_manifest.professional_summary)

    #Education Section
    add_section_heading(document,"EDUCATION")

    education1 = document.add_paragraph()
    masters_degree_run = education1.add_run("Master's of Science in Computer Science")
    masters_degree_run.bold = True
    masters_program_run = education1.add_run(" 一 University of Colorado Boulder")
    education1.paragraph_format.space_before = Pt(0)
    education1.paragraph_format.space_after = Pt(0)

    education2 = document.add_paragraph()
    bachelors_degree_run = education2.add_run("Bachelor's of Science in Information Technology")
    bachelors_degree_run.bold = True
    bachelors_program_run = education2.add_run(" 一 United States Naval Academy")
    education2.paragraph_format.space_before = Pt(0)
    education2.paragraph_format.space_after = Pt(0)

    # Core Skills Section
    add_section_heading(document,"CORE SKILLS")

    skills = document.add_paragraph()
    skills_text = " | ".join(content_manifest.core_skills)
    skills.add_run(skills_text)

    # Certification Section
    add_section_heading(document,"CERTIFICATIONS")

    certifications = document.add_paragraph()
    certifications_text = " | ".join(content_manifest.certifications)
    certifications.add_run(certifications_text)

    # Experience Section
    add_section_heading(document,"KEY PROFESSIONAL EXPERIENCE")

    
    #static experience one location and time
    title_info = [
        ", Independent and Contract Consulting, Hawaii - Washington, Feb 2026 – Present",
        ", United States Marine Corps, Hawaii, May 2022 – May 2026",
        ", United States Marine Corps, Virginia, Jan 2020 – May 2022",
        ", Department of the Navy, Virginia, Jun 2017 – Jan 2020",
    ]

    for index,experience in enumerate(content_manifest.experiences):
        if(index == 4):
            break
        add_experience_content(document, title_info[index],experience)
    
    # Volunteer Section
    add_section_heading(document,"LEADERSHIP & COMMUNITY IMPACT")

    v_title_info = ", Centers for Adaptive Warfighting, NavalX, Oct 2022 - May 2026"
    add_experience_content(document, v_title_info, content_manifest.experiences[4])

    # Save the document object
    document.save(output_path)

def run_writer(context):
    context.logger_client.log("writer started")

    run_analyst(context)

    # Agent inputs
    file_path = Path(__file__).parent/"contracts"/"writer.txt"

    with open(file_path,"r") as file:
        contract = file.read()

    file_path = Path(__file__).parent/"instructions"/"generate_resume_content_manifest.txt"

    with open(file_path,"r") as file:
        instructions = file.read()

    #TODO: call agent, give candidatejobanalysis, get resumecontentmanifest
    #resume_content_manifest_json = context.agent_client.get_fake_resume_content_manifest()
    current_candidate_job_analysis_json = context.current_candidate_job_analysis.model_dump_json(indent=2)
    resume_content_manifest = context.agent_client.get_structured_response(contract + instructions, current_candidate_job_analysis_json, ResumeContentManifest, context)

    # commit manifest json output to fileclient
    #context.file_client.commit_text_file("resume_content_manifest_json", resume_content_manifest_json,"json")
    context.logger_client.log("writer committed resume content manifest json")

    # validate json to get resumecontentmanifest object
    #resume_content_manifest = ResumeContentManifest.model_validate_json(resume_content_manifest_json)
    #context.logger_client.log("writer validated resume content manifest")

    # render the resume
    output_path = context.file_client.get_path()
    render_resume(resume_content_manifest,output_path/"Maurice_Trammell_Resume.docx")
    context.logger_client.log("writer rendered resume")


    return

def run_analyst(context):
    context.logger_client.log("analyst started") 

    #get job description from fileclient
    job_description = context.job_description
    context.logger_client.log("analyst got job description")
    #context.logger_client.term_log(job_description)

    #job_analysis_json = context.agent_client.get_fake_job_analysis()
    # commit analysis json output to fileclient
    #context.file_client.commit_text_file("job_analysis_json",job_analysis_json,"json")
    
    # Agent inputs
    file_path = Path(__file__).parent/"contracts"/"analyst.txt"

    with open(file_path,"r") as file:
        contract = file.read()

    file_path = Path(__file__).parent/"instructions"/"job_analysis.txt"

    with open(file_path,"r") as file:
        instructions = file.read()

    job_analysis = context.agent_client.get_structured_response(contract + instructions,job_description,JobAnalysis,context)
    context.logger_client.log("analyst committed job analysis json")

    #validate json to get jobanalysisobject
    #job_analysis = JobAnalysis.model_validate_json(job_analysis_json)
    #context.logger_client.log("analyst validated job analysis json")

    context.current_job_analysis = job_analysis
    context.logger_client.log("analyst set current job analysis")

    run_custodian(context)

    context.logger_client.log("analyst")

    # TODO: call Agent - getback candidate job analysis map the evidence authorization to the job analysis and create a candidate job analysis

    file_path = Path(__file__).parent/"instructions"/"candidate_job_analysis.txt"

    with open(file_path,"r") as file:
        instructions = file.read()

    job_analysis_json = job_analysis.model_dump_json(indent=2) 
    current_evidence_authorization_json = context.current_evidence_authorization.model_dump_json(indent=2)

    #candidate_job_analysis_json = context.agent_client.get_fake_candidate_job_analysis()
    candidate_job_analysis = context.agent_client.get_structured_response(contract + instructions,job_analysis_json+current_evidence_authorization_json,CandidateJobAnalysis,context)


    # commit analysis json output to fileclient
    # context.file_client.commit_text_file("candidate_job_analysis_json",candidate_job_analysis_json,"json")
    context.logger_client.log("analyst committed candidate job analysis json")

    # validate json to get a candidatejobanalysis object
    #candidate_job_analysis = CandidateJobAnalysis.model_validate_json(candidate_job_analysis_json)
    #context.logger_client.log("analyst validated candidate job analysis json")
  
    context.current_candidate_job_analysis = candidate_job_analysis
    return 

def run_custodian(context):
    context.logger_client.log("custodian started")
    
    #TODO: initialize AI - contract, task instruction, api keys, etc

    #TODO: CREATE RANDOM WHILE LOOP FOR EVIDENCE AUTHORIZATION W/WO INFO REQUESTS

    while(True): # eventually the custodian agent should return an evidence authorization with no open information requests
        #call AI agent - get back an AUTHORIZED EVIDENCE AND/OR INFORMATION REQUESTS
        # Agent inputs
        file_path = Path(__file__).parent/"contracts"/"custodian.txt"

        with open(file_path,"r") as file:
            contract = file.read()

        file_path = Path(__file__).parent/"instructions"/"authorize_evidence.txt"

        with open(file_path,"r") as file:
            instructions = file.read()

        experience_corpus = context.file_client.get_experience_corpus()

        job_analysis_text = context.current_job_analysis.model_dump_json()
        evidence_authorization = context.agent_client.get_structured_response(contract + instructions,job_analysis_text + " " + experience_corpus ,EvidenceAuthorization,context)
        #context.agent_client.get_fake_evidence_authorization()

        #commit evidence authorization json output to fileclient
        #context.file_client.commit_text_file("evidence_authorization_json",evidence_authorization_json,"json")
        context.logger_client.log("custodian committed evidence authorization json")

        #validate json to get evidence authorization object
        #evidence_authorization = EvidenceAuthorization.model_validate_json(evidence_authorization_json)
        #context.logger_client.log("custodian validated evidence authorization json")

        context.current_evidence_authorization = evidence_authorization
        context.logger_client.log("custodian set current evidence authorization")

        # if the evidence authorization has open information requests
        if(len(context.current_evidence_authorization.information_requests) > 0):

            #set working list of current information requests
            context.open_information_requests = context.current_evidence_authorization.information_requests

            #while there are still open information requests
            while(len(context.open_information_requests) > 0):
                context.logger_client.log("custodian - open info requests - calling interviewer")
                run_interviewer(context)
                context.open_information_requests.pop(0)

            context.logger_client.log("custodian - interviewer complete")

        else:
            break

    #TODO: Add evidence into drive

    return

def run_interviewer(context):
    context.logger_client.log("interviewer started")

    #TODO: standardize the information requests structure and retrieval
    #log the length of the open information request list
    context.logger_client.log(f"interviewer - open info requests: {len(context.open_information_requests)}")

    #get the first open evidence request
    current_evidence_request = context.open_information_requests[0]

    file_path = Path(__file__).parent/"contracts"/"interviewer.txt"

    with open(file_path,"r") as file:
        contract = file.read()

    file_path = Path(__file__).parent/"instructions"/"resolve_information_request.txt"

    with open(file_path,"r") as file:
        instruction = file.read()

    #TODO: make while loop for response not being an evidence record

    previous_response_id = None

    # First model input is the InformationRequest
    input_text = (
        current_evidence_request
        .model_dump_json(indent=2)
    )
    
    while(True):
        
        #interviewer_output = context.agent_client.get_fake_random_interviewer_outputs()
        interviewer_output, response_id = context.agent_client.get_conversational_structured_response(contract + instruction, input_text,InterviewerOutput,context,previous_response_id)

        if interviewer_output.output_type == "question":
            #ask a question to the human
            context.logger_client.log("interviewer - question")
            answer = context.message_client.ask_question(interviewer_output.question)
            context.logger_client.log(answer)

            input_text = answer
            previous_response_id = response_id

        elif interviewer_output.output_type == "information_response":
            information_response = interviewer_output.information_response
            context.file_client.commit_text_file(information_response.response_id,information_response.model_dump_json(indent=2),"json")

            break

            
    return 
