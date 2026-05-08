import os
import time  # NEW: Required for the delay
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool

# Import your model
from my_research_agent.models import VCReadyOutput 

@CrewBase
class MyResearchAgent():
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    search_tool = SerperDevTool()

    # We keep temperature low for more stable VC-grade output
    llm = LLM(model="gemini/gemini-2.5-flash", temperature=0.5)

    @agent
    def data_scout(self) -> Agent:
        return Agent(config=self.agents_config['data_scout'], llm=self.llm, tools=[self.search_tool])

    @agent
    def financial_architect(self) -> Agent:
        return Agent(config=self.agents_config['financial_architect'], llm=self.llm)

    @agent
    def strategic_auditor(self) -> Agent:
        return Agent(config=self.agents_config['strategic_auditor'], llm=self.llm)

    @task
    def market_scouting_task(self) -> Task:
        return Task(config=self.tasks_config['market_scouting_task'], tools=[self.search_tool])

    @task
    def economic_modeling_task(self) -> Task:
        return Task(config=self.tasks_config['economic_modeling_task'])

    @task
    def investment_audit_task(self) -> Task:
        return Task(
            config=self.tasks_config['investment_audit_task'],
            output_pydantic=VCReadyOutput 
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential, 
            verbose=True,
            # FIX 1: Limit requests per minute to stay under Free Tier limits
            max_rpm=10, 
            # FIX 2: Explicitly pause for 2 seconds after EVERY agent step
            step_callback=lambda step: time.sleep(2) 
        )