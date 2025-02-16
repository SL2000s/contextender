from typing import Generator


def find_context_len(llm: callable) -> int:
    # TODO: don't hardcode - try prompts of different lengths until failure
    context_len = 20000  # NOTE: 20000 chars corresponds to ~5000 tokens
    return context_len


def _text_splitter(text: str, max_chars: int):
    start_now = 0
    while start_now < len(text):
        end_now = min(start_now + max_chars, len(text))
        yield text[start_now:end_now]
        start_now = end_now


def _yield_split_sb(sb: str, join_str: str):
    s = join_str.join(sb)
    for text_part in _text_splitter(s):
        yield text_part


# TODO: change default separator to space ' '?
def text_splitter(
    text: str, max_chars: int, separator: str = None
) -> Generator[str, None, None]:
    if isinstance(separator, str) and len(separator) > 0:
        sb = []
        sb_acc_len = 0
        for text_part in text.split(separator):
            if sb_acc_len + len(separator) + len(text_part) < max_chars:
                sb.append(text_part)
            else:
                if len(sb) == 0:
                    pass
                else:
                    # NOTE: should be 1 it. if the separator is well chosen
                    for s_part in _yield_split_sb(sb, separator):
                        yield s_part
                    sb = [separator + text_part]
                    sb_acc_len = len(sb[0])
        # NOTE: should be 1 it. if the separator is well chosen
        for s_part in _yield_split_sb(sb, separator):
            yield s_part
    else:
        for text_part in _text_splitter(text, max_chars):
            yield text_part
