from retry import retry
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


@retry(tries=5)
def extract(text: str):
    completion = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {'role': 'system',
             'content': '我需要你模仿一个番信息提取器，当我输入一个番文件名时，你需要使用 json 格式返回我 title, title_english, group, season, episode_number, resolution, format, language，如果没有 season 则返回 1, 除了 json 不要返回任何其他信息'},
            {'role': 'user', 'content': text}
        ]
    )
    json_result = _find_json(completion.choices[0].message.content)
    return json.loads(json_result)
