from enum import Enum
import os


class ChatModel(Enum):
    QWEN = "qwen-turbo"
    GPT = "gpt-4o-mini"
    DEEPSEEK = "deepseek-chat"
    OTHERS = "..."


model_endpoints: dict[str, str] = {
    ChatModel.GPT.value: "https://api.openai.com/v1",
    ChatModel.QWEN.value: "https://dashscope.aliyuncs.com/compatible-mode/v1",
    ChatModel.DEEPSEEK.value: "https://api.deepseek.com/v1",
}


class Task(Enum):
    INTERACTION_DESIGN = "Generate Interaction Prototype"
    LOGIC_DESIGN = "Generate Business Process"


resp_formats: dict[str, str] = {
    Task.INTERACTION_DESIGN.value: "html",
    Task.LOGIC_DESIGN.value: "puml",
}

API_HOST = os.environ.get("API_HOST", "")
PRODUCT_NAME = "Software Designer"
PRODUCT_TITLE = f"{PRODUCT_NAME} - An AI partner for software developers "
PUML_API = os.environ.get("PUML_API", "")

setting_items = ["model", "endpoint", "api_key"]
