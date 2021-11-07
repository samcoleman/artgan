from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import random
import requests
import logging
from itertools import cycle

class header_proxy_pool:
  logger = None

  proxies_pool, headers_pool = None, None
  current_proxy, current_header = None, None

  def __init__(self, logger: logging.Logger or None) -> None:
      self.logger = logger
      self.update_proxyheaderpool()

  def header_list(self):
      # Create a dict of accept headers for each user-agent.
      accepts = {"Firefox": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                 "Safari, Chrome": "application/xml,application/xhtml+xml,text/html;q=0.9, text/plain;q=0.8,image/png,*/*;q=0.5"}

      # Get a random user-agent. We used Chrome and Firefox user agents.
      # Take a look at fake-useragent project's page to see all other options - https://pypi.org/project/fake-useragent/
      try:
          # Getting a user agent using the fake_useragent package
          ua = UserAgent()
          if random.random() > 0.5:
              random_user_agent = ua.chrome
          else:
              random_user_agent = ua.firefox

      # In case there's a problem with fake-useragent package, we still want the scraper to function
      # so there's a list of user-agents that we created and swap to another user agent.
      # Be aware of the fact that this list should be updated from time to time.
      # List of user agents can be found here - https://developers.whatismybrowser.com/.
      except:
          self.logger.debug("UserAgent unable to generate header, using defaults")

          user_agents = [
              "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
              "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"]  # Just for case user agents are not extracted from fake-useragent package
          random_user_agent = random.choice(user_agents)

      # Create the headers dict. It's important to match between the user-agent and the accept headers as seen in line 35
      finally:
          valid_accept = accepts['Firefox'] if random_user_agent.find('Firefox') > 0 else accepts['Safari, Chrome']
          headers = {"User-Agent": random_user_agent,
                     "Accept": valid_accept}
      return headers

  def proxy_list(self):
      url = 'https://www.sslproxies.org/'

      # Retrieve the site's page. The 'with'(Python closure) is used here in order to automatically close the session when done
      with requests.Session() as res:
          proxies_page = res.get(url)

      # Create a BeutifulSoup object and find the table element which consists of all proxies
      soup = BeautifulSoup(proxies_page.content, 'html.parser')
      proxies_table = soup.find("table", {"class":'table table-striped table-bordered'})


      # Go through all rows in the proxies table and store them in the right format (IP:port) in our proxies list
      proxies = []
      for row in proxies_table.tbody.find_all('tr'):
          if "elite proxy" in row.getText():
              # if "FR" in row.getText():
              proxies.append('http://{}:{}'.format(row.find_all('td')[0].string, row.find_all('td')[1].string))
          # elif "GB" in row.getText():
          #    proxies.append('{}:{}'.format(row.find_all('td')[0].string, row.find_all('td')[1].string))
          # elif "IE" in row.getText():
          #    proxies.append('{}:{}'.format(row.find_all('td')[0].string, row.find_all('td')[1].string))
          # elif "BE" in row.getText():
          #    proxies.append('{}:{}'.format(row.find_all('td')[0].string, row.find_all('td')[1].string))
      return proxies


  # Generate the pools
  def create_pools(self):
      proxies = self.proxy_list()  # ["51.255.103.170:3129"]
      headers = [self.header_list() for ind in
                 range(len(proxies))]  # list of headers, same length as the proxies list

      # This transforms the list into itertools.cycle object (an iterator) that we can run
      # through using the next() function in lines 16-17.
      proxies_pool = cycle(proxies)
      headers_pool = cycle(headers)

      return proxies_pool, headers_pool


  def next_proxyheader(self):
      self.current_proxy = next(self.proxypool)
      self.current_header = next(self.headerspool)

      if self.current_proxy == self.firstproxy:
          self.update_proxyheaderpool()
          return

      self.logger.debug("Now using proxy:" + str(self.current_proxy))


  def update_proxyheaderpool(self):
      self.proxypool, self.headerspool = self.create_pools()

      self.current_proxy = next(self.proxypool)
      self.current_header = next(self.headerspool)

      self.firstproxy = self.current_proxy

      self.logger.debug("Updating proxy & header pool")
      self.logger.debug("Creating proxies:" + self.current_proxy)

  def get_currentproxy(self):
      return self.current_proxy

  def get_currentheader(self):
      return self.current_header