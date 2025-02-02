from common import Task, API_HOST
import os
from urllib.parse import urljoin


def build_errors(store: dict, keys: list[str]) -> list[str]:
    err_msgs: list[str] = []
    for key in keys:
        if key not in store or not store[key]:
            err_msgs.append(f"{key} cannot be empty")
    return err_msgs


def get_endpoint(task: Task) -> str:
    match task:
        case Task.INTERACTION_DESIGN:
            return urljoin(
                API_HOST, os.environ.get("INTERACTION_DESIGN_PATH", "").lstrip("/")
            )
        case Task.LOGIC_DESIGN:
            return urljoin(
                API_HOST, os.environ.get("LOGIC_DESIGN_PATH", "").lstrip("/")
            )
