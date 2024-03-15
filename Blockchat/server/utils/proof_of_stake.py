import random


def proof_of_stake(stakes, seed):

    node_num = len(stakes)
    all_stakes_zero = True
    lottary = []
    lottary.append((1, stakes[0]))
    for i in range(1, len(stakes)):
        if stakes[i] > 0:
            all_stakes_zero = False
        lottary.append((lottary[i - 1][1] + 1, lottary[i - 1][1] + stakes[i]))

    total_stakes = lottary[len(stakes) - 1][1]
    validator = 0
    if not all_stakes_zero:
        random.seed(seed)
        random_number = random.randint(1, total_stakes)
        for i in range(0, len(lottary)):
            if random_number >= lottary[i][0] and random_number <= lottary[i][1]:
                validator = i
                break

    # If all stakes are zero, select randomly a node id. This id is the validator of the block
    else:
        random.seed(seed)
        random_number = random.randint(0, node_num - 1)
        validator = random_number

    # print(total_stakes)
    # print(lottary)
    # print(random_number)
    # print("validator: " + str(validator))


if __name__ == "__main__":
    proof_of_stake([10, 20, 12, 27, 42], 8001)
