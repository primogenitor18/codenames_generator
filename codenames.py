from typing import List, Literal
import itertools
import random
import aiofiles
from dataclasses import dataclass
import traceback

from transliterate import translit
from transliterate.exceptions import LanguagePackNotFound

from vocabulary import vocabulary


@dataclass
class Words:
    adjs: List[str]
    adjs_weights: List[int]
    nouns: List[str]
    nouns_weights: List[int]


async def load_words(filename):
    async with aiofiles.open(filename) as f:
        words = [line.split() async for line in f]
    return (
        [word for word, count in words],
        list(itertools.accumulate(int(count) for word, count in words))
    )


async def gen_word(words: Words) -> str:
    while True:
        adj = random.choices(words.adjs, cum_weights=words.adjs_weights)[0]
        noun = random.choices(words.nouns, cum_weights=words.nouns_weights)[0]
        if len(adj) >= 3 and len(noun) >= 3:
            break
    return adj, noun


async def gen_name(
    words: Words,
    language: str,
    project: Literal["project", "operation"],
    number: int,
) -> str:
    adj, noun = await gen_word(words)
    _project_type = vocabulary.get(project, {}).get(language, "project")
    try:
        project_name = translit(f"{adj} {noun}", language)
    except LanguagePackNotFound:
        print(traceback.format_exc())
    return f"{_project_type} {project_name} {number}"
