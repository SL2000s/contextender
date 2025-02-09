from contextender._prompts import (
    DEFAULT_SUMMARY_CONSTRAINTS_PROMPT,
    DEFAULT_TASK_PROMPT,
    POST_SUMMARY_TASK_PROMPT,
    SOLVE_TASK_IMMIDIATELY_PROMPT,
    SOLVE_TASK_PROMPT,
    SUMMARIZE_PROMPT,
    SUMMARIZE_SUMMARIES_PROMPT,
    SUMMARY_ITEM,
    SUMMARY_ITEM_PREFIX,
)
from contextender.utils import text_splitter


def summarize(
    llm: callable,
    text: str,
    llm_context_len: int,
    task: str = DEFAULT_TASK_PROMPT,
    constraints: str = DEFAULT_SUMMARY_CONSTRAINTS_PROMPT,
) -> str:
    solve_task_immidiately_prompt = SOLVE_TASK_IMMIDIATELY_PROMPT.format(
        text=text,
        task=task,
    )
    if len(solve_task_immidiately_prompt) <= llm_context_len:
        return llm(solve_task_immidiately_prompt)
    extra_instructions = POST_SUMMARY_TASK_PROMPT.format(task=task)
    summaries = []
    max_len_text_part = (
        llm_context_len
        - len(SUMMARIZE_PROMPT)
        - len(constraints)
        - len(extra_instructions)
    )
    for text_part in text_splitter(text, max_len_text_part):
        summarize_prompt = SUMMARIZE_PROMPT.format(
            constraints=constraints,
            extra_instructions=extra_instructions,
            text=text_part,
        )
        llm_summary = llm(summarize_prompt)
        summary_item = SUMMARY_ITEM.format(summary=llm_summary)
        summaries.append(summary_item)
    summaries_str = "\n".join(summaries)
    prompt_len = len(SOLVE_TASK_PROMPT) + len(summaries_str) + len(task)
    while prompt_len > llm_context_len:
        summaries = []
        for text_part in text_splitter(
            summaries_str, llm_context_len, SUMMARY_ITEM_PREFIX
        ):
            summarize_prompt = SUMMARIZE_SUMMARIES_PROMPT.format(
                constraints=constraints,
                extra_instructions=extra_instructions,
                summaries=text_part,
            )
            llm_summary = llm(summarize_prompt)
            summary_item = SUMMARY_ITEM_PREFIX.format(summary=llm_summary)
            summaries.append(summary_item)
        summaries_str = "\n".join(summaries)
        prompt_len = len(SOLVE_TASK_PROMPT) + len(summaries_str) + len(task)

    solve_task_prompt = SOLVE_TASK_PROMPT.format(
        summaries=summaries_str,
        task=task,
    )
    return llm(solve_task_prompt)
