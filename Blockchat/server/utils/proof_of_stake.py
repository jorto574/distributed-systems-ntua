import random


def proof_of_stake(stakes):
    """blockchain = state.blockchain
    last_block = blockchain.block_list[-1]
    seed = last_block.current_hash

    stakes = state.stakes"""

    lottary = []
    lottary.append((1, stakes[0]))
    for i in range(1, len(stakes)):
        lottary.append((lottary[i - 1][1] + 1, lottary[i - 1][1] + stakes[i]))

    total_stakes = lottary[len(stakes) - 1][1]
    seed_value = 42
    random.seed(seed_value)
    random_number = random.randint(1, total_stakes)

    validator = 0
    for i in range(0, len(lottary)):
        if random_number >= lottary[i][0] and random_number <= lottary[i][1]:
            validator = i
            break

    print(total_stakes)
    print(lottary)
    print(random_number)
    print("validator: " + str(validator))


# TODO examine edge cases: what happens if some node or all nodes staKe 0 BCC

if __name__ == "__main__":
    proof_of_stake([0, 0, 0, 0, 0])
