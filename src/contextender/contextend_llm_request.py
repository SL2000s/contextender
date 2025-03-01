from typing import Callable, List

from contextender._config import DEFAULT_MAX_COMPRESS_ITERATIONS
from contextender.utils import max_tv_values_len, text_splitter


def split_llm_request(
    llm: Callable,
    llm_context_len: int,
    prompt_template: str,
    text_template_variable_name: str,  # TODO: input template variables instead
    text: str,
    text_separator: str,
) -> List[str]:
    max_text_part_len = max_tv_values_len(
        prompt_template,
        [text_template_variable_name],
        llm_context_len,
    )
    if max_text_part_len <= 0:
        raise ValueError("prompt_template is bigger than llm_context_len")
    llm_answers = []
    for text_part in text_splitter(text, max_text_part_len, text_separator):
        prompt = prompt_template.format(**{text_template_variable_name: text})
        llm_answer = llm(prompt)
        llm_answers.append(llm_answer)
    return llm_answers


def split_join_llm_request(
    llm: Callable,
    llm_context_len: int,
    prompt_template: str,
    text_template_variable_name: str,  # TODO: input template variables instead
    text: str,
    text_separator: str,
    post_process: Callable,
    separator: str,
) -> str:
    llm_answers = split_llm_request(
        llm,
        llm_context_len,
        prompt_template,
        text_template_variable_name,
        text,
        text_separator,
    )
    post_processed_answers = [post_process(ans) for ans in llm_answers]
    separator.join(post_processed_answers)


def iterating_split_llm_request(
    text: str,
    llm: Callable,
    llm_context_len: int,
    immidiate_solve_prompt_template: str,
    init_compress_prompt_template: str,
    compress_compression_prompt_template: str,
    final_task_prompt_template: str,
    immidiate_text_template_variable_name: str = "text",
    init_text_template_variable_name: str = "text",
    compressions_template_variable_name: str = "compressions",
    final_compressions_template_variable_name: str = "compressions",
    text_separator: str = " ",
    compression_item_prefix: str = "NEW ITEM:\n",
    compression_items_separator: str = "\n\n",
    max_iterations: int = DEFAULT_MAX_COMPRESS_ITERATIONS,
) -> str:
    # Try to solve task with one single prompt
    immidiate_solve_prompt = immidiate_solve_prompt_template.format(
        **{immidiate_text_template_variable_name: text}
    )
    if len(immidiate_solve_prompt) <= llm_context_len:
        return llm(immidiate_solve_prompt)

    # Initial compression
    compressions_str = split_join_llm_request(
        llm,
        llm_context_len,
        init_compress_prompt_template,
        init_text_template_variable_name,
        text,
        text_separator,
        lambda s: compression_item_prefix + s,
        compression_items_separator,
    )

    # Compress compressions until it is possivle to render final_task_prompt
    max_final_compressions_len = max_tv_values_len(
        final_task_prompt_template,
        [final_compressions_template_variable_name],
        llm_context_len,
    )
    count_iterations = 1
    while len(compressions_str) > max_final_compressions_len:
        if count_iterations > max_iterations:
            raise RuntimeError(
                "Maximum iterations reached during compression."
            )  # noqa: E501
        new_compressions_str = split_join_llm_request(
            llm,
            llm_context_len,
            compress_compression_prompt_template,
            compressions_template_variable_name,
            compressions_str,
            compression_item_prefix,
            lambda s: compression_item_prefix + s,
            compression_items_separator,
        )
        if len(new_compressions_str) >= len(compressions_str):
            raise RuntimeError("Infinite loop detected during compression.")
        compressions_str = new_compressions_str
        count_iterations += 1

    # Solve task
    final_prompt = final_task_prompt_template.format(
        **{final_compressions_template_variable_name: compressions_str}
    )
    final_answer = llm(final_prompt)
    return final_answer
