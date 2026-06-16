import os
import http.client
import json
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.tools import tool
from my_research_agent.models import VCReadyOutput
from langchain_google_genai import ChatGoogleGenerativeAI

# Framework-safe native search tool to completely bypass built-in tool abstractions
@tool("Search the Internet")
def native_serper_search(search_query: str) -> str:
    """
    Search the internet for recent news, market metrics, benchmarks, and competitor data using the Serper API.
    """
    api_key = os.environ.get("SERPER_API_KEY", "")
    if not api_key:
        return "Error: SERPER_API_KEY environment variable is not set."

    try:
        conn = http.client.HTTPSConnection("google.serper.dev")
        payload = json.dumps({"q": search_query, "num": 10})
        headers = {
            'X-API-KEY': api_key,
            'Content-Type': 'application/json'
        }
        conn.request("POST", "/search", payload, headers)
        res = conn.getresponse()
        data = res.read()
        conn.close()
        
        search_results = json.loads(data.decode("utf-8"))
        snippets = []
        if "organic" in search_results:
            for item in search_results["organic"][:5]:
                snippets.append(f"Title: {item.get('title')}\nLink: {item.get('link')}\nSnippet: {item.get('snippet')}\n---")
        return "\n".join(snippets) if snippets else "No highly relevant organic search results found."
    except Exception as e:
        return f"Error executing live search engine call: {str(e)}"


@CrewBase
class MyResearchAgent():
    """Venture Intelligence Multi-Agent System"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    def __init__(self) -> None:
        # The key prefix format that satisfies both LiteLLM and LangChain 4.2.2
        self.llm_instance = ChatGoogleGenerativeAI(
            model="gemini/gemini-2.5-flash",
            temperature=0.5
        )

    @agent
    def data_scout(self) -> Agent:
        return Agent(
            config=self.agents_config['data_scout'],
            tools=[native_serper_search],
            llm=self.llm_instance,
            verbose=True,
            allow_delegation=False
        )

    @agent
    def financial_architect(self) -> Agent:
        return Agent(
            config=self.agents_config['financial_architect'],
            llm=self.llm_instance,
            verbose=True,
            allow_delegation=False
        )

    @agent
    def strategic_auditor(self) -> Agent:
        return Agent(
            config=self.agents_config['strategic_auditor'],
            llm=self.llm_instance,
            verbose=True,
            allow_delegation=False
        )

    @task
    def market_scouting_task(self) -> Task:
        return Task(
            config=self.tasks_config['market_scouting_task'],
        )

    @task
    def economic_modeling_task(self) -> Task:
        return Task(
            config=self.tasks_config['economic_modeling_task'],
        )

    @task
    def investment_audit_task(self) -> Task:
        return Task(
            config=self.tasks_config['investment_audit_task'],
            output_pydantic=VCReadyOutput,
            output_file='final_market_analysis.md'
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents, 
            tasks=self.tasks, 
            process=Process.sequential,
            verbose=True,
        )