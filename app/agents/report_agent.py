from langchain_openai import ChatOpenAI
from app.config.settings import load_settings
from app.prompts.prompts import PromptTemplates

settings = load_settings()


class ReportAgent:
    def __init__(self, model_name: str = settings.model_name):
        self.llm = ChatOpenAI(model_name=model_name, temperature=0)

    def generate_report_summary(self, data: str) -> str:
        prompt = PromptTemplates.REPORT_SUMMARY.value.format(data=data)
        response = self.llm.generate([prompt])
        return response.generations[0][0].text
