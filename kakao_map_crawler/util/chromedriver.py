import re
import sys

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager

from kakao_map_crawler.util.exceptions import WebDriverException
from kakao_map_crawler.util.logger import KakaoMapCrawlingLogger
from kakao_map_crawler.util.settings import Settings


class SetupBrowserEnvironment:
    def __init__(self, chrome_options=None, capabilities=None):
        if chrome_options is None:
            chrome_options = Options()
            prefs = {'profile.managed_default_content_settings.images': 2, 'disk-cache-size': 4096,
                     'intl.accept_languages': 'en-US'}
            chrome_options.add_argument('--dns-prefetch-disable')
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--lang=en-US')
            chrome_options.add_argument('--headless')
            chrome_options.add_experimental_option('prefs', prefs)

        if capabilities is None:
            capabilities = DesiredCapabilities.CHROME

        self.chrome_options = chrome_options
        self.capabilities = capabilities

    def __enter__(self):
        self.browser = init_chromedriver(self.chrome_options, self.capabilities)
        return self.browser

    def __exit__(self, exc_type, exc_value, traceback):
        self.browser.delete_all_cookies()
        self.browser.quit()


def init_chromedriver(chrome_options, capabilities):
    chromedriver_location = Settings.chromedriver_location

    try:
        # browser = webdriver.Chrome(chromedriver_location,
        #                                         desired_capabilities=capabilities,
        #                                         chrome_options=chrome_options)
        browser = webdriver.Chrome(ChromeDriverManager().install())
    except WebDriverException as exc:
        KakaoMapCrawlingLogger.logger().error('ensure chromedriver is installed at {}'.format(
            Settings.chromedriver_location))
        raise exc

    matches = re.match(r'^(\d+\.\d+)',
                       browser.capabilities['chrome']['chromedriverVersion'])
    if float(matches.groups()[0]) < Settings.chromedriver_min_version:
        KakaoMapCrawlingLogger.logger().error('chromedriver {} is not supported, expects {}+'.format(
            float(matches.groups()[0]), Settings.chromedriver_min_version))
        browser.close()
        raise Exception('wrong chromedriver version')

    return browser
