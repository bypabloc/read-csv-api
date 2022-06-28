from app import app

from controllers.read_csv.read_csv import read_csv


def index():
    return 'Index Page'


app.add_url_rule('/', view_func=index, methods=['GET'])


app.add_url_rule('/v1/read-csv', view_func=read_csv, methods=['POST'])
