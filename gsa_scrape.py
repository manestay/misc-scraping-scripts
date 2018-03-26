import os
from robobrowser import RoboBrowser as rb
from time import sleep
SITE = 'https://www.gsa.gov'
url = 'https://www.gsa.gov/portal/category/107259'

browser = rb(parser='lxml')
browser.open(url)
regions = [x for x in browser.get_links() if 'Lease Documents Region' in x.text]
print('downloading '),

if not os.path.exists('GSA'):
    os.makedirs('GSA')

for rl in regions:
  region = rl.text.strip()
  print(region)
  browser.open('https://www.gsa.gov{}'.format(rl['href']))
  links = browser.get_links(href=True)
  # print(browser.url)
  dl_links = [x for x in links if '.zip' in x['href']]
  print('Found {} files'.format(len(dl_links)))
  for dll in dl_links:
    browser.follow_link(dll)
    filename = os.path.basename(dll['href'])

    region_path = 'GSA/{}/'.format(region.replace(' ', '_'))
    if not os.path.exists(region_path):
        os.makedirs(region_path)

    filename = region_path + filename
    f = open(filename, "wb")
    f.write(browser.response.content)
    f.close()
    sleep(1)
  print()
