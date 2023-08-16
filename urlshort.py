import os.path
import json
from flask import Flask, render_template, request, flash, \
    redirect, url_for, abort, jsonify
from common import urls_json_file, index_page, your_url_page, \
    not_found_404_page
from logger import logger


logger = logger.create_logger()
app = Flask(__name__)
app.secret_key = 'ZSeraqfhjyipokplonmnbnvxz'


@app.route('/', endpoint='index')
def index():
    return render_template(index_page)


@app.route('/your-url', methods=['GET', 'POST'])
def your_url():
    if request.method == 'POST':
        try:
            urls = {}
            if os.path.exists(urls_json_file):
                with open(urls_json_file) as urls_file:
                    urls = json.load(urls_file)

            if request.form['code'] in urls.keys():
                flash('Short name already exists! Please use another name.')
                return render_template(index_page)

            urls[request.form['code']] = {'url': request.form['url']}

            with open(urls_json_file, 'w') as url_file:
                json.dump(urls, url_file)
                # session[request.form['code']]=True

            return render_template(your_url_page, code=request.form['code'])
        except FileNotFoundError:
            logger.error(f"The file '{urls_json_file}' does not exist.")
        except json.JSONDecodeError:
            logger.error(f"Error decoding JSON content in '{urls_json_file}'.")
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
    else:
        return redirect(url_for('index'))


@app.route('/<string:code>')
def redirect_to_url(code):
    try:
        if os.path.exists(urls_json_file):
            with (open(urls_json_file) as urls_file):
                urls = json.load(urls_file)
                if code in urls.keys():
                    if 'url' in urls[code].keys():
                        return redirect(urls[code]['url'])
    except FileNotFoundError:
        logger.error(f"The file '{urls_json_file}' does not exist.")
    except json.JSONDecodeError:
        logger.error(f"Error decoding JSON content in '{urls_json_file}'.")
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")

    return abort(404)


@app.errorhandler(404)
def page_not_found(error):
    return render_template(not_found_404_page), 404


@app.route('/api', endpoint='api')
def api():
    logger.info("Checking shortened urls!")
    response = {}
    with open('urls.json') as urls_file:
        f_dict = json.load(urls_file)
        for k, v in f_dict.items():
            response[k] = f_dict[k]['url']

    return jsonify(response)
    # return jsonify(list(session.keys()))
