from typing import Generator


def find_context_len(llm: callable) -> int:
    # TODO: don't hardcode - try prompts of different lengths until failure
    context_len = 20000  # NOTE: 20000 chars corresponds to ~5000 tokens
    return context_len


def text_splitter(
    text: str, max_chars: str, split_keyword: str = None
) -> Generator[str, None, None]:
    pass  # TODO
