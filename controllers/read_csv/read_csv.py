import base64
import csv as csv_lib

from datetime import datetime
from app import app
from app import json
from app import request


def is_float(value) -> bool or float:
    if value is None:
        return float(0)
    if value == '':
        return float(0)
    if value == 'NaN':
        return float(0)
    try:
        return float(value)
    except ValueError:
        return float(0)


def read_csv():
    body = request.get_json()
    csv = body.get('csv')
    if csv is None:
        return json.dumps({
            'message': 'No csv provided',
            'status': 'error',
        })

    csv_base64_content = csv.split('data:text/csv;base64,', 1)
    if len(csv_base64_content) != 2:
        return json.dumps({
            'message': 'Invalid csv provided',
            'status': 'error',
        })

    csv_base64_content = csv_base64_content[1]
    decoded = base64.standard_b64decode(csv_base64_content).decode('latin-1')
    spreadSheet = csv_lib.reader(decoded.splitlines(), delimiter=',')
    data = []
    for (i, row) in enumerate(spreadSheet):
        if i == 0:
            row_new = []
            if len(row) == 1:
                row_new = row[0].replace('Date,Time,"', '').split('","')
                row_new[-1] = row_new[-1].replace('",', '')
                data.append(row_new)
            else:
                data.append(row[2:-1])
            continue
        data.append(row)

    headers = data[0]
    data = data[1:-2]
    datetime_list = []
    value_list = []
    for i in range(0, len(data)):
        item = data[i]
        datetime_string = item[0] + " " + item[1]
        datetime_string = datetime_string.replace('.', '/', 2)
        datetime_obj = datetime.strptime(datetime_string, '%d/%m/%Y %H:%M:%S.%f')
        datetime_string = datetime_obj.strftime('%Y-%m-%d %H:%M:%S')
        datetime_list.append(datetime_string)
        value_list.append(item[2:])

    data_for_graphs = {}
    for i in range(0, len(headers)):
        header = headers[i]
        data_for_graphs[header] = []
        for j in range(0, len(data)):
            data_for_graphs[header].append(is_float(data[j][i+2]))

    response = app.response_class(
        response=json.dumps({
            'data': {
                'data_for_graphs': data_for_graphs,
                'datetime_list': datetime_list,
            },
            'message': 'Csv readed',
        }),
        status=200,
        mimetype='application/json'
    )
    return response
