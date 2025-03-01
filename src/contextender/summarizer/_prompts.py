DEFAULT_TASK_PROMPT = "Summarize this text."

IMMIDIATE_SOLVE_PROMPT_TEMPLATE = """Given the text below, solve the task below.

TEXT:
{text}

TASK:
{task}
"""  # noqa: E501
IMMIDIATE_SOLVE_PROMPT_TEMPLATE_VARIABLE_NAME = "text"

SUMMARIZE_PROMPT_TEMPLATE_TEMPLATE = """You are an assistant summarizing texts.
Summarize the text below as good as you can (it is a part of a larger text and may have been cut of in the middle of a sentence).  # noqa: E501
Output nothing else than the summary.
Constraints: {constraints}
Other instructions: {extra_instructions}

TEXT TO SUMMARIZE:
{{text}}
"""
SUMMARIZE_PROMPT_TEMPLATE_VARIABLE_NAME = "text"


SUMMARIZE_SUMMARIES_PROMPT_TEMPLATE_TEMPLATE = """You are an assistant summarizing texts.
Given the summaries of different parts of a larger text below, write an overall summary of the whole text.  # noqa: E501
Summaries from some parts of the larger text might be missing, but still write the summary of the whole text as good as you can.  # noqa: E501
Output nothing else than the summary.
Constraints: {constraints}
Other instructions: {extra_instructions}

SUMMARIES TO SUMMARIZE:
{{summaries}}
"""
SUMMARIZE_SUMMARIES_TEMPLATE_VARIABLE_NAME = "summaries"


FINAL_SUMMARY_PROMPT = """You are an assistant answering to questions and solving tasks.
Given the summaries of a longer text below, solve the task below.

SUMMARIES:
{summaries}

TASK:
{task}
"""  # noqa: E501


DEFAULT_SUMMARY_CONSTRAINTS = (
    "The summary should be one paragraph and at most five sentences."
)
DEFAULT_EXTRA_INSTRUCTIONS = "-"
DEFAULT_SUMMARIZE_PROMPTS_TEMPLATE_TEMPLATE_VARIABLES = {
    "constraints": DEFAULT_SUMMARY_CONSTRAINTS,
    "extra_instructions": DEFAULT_EXTRA_INSTRUCTIONS,
}


SUMMARY_ITEM_PREFIX = "Summary:\n"
SUMMARY_ITEM = f"{SUMMARY_ITEM_PREFIX}{{summary}}"


TASK2EXTRA_INSTRUCTIONS = "Write the summary bearing in mind that this question/task is to be answered/solved from the summary: '{task}'"  # noqa: E501
