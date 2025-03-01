from contextender.summarizer._prompts import (
    DEFAULT_TASK,
    FINAL_SUMMARY_PROMPT_TEMPLATE_TEMPLATE,
    IMMIDIATE_SOLVE_PROMPT_TEMPLATE_TEMPLATE,
)
from contextender.summarizer.summarizer import summarize


# Simulated LLM function for testing
def simulated_llm(prompt):
    return prompt[:50]


def test_immidiate_summarize():
    text = "a" * 50
    llm_context_len = 1 << 30
    expected = simulated_llm(
        IMMIDIATE_SOLVE_PROMPT_TEMPLATE_TEMPLATE.format(
            task=DEFAULT_TASK,
        ).format(text=text)
    )
    result = summarize(text, simulated_llm, llm_context_len)
    assert result == expected


def test_1_iteration_summarize():
    text = "This is a sample text for testing the summarize function." * 12
    llm_context_len = 700
    expected = simulated_llm(
        FINAL_SUMMARY_PROMPT_TEMPLATE_TEMPLATE
    )  # NOTE: approximation
    result = summarize(text, simulated_llm, llm_context_len)
    assert result == expected


def test_2_iteration_summarize():
    text = "This is a sample text for testing the summarize function." * 50
    llm_context_len = 700
    expected = simulated_llm(
        FINAL_SUMMARY_PROMPT_TEMPLATE_TEMPLATE
    )  # NOTE: approximation
    result = summarize(text, simulated_llm, llm_context_len)
    assert result == expected


def test_summarize_empty_text():
    text = ""
    llm_context_len = 1 << 30
    expected = simulated_llm(
        IMMIDIATE_SOLVE_PROMPT_TEMPLATE_TEMPLATE.format(task=DEFAULT_TASK).format(
            text=text
        )
    )
    result = summarize(text, simulated_llm, llm_context_len)
    assert result == expected


def test_infinity_iteration_summarize():  # TODO
    pass


if __name__ == "__main__":  # TODO: remove
    test_summarize_empty_text()
