import os
from crewai_tools import EXASearchTool

class ExaSearchToolSet():
    @staticmethod
    def tools():
        # Use the built-in EXASearchTool from crewai_tools
        # It will automatically use the EXA_API_KEY from environment variables
        return [
            EXASearchTool(),
        ]