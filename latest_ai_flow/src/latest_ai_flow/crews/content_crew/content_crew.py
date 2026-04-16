# src/latest_ai_flow/crews/content_crew/content_crew.py
import os
from typing import List

from crewai import LLM, Agent, Crew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool, WikipediaTools


# Create tools
search_tool = SerperDevTool()
wiki_tool = WikipediaTools()

@CrewBase
class ResearchCrew:
    """Single-agent research crew used inside the Flow."""

    agents: List[BaseAgent]
    tasks: List[Task]

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    # 1. Define the OpenRouter LLM
    # You can change the model string to any model available on OpenRouter
    openrouter_llm = LLM(
        model="openai/gpt-4o-mini",
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
    )

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config["researcher"],  # type: ignore[index]
            verbose=True,
            memory=True,
            tools=[search_tool, wiki_tool],
            # 2. Assign the OpenRouter LLM here
            llm=self.openrouter_llm,
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config["research_task"],  # type: ignore[index]
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
