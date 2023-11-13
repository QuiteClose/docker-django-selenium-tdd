import os
import unittest
import uuid

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

###############################################################################

SERVER_HOST = os.getenv('SERVER_HOST', 'localhost')
SERVER_PORT = os.getenv('SERVER_PORT', '8000')


def get_server_url():
    return 'http://{}:{}'.format(SERVER_HOST, SERVER_PORT)


###############################################################################


def _unique_str():
    '''
    Get a unique string.
    '''
    return uuid.uuid4().hex


def _unique_int():
    '''
    Get a unique integer.
    '''
    return uuid.uuid1().int >> 64


###############################################################################


class FunctionalTestCase(unittest.TestCase):
    WAIT_TIMEOUT = 1

    @staticmethod
    def _get_webdriver_session():
        '''
        Returns a webdriver.Chrome browser session.
        '''
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument("--window-size=1920,1080")
        return webdriver.Chrome(options=chrome_options)

    def setUp(self):
        self.server_url = get_server_url()
        self.browser = self._get_webdriver_session()

    def tearDown(self):
        self.browser.quit()

    def wait_until(self, condition, message='Timeout raised'):
        '''
        Uses selenium.WebDriverWait and fails the test on TimeOut
        '''
        try:
            WebDriverWait(self.browser, self.WAIT_TIMEOUT).until(condition)
        except TimeoutException:
            self.fail(message)

