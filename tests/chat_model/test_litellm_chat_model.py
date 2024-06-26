import pytest

from magentic.chat_model.litellm_chat_model import LitellmChatModel
from magentic.chat_model.message import UserMessage
from magentic.function_call import (
    AsyncParallelFunctionCall,
    FunctionCall,
    ParallelFunctionCall,
)


@pytest.mark.parametrize(
    ("prompt", "output_types", "expected_output_type"),
    [
        ("Say hello!", [str], str),
        ("Return True", [bool], bool),
        ("Return the numbers 1 to 5", [list[int]], list),
        ("List three fruits", [list[str]], list),
    ],
)
@pytest.mark.litellm_openai
def test_litellm_chat_model_complete_openai(prompt, output_types, expected_output_type):
    chat_model = LitellmChatModel("gpt-3.5-turbo")
    message = chat_model.complete(
        messages=[UserMessage(prompt)], output_types=output_types
    )
    assert isinstance(message.content, expected_output_type)


@pytest.mark.parametrize(
    ("prompt", "output_types", "expected_output_type"),
    [
        ("Say hello!", [str], str),
        ("Return True", [bool], bool),
        ("Return the numbers 1 to 5", [list[int]], list),
        pytest.param(
            "Use the tool to return a list of three fruits",
            [list[str]],
            list,
            marks=pytest.mark.skip(reason="Claude fails to format list of strings."),
        ),
    ],
)
@pytest.mark.litellm_anthropic
def test_litellm_chat_model_complete_anthropic(
    prompt, output_types, expected_output_type
):
    chat_model = LitellmChatModel("anthropic/claude-3-haiku-20240307")
    message = chat_model.complete(
        messages=[UserMessage(prompt)], output_types=output_types
    )
    assert isinstance(message.content, expected_output_type)


@pytest.mark.litellm_anthropic
def test_litellm_chat_model_complete_anthropic_function_call():
    def plus(a: int, b: int) -> int:
        """Sum two numbers."""
        return a + b

    chat_model = LitellmChatModel("anthropic/claude-3-haiku-20240307")
    message = chat_model.complete(
        messages=[UserMessage("Use the tool to sum 1 and 2")],
        functions=[plus],
        output_types=[FunctionCall[int]],  # type: ignore[misc]
    )
    assert isinstance(message.content, FunctionCall)


@pytest.mark.litellm_anthropic
def test_litellm_chat_model_complete_anthropic_parallel_function_call():
    def plus(a: int, b: int) -> int:
        return a + b

    def minus(a: int, b: int) -> int:
        return a - b

    chat_model = LitellmChatModel("anthropic/claude-3-haiku-20240307")
    message = chat_model.complete(
        messages=[
            UserMessage(
                "Use the plus tool to sum 1 and 2. Use the minus tool to subtract 1 from 2."
            )
        ],
        functions=[plus, minus],
        output_types=[ParallelFunctionCall[int]],
    )
    assert isinstance(message.content, ParallelFunctionCall)
    # Claude does not return multiple tool calls, so this returns a single function call


@pytest.mark.parametrize(
    ("prompt", "output_types", "expected_output_type"),
    [("Say hello!", [str], str)],
)
@pytest.mark.ollama
def test_litellm_chat_model_complete_ollama(prompt, output_types, expected_output_type):
    chat_model = LitellmChatModel("ollama/llama2", api_base="http://localhost:11434")
    message = chat_model.complete(
        messages=[UserMessage(prompt)], output_types=output_types
    )
    assert isinstance(message.content, expected_output_type)


@pytest.mark.skip(reason="LiteLLM does not parse ollama tool calls")
@pytest.mark.ollama
def test_litellm_chat_model_complete_ollama_function_call():
    def plus(a: int, b: int) -> int:
        """Sum two numbers."""
        return a + b

    chat_model = LitellmChatModel("ollama/llama2", api_base="http://localhost:11434")
    message = chat_model.complete(
        messages=[UserMessage("Sum 1 and 2")], functions=[plus]
    )
    assert isinstance(message.content, FunctionCall)


@pytest.mark.parametrize(
    ("prompt", "output_types", "expected_output_type"),
    [
        ("Say hello!", [str], str),
        ("Return True", [bool], bool),
        ("Return the numbers 1 to 5", [list[int]], list),
        ("List three fruits", [list[str]], list),
    ],
)
@pytest.mark.asyncio
@pytest.mark.litellm_openai
async def test_litellm_chat_model_acomplete_openai(
    prompt, output_types, expected_output_type
):
    chat_model = LitellmChatModel("gpt-3.5-turbo")
    message = await chat_model.acomplete(
        messages=[UserMessage(prompt)], output_types=output_types
    )
    assert isinstance(message.content, expected_output_type)


@pytest.mark.parametrize(
    ("prompt", "output_types", "expected_output_type"),
    [
        ("Say hello!", [str], str),
        ("Return True", [bool], bool),
        ("Return the numbers 1 to 5", [list[int]], list),
        pytest.param(
            "Use the tool to return a list of three fruits",
            [list[str]],
            list,
            marks=pytest.mark.skip(reason="Claude fails to format list of strings."),
        ),
    ],
)
@pytest.mark.asyncio
@pytest.mark.litellm_anthropic
async def test_litellm_chat_model_acomplete_anthropic(
    prompt, output_types, expected_output_type
):
    chat_model = LitellmChatModel("anthropic/claude-3-haiku-20240307")
    message = await chat_model.acomplete(
        messages=[UserMessage(prompt)], output_types=output_types
    )
    assert isinstance(message.content, expected_output_type)


@pytest.mark.asyncio
@pytest.mark.litellm_anthropic
async def test_litellm_chat_model_acomplete_anthropic_function_call():
    def plus(a: int, b: int) -> int:
        """Sum two numbers."""
        return a + b

    chat_model = LitellmChatModel("anthropic/claude-3-haiku-20240307")
    message = await chat_model.acomplete(
        messages=[UserMessage("Use the tool to sum 1 and 2")],
        functions=[plus],
        output_types=[FunctionCall[int]],  # type: ignore[misc]
    )
    assert isinstance(message.content, FunctionCall)


@pytest.mark.asyncio
@pytest.mark.litellm_anthropic
async def test_litellm_chat_model_acomplete_anthropic_async_parallel_function_call():
    def plus(a: int, b: int) -> int:
        return a + b

    def minus(a: int, b: int) -> int:
        return a - b

    chat_model = LitellmChatModel("anthropic/claude-3-haiku-20240307")
    message = await chat_model.acomplete(
        messages=[
            UserMessage(
                "Use the plus tool to sum 1 and 2. Use the minus tool to subtract 1 from 2."
            )
        ],
        functions=[plus, minus],
        output_types=[AsyncParallelFunctionCall[int]],
    )
    assert isinstance(message.content, AsyncParallelFunctionCall)
    # Claude does not return multiple tool calls, so this returns a single function call


@pytest.mark.parametrize(
    ("prompt", "output_types", "expected_output_type"),
    [("Say hello!", [str], str)],
)
@pytest.mark.asyncio
@pytest.mark.ollama
async def test_litellm_chat_model_acomplete_ollama(
    prompt, output_types, expected_output_type
):
    chat_model = LitellmChatModel("ollama/llama2", api_base="http://localhost:11434")
    message = await chat_model.acomplete(
        messages=[UserMessage(prompt)], output_types=output_types
    )
    assert isinstance(message.content, expected_output_type)
