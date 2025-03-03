from typing import Callable

from contextender._config import ITEM_CHOOSE_TASK_MODE, SUMMARY_TASK_MODE
from contextender.item_chooser.item_chooser import choose_item
from contextender.summarizer.summarizer import summarize
from contextender.utils import find_context_len


def contextend(
    llm: Callable,
    text: str,  # TODO: support List[str] also (for item_chooser)
    task_mode: str = SUMMARY_TASK_MODE,
    task: str = None,
    llm_context_len: int = None,
) -> str:
    if llm_context_len is None:
        llm_context_len = find_context_len(llm)
    if task_mode == SUMMARY_TASK_MODE:
        return summarize(text, llm, llm_context_len, task)
    elif task_mode == ITEM_CHOOSE_TASK_MODE:
        return choose_item(text, llm, llm_context_len, task)
    else:
        pass  # TODO: raise error "unknown task_mode"
