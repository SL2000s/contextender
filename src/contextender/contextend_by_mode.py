from typing import Callable, List, Union

from contextender._config import ITEM_CHOOSE_TASK_MODE, SUMMARY_TASK_MODE
from contextender.summarizer.summarizer import summarize
from contextender.text_item_chooser.item_chooser import choose_item
from contextender.utils import find_context_len


def contextend(
    llm: Callable,
    context: Union[str, List[str]],
    task_mode: str = SUMMARY_TASK_MODE,
    task: str = None,
    llm_context_len: int = None,
) -> str:
    if llm_context_len is None:
        llm_context_len = find_context_len(llm)
    if task_mode == SUMMARY_TASK_MODE:
        return summarize(context, llm, llm_context_len, task)
    elif task_mode == ITEM_CHOOSE_TASK_MODE:
        return choose_item(context, llm, llm_context_len, task)
    else:
        pass  # TODO: raise error "unknown task_mode"
