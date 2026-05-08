from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from my_research_agent.models import VCReadyOutput  # Critical: Importing your vision's model

@CrewBase
class MyResearchAgent():
    """Venture Intelligence Multi-Agent System"""

    # --- CONFIG PATHS ---
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    def __init__(self) -> None:
        # 2026 Strategy: Use string-based LLM for maximum stability 
        # across local and Streamlit Cloud environments.
        self.llm = "gemini/gemini-2.5-flash"

    @agent
    def data_scout(self) -> Agent:
        return Agent(
            config=self.agents_config['data_scout'],
            tools=[SerperDevTool()],
            llm=self.llm,
            verbose=True
        )

    @agent
    def financial_architect(self) -> Agent:
        return Agent(
            config=self.agents_config['financial_architect'],
            llm=self.llm,
            verbose=True
        )

    @agent
    def strategic_auditor(self) -> Agent:
        return Agent(
            config=self.agents_config['strategic_auditor'],
            llm=self.llm,
            verbose=True
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
        """
        The final audit task now uses the VCReadyOutput model to ensure 
        the UI can safely read 'investment_thesis' and 'market_sizing'.
        """
        return Task(
            config=self.tasks_config['investment_audit_task'],
            output_pydantic=VCReadyOutput,  # Bridges the Agent output to your Model
            output_file='final_market_analysis.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Venture Intelligence crew"""
        return Crew(
            agents=self.agents, 
            tasks=self.tasks, 
            process=Process.sequential,
            verbose=True,
        )