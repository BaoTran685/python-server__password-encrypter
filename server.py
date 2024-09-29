from flask import Flask, request, jsonify

from generate import generate_password
from encrypt_decrypt import function_password

app = Flask(__name__)

# GET
# POST
# PUT
# DELETE

# systemctl status ...
# ssytemctl restart ...

@app.route('/generate/', methods=['POST'])
def handleGenerate():
  LOW = 0
  HIGH = 100
  data = request.get_json()
  # convert to int
  for key in data.keys():
    data[key] = int(data[key])
    # check for invalid input
    if (data[key] < LOW or data[key] > HIGH):
      return jsonify(), 400
  # generate a random password
  password = generate_password(data['specialChar'], data['upperCase'])
  return jsonify({"password": password}), 200

@app.route('/function/', methods=['POST'])
def handleFunction():
  data = request.get_json()
  password = function_password(data['key'], data['password'], data['type'])
  return jsonify({"password": password}), 200


if (__name__ == "__main__"):
  app.run(debug=True)

