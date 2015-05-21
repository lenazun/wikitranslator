import os
from flask import Flask, render_template, redirect, request, flash, session, url_for

import linker

app = Flask(__name__)


# langcodes = {'en': 'English',
# 		'es': 'Spanish',
# 		'de': 'German',
# 		'fr': 'French',
# 		'it': 'Italian',
# 		'ja': 'Japanese',
# 		'ar': 'Arabic',
# 		'ru': 'Russian',
# 		'pt': 'Portuguese',
# 		'zh': 'Chinese',															
# 		}

@app.route('/')
def hello():

	return render_template("base.html")


@app.route('/translate', methods=["GET", "POST"])
def translate():
	sourcelang = 'en'
	string = str(request.form.get("string"))
	items = linker.get_wiki_data(string, sourcelang)

	return render_template("index.html", items = items)




if __name__ == "__main__":
    app.run(debug = True)