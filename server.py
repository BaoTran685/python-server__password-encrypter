from flask import Flask, request, jsonify

from process import generate_password

app = Flask(__name__)

# GET
# POST
# PUT
# DELETE

LOW = 0
HIGH = 20

@app.route('/generate/', methods=['POST'])
def handleGenerate():
  data = request.get_json()
  # convert to int
  for key in data.keys():
    data[key] = int(data[key])
    # check for invalid input
    if (data[key] < LOW or data[key] > HIGH):
      return jsonify(), 400
  # generate a random password
  password = generate_password(data)
  return jsonify({"password": password}), 200

if (__name__ == "__main__"):
  app.run(debug=True)