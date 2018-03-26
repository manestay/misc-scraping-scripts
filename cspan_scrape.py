from robobrowser import RoboBrowser as rb
import json
from urllib.request import urlretrieve

urls = [ #first is senate, then house
  'https://www.c-span.org/search/?sdate=&edate=&searchtype=Videos&sort=Most+Recent+Airing&text=0&sponsorid%5B%5D=2102&show100=',
  'https://www.c-span.org/search/?sdate=&edate=&searchtype=Videos&sort=Most+Recent+Airing&text=0&sponsorid%5B%5D=187&show100='
  ]
browser = rb(parser='lxml')

def ajax_link(progid):
  return 'https://www.c-span.org/assets/player/ajax-player.php?os=html&html5=program&id={}&html5=program&width=1024'.format(progid)

for url in urls:
  print('URL: {}'.format(url))
  page = 0
  while True:
    browser.open(url + '&ajax&page={}'.format(page))
    if not browser.parsed: break # no more pages to be loaded
    print('working on page {}'.format(page))
    links = browser.get_links()
    video_links = [link for link in links if link.get('class') and 'title' in link.get('class')]

    for link in video_links:
      browser.follow_link(link)
      title = browser.parsed.title.string.split('|')[0].strip()
      tag = browser.find('div',id='flagVideo')
      progid = tag['rel'].split('=')[1]
      alink = ajax_link(progid)
      browser.open(alink)
      data = browser.parsed.string
      parsed = json.loads(data)
      # file_link = parsed['video']['files'][0]['path']['#text']
      file_link = parsed['video']['files'][0]['qualities'][-1]['file']['#text'] # lower quality video
      
      video_name = '{}.{}.mp4'.format(title,progid)
      print(video_name)
      urlretrieve(file_link,video_name)
