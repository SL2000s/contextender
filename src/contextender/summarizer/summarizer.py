from typing import Dict

from contextender.contextend_llm_request import iterating_split_llm_request
from contextender.summarizer._prompts import (
    DEFAULT_SUMMARIZE_PROMPTS_TEMPLATE_TEMPLATE_VARIABLES,
    DEFAULT_TASK_PROMPT,
    FINAL_SUMMARY_PROMPT,
    IMMIDIATE_SOLVE_PROMPT_TEMPLATE,
    SUMMARIZE_PROMPT_TEMPLATE_TEMPLATE,
    SUMMARIZE_SUMMARIES_PROMPT_TEMPLATE_TEMPLATE,
)


def summarize(
    text: str,
    llm: callable,
    llm_context_len: int,
    immidiate_solve_prompt_template: str = IMMIDIATE_SOLVE_PROMPT_TEMPLATE,
    summarize_prompt_template_template: str = SUMMARIZE_PROMPT_TEMPLATE_TEMPLATE,  # noqa: E501
    summarize_prompt_template_template_variables: Dict[
        str, str
    ] = DEFAULT_SUMMARIZE_PROMPTS_TEMPLATE_TEMPLATE_VARIABLES,  # noqa: E501
    summarize_summaries_prompt_template_template: str = SUMMARIZE_SUMMARIES_PROMPT_TEMPLATE_TEMPLATE,  # noqa: E501
    summarize_summaries_prompt_template_template_variables: Dict[
        str, str
    ] = DEFAULT_SUMMARIZE_PROMPTS_TEMPLATE_TEMPLATE_VARIABLES,  # noqa: E501
    final_summary_prompt_template_template: str = FINAL_SUMMARY_PROMPT,
    task: str = DEFAULT_TASK_PROMPT,
) -> str:

    summarize_prompt_template = summarize_prompt_template_template.format(
        **summarize_prompt_template_template_variables,
    )
    summarize_summaries_prompt_template = (
        summarize_summaries_prompt_template_template.format(
            **summarize_summaries_prompt_template_template_variables,
        )
    )
    final_summary_prompt_template_template
    task
    return iterating_split_llm_request(
        text,
        llm,
        llm_context_len,
        immidiate_solve_prompt_template,
        summarize_prompt_template,
        summarize_summaries_prompt_template,
        # final_task_prompt_template,
        # text_template_variable_name,
        # compressions_template_variable_name,
        # final_compressions_template_variable_name,
        # text_separator,
        # compression_items_prefix,
        # compression_items_separator,
    )


def summarize_for_task():
    pass
