from robobrowser import RoboBrowser as rb
from requests import get
import os.path
from time import sleep

SITE = 'https://www.dol.gov'
url = 'https://www.dol.gov/olms/regs/compliance/cba/index.htm'
browser = rb(parser='html.parser')
count = 0

if not os.path.exists('DOL'):
    os.makedirs('DOL')

def get_links():
  browser.open(url)
  links = [x for x in browser.find_all('a', href=True) if 'Cba' in x['href']]
  return links


def download_pdfs():
  global count
  print('downloading '),
  for tag in browser.find_all('a', href=True):
      a=  tag['href']
      filename = 'DOL/'+ os.path.basename(a)
      if os.path.isfile(filename):
          continue
      if filename.endswith('.pdf'):
          print(filename, end=' ', flush=True)
          f = open(filename, "wb")
          response = get(SITE + a)
          # write to file
          f.write(response.content)
          f.close()

def main():
  links = get_links()
  for link in links:
    browser.follow_link(link)
    download_pdfs()
    browser.back()
    sleep(3)

if __name__ == '__main__':
    main()
