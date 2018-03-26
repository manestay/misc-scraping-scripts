from robobrowser import RoboBrowser as rb

url = 'http://ronald.cori.missouri.edu/cori_search/client_search.php'
browser = rb(parser='lxml', user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36')
browser.open(url)
login_form = browser.get_form()
login_form.fields['User_EMail'].value = 'cori@mailinator.com'
browser.submit_form(login_form)
browser.open(url)


categories = [x['value'] for x in browser.find_all('input')
              if 'category[]' in x['name']]

search_form = browser.get_form()
search_form['Display_Rows'].value = '100'
search_form['category[]']=categories
d = search_form.serialize().data

browser.submit_form(search_form)
