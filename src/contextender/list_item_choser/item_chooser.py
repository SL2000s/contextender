from typing import Callable, List

from contextender._config import DEFAULT_MAX_COMPRESS_ITERATIONS
from contextender.list_item_chooser._prompts import (
    ITEM_CHOOSE_PROMPT_TEMPLATE,
    ITEMS_TEMPLATE_VARIABLE,
    TASK_TEMPLATE_VARIABLE,
)
from contextender.utils import extract_list


def choose_item(
    items: List,
    llm: Callable,
    task: str,
    max_nr_iteration_items: int,
    iteration_task: str = None,
    item_choose_prompt_template: str = ITEM_CHOOSE_PROMPT_TEMPLATE,
    task_template_variable: str = TASK_TEMPLATE_VARIABLE,
    items_template_variable: str = ITEMS_TEMPLATE_VARIABLE,
    max_iterations=DEFAULT_MAX_COMPRESS_ITERATIONS,
):
    """Choose the most relevant items from a list according to a task.

    Args:
        items (List): A list of items.
        llm (Callable): An LLM that takes a prompt as input and outputs the response as a string.
        task (str): The task to solve (e.g. 'Choose the largest integer').
        max_nr_iteration_items (int): The maximum number of items to consider in each iteration/llm request.
        iteration_task (str, optional): The subtask to solve in each iteration (e.g. 'Choose the two largest integers') to pick out the final items to solve the main task. Defaults to None, and in that case, the main task will be used.
        max_iterations (int, optional): The maximum number of iterations. Defaults to DEFAULT_MAX_COMPRESS_ITERATIONS.

    Returns:
        List: A list of the most relevant items.
    """  # noqa: E501
    iteration_task = task if iteration_task is None else iteration_task
    iteration = 0
    while len(items) > max_nr_iteration_items:
        iteration += 1
        if iteration > max_iterations:
            raise RuntimeError(
                f"Exceeded maximum number of iterations ({max_iterations})"
            )
        next_items = []
        for i in range(0, len(items), max_nr_iteration_items):
            iteration_items = items[i : min(i + max_nr_iteration_items, len(items))]
            prompt = item_choose_prompt_template.format(
                **{
                    task_template_variable: iteration_task,
                    items_template_variable: iteration_items,
                }
            )
            llm_response = llm(prompt)
            next_items += extract_list(llm_response)
        if len(next_items) >= len(items):
            raise RuntimeError("Infinite loop detected during compression.")
        items = next_items
    final_prompt = item_choose_prompt_template.format(
        **{task_template_variable: task, items_template_variable: items}
    )
    llm_response = llm(final_prompt)
    items = extract_list(llm_response)
    return items
