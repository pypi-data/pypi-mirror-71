import asyncio
from dataclasses import dataclass
import aiohttp
from typing import List, Union
import io
import difflib
from aiomangadex.chapter import Chapter, ChapterList

@dataclass(frozen=True)
class Manga:
    """Represents part of result of https://mangadex.org/api/manga/{id}

.. note::
    Some of the chapter data is *not* included in the initial fetch, meaning you'll have to fetch the missing things in the :class:`aiomangadex.Chapter`.
    """
    id: int
    cover_url: str
    description: str
    rating: dict
    alt_names: list
    title : str
    artist: str
    author: str
    status: int
    genres: list
    last_chapter: int
    lang_name: str
    lang_flag: str
    hentai: bool
    links: dict
    chapters: ChapterList
    session: aiohttp.ClientSession = None
    _user_session: bool = False

    async def close_session(self):
        await self.session.close()

    def __del__(self):
        if not self._user_session:
            asyncio.create_task(self.session.close())

async def fetch_manga(manga_id: int, session: aiohttp.ClientSession = None) -> Manga:
    """Function used for fetching a manga by id. If no session is provided, the library will create one per manga fetched.
    It is recommended to reuse the aiohttp ClientSession instances.

    :param manga_id: Manga to fetch
    :type manga_id: int
    :param session: defaults to None
    :type session: aiohttp.ClientSession, optional
    :return:  A Manga instance with some chapter data.
    :rtype: Manga
    """
    if session is not None:
        user_session = True
        async with session.get(f'https://mangadex.org/api/manga/{manga_id}') as resp:
            response = await resp.json()
    else:
        user_session = False
        session = aiohttp.ClientSession(json_serialize=ujson.dumps)
        async with session.get(f'https://mangadex.org/api/manga/{manga_id}') as resp:
            response = await resp.json()
    chapters = []
    for key, value in response.get('chapter').items():
        chapters.append(Chapter(id=key, **dict(value), session=session, _user_session=True))
    chapters.reverse()
    return Manga(**dict(response.get('manga')), chapters=ChapterList(chapters), id=manga_id, session=session, _user_session=user_session)

async def fetch_chapter(chapter_id: int, session: aiohttp.ClientSession = None) -> Chapter:
    if session is not None:
        async with session.get(f'https://mangadex.org/api/chapter/{chapter_id}') as resp:
            response = await resp.json()
        return Chapter(**response, _user_session=True, session=session)
    session = aiohttp.ClientSession(json_serialize=ujson.dumps)
    async with session.get(f'https://mangadex.org/api/chapter/{chapter_id}') as resp:
        response = await resp.json()
    return Chapter(**response, _user_session=False, session=session)