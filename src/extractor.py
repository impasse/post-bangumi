from retry import retry
from loguru import logger
from functools import lru_cache
import openai
import json
import re

_re = re.compile(r'```(?:json)?\s*(.+)\s*```', re.DOTALL | re.MULTILINE)


def _find_json(text: str):
    text = text.strip()
    if text.startswith('{') and text.endswith('}'):
        return text
    else:
        match = _re.findall(text)
        return match[0]


@lru_cache(100)
@retry(tries=5)
def extract_bangumi(text: str):
    completion = openai.ChatCompletion.create(
        model='gpt-4',
        messages=[
            {'role': 'system',
             'content': '我需要你模仿一个番信息提取器，当我输入一个番名时，你需要使用 json 格式返回我 title、 season 和 season_number，如果没有 season 则返回空字符串，如果没有 season_number 则返回 0， 除了 json 不要返回任何其他信息'},
            {'role': 'user', 'content': text}
        ]
    )
    logger.info('extract_bangumi({}) = {}', text, completion.choices[0].message.content)
    json_result = _find_json(completion.choices[0].message.content)
    return json.loads(json_result)


@lru_cache(100)
@retry(tries=5)
def extract_episode(text: str):
    completion = openai.ChatCompletion.create(
        model='gpt-4',
        messages=[
            {'role': 'system',
             'content': '我需要你模仿一个番信息提取器，当我输入一个番名时，你需要使用 json 格式返回我 title, season, episode_number, resolution, format, language (如果没有 season 则返回 0, season 和 episode_number 为数字, 除了 json 不要返回任何其他信息)'},
            {'role': 'user', 'content': text}
        ]
    )
    logger.info('extract_episode({}) = {}', text, completion.choices[0].message.content)
    json_result = _find_json(completion.choices[0].message.content)
    return json.loads(json_result)
