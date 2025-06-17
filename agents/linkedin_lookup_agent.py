from dotenv import load_dotenv
load_dotenv()
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate  # Fixed import
from langchain_core.tools import Tool
from langchain.agents import (
    create_react_agent,
    AgentExecutor,
)
from langchain_ollama import ChatOllama
from langsmith import Client
from langchain import hub
from tools.tools import get_profile_url_tavily
import os

def lookup(name: str) -> str:
    llm = ChatOllama(model="llama3")
    
    # This template formats the input for the agent
    template = """given the full name {name_of_person} I want you to get me a link to their LinkedIn profile page.
                  Your answer should contain only a URL"""
    prompt_template = PromptTemplate(
        template=template, input_variables=["name_of_person"]
    )
    
    tools_for_agent = [
        Tool(
            name="Crawl Google 4 linkedin profile page",
            func=get_profile_url_tavily,
            description="useful for when you need get the LinkedIn Page URL",
        )
    ]
    
    client = Client(api_key=os.getenv("LANGSMITH_API_KEY"))
    prompt = client.pull_prompt("hwchase17/react", include_model=True)
    agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)
    
    # Fixed: use .format() instead of .format_prompt()
    formatted_input = prompt_template.format(name_of_person=name)
    result = agent_executor.invoke(input={"input": formatted_input})
    
    linked_profile_url = result["output"]
    return linked_profile_url

if __name__ == "__main__":  # Fixed syntax
    print(lookup(name="Eden Marco Udemy"))