import json

import flask
import requests
from flask import Blueprint, request, jsonify

from db.setup import DBConnection

api = Blueprint("all", __name__)


@api.route('/')
def hello_world():
    with open('countries_data.json', 'r') as f:
        data = json.load(f)
    total_count, total_d = None, None
    for d in data:
        if d['country'] == 'Total:':
            total_d = d
            total_count = int(d['total'].replace(',', ''))
            break

    print(total_count)
    count_data = []
    for d1 in data[:5]:
        total = int(d1['total'].replace(',', ''))
        percentage = int((total * 100 / total_count))
        if percentage == 0:
            percentage = round((total * 100 / total_count), 1)
        count_data.append({'total': d1['total'], 'percentage': percentage, 'country': d1['country']})

    return flask.render_template('index.html', count_data=count_data, total=total_d)


@api.route('/world-stats')
def world_stat():
    with open('countries_data.json', 'r') as f:
        data = json.load(f)

    total = None
    for d in data:
        if d['country'] == 'Total:':
            total = d
            break
    return flask.render_template('world-stats.html', data=data, total=total, open_world="open")


@api.route('/india-stats')
def india_stats():
    total = None
    response = requests.get('https://edata.ndtv.com/cricket/coronavirus/data.json')
    d = json.loads(response.text)
    dataset = []
    for e in d['countries']:
        if e['country'] == 'India':
            dataset = e['states']
    with open('countries_data.json', 'r') as f:
        data = json.load(f)
    for d in data:
        if d['country'] == 'India':
            total = d
            break
    return flask.render_template('india-stats.html', total=total, data=dataset, open_india="open")


@api.route('/india-live')
def india_live():
    from tasks.tasks import dummy_task
    dummy_task.apply_async()
    db_conn = DBConnection()
    india_news = db_conn.db_conn.fetch_india_news()
    return flask.render_template('india-live.html', india_news=india_news, open_india="open")


@api.route('/world-live')
def world_live():
    db_conn = DBConnection()
    world_news = db_conn.db_conn.fetch_world_news()
    return flask.render_template('world-live.html', world_news=world_news)


@api.route('/good-news')
def good_news():
    return flask.render_template('good-news.html')


@api.route('/how-to')
def how_to():
    return flask.render_template('how-to.html')


@api.route('/india-links')
def india_links():
    return flask.render_template('india-links.html')


@api.route('/subscribe', methods=['POST'])
def subscribe():
    # save the email address in the db
    db_conn = DBConnection()
    email = request.form.get('email')
    country = request.form.get('subscribe_country', 'world')
    frequency = request.form.get('subscribe_frequency', '24')
    db_conn.db_conn.save_subscriber(email, country, frequency)
    return jsonify({'success': True})
