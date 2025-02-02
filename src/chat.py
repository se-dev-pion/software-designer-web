import streamlit as st
from plantuml import PlantUML
from common import Task, setting_items, PRODUCT_NAME, resp_formats, PUML_API
from utils import get_endpoint, build_errors
from dataclasses import dataclass, asdict
import requests, uuid, time


@dataclass
class GenerateRequestBody:
    endpoint: str
    model: str
    entry: str


class ChatPage:
    api_endpoints: dict[str, str] = {
        Task.INTERACTION_DESIGN.value: get_endpoint(Task.INTERACTION_DESIGN),
        Task.LOGIC_DESIGN.value: get_endpoint(Task.LOGIC_DESIGN),
    }
    puml_client = PlantUML(url=PUML_API)

    def __init__(self):
        self.widget = st
        self.store = st.session_state

    def render(self):
        self.widget.title(PRODUCT_NAME)
        if "messages" not in self.store:
            self.store.messages = []
        chat_container = self.widget.container()
        with chat_container:
            for i, msg in enumerate(self.store.messages):
                with self.widget.chat_message(msg["role"]):
                    match msg["role"]:
                        case "user":
                            self.widget.markdown(msg["content"])
                        case "assistant":
                            col1, col2 = self.widget.columns([1, 1])
                            with col1:
                                if self.widget.button(
                                    label="Preview", key=f"preview-{i}"
                                ):
                                    match msg["type"]:
                                        case "html":
                                            self.widget.html(msg["content"])
                                        case "puml":
                                            self.widget.image(
                                                self.puml_client.get_url(msg["content"])
                                            )
                            with col2:
                                self.widget.download_button(
                                    label="Export",
                                    key=f"export-{i}",
                                    data=msg["content"],
                                    mime="text/plain",
                                    file_name=f"{uuid.uuid4()}.{msg['type']}",
                                )

        if prompt := self.widget.chat_input("Input your prompt here"):
            if err_msgs := build_errors(self.store, setting_items):
                for msg in err_msgs:
                    self.widget.error(msg)
            else:
                req_body: dict[str, str] = asdict(
                    GenerateRequestBody(
                        endpoint=self.store.endpoint,
                        model=self.store.model,
                        entry=prompt,
                    )
                )
                self.store.messages.append({"role": "user", "content": prompt})
                with chat_container:
                    with self.widget.chat_message("assistant"):
                        self.widget.markdown("Generating...")
                response = requests.post(
                    url=self.api_endpoints[self.store.task],
                    json=req_body,
                    headers={
                        "Authorization": self.store.api_key,
                    },
                )
                if response.status_code == 200:
                    content: str = (
                        response.text.replace("\\n", "\n")
                        .replace('\\"', '"')
                        .strip('"')
                    )
                    msg_type = resp_formats[self.store.task]
                    if msg_type == "puml" and content.endswith("@end"):
                        content = content.replace("@end", "@enduml")
                    self.store.messages.append(
                        {
                            "role": "assistant",
                            "type": msg_type,
                            "content": content,
                        }
                    )
                    self.widget.toast("Generation Success!")
                    time.sleep(1)
                    st.rerun()
                else:
                    self.widget.error(f"Error: {response.status_code} {response.text}")
