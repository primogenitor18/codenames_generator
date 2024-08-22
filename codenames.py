from typing import List
import itertools
import random
import aiofiles
from dataclasses import dataclass


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
    return f"{adj}_{noun}"
