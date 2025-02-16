from functools import reduce
from typing import Generator, List


def find_context_len(llm: callable) -> int:
    # TODO: don't hardcode - try prompts of different lengths until failure
    context_len = 20000  # NOTE: 20000 chars corresponds to ~5000 tokens
    return context_len


def max_tv_values_len(
    template_str: str, template_variables: List[str], max_chars: int
) -> int:
    return (
        max_chars - len(template_str) + sum(len(x) for x in template_variables)
    )  # noqa


def _text_splitter(text: str, max_chars: int):
    start_now = 0
    while start_now < len(text):
        end_now = min(start_now + max_chars, len(text))
        yield text[start_now:end_now]
        start_now = end_now


# TODO: change default separator to space ' '?
def text_splitter(
    text: str, max_chars: int, prefix_separator: str = None
) -> Generator[str, None, None]:
    if isinstance(prefix_separator, str) and len(prefix_separator) > 0:
        wo_sep_parts = text.split(prefix_separator)
        text_parts = [prefix_separator + part for part in wo_sep_parts[1:]]
        if not text.startswith(prefix_separator):
            text_parts = [wo_sep_parts[0]] + text_parts
        # TODO: raise warning if too long items
        text_parts = reduce(
            lambda x, y: x + list(_text_splitter(y, max_chars)), text_parts, []
        )  # Split too long iterms (shouln't be any if separator well chosen)
        sb = []
        sb_acc_len = 0
        for text_part in text_parts:
            if sb_acc_len + len(text_part) <= max_chars:
                sb.append(text_part)
                sb_acc_len += len(text_part)
            else:
                yield "".join(sb)
                sb = [text_part]
                sb_acc_len = len(text_part)
        yield "".join(sb)
    else:
        for text_part in _text_splitter(text, max_chars):
            yield text_part
