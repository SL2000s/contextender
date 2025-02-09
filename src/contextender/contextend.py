from contextender._config import ITEM_CHOOSE_TASK_MODE, SUMMARY_TASK_MODE
from contextender.summarizer import summarize
from contextender.utils import find_context_len


def contextend(
    llm: callable,
    text: str,
    task_mode: str = SUMMARY_TASK_MODE,
    task: str = None,
    llm_context_len: int = None,
) -> str:
    if llm_context_len is None:
        llm_context_len = find_context_len(llm)
    if task_mode == SUMMARY_TASK_MODE:
        return summarize(llm, text, llm_context_len, task)
    elif task_mode == ITEM_CHOOSE_TASK_MODE:
        pass
    else:
        pass  # TODO: raise error "unknown task_mode"
