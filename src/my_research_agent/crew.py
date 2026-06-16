from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from my_research_agent.models import VCReadyOutput
from langchain_google_genai import ChatGoogleGenerativeAI

@CrewBase
class MyResearchAgent():
    """Venture Intelligence Multi-Agent System"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    def __init__(self) -> None:
        # One clean, explicit model instance used globally across the entire pipeline
        self.llm_instance = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.5
        )

    @agent
    def data_scout(self) -> Agent:
        return Agent(
            config=self.agents_config['data_scout'],
            # Explicitly passing the langchain instance directly to the search tool config
            # overrides CrewAI's default LiteLLM parser path completely!
            tools=[SerperDevTool(llm=self.llm_instance)],
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