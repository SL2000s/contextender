from contextender._config import DEFAULT_MAX_COMPRESS_ITERATIONS
from contextender.contextend_llm_request import iterating_split_llm_request
from contextender.summarizer._prompts import (
    DEFAULT_SUMMARY_CONSTRAINTS,
    DEFAULT_TASK,
    DEFAULT_TEXT_SEPARATOR,
    FINAL_SUMMARY_PROMPT_TEMPLATE_TEMPLATE,
    FINAL_SUMMARY_PROMPT_TEMPLATE_VARIABLE_NAME,
    IMMEDIATE_SOLVE_PROMPT_TEMPLATE_TEMPLATE,
    IMMEDIATE_SOLVE_PROMPT_TEMPLATE_VARIABLE_NAME,
    SUMMARIZE_PROMPT_TEMPLATE_TEMPLATE,
    SUMMARIZE_PROMPT_TEMPLATE_VARIABLE_NAME,
    SUMMARIZE_SUMMARIES_PROMPT_TEMPLATE_TEMPLATE,
    SUMMARIZE_SUMMARIES_TEMPLATE_VARIABLE_NAME,
    SUMMARY_ITEM_PREFIX,
    SUMMARY_ITEMS_SEPARATOR,
    TASK2EXTRA_INSTRUCTIONS,
)


def summarize(
    text: str,
    llm: callable,
    llm_context_len: int,
    task: str = DEFAULT_TASK,
    summary_constraints: str = DEFAULT_SUMMARY_CONSTRAINTS,
    text_separator: str = DEFAULT_TEXT_SEPARATOR,
    max_iterations: int = DEFAULT_MAX_COMPRESS_ITERATIONS,
) -> str:
    immediate_solve_prompt_template = IMMEDIATE_SOLVE_PROMPT_TEMPLATE_TEMPLATE.format(
        task=task,
    )
    extra_instructions = TASK2EXTRA_INSTRUCTIONS.format(task=task)
    summarize_prompt_template = SUMMARIZE_PROMPT_TEMPLATE_TEMPLATE.format(
        constraints=summary_constraints,
        extra_instructions=extra_instructions,
    )
    summarize_summaries_prompt_template = (
        SUMMARIZE_SUMMARIES_PROMPT_TEMPLATE_TEMPLATE.format(
            constraints=summary_constraints,
            extra_instructions=extra_instructions,
        )
    )
    final_summary_prompt_template = FINAL_SUMMARY_PROMPT_TEMPLATE_TEMPLATE.format(
        task=task,
    )
    return iterating_split_llm_request(
        text,
        llm,
        llm_context_len,
        immediate_solve_prompt_template,
        summarize_prompt_template,
        summarize_summaries_prompt_template,
        final_summary_prompt_template,
        IMMEDIATE_SOLVE_PROMPT_TEMPLATE_VARIABLE_NAME,
        SUMMARIZE_PROMPT_TEMPLATE_VARIABLE_NAME,
        SUMMARIZE_SUMMARIES_TEMPLATE_VARIABLE_NAME,
        FINAL_SUMMARY_PROMPT_TEMPLATE_VARIABLE_NAME,
        text_separator,
        SUMMARY_ITEM_PREFIX,
        SUMMARY_ITEMS_SEPARATOR,
        max_iterations,
    )
