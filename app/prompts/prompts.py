from enum import Enum
from langchain_core.prompts import ChatPromptTemplate


class PromptTemplates(Enum):
    REPORT_SUMMARY = ChatPromptTemplate.from_template(
        "Generate a concise summary of the following healthcare report data: {data}"
    )
