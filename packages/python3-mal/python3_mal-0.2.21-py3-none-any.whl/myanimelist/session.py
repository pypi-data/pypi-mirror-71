#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests

from . import anime
from . import manga

from . import character
from . import person

from . import user

from . import club
from . import genre
from . import tag
from . import publication
from . import producer

from . import anime_list
from . import manga_list

from .base import Error

from lxml import html as ht
import time


class UnauthorizedError(Error):
    """
      Indicates that the current session is unauthorized to make the given request.
    """

    def __init__(self, session, url, result):
        """Creates a new instance of UnauthorizedError.

        :type session: :class:`.Session`
        :param session: A valid MAL session.

        :type url: str
        :param url: The requested URL.

        :type result: str
        :param result: The result of the request.

        :rtype: :class:`.UnauthorizedError`
        :return: The desired error.

        """
        super(UnauthorizedError, self).__init__()
        self.session = session
        self.url = url
        self.result = result

    def __str__(self):
        return "\n".join([
            super(UnauthorizedError, self).__str__(),
            "URL: " + self.url,
            "Result: " + self.result
        ])


class Session(object):
    """Class to handle requests to MAL. Handles login, setting HTTP headers, etc.
    """

    def __init__(self, username=None, password=None,
                 user_agent="Mozilla/5.0 (X11; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0",
                 proxy_settings=None):
        """Creates a new instance of Session.

        :type username: str
        :param username: A MAL username. May be omitted.

        :type password: str
        :param username: A MAL password. May be omitted.

        :type user_agent: str
        :param user_agent: A user-agent to send to MAL in requests. If you have a user-agent assigned to you by Incapsula, pass it in here.

        :rtype: :class:`.Session`
        :return: The desired session.

        """
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': user_agent,
            'DNT': "1",
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.7,ja;q=0.3',
            'Connection': 'keep-alive',
        })
        if proxy_settings is not None and type(proxy_settings) is dict:
            self.session.proxies.update(proxy_settings)

        """Suppresses any Malformed*PageError exceptions raised during parsing.

        Attributes which raise these exceptions will be set to None.
        """
        self.suppress_parse_exceptions = False

    def logged_in(self):
        """Checks the logged-in status of the current session.
        Expensive (requests a page), so use sparingly! Best practice is to try a request and catch an UnauthorizedError.

        :rtype: bool
        :return: Whether or not the current session is logged-in.

        """
        if self.session is None:
            return False

        panel_url = 'https://myanimelist.net'
        panel = self.session.get(panel_url)
        html = ht.fromstring(panel.content.decode("utf-8"))

        if 'Logout' in panel.content.decode("utf-8") or len(html.xpath(".//*[text()[contains(.,'Logout')]]")) > 0:
            return True

        if len(html.xpath("//form[@action='https://myanimelist.net/logout.php']")) > 0:
            return True

        return False

    def login(self):
        """Logs into MAL and sets cookies appropriately.

        :rtype: :class:`.Session`
        :return: The current session.

        """
        mal_headers = {
            'Host': 'myanimelist.net',
            'DNT': '1',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.7,ja;q=0.3',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'iMAL-iOS',
        }

        panel_url = 'https://myanimelist.net'
        # set the session cookies:
        r = self.session.get(panel_url)

        if len(r.history) > 0:
            cookies = r.history[0].cookies
            html = ht.fromstring(r.content.decode("utf-8"))
            token_tag = html.xpath(".//meta[@name='csrf_token']")
        else:
            cookies = r.cookies
            html = ht.fromstring(r.content.decode("utf-8"))
            token_tag = html.xpath(".//meta[@name='csrf_token']")

        if len(token_tag) == 0:
            return self

        token_tag = token_tag[0]
        token = token_tag.get("content")

        # POSTS a login to mal_crawler.
        mal_payload = {
            'user_name': self.username,
            'password': self.password,
            'cookie': '1',
            'sublogin': 'Login',
            'submit': '1',
            'csrf_token': token
        }
        self.session.headers.update(mal_headers)
        if "MALHLOGSESSID" in cookies.keys():
            self.session.cookies = cookies
        r = self.session.post('https://myanimelist.net/login.php?from=/', data=mal_payload)

        x = ht.fromstring(r.content.decode('utf-8'))
        if len(x.xpath("//div[@class='badresult']")) > 0:
            print('Captcha is required to login. Please login first on the website and try again.')

        # remove content type:
        self.session.headers.pop("Content-Type")
        return self

    def anime(self, anime_id):
        """Creates an instance of myanimelist.Anime with the given ID.

        :type anime_id: int
        :param anime_id: The desired anime's ID.

        :rtype: :class:`myanimelist.anime.Anime`
        :return: A new Anime instance with the given ID.

        """
        return anime.Anime(self, anime_id)

    def anime_list(self, username):
        """Creates an instance of myanimelist.AnimeList belonging to the given username.

        :type username: str
        :param username: The username to whom the desired anime list belongs.

        :rtype: :class:`myanimelist.anime_list.AnimeList`
        :return: A new AnimeList instance belonging to the given username.

        """
        return anime_list.AnimeList(self, username)

    def character(self, character_id):
        """Creates an instance of myanimelist.Character with the given ID.

        :type character_id: int
        :param character_id: The desired character's ID.

        :rtype: :class:`myanimelist.character.Character`
        :return: A new Character instance with the given ID.

        """
        return character.Character(self, character_id)

    def club(self, club_id):
        """Creates an instance of myanimelist.Club with the given ID.

        :type club_id: int
        :param club_id: The desired club's ID.

        :rtype: :class:`myanimelist.club.Club`
        :return: A new Club instance with the given ID.

        """
        return club.Club(self, club_id)

    def genre(self, genre_id):
        """Creates an instance of myanimelist.Genre with the given ID.

        :type genre_id: int
        :param genre_id: The desired genre's ID.

        :rtype: :class:`myanimelist.genre.Genre`
        :return: A new Genre instance with the given ID.

        """
        return genre.Genre(self, genre_id)

    def manga(self, manga_id):
        """Creates an instance of myanimelist.Manga with the given ID.

        :type manga_id: int
        :param manga_id: The desired manga's ID.

        :rtype: :class:`myanimelist.manga.Manga`
        :return: A new Manga instance with the given ID.

        """
        return manga.Manga(self, manga_id)

    def manga_list(self, username):
        """Creates an instance of myanimelist.MangaList belonging to the given username.

        :type username: str
        :param username: The username to whom the desired manga list belongs.

        :rtype: :class:`myanimelist.manga_list.MangaList`
        :return: A new MangaList instance belonging to the given username.

        """
        return manga_list.MangaList(self, username)

    def person(self, person_id):
        """Creates an instance of myanimelist.Person with the given ID.

        :type person_id: int
        :param person_id: The desired person's ID.

        :rtype: :class:`myanimelist.person.Person`
        :return: A new Person instance with the given ID.

        """
        return person.Person(self, person_id)

    def producer(self, producer_id):
        """Creates an instance of myanimelist.Producer with the given ID.

        :type producer_id: int
        :param producer_id: The desired producer's ID.

        :rtype: :class:`myanimelist.producer.Producer`
        :return: A new Producer instance with the given ID.

        """
        return producer.Producer(self, producer_id)

    def publication(self, publication_id):
        """Creates an instance of myanimelist.Publication with the given ID.

        :type publication_id: int
        :param publication_id: The desired publication's ID.

        :rtype: :class:`myanimelist.publication.Publication`
        :return: A new Publication instance with the given ID.

        """
        return publication.Publication(self, publication_id)

    def tag(self, tag_id):
        """Creates an instance of myanimelist.Tag with the given ID.

        :type tag_id: int
        :param tag_id: The desired tag's ID.

        :rtype: :class:`myanimelist.tag.Tag`
        :return: A new Tag instance with the given ID.

        """
        return tag.Tag(self, tag_id)

    def user(self, username):
        """Creates an instance of myanimelist.User with the given username

        :type username: str
        :param username: The desired user's username.

        :rtype: :class:`myanimelist.user.User`
        :return: A new User instance with the given username.

        """
        return user.User(self, username)

    def get(self, url, **kwargs):
        retries = 0
        response = self.session.get(url, **kwargs)
        while response.status_code == 429 and retries < 5:
            time.sleep(7)
            retries = retries + 1
            response = self.session.get(url, **kwargs)

        return response
