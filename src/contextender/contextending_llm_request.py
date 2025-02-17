from typing import Callable

from contextender.utils import max_tv_values_len, text_splitter


def split_llm_request(
    llm: Callable,
    llm_context_len: int,
    prompt_template: str,
    text_template_variable_name: str,
    text: str,
    text_separator: str,
):
    max_text_part_len = max_tv_values_len(
        prompt_template,
        [text_template_variable_name],
        llm_context_len,
    )
    llm_answers = []
    for text_part in text_splitter(text, max_text_part_len, text_separator):
        prompt = prompt_template.format(**{text_template_variable_name: text})
        llm_answer = llm(prompt)
        llm_answers.append(llm_answer)
    return llm_answers


def split_and_join_llm_request(
    llm: Callable,
    llm_context_len: int,
    prompt_template: str,
    text_template_variable_name: str,
    text: str,
    text_separator: str,
    post_process: Callable,
    separator: str,
):
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


def iterating_compression_llm_request(
    llm: Callable,
    llm_context_len: int,
    text: str,
    solve_task_immidiately_prompt: str,
    init_compress_prompt_template: str,
    compress_compression_prompt_template: str,
    final_task_prompt_template: str,
    text_template_variable_name: str = "text",
    compressions_template_variable_name: str = "compressions",
    final_compressions_template_variable_name: str = "compressions",
    text_separator: str = " ",
    compression_items_prefix: str = "NEW ITEM:\n",
    compression_items_separator: str = "\n\n",
):
    # Try to solve task with one single prompt
    if len(solve_task_immidiately_prompt) <= llm_context_len:
        return llm(solve_task_immidiately_prompt)

    # Initial compression
    compressions_str = split_and_join_llm_request(
        llm,
        llm_context_len,
        init_compress_prompt_template,
        text_template_variable_name,
        text,
        text_separator,
        lambda s: compression_items_prefix + s,
        compression_items_separator,
    )

    # Compress compressions until it is possivle to render final_task_prompt
    max_final_compressions_len = max_tv_values_len(
        final_task_prompt_template,
        [final_compressions_template_variable_name],
        llm_context_len,
    )
    while len(compressions_str) > max_final_compressions_len:
        compressions_str = split_and_join_llm_request(
            llm,
            llm_context_len,
            compress_compression_prompt_template,
            compressions_template_variable_name,
            compressions_str,
            compression_items_prefix,
            lambda s: compression_items_prefix + s,
            compression_items_separator,
        )

    # Solve task
    final_prompt = final_task_prompt_template.format(
        **{final_compressions_template_variable_name: compressions_str}
    )
    final_answer = llm(final_prompt)
    return final_answer
