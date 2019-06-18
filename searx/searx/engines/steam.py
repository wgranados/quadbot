from searx.url_utils import quote, urljoin, urlencode
from lxml import html
from searx.engines.xpath import extract_text
from searx.utils import get_torrent_size, int_or_zero

"""
 Steam (Games)

 @website https://steamcommunity.com
 @provide-api yes ()

 @using-api no
 @results HTML (using search portal)
 @stable no (HTML can change)
 @parse url, title content

"""

#search-url
base_url = 'https://store.steampowered.com/'
search_string = 'search/suggest?{query}&f=games&cc=CA&l=english'

# do search-request
def request(query, params):
  # do search-request
  search_path = search_string.format(query=urlencode({'term': query}))
  params['url'] = base_url + search_path
  params['language'] = 'english'
  return params


# get response from search-request
def response(resp):
    results = []

    dom = html.fromstring(resp.text)
    for result in dom:
      try:
        href = result.attrib.get('href')
        title = result.xpath("./div[1]")[0].text
        content = result.xpath("./div[2]/img")[0].attrib.get('src')
      except:
        pass

      results.append({'url': href, 'title': title, 'content': content})

    return results