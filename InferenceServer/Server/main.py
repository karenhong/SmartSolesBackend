from flask import Flask, request, jsonify
import numpy as np
from keras.models import model_from_json

app = Flask(__name__)

print("Hello World")
current = "good"

@app.route("/")
def home():
    res = {"result": current}
    print(res)
    return jsonify(res)

@app.route("/smartsoles", methods = ["POST"])
def interpret():
    print("Interpreting")
    payload = request.get_json(force=True)
    print("The request was:")
    print(payload["data"])
    df = np.array(payload["data"])

    result = interpret_data(df)
    print("The result was:")

    global current 
    current = result

    print(current)

    return current

def interpret_data(request_data):
    verbose, epochs, batch_size = 0, 25, 64
    print("The request")
    print(request_data)

    n_timesteps, n_features, n_outputs = 501, 5, 2 # request_data.shape[1], request_data.shape[2], 2 # last 2 used to be trainy.shape[1]
    n_steps, n_length = 3, 167
    request_data = request_data.reshape((1, n_steps, 1, n_length, n_features))

    json_file = open('model/model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights("model/model.h5")
    loaded_model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    onehotresult = loaded_model.predict(request_data)

    print("Result")
    print(onehotresult)

    if onehotresult[0][0] >= onehotresult[0][1] :
        return "good"
    else:
        return "bad"
    

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)