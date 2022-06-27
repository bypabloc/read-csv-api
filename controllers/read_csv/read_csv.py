import base64
import csv as csv_lib

from app import app
from app import json
from app import request


def read_csv():
    print("read_csv")

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
    spreadSheet = csv_lib.reader(decoded.splitlines(), delimiter=',', quotechar='"')
    data = []
    for (i, row) in enumerate(spreadSheet):
        if i == 0:
            row_new = row[0].replace('Date,Time,"', '').split('","')
            row_new[-1] = row_new[-1].replace('",', '')
            data.append(row_new)
            continue
        data.append(row)

    headers = data[0]
    data = data[1:]
    data_dict = {}
    for i in range(0, len(headers)):
        data_dict[headers[i]] = {
            'data': [],
            'time': [],
        }
        for j in range(0, len(data)):
            data_dict[headers[i]]['time'].append(data[j][0] + " " + data[j][1])
            data_dict[headers[i]]['data'].append(data[j][i+2])

    response = app.response_class(
        response=json.dumps({
            'data': {
                'data': data_dict,
            },
            'message': 'Csv readed',
        }),
        status=200,
        mimetype='application/json'
    )
    return response
