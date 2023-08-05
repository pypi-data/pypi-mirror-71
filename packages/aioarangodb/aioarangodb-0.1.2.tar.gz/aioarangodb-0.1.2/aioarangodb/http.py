from __future__ import absolute_import, unicode_literals

__all__ = ['HTTPClient', 'DefaultHTTPClient']

from abc import ABCMeta, abstractmethod

import aiohttp

from .response import Response


class HTTPClient(object):  # pragma: no cover
    """Abstract base class for HTTP clients."""

    __metaclass__ = ABCMeta

    @abstractmethod
    def create_session(self, host):
        """Return a new requests session given the host URL.

        This method must be overridden by the user.

        :param host: ArangoDB host URL.
        :type host: str | unicode
        :returns: Requests session object.
        :rtype: requests.Session
        """
        raise NotImplementedError

    @abstractmethod
    async def send_request(
            self,
            session,
            method,
            url,
            headers=None,
            params=None,
            data=None,
            auth=None):
        """Send an HTTP request.

        This method must be overridden by the user.

        :param session: Requests session object.
        :type session: requests.Session
        :param method: HTTP method in lowercase (e.g. "post").
        :type method: str | unicode
        :param url: Request URL.
        :type url: str | unicode
        :param headers: Request headers.
        :type headers: dict
        :param params: URL (query) parameters.
        :type params: dict
        :param data: Request payload.
        :type data: str | unicode | bool | int | list | dict
        :param auth: Username and password.
        :type auth: tuple
        :returns: HTTP response.
        :rtype: arango.response.Response
        """
        raise NotImplementedError


class DefaultHTTPClient(HTTPClient):
    """Default HTTP client implementation."""

    def create_session(self, host):
        """Create and return a new session/connection.

        :param host: ArangoDB host URL.
        :type host: str | unicode
        :returns: requests session object
        :rtype: requests.Session
        """
        return aiohttp.ClientSession()

    async def send_request(
            self,
            session,
            method,
            url,
            params=None,
            data=None,
            headers=None,
            auth=None):
        """Send an HTTP request.

        :param session: Requests session object.
        :type session: requests.Session
        :param method: HTTP method in lowercase (e.g. "post").
        :type method: str | unicode
        :param url: Request URL.
        :type url: str | unicode
        :param headers: Request headers.
        :type headers: dict
        :param params: URL (query) parameters.
        :type params: dict
        :param data: Request payload.
        :type data: str | unicode | bool | int | list | dict
        :param auth: Username and password.
        :type auth: tuple
        :returns: HTTP response.
        :rtype: arango.response.Response
        """
        request = getattr(session, method)
        if auth is not None:
            auth = aiohttp.BasicAuth(auth[0], auth[1])
        response = await request(
            url=url,
            params=params,
            data=data,
            headers=headers,
            auth=auth
        )
        return Response(
            method=method,
            url=url,
            headers=response.headers,
            status_code=response.status,
            status_text=response.reason,
            raw_body=await response.text(),
        )
