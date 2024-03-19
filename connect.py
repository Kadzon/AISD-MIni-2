import pandas as pd
from flask import Flask, Response, request, jsonify

from base_iris_lab1 import train, new_model, score, add_dataset

app = Flask(__name__)

base_url = '/iris/'


@app.route(base_url + "dataset", methods=['POST'])
def dataset():
    file = request.files['train']

    if file.filename == '':
        return Response("file is required", status=400)

    if file.filename.split('.')[-1] != 'csv':
        return Response("file must be a csv", status=400)

    try:
        df = pd.read_csv(file)
        dataset_id = add_dataset(df)

        return Response(str(dataset_id))

    except Exception as e:
        return Response(str(e), status=400)


@app.route(base_url + "model", methods=['POST'])
def train_new_model():
    dataset_id = int(request.form.get("dataset"))

    if dataset_id is None:
        return Response("dataset is required", status=400)

    model_id = new_model(dataset_id)

    return Response(str(model_id))


@app.route(base_url + "model/<int:model_id>", methods=['PUT'])
def retrain_model(model_id: int):
    dataset_id = int(request.args.get("dataset"))

    if dataset_id is None:
        return Response("dataset is required", status=400)

    try:
        history = train(model_id, dataset_id)

        return jsonify(history)

    except Exception as e:
        return Response(str(e), status=400)


@app.route(base_url + "model/<int:model_id>", methods=['GET'])
def score_model(model_id: int):
    fields = request.args.get("fields")
    if fields is not None:
        fields = fields.split(',')
        fields = [float(f) for f in fields]
    else:
        return Response("fields are required", status=400)

    try:
        the_score = score(model_id, fields)
        return Response(the_score)

    except Exception as e:
        return Response(str(e), status=400)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=6000)
