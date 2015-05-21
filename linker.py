import urllib
import urllib2
import simplejson




def get_wiki_data(title, source_lang):
	""" Gets wiki language data from the wikipedia API """


	URL = 'http://' +  source_lang + '.wikipedia.org/w/api.php'
	LANGS = ['ja', 'ru', 'es', 'ar', 'zh', 'de', 'nl', 'pt']

	#creates a dictionary for the item 
	item_dict = {}


	def get_json(values):
			print "."
			data = urllib.urlencode(values)  
			req = urllib2.Request(URL, data)
			response = urllib2.urlopen(req)
			json_file = response.read()            
			json_file = simplejson.loads(json_file)

			return json_file


	equivalents = {}
	for target_lang in LANGS:

		langvalues = {'action' : 'query',
				'prop' : 'langlinks',
				'lllang': target_lang,
				'titles' : title.encode('utf8'),
				'redirects': '',
				'format' : 'json'}

		#get json lang file based on the values above
		lang_json = get_json(langvalues)

		#gets the wiki id from the json file
		wiki_id = str([key for key in lang_json['query']['pages'].keys()])
		wiki_id = wiki_id.strip("['']")

		#if the article doesn't exist in English, returns None
		if '-1' in lang_json['query']['pages']:
			return None

		else:
			#if the article has language links, extracts the equivalent titles
			if 'langlinks' in lang_json['query']['pages'][wiki_id]:

				lang_dict = lang_json['query']['pages'][wiki_id]['langlinks'][0]
				langcode = lang_dict['lang']
				equivalent = lang_dict['*']

			else:
				langcode = False
				equivalent = " "

			equivalents[langcode] = equivalent

		

	#getting the image for an entry
	imagevalues = {'action' : 'query',
          'prop' : 'pageimages',
          'titles' : title.encode('utf8'),
          'redirects': '',
          'format' : 'json', 
          'pithumbsize': '500'}

	#if the image json contains an image, it sets it as thumbnail
	image_json = get_json(imagevalues)
	if 'thumbnail' in image_json['query']['pages'][wiki_id]:
		thumbnail = image_json['query']['pages'][wiki_id]['thumbnail']['source']

	else:
		thumbnail = False	



	item_dict[wiki_id] = { 'title' : title,	
							'equivalents': equivalents,
							'thumbnail': thumbnail}

	
	return item_dict



def main():


	#print get_wiki_data("Barack Obama", "en")
	pass
	
if __name__ == "__main__":
    main()

