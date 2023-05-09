import re
import contextlib
from collections import namedtuple
from unicodedata import numeric


Rule = namedtuple('Rule', ['getter', 'extractor'])
Info = namedtuple('Info', ['title', 'season', 'episode'])

_bangumi_title_patterns = [
    Rule(
        lambda x: re.fullmatch('鬼灭之刃 刀匠村篇', x),
        lambda m, i: i._replace(title='鬼灭之刃', season=4)
    ),
    Rule(
        lambda x: re.fullmatch(r'\s*(.+)\s+第(.)季\s*', x),
        lambda m, i: i._replace(title=m[1], season=chinese2num(m[2]))
    ),
    Rule(
        lambda x: re.fullmatch(r'\s*(\S+)\s*(\S+)篇\s*', x),
        lambda m, i: i._replace(title=m[1])
    ),
    Rule(
        lambda x: re.fullmatch(r'【?\s*(.+?)\s*】?', x),
        lambda m, i: i._replace(title=m[1])
    ),
]

_season_patterns = [
    Rule(
        lambda x: re.fullmatch(r'S(\d+)', x),
        lambda m, i: i._replace(season=m[1])
    ),
]

_episode_title_patterns = [
    Rule(
        lambda x: re.fullmatch(r'(\d+)\-(\d+)', x),
        lambda m, i: i._replace(episode=[m[1], m[2]])
    ),
    Rule(
        lambda x: re.fullmatch(r'0?\d{1,2}', x),
        lambda m, i: i._replace(episode=m[0])
    ),
    Rule(
        lambda x: re.fullmatch(r'(0?\d{1,2})(V\d+)?', x),
        lambda m, i: i._replace(episode=m[1])
    ),
    Rule(
        lambda x: re.fullmatch(r'第?(\d+)[集话]', x),
        lambda m, i: i._replace(episode=m[1])
    ),
    Rule(
        lambda x: re.fullmatch(r'OP(\d{2})', x),
        lambda m, i: i._replace(episode=m[1])
    ),
    Rule(
        lambda x: re.fullmatch(r'(\d{2})[\u4e00-\u9fa5]+', x),
        lambda m, i: i._replace(episode=m[1])
    ),
    Rule(
        lambda x: re.fullmatch(r'\d{2,4}', x),
        lambda m, i: i._replace(episode=m[0])
    ),
]


@contextlib.contextmanager
def match(pattern, string):
    yield re.match(pattern, string)


@contextlib.contextmanager
def fullmatch(pattern, string):
    yield re.fullmatch(pattern, string)


def chinese2num(s):
    amount = 0
    digit = 0
    if s[0] == "十": s = "一" + s
    for ch in s:
        number = numeric(ch)
        if number < 10:
            digit = number
        else:
            amount = (amount + digit) * number if number > amount else amount + digit * number
            digit = 0
    return int(amount + digit)


def _get_tokens(text):
    return re.split(r'\[|\]|【|】|（|）|\(|\)|\s+|\.', text)


def _format_info(info):
    season = info.season
    if type(season) is int:
        season_on_episode = 'S' + str(season).rjust(2, '0')
        season = f'Season {season}'
    elif type(season) is str:
        num = int(season)
        season = 'Season ' + str(num)
        season_on_episode = 'S' + str(num).rjust(2, '0')
    else:
        season = 'Season 1'
        season_on_episode = 'S01'

    episode = info.episode
    if type(episode) is int:
        episode = season_on_episode + 'E' + str(episode).rjust(2, '0')
    elif type(episode) is str:
        episode = season_on_episode + 'E' + str(int(episode)).rjust(2, '0')
    elif type(episode) is list:
        episode = season_on_episode + 'E' + episode[0].rjust(2, '0') + '-E' + episode[1].rjust(2, '0')
    else:
        episode = season_on_episode + 'E01'
    return info._replace(
        season=season,
        episode=episode
    )


def extract(bangumi_title, episode_title) -> Info:
    info = Info(None, None, None)
    for rule in _bangumi_title_patterns:
        matched = rule.getter(bangumi_title)
        if matched:
            info = rule.extractor(matched, info)
            break
    tokens = _get_tokens(episode_title)
    for token in tokens:
        if info.episode is None:
            for rule in _episode_title_patterns:
                matched = rule.getter(token)
                if matched:
                    info = rule.extractor(matched, info)
                    break
        if info.season is None:
            for rule in _season_patterns:
                matched = rule.getter(token)
                if matched:
                    info = rule.extractor(matched, info)
                    break
    return _format_info(info)
