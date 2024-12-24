import json
from flask import Flask, request
import db

app = Flask(__name__)

DB = db.DatabaseDriver()


@app.route("/")

@app.route("/api/users/")
def get_users():
    """
    returns all users
    """
    return json.dumps({"users": DB.get_all_users()}), 200


@app.route("/api/users/", methods=["POST"])
def create_user():
    """
    creates a user and puts it into db
    """
    body = json.loads(request.data)
    name = body.get("name")
    username = body.get("username")
    balance = body.get("balance")
    user_id = DB.insert_user_table(name, username, balance)
    user = DB.get_user_by_id(user_id)
    if user is None:
        return json.dumps({"error": "User not found"}), 400
    return json.dumps(user), 201

@app.route("/api/user/<int:user_id>/")
def get_user(user_id):
    """
    returns a specific user from the db according to the user_id
    """
    user = DB.get_user_by_id(user_id)
    if user is None:
        return json.dumps({"error": "User not found"}), 404
    return json.dumps(user), 200

@app.route("/api/user/<int:user_id>/", methods=["DELETE"])
def delete_user(user_id):
    """
    deletes a user from the db based on the user_id
    """
    user = DB.get_user_by_id(user_id)
    if user is None:
        return json.dumps({"error": "User not found"}), 404 
    DB.delete_user_by_id(user_id)
    return json.dumps(user), 200

@app.route("/api/send/", methods=["POST"])
def send_money():
    """
    changes the amount that the sender and reciever has depending on how much was sent/recieved
    """
    body = json.loads(request.data)
    sender_id = body.get("sender_id")
    receiver_id = body.get("receiver_id")
    amount = body.get("amount")

    if not sender_id or not receiver_id or amount is None:
        return json.dumps({"error": "Missing required field"}), 400
    if amount <= 0:
        return json.dumps({"error": "amount must be greater than 0"}), 400

    sender = DB.get_user_by_id(sender_id)
    receiver = DB.get_user_by_id(receiver_id)
    if sender is None or receiver is None:
        return json.dumps({"error": "User not found"}), 400
    
    if sender["balance"] < amount:
        return json.dumps({"error": "sender does not have enough balance"}), 400
    
    DB.update_user_balance(sender_id, sender["balance"] - amount)
    DB.update_user_balance(receiver_id, receiver["balance"] + amount)

    return json.dumps({
        "sender_id": sender_id,
        "receiver_id": receiver_id,
        "amount": amount
    }), 200
    



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
