from flask import Blueprint, request, current_app, jsonify
from utils.broadcast import broadcast
import time
import os

end_exp_bp = Blueprint("endExp", __name__)

@end_exp_bp.route("/endExp", methods=["POST"])
def end_exp():
    data = request.json
    node_id = data["node_id"]
    current_app.config["times"][node_id] = data["time"]

    current_app.config["node_count"] += 1
    node_count = current_app.config["node_count"]
    node_num = current_app.config["node_num"]
    if (node_count) == node_num:
        times = current_app.config["times"]
        start_time = current_app.config["start_time"]
        blockchain_len = len(current_app.config["my_state"].blockchain.block_list)
        val_count = current_app.config["my_state"].validation_count
        end_time = time.time()
        elapsed_time = end_time - start_time

        folder_path = "../runs"
        test_name = f"NodeNum={node_num}Capacity={current_app.config["capacity"]}Staking=one100.txt"
        output_file_path = os.path.join(folder_path, test_name)

        with open(output_file_path, 'w') as f:
            f.write(f"Elapsed time: {elapsed_time} seconds\n")
            f.write(f"Throughput: {(100*node_num)/elapsed_time} transactions/second\n")
            f.write(f"Block time: {elapsed_time/blockchain_len} seconds/block\n\n")
            for node_id, end_time in times.items():
                f.write(f"Node {node_id} elapsed time: {end_time} seconds\n")
                f.write(f"Node {node_id} throughput: {100/end_time} transactions/second\n")
                f.write(f"Node {node_id} validated {val_count[node_id]} blocks\n\n")

        print("Test results saved to:", output_file_path)


        # print()
        # print("Elapsed time:", elapsed_time, "seconds")
        # print("Throughput:", (100*node_num)/elapsed_time, "transactions/second")
        # print()
        # for node_id, end_time in times.items():
        #     print(f"Node {node_id} elapsed time: {end_time} seconds")
        #     print(f"Node {node_id} throughput: {100/end_time} transactions/second")
        #     print()


    response_data = {"status": "logged"}
    response_status = 200

    return jsonify(response_data), response_status
