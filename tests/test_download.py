import os
import tempfile
import requests_mock as req_mock

from page_loader import download

DIR_PATH = os.path.dirname(__file__)
SOURCE_PATH = 'https://ru.hexlet.io/courses'
names_fixture = {
    'html_after': 'ru-hexlet-io-courses.html',
    'html_before': 'courses.html',
    'image': 'ru-hexlet-io-assets-professions-python.png',
    'css': 'ru-hexlet-io-assets-application.css',
    'js': 'ru-hexlet-io-packs-js-runtime.js',
    'folder': 'ru-hexlet-io-courses_files',
}


def get_fixture_path(filename):
    return os.path.join(DIR_PATH, 'fixtures', filename)


def read_file(filename):
    return open(get_fixture_path(filename)).read()


before = read_file('before.html')
after = read_file('after.html')
structure = [
    names_fixture['folder'],
    names_fixture['image'],
    names_fixture['js'],
    names_fixture['css'],
    names_fixture['html_after'],
    names_fixture['html_after'],
]


def dir_tree(dir_parth):
    tree = []
    for _, dir, file in os.walk(dir_parth):
        tree.extend(dir + file)
    return tree


def test_download(requests_mock):
    requests_mock.get(req_mock.ANY, text=before)

    with tempfile.TemporaryDirectory() as tmpdirname:
        expected = os.path.join(tmpdirname, names_fixture['html_after'])
        actual = download(SOURCE_PATH, tmpdirname)

        assert expected == actual


def test_download_html_data(requests_mock):
    requests_mock.get(req_mock.ANY, text=before)
    with tempfile.TemporaryDirectory() as tmpdirname:
        actual = download(SOURCE_PATH, tmpdirname)

        assert read_file(actual) == after


def test_download_structire(requests_mock):
    requests_mock.get(req_mock.ANY, text=before)
    with tempfile.TemporaryDirectory() as tmpdirname:
        download(SOURCE_PATH, tmpdirname)
        actual = dir_tree(tmpdirname)
        assert sorted(actual) == sorted(structure)
