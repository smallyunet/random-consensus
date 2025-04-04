import json
import random
import uuid

class Block:
    """
    A simplified block structure.
    """
    def __init__(self, height, parent_hash):
        self.height = height
        self.parent_hash = parent_hash
        self.hash = str(uuid.uuid4())

    def __repr__(self):
        return f"Block(h={self.height}, hash={self.hash[:6]}, parent={self.parent_hash[:6] if self.parent_hash else None})"

FIXED_GENESIS_HASH = "00000000-0000-0000-0000-000000000000"

GENESIS_BLOCK_TEMPLATE = Block(0, None)
GENESIS_BLOCK_TEMPLATE.hash = FIXED_GENESIS_HASH

class Node:
    def __init__(self, node_id):
        self.node_id = node_id
        # Clone the genesis block
        genesis = Block(GENESIS_BLOCK_TEMPLATE.height, GENESIS_BLOCK_TEMPLATE.parent_hash)
        genesis.hash = GENESIS_BLOCK_TEMPLATE.hash
        self.chain = [genesis]

    def current_height(self):
        return self.chain[-1].height

    def propose_block(self):
        latest = self.chain[-1]
        new_block = Block(latest.height + 1, latest.hash)
        return new_block

    def add_block(self, block):
        if block.height == self.current_height() + 1:
            if block.parent_hash == self.chain[-1].hash:
                self.chain.append(block)

    def discard_last_block(self):
        if len(self.chain) > 1:
            self.chain.pop()

def random_consensus_round(nodes):
    """
    This version is very similar to your code, but returns a summary of each node's state
    so we can record it for visualization.
    """
    proposed_blocks = [node.propose_block() for node in nodes]

    for node in nodes:
        nxt = node.current_height() + 1
        valid = [b for b in proposed_blocks if b.height == nxt]
        if valid:
            chosen = random.choice(valid)
            node.add_block(chosen)
        else:
            max_h = max(n.current_height() for n in nodes)
            if max_h > node.current_height():
                node.discard_last_block()

    # "Majority-wins" logic (very simple: we just track height majority)
    height_count = {}
    for nd in nodes:
        h = nd.current_height()
        height_count[h] = height_count.get(h, 0) + 1

    majority_height = max(height_count, key=height_count.get)

    # If some nodes are not at the majority height, do nothing or do partial discards
    # (Simplified: we won't do big merges or adoption in this version.)

    # Return summary data for each node: node_id, height, chain_top_hash
    round_state = []
    for nd in nodes:
        round_state.append({
            "node_id": nd.node_id,
            "height": nd.current_height(),
            "hash": nd.chain[-1].hash[:6]  # short hash for readability
        })
    return round_state

def main():
    NODES = 5
    ROUNDS = 5
    nodes = [Node(i) for i in range(NODES)]

    all_rounds_data = []  # will store states for each round

    for r in range(ROUNDS):
        # run one consensus round
        round_state = random_consensus_round(nodes)
        # store the result
        # also add a "round_index" to each node's data for identification in the final JSON
        for s in round_state:
            s["round"] = r
        all_rounds_data.extend(round_state)

    # Save into a JSON file
    with open("consensus_data.json", "w") as f:
        json.dump(all_rounds_data, f, indent=2)

if __name__ == "__main__":
    main()
