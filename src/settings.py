from streamlit.delta_generator import DeltaGenerator
from streamlit.runtime.state import SessionStateProxy
from common import ChatModel, Task, model_endpoints


class Settings:
    def __init__(self, widget: DeltaGenerator, store: SessionStateProxy):
        self.widget = widget
        self.store = store

    def render(self):
        self.widget.header("Settings")
        selected_model: str = self.widget.selectbox(
            "AI model", [model.value for model in ChatModel]
        )
        if selected_model == ChatModel.OTHERS.value:
            self.widget.info("Use another model that is compatible with OpenAI")
            self.store.model = self.widget.text_input("Model ID")
            self.store.endpoint = self.widget.text_input("Model endpoint")
        else:
            self.store.model = selected_model
            self.store.endpoint = model_endpoints[selected_model]

        self.store.api_key = self.widget.text_input(
            "API Key",
            type="password",
            value="" if "api_key" not in self.store else self.store.api_key,
        )

        self.store.task = self.widget.selectbox("Task", [task.value for task in Task])
