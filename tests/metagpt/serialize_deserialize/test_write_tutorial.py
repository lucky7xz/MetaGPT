# -*- coding: utf-8 -*-
# @Desc    :
from typing import Dict

import pytest

from metagpt.actions.write_tutorial import WriteContent, WriteDirectory


@pytest.mark.asyncio
@pytest.mark.parametrize(("language", "topic"), [("English", "Write a tutorial about Python")])
@pytest.mark.usefixtures("llm_mock")
async def test_write_directory_deserialize(language: str, topic: str):
    action = WriteDirectory()
    serialized_data = action.model_dump()
    assert serialized_data["name"] == "WriteDirectory"
    assert serialized_data["language"] == "Chinese"

    new_action = WriteDirectory(**serialized_data)
    ret = await new_action.run(topic=topic)
    assert isinstance(ret, dict)
    assert "title" in ret
    assert "directory" in ret
    assert isinstance(ret["directory"], list)
    assert len(ret["directory"])
    assert isinstance(ret["directory"][0], dict)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("language", "topic", "directory"),
    [("English", "Write a tutorial about Python", {"Introduction": ["What is Python?", "Why learn Python?"]})],
)
@pytest.mark.usefixtures("llm_mock")
async def test_write_content_deserialize(language: str, topic: str, directory: Dict):
    action = WriteContent(language=language, directory=directory)
    serialized_data = action.model_dump()
    assert serialized_data["name"] == "WriteContent"

    new_action = WriteContent(**serialized_data)
    ret = await new_action.run(topic=topic)
    assert isinstance(ret, str)
    assert list(directory.keys())[0] in ret
    for value in list(directory.values())[0]:
        assert value in ret
