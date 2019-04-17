#!/usr/bin/env python
# encoding: utf-8
from os import environ
from os import listdir, path

import ckan.plugins as p
from ckan.plugins.toolkit import url_for, redirect_to

from flask import jsonify, send_from_directory, Blueprint, abort

CURRENT_PATH = environ['METADATA_FOLDER']

app = Blueprint('file_server', __name__)


def get_folder_content(guid):
    if guid in listdir(CURRENT_PATH):
        folder_content = listdir(path.join(CURRENT_PATH, guid))
        xml_file = "{}.xml".format(guid)
        if xml_file in folder_content:
            folder_content.remove(xml_file)
            return folder_content
    else:
        return False


def get_folder_by_index(index):
    print("in get by index")
    data_content = listdir(CURRENT_PATH)
    if index > len(data_content):
        return False
    else:
        return data_content[index]

@app.route("/data", endpoint='get_data_content')
def get_data_content():
    return jsonify({'data_content': listdir(CURRENT_PATH)})


@app.route("/data/<string:guid>", endpoint='get_content')
def get_content(guid):
    content = get_folder_content(guid)
    if content:
        return jsonify({'folder_content': content})
    else:
        return 'Folder not found. Check metadata.'


@app.route("/data/<int:index>/",endpoint='get_index')
def get_index(index):
    data_content = listdir(CURRENT_PATH)
    if index > len(data_content):
        return abort(404)
    else:
        guid = data_content[index]
        return redirect_to(url_for('file_server.get_content', guid=guid))


@app.route("/data/<string:guid>/<string:file_name>", endpoint='get_file')
def get_file(guid, file_name):
    folder_content = get_folder_content(guid)
    if folder_content:
        if file_name in folder_content:
            return send_from_directory(path.join(CURRENT_PATH, guid), file_name)
    else:
        return 'Folder not found. Check metadata.'


@app.route("/data/<int:folder_index>/<string:file_name>", endpoint='get_file_by_folder_index')
def get_file_by_folder_index(folder_index, file_name):
    print('get_file_by_folder_index')
    guid = get_folder_by_index(folder_index)
    if guid:
        return redirect_to(url_for('file_server.get_file', guid=guid, file_name=file_name))


@app.route("/data/<string:guid>/<int:file_index>",endpoint='get_file_by_index_in_folder')
def get_file_by_index_in_folder(guid, file_index):
    print('get_file_by_index_in_folder')
    folder_content = get_folder_content(guid)
    if folder_content and file_index < len(folder_content):
        file_name = folder_content[file_index]
        return redirect_to(url_for('file_server.get_file', guid=guid, file_name=file_name))


class Create_Resource_From_CsvPlugin(p.SingletonPlugin):
    p.implements(p.IBlueprint)

    def get_blueprint(self):
        return app
