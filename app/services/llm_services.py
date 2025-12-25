from langchain_openai import ChatOpenAI
from pydantic import BaseModel, SecretStr


class AuditResult(BaseModel):
    is_valid: bool
    feedback: str
    risk_score: float


def create_llm(model_name: str, api_key: str) -> ChatOpenAI:
    return ChatOpenAI(model=model_name, temperature=0, api_key=SecretStr(api_key))


def create_audit_llm(model_name: str, api_key: str) -> ChatOpenAI:
    return ChatOpenAI(
        model=model_name, temperature=0, api_key=SecretStr(api_key)
    ).with_structured_output(schema=AuditResult, method="json_schema")  # type: ignore
