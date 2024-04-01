from flask import Blueprint, request, current_app, jsonify
from utils.broadcast import broadcast
import time

end_exp_bp = Blueprint("endExp", __name__)

@end_exp_bp.route("/endExp", methods=["POST"])
def end_exp():
    data = request.json
    node_id = data["node_id"]
    times = app.config["times"][node_id] = data["time"]

    current_app.config["node_count"] += 1
    node_num = current_app.config["node_num"]
    if (node_count + 1) == node_num:
        start_time = current_app.config["start_time"]
        end_time = time.time()
        elapsed_time = end_time - start_time
        print("Elapsed time:", elapsed_time, "seconds")
        print("Throughput:", (100*node_num)/elapsed_time, "transactions/second")
        print()
        for node_id, time in times.items():
            print(f"Node {node_id} elapsed time: {time} seconds")
            print(f"Node {node_id} throughput: {100/time} transactions/second")
            print()


    response_data = {"status": "logged"}
    response_status = 200

    return jsonify(response_data), response_status
