
import requests
import time

from utils.logger import create_logger
from utils.header_proxy_pool import header_proxy_pool

class rq:
  logger = create_logger("request_logs")
  requests = requests.Session()
  last_request = time.time()

  hpp = header_proxy_pool(logger)

  @staticmethod
  def get(html:str, proxies=True, delay=0.5, limit=50, tries=0):
    try:
      curtime = time.time()
      dt = curtime - rq.last_request


      if dt < delay:
        time.sleep(delay-dt)

      a = {}
      if proxies:
        a = {"http": rq.hpp.get_currentproxy(),
             "https": rq.hpp.get_currentproxy()}

      print(f"REQUEST: {html}")
      s = rq.requests.get(html, proxies=a,
           headers=rq.hpp.get_currentheader(), timeout=5)

      
      rq.last_request = time.time()
      return s
    except requests.exceptions.RequestException as err:
      rq.logger.debug("Connection Error to:" + html + ", Error:" + str(err))

      rq.hpp.next_proxyheader()

      if tries < limit:
          rq.logger.debug("Attempt:" + str(tries + 1))
          return rq.get(html, proxies, delay, limit, tries + 1)
      else:
          rq.logger.debug("Something very wrong, aborting request")
          return False
        

  def __del__(self):
      self.requests.close()
