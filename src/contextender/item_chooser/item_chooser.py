from typing import Callable, List, Union

from contextender._config import DEFAULT_MAX_COMPRESS_ITERATIONS
from contextender.contextend_llm_request import iterating_split_llm_request
from contextender.item_chooser._prompts import (
    DEFAULT_EXTRA_INSTRUCTIONS,
    FINAL_ITEM_CHOOSE_PROMPT_TEMPLATE_TEMPLATE,
    FINAL_ITEM_CHOOSE_PROMPT_TEMPLATE_VARIABLE_NAME,
    IMMIDIATE_SOLVE_PROMPT_TEMPLATE_TEMPLATE,
    IMMIDIATE_SOLVE_PROMPT_TEMPLATE_VARIABLE_NAME,
    ITEM_CHOOSE_PROMPT_TEMPLATE_TEMPLATE,
    ITEM_CHOOSE_PROMPT_TEMPLATE_VARIABLE_NAME,
    ITEM_PREFIX,
    ITEM_SEPARATOR,
)


def list2text(lst: List[str]):
    return ITEM_PREFIX + (ITEM_SEPARATOR + ITEM_PREFIX).join(lst)


def choose_item(
    context: Union[str, List[str]],
    llm: Callable,
    llm_context_len: int,
    task: str,
    item_separator: str = ITEM_SEPARATOR,
    item_prefix: str = ITEM_PREFIX,
    extra_iteration_instructions=DEFAULT_EXTRA_INSTRUCTIONS,
    max_iterations=DEFAULT_MAX_COMPRESS_ITERATIONS,
):
    if isinstance(context, list):
        context = list2text(context)
    immidiate_solve_prompt_template = IMMIDIATE_SOLVE_PROMPT_TEMPLATE_TEMPLATE.format(
        task=task,
    )
    item_choose_prompt_template = ITEM_CHOOSE_PROMPT_TEMPLATE_TEMPLATE.format(
        extra_instructions=extra_iteration_instructions,
        task=task,
    )
    final_choose_prompt_template = FINAL_ITEM_CHOOSE_PROMPT_TEMPLATE_TEMPLATE.format(
        task=task,
    )
    return iterating_split_llm_request(
        context,
        llm,
        llm_context_len,
        immidiate_solve_prompt_template,
        item_choose_prompt_template,
        item_choose_prompt_template,
        final_choose_prompt_template,
        IMMIDIATE_SOLVE_PROMPT_TEMPLATE_VARIABLE_NAME,
        ITEM_CHOOSE_PROMPT_TEMPLATE_VARIABLE_NAME,
        ITEM_CHOOSE_PROMPT_TEMPLATE_VARIABLE_NAME,
        FINAL_ITEM_CHOOSE_PROMPT_TEMPLATE_VARIABLE_NAME,
        item_separator,
        item_prefix,
        item_separator,
        max_iterations,
    )
