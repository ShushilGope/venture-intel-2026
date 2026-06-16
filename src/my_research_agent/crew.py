from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.llm import LLM
from crewai_tools import SerperDevTool
from my_research_agent.models import VCReadyOutput
from langchain_google_genai import ChatGoogleGenerativeAI

@CrewBase
class MyResearchAgent():
    """Venture Intelligence Multi-Agent System"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    def __init__(self) -> None:
        # 1. Main Agent Core LLM: Clean LangChain implementation
        self.llm_instance = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.5
        )
        
        # 2. Tool-Isolated Context LLM: Clean CrewAI wrapper context
        # This completely satisfies the internal LiteLLM parser used by SerperDevTool
        self.tool_llm = LLM(
            model="gemini/gemini-2.5-flash",
            temperature=0.3
        )

    @agent
    def data_scout(self) -> Agent:
        return Agent(
            config=self.agents_config['data_scout'],
            # Explicitly pass the separate tool_llm straight to the tool configuration
            tools=[SerperDevTool(llm=self.tool_llm)],
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