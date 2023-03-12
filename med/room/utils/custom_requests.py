import requests
import json
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from requests.auth import HTTPBasicAuth
from .logger import logger


class RequestObjects:
    """
    Intercepts small errors in the HTTP call and tries to resolve using functions such as:
        - HTTP Adapter
        - HTTP Retry
        - HTTP BasicAuth
    References of the function implementation:
    - https://dev.to/ssbozy/python-requests-with-retries-4p03
    - https://urllib3.readthedocs.io/en/latest/reference/urllib3.util.html#module-urllib3.util.retry
    Usage:
        .. code-block:: python
        response = RequestObjects(url=url).post(
            body=body,
            timeout=timeout,
            headers=headers
        )
    """

    __slots__ = ['_url']

    def __init__(self, url):
        """
        Args:
            :param: url
            :type: str
            :return: uri and path of API informed
        Returns:
            :rtype: dict
            :raises: requests.exceptions.HTTPError, requests.exceptions.RequestException
        """
        self._url = url

    @property
    def url(self):
        return self._url

    @staticmethod
    def _requests_retry_session(
        retries=3,
        backoff_factor=0.3,
        status_forcelist=(500, 502, 504),
        session=None,
    ):
        """
        References of the function implementation:
        - https://dev.to/ssbozy/python-requests-with-retries-4p03
        - https://urllib3.readthedocs.io/en/latest/reference/urllib3.util.html#module-urllib3.util.retry
        """
        session = session or requests.Session()
        retry = Retry(
            total=retries,
            read=retries,
            connect=retries,
            backoff_factor=backoff_factor,
            status_forcelist=status_forcelist,
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session

    def api_response(self, response):
        logger.info(f'Request data on url: {self.url}')
        try:
            if response.status_code >= 500:
                logger.critical(f'[X] - Server Error {response.status_code}: {response.content}')
            elif response.status_code == 400:
                logger.critical(f'[X] - Bad Request: {response.status_code}')
            elif response.status_code == 403:
                logger.warning(f'[!] - Forbidden: {response.status_code}')
            elif response.status_code == 401:
                logger.warning(f'[!] - Unauthorized: {response.status_code}')
            elif response.status_code >= 200 and response.status_code < 299:
                logger.info(f'[V] - Request Success: {response.status_code}')
                return response.json()
        except requests.exceptions.HTTPError:
            logger.exception('[X] - Unexpected Error: ')
            raise requests.exceptions.HTTPError('parse of obj response HTTP')

        return None

    def post(self, body, timeout=15, retries=3, user='', _pass='', headers={}):
        """
        Args:
            :param: body
            :type: dict
            :return: data to sent as request
            :param: timeout
            :type: int
            :default: 15
            :return: time in seconds defined to guest connection HTTP
            :param: retries
            :type: int
            :default: 3
            :return: Max retries HTTP
            :param: user
            :type: str
            :default: empty
            :return: username to connect with API using HTTPBasicAuth
            :param: _pass
            :type: str
            :default: empty
            :return: password to connect with API using HTTPBasicAuth
            :param: headers
            :type: dict
            :default: empty
            :return: HTTP Headers used for exemple to define Authenticate or Content-Type
        """
        logger.info(f'Body: {body}')
        default_header = {
            'content-type': 'application/json',
            'cache-control': 'no-cache',
        }
        # add only new keys and values in the dict
        default_header.update(headers)
        if user and _pass:
            response = self._requests_retry_session(retries=retries).post(
                url=self.url, json=body, timeout=timeout, auth=HTTPBasicAuth(user, _pass)
            )
        else:
            response = self._requests_retry_session(retries=retries).post(
                url=self.url, json=body, timeout=timeout, headers=headers
            )

        return self.api_response(response)
