from pathlib import Path

import os
from dotenv import load_dotenv

import discord

import requests
from bs4 import BeautifulSoup

import random

from openai import OpenAI



class WebsiteClient():
    def get_website_text(url):
        # 1. Send an HTTP GET request to the URL
        headers = {"User-Agent": "Mozilla/5.0"}  # Mimic a browser to prevent blocks
        response = requests.get(url, headers=headers)
        
        # Check if the request was successful
        if response.status_code != 200:
            return f"Failed to retrieve webpage. Status code: {response.status_code}"
        
        # 2. Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")
        
        # 3. Remove script and style elements so their code doesn't leak into your text
        for script_or_style in soup(["script", "style"]):
            script_or_style.decompose()
            
        # 4. Extract human-readable text
        # 'separator=" "' keeps words from sticking together when structural tags are removed
        clean_text = soup.get_text(separator=" ", strip=True)
        
        return clean_text
    
class FileClient():
    def __init__(self,job_title):
        self.job_title = job_title
            #TODO: Make the local file path the job title
        self.local_directory_path = Path(self.job_title)
        self.log_file_path = Path(self.job_title+"/log.txt")

    def create_structure(self):
        self.local_directory_path.mkdir(exist_ok=True) # TODO: Move filestructure out of repo

    def get_path(self):
        return self.local_directory_path

    def append_to_log_file(self,message):
        # 3. Create and append to the file
        with open(self.log_file_path, "a") as file:
            file.write("\n")
            file.write(message)

    def commit_text_file(self,file_title,text,extension):
        file_path = Path(self.local_directory_path/f"{file_title}.{extension}")
        with open(file_path,"w") as file:
            file.write(text)

    def get_file_contents(self,file_title,extension):
        file_path = Path(self.local_directory_path/f"{file_title}.{extension}")
        with open(file_path,"r") as file:
            file_contents_text = file.read()
        return file_contents_text

    def get_experience_corpus(self):
        corpus_path = (
            Path(__file__).parent
            / "experience_corpus"
        )

        documents = []

        for file_path in sorted(
            corpus_path.glob("*.yaml")
        ):

            with open(file_path, "r") as file:
                file_contents = file.read()

            documents.append(
                f"""
        --- SOURCE START ---
        filename: {file_path.name}

        {file_contents}

        --- SOURCE END ---
        """
            )

        experience_corpus = "\n".join(
            documents
        )

        return experience_corpus

class LoggerClient():
    def __init__(self,file_client):
        self.file_client = file_client

    def log(self, message):
        self.term_log(message)
        self.file_client.append_to_log_file(message)

    def term_log(self, message):
        print(message)
        return

class AgentClient():
    #define the specs of the agent
    def __init__(self, model="open-ai"):
        self.model = model
    # TODO: do openai api stuff here

    def get_structured_response(self,contract,input,output_model,context):
        # load API key
        load_dotenv()

        # initialize the agent
        client = OpenAI()

        response = client.responses.parse(
            model="gpt-5.6-sol",
            instructions = contract + "Adopt this contract.",
            input = input,
            text_format=output_model
        )

        structured_output = response.output_parsed

        #TODO: save this to the right folder with the fileclient
        context.file_client.commit_text_file(type(structured_output).__name__,structured_output.model_dump_json(indent=2),"json")

        return structured_output

    def get_conversational_structured_response(self,contract,input,output_model,context,previous_response_id=None):
        # load API key
        load_dotenv()

        # initialize the agent
        client = OpenAI()

        response = client.responses.parse(
            model="gpt-5-nano",
            instructions = contract + "Adopt this contract.",
            input = input,
            text_format=output_model,
            previous_response_id=previous_response_id
        )

        structured_output = response.output_parsed

        #TODO: save this to the right folder with the fileclient
        context.file_client.commit_text_file(type(structured_output).__name__,structured_output.model_dump_json(indent=2),"json")

        return structured_output, response.id

    
    ###TEST FUNCTIONS
    def get_fake_job_analysis(self):
        file_path = Path(__file__).parent/"fixtures"/"fake_job_analysis.json"
        with open(file_path,"r") as file:
            file_contents_text = file.read()
        return file_contents_text   

    def get_fake_candidate_job_analysis(self):
        file_path = Path(__file__).parent/"fixtures"/"fake_candidate_job_analysis.json"
        with open(file_path,"r") as file:
            file_contents_text = file.read()
        return file_contents_text              

    def get_fake_evidence_authorization(self):
        file_path = Path(__file__).parent/"fixtures"/"fake_evidence_authorization_b.json"
        with open(file_path,"r") as file:
            file_contents_text = file.read()
        return file_contents_text 
  
    def get_fake_random_evidence_authorization(self):
        num = random.randint(0, 1)
        if(num == 0):
            file_path = Path(__file__).parent/"fixtures"/"fake_evidence_authorization.json"
        elif(num == 1):
            file_path = Path(__file__).parent/"fixtures"/"fake_evidence_authorization_b.json"
        with open(file_path,"r") as file:
            file_contents_text = file.read()
        return file_contents_text 

    def get_fake_information_response(self):
        file_path = Path(__file__).parent/"fixtures"/"fake_information_response.json"
        with open(file_path,"r") as file:
            file_contents_text = file.read()
        return file_contents_text 

    def get_fake_random_interviewer_outputs(self):
        # Generates a random integer between 1 and 10 (inclusive)
        num = random.randint(0, 4)
        fake_interviewer_outputs = ["Test Question 1", "Test Question 2", "Test Question 3", "Test Question 4"]
        if(num<=3):
            return fake_interviewer_outputs[num]
        else:
            return self.get_fake_information_response()

    def get_fake_resume_content_manifest(self):
        file_path = Path(__file__).parent/"fixtures"/"fake_resume_content_manifest.json"
        with open(file_path,"r") as file:
            file_contents_text = file.read()
        return file_contents_text 

class DiscordClient:
    def __init__(self):
        load_dotenv()

        self.token = os.getenv(
            "DISCORD_BOT_TOKEN"
        )

        

    def ask_question(self, question):

        self.question = question
        self.answer = None

        intents = discord.Intents.default()
        intents.message_content = True

        self.client = discord.Client(
            intents=intents
        )

        @self.client.event
        async def on_ready():
            channel = discord.utils.get(
                self.client.guilds[0].text_channels,
                name="general",
            )

            await channel.send(self.question)

            response = await self.client.wait_for(
                "message",
                check=lambda message: (
                    message.author
                    != self.client.user
                ),
            )

            self.answer = response.content

            await self.client.close()

        self.client.run(self.token, log_handler=None)

        return self.answer


def main():
    file_client = FileClient("test")
    experience = file_client.get_experience_corpus()
    print(experience)

if __name__ == "__main__":
    main()