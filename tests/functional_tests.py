
from selenium.common.exceptions import WebDriverException
import unittest

import helpers

###############################################################################


class HomePageTest(helpers.FunctionalTestCase):
    def test_page_title(self):
        """Test that the page title is correct."""
        try:
            self.browser.get(self.server_url)
        except WebDriverException as e:
            self.fail(e)
        else:
            self.assertIn('Replace with your expected title.', self.browser.title)


###############################################################################


if __name__ == '__main__':
    unittest.main(warnings='ignore')

