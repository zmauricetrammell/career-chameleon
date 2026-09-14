from pathlib import Path

from resume_system.clients import DiscordClient,FileClient,LoggerClient,WebsiteClient,AgentClient
from resume_system.context import WorkflowContext
from resume_system.workflow import run_supervisor

def main():

    job_title = "IT Manager"
    #job_title = input("Enter job title ")
    #job_description_url = input("Enter URL of job description ")

    #job_description_text = WebsiteClient.get_website_text(job_description_url)    
    
    file_path = Path(__file__).parent/"fixtures"/"job_description.txt"

    with open(file_path,"r") as file:
        job_description_text = file.read()

    #job_description_text = input("Enter job description text")

    file_client = FileClient(job_title)
    logger_client = LoggerClient(file_client)
    discord_client = DiscordClient()
    agent_client = AgentClient()

    #create folder structure using FileClient
    file_client.create_structure()

    #save job description to a file
    file_client.commit_text_file("job_description",job_description_text,"txt")

    context = WorkflowContext(
        job_title=job_title,
        file_client=file_client,
        message_client=discord_client,
        agent_client=agent_client,
        logger_client=logger_client,
        job_description=job_description_text,
    )

    run_supervisor(context)



if __name__ == "__main__":
    main()