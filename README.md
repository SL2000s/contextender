# contextender

`contextender` is a Python package designed to handle tasks that exceed the context length of large language models (LLMs). By dividing prompts iteratively, it enables processing of large inputs while improving accuracy by splitting tasks into smaller, manageable parts.

## Installation

Install the package using pip:

```bash
pip install contextender
```

## Purpose

Large language models often have limitations on the maximum context length they can process. `contextender` overcomes this limitation by splitting large inputs into smaller chunks and processing them iteratively. This approach allows for handling tasks that exceed the LLM's context length and increases accuracy by focusing on smaller, more manageable subtasks.

## Methods

### 1. `summarize`
**Purpose**: Summarizes text that may exceed the LLM's context length.

- **Use Case**: When you need to summarize a large body of text that cannot fit into the LLM's context window.
- **Approach**: Splits the text into smaller chunks, summarizes each chunk, and combines the results iteratively.

### 2. `item_chooser`
**Purpose**: Chooses one or more items from a long list by splitting the list and iteratively choosing or eliminating items.

- **Use Case**: When you need to select items from a Python list that is too large to process in one go.
- **Approach**: Focuses on the number of items in each split rather than the context length.

### 3. `text_choose_item`
**Purpose**: Chooses an item from a list embedded in a text (e.g., when the list is not a Python list).

- **Use Case**: When you need to select an item from a textual list while ensuring the context length is not exceeded.
- **Approach**: Focuses on splitting the text to avoid exceeding the LLM's context length.

## Example Usage

### Summarize a Large Text
```python
from contextender import summarize

text = "..."  # Large text to summarize
summary = summarize(
    text=text,
    llm=my_llm_callable,  # Replace with your LLM callable that takes a prompt (str) and outputs the answer (str)
    llm_context_len=10000  # Approximate number of characters (note: not tokens!) your LLM can handle
)
print(summary)
```

### Choose Items from a Long List
```python
from contextender import choose_item

items = [101, 42, 123, ...]  # Long list of items (of any type that can be converted to a string)
chosen_item = item_chooser(
    context=items,
    llm=my_llm_callable,  # Replace with your LLM callable that takes a prompt (str) and outputs the answer (str)
    llm_context_len=10000,  # Approximate number of characters (note: not tokens!) your LLM can handle
    task="Choose the maximum integer"
)
print(chosen_item)
```

### Choose an Item from a Textual List
```python
from contextender import text_choose_item

text = "1. Option A\n2. Option B\n3. Option C\n..."  # Text containing a list
chosen_item = text_choose_item(
    context=text,
    llm=my_llm_callable,  # Replace with your LLM callable that takes a prompt (str) and outputs the answer (str)
    llm_context_len=10000,  # Approximate number of characters (note: not tokens!) your LLM can handle
    task="Choose the best option"
)
print(chosen_item)
```

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/SL2000s/contextender/blob/main/LICENSE) file for details.
