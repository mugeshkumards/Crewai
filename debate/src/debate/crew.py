import os

from crewai import Agent, Crew, Process, Task
from crewai.llm import LLM
from crewai.project import CrewBase, agent, crew, task


@CrewBase
class Debate:
    """Debate crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def debater(self) -> Agent:
        return Agent(
            config=self.agents_config["debater"],
            llm=LLM(
                model="openai/gpt-4.1-nano",
                api_key=os.environ.get("OPENROUTER_API_KEY"),
                base_url="https://openrouter.ai/api/v1",
                max_tokens=15000,
            ),
            verbose=True,
        )

    @agent
    def judge(self) -> Agent:
        return Agent(
            config=self.agents_config["judge"],
            llm=LLM(
                model="openai/gpt-4.1-nano",
                api_key=os.environ.get("OPENROUTER_API_KEY"),
                base_url="https://openrouter.ai/api/v1",
                max_tokens=15000,
            ),
            verbose=True,
        )

    @task
    def propose(self) -> Task:
        return Task(
            config=self.tasks_config["propose"],
        )

    @task
    def oppose(self) -> Task:
        return Task(
            config=self.tasks_config["oppose"],
        )

    @task
    def decide(self) -> Task:
        return Task(
            config=self.tasks_config["decide"],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Debate crew"""

        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
