from textwrap import dedent
from crewai import Agent, LLM
from tools import ExaSearchToolSet
import os

class MeetingPrepAgents():
    def __init__(self):
        # Gunakan CrewAI's LLM class dengan format litellm yang benar
        self.llm = LLM(
            model="gemini/gemini-2.0-flash-exp",
            api_key=os.getenv("GOOGLE_API_KEY")
        )
    
    def research_agent(self):
        return Agent(
            role="Research Specialist",
            goal='Conduct thorough research on people and companies involved in the meeting',
            tools=ExaSearchToolSet.tools(),
            backstory=dedent("""\
                As a Research Specialist, your mission is to uncover detailed information
                about the individuals and entities participating in the meeting. Your insights
                will lay the groundwork for strategic meeting preparation."""),
            llm=self.llm,
            verbose=True
        )
    
    def industry_analysis_agent(self):
        return Agent(
            role='Industry Analyst',
            goal='Analyze the current industry trends, challenges, and opportunities',
            tools=ExaSearchToolSet.tools(),
            backstory=dedent("""\
                As an Industry Analyst, your analysis will identify key trends,
                challenges facing the industry, and potential opportunities that
                could be leveraged during the meeting for strategic advantage."""),
            llm=self.llm,
            verbose=True
        )
    
    def meeting_strategy_agent(self):
        return Agent(
            role='Meeting Strategy Advisor',
            goal='Develop talking points, questions, and strategic angles for the meeting',
            backstory=dedent("""\
                As a Strategy Advisor, your expertise will guide the development of
                talking points, insightful questions, and strategic angles
                to ensure the meeting's objectives are achieved."""),
            llm=self.llm,
            verbose=True
        )
    
    def summary_and_briefing_agent(self):
        return Agent(
            role='Briefing Coordinator',
            goal='Compile all gathered information into a concise, informative briefing document',
            backstory=dedent("""\
                As the Briefing Coordinator, your role is to consolidate the research,
                analysis, and strategic insights."""),
            llm=self.llm,
            verbose=True
        )