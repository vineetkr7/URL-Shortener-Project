from flask import Flask, render_template, request, session, redirect, url_for, abort, jsonify, flash
import json
import os.path

app = Flask(__name__)
app.secret_key = 'ZSeraqfhjyipokplonmnbnvxz'

@app.route('/', endpoint='index')
def index():
	return render_template('index.html')

@app.route('/your-url', methods=['GET', 'POST'])
def your_url():
	if request.method == 'POST':
		urls = {}
		if os.path.exists('urls.json'): # checks if 'urls.json' exists
			with open('urls.json') as urls_file:
				try:
					urls = json.load(urls_file) # takes the file object 'urls_file' and returns the json object 'urls'
				except:
					pass
				
		if request.form['code'] in urls.keys():
			flash('Short name already exists! Please use another name.')
			return render_template('index.html')

		urls[request.form['code']] = {'url': request.form['url']}
		with open('urls.json', 'w') as url_file:
			json.dump(urls, url_file)
			# session[request.form['code']]=True

		return render_template('your_url.html', code=request.form['code'])
	else:
		return redirect(url_for('index'))

@app.route('/<string:code>')
def redirect_to_url(code):
	if os.path.exists('urls.json'): # checks if 'urls.json' exists
		with open('urls.json') as urls_file:
			try:
				urls = json.load(urls_file) # takes the file object 'urls_file' and returns the json object 'urls'
				if code in urls.keys():
					if 'url' in urls[code].keys():
						return redirect(urls[code]['url'])
			except:
				pass

	return abort(404)

@app.errorhandler(404)
def page_not_found(error):
	return render_template('page_not_found.html'), 404

@app.route('/api', endpoint='api')
def api():
	response = {}
	with open('urls.json') as urls_file:
		f_dict = json.load(urls_file)
		for k, v in f_dict.items():
			response[k] = f_dict[k]['url']

	return jsonify(response)
	# return jsonify(list(session.keys()))