
import requests
import time
from selenium import webdriver
import undetected_chromedriver as uc
from selenium.common.exceptions import TimeoutException

from utils.logger import create_logger
from utils.header_proxy_pool import header_proxy_pool

class sel:
  logger = create_logger("selenium_logs")
  last_request = time.time()

  hpp = header_proxy_pool(logger)

  chrome_options = webdriver.ChromeOptions()
  #chrome_options.add_argument('--proxy-server=%s' % hpp.get_currentproxy())
  driver = uc.Chrome(executable_path='webdriver/chromedriver.exe', chrome_options=chrome_options)

  #driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": hpp.get_currentheader()['User-Agent']})

  @staticmethod
  def update_driver():
      pass
      #sel.driver.close()

      #sel.hpp.next_proxyheader()
      #sel.driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": sel.hpp.get_currentheader()['User-Agent']})

  @staticmethod
  def get(html:str, delay=0.5, limit=50, tries=0):
    try:
      curtime = time.time()
      dt = curtime - sel.last_request


      if dt < delay:
        time.sleep(delay-dt)


      sel.driver.set_page_load_timeout(10)
      sel.driver.get(html)

      sel.last_request = time.time()
      return sel.driver

    except TimeoutException as ex:
      sel.logger.debug("Timeout Exception:" + html + ", Error:" + str(ex))

      sel.update_driver()

      if tries < limit:
          sel.logger.debug("Attempt:" + str(tries + 1))
          return sel.get(html, delay, limit, tries + 1)
      else:
          sel.logger.debug("Something very wrong, aborting request")
          return False
        

  def __del__(self):
    pass
