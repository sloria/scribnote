# -*- coding: utf-8 -*-
import os

from flask import Flask, make_response

HERE = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    STATIC_FOLDER = os.path.join(HERE, 'app')
    STATIC_URL_PATH = ''


def create_app(config_obj=Config):

    app = Flask('scribnoteapp', static_folder=Config.STATIC_FOLDER,
        static_url_path=Config.STATIC_URL_PATH)
    app.config.from_object(config_obj)

    @app.route('/')
    def index():
        index_template = os.path.join(HERE, 'app', 'index.html')
        return make_response(open(index_template).read())
    return app
