import random
import uuid

class Block:
    """
    A simplified block structure.
    - height: The block height.
    - parent_hash: The hash of the parent block.
    - hash: The block's own hash (randomly generated).
    """
    def __init__(self, height, parent_hash):
        self.height = height
        self.parent_hash = parent_hash
        self.hash = str(uuid.uuid4())  # Use random UUID to simulate a block hash

    def __repr__(self):
        # Truncate hashes for readability
        short_hash = self.hash[:6]
        short_parent = self.parent_hash[:6] if self.parent_hash else None
        return f"Block(h={self.height}, hash={short_hash}, parent={short_parent})"


# Use a single genesis block shared by all nodes
FIXED_GENESIS_HASH = "00000000-0000-0000-0000-000000000000"

GENESIS_BLOCK_TEMPLATE = Block(height=0, parent_hash=None)
GENESIS_BLOCK_TEMPLATE.hash = FIXED_GENESIS_HASH


class Node:
    """
    A simplified node maintaining a local chain.
    - self.chain is a list of blocks.
    - self.chain[-1] is considered the tip of the chain.
    """
    def __init__(self, node_id):
        self.node_id = node_id
        # Clone the shared genesis block for each node
        genesis_block = Block(height=GENESIS_BLOCK_TEMPLATE.height,
                              parent_hash=GENESIS_BLOCK_TEMPLATE.parent_hash)
        genesis_block.hash = GENESIS_BLOCK_TEMPLATE.hash
        self.chain = [genesis_block]

    def current_height(self):
        """Returns the height of the local chain tip."""
        return self.chain[-1].height

    def propose_block(self):
        """
        Produce a new block:
          - height is current_height + 1
          - parent_hash is the hash of the local chain tip
        """
        latest = self.chain[-1]
        new_block = Block(height=latest.height + 1, parent_hash=latest.hash)
        return new_block

    def add_block(self, block):
        """
        Add a block if it correctly follows our chain tip:
          - block.height == current_height + 1
          - block.parent_hash == local tip's hash
        """
        if block.height == self.current_height() + 1:
            if block.parent_hash == self.chain[-1].hash:
                self.chain.append(block)

    def discard_last_block(self):
        """Discard the last block, simulating 'self-correction'."""
        if len(self.chain) > 1:
            self.chain.pop()


def random_consensus_round(nodes):
    """
    One round of the consensus:
      1. Every node proposes a block (gathered in proposed_blocks).
      2. Each node randomly picks one valid block (if any) to add.
      3. If no valid block is found and the network is higher, the node discards its last block.
      4. Identify the majority height and the majority block-hash at that height.
         - Any node that is behind that height or on a different hash at that same height
           discards its tip (if needed) and adopts the majority block.
    """
    # 1. Collect all proposed blocks
    proposed_blocks = []
    for node in nodes:
        proposed_blocks.append(node.propose_block())

    # 2. Randomly pick and add one valid block (matching next_height) for each node
    for node in nodes:
        next_h = node.current_height() + 1
        valid_blocks = [b for b in proposed_blocks if b.height == next_h]

        if valid_blocks:
            chosen = random.choice(valid_blocks)
            node.add_block(chosen)
        else:
            # 3. If no block is found and there's a higher chain in the network, discard
            max_h = max(n.current_height() for n in nodes)
            if max_h > node.current_height():
                print(f"Node {node.node_id} discarding last block (behind network: {node.current_height()} < {max_h})")
                node.discard_last_block()

    # 4. "Majority-wins" approach, focusing on block hash at the majority height

    # Count how many nodes are at each height
    height_count = {}
    for node in nodes:
        h = node.current_height()
        height_count[h] = height_count.get(h, 0) + 1

    # Pick the height that has the largest number of nodes (the "majority height")
    if not height_count:
        return
    majority_height = max(height_count, key=height_count.get)

    # Among the nodes that are at majority_height, count how many times each hash occurs
    hash_count = {}
    for node in nodes:
        if node.current_height() == majority_height:
            tip_hash = node.chain[-1].hash
            hash_count[tip_hash] = hash_count.get(tip_hash, 0) + 1

    if not hash_count:
        return
    # Find the block hash that is the majority at that height
    majority_hash = max(hash_count, key=hash_count.get)

    # Pick one node that actually has this majority hash to copy from
    # (In a real system, you'd also reconstruct the entire chain from a common ancestor.)
    reference_block = None
    for node in nodes:
        if node.current_height() == majority_height and node.chain[-1].hash == majority_hash:
            reference_block = node.chain[-1]
            break

    if not reference_block:
        return

    # Now, for each node that is either behind (height < majority_height)
    # or at majority_height but with a different hash, adopt the majority block
    for node in nodes:
        if node.current_height() < majority_height:
            # Node is behind. Discard blocks until height is just below majority_height
            while node.current_height() >= majority_height and len(node.chain) > 1:
                node.discard_last_block()

            # Then add the majority block if the height is exactly one less
            if node.current_height() + 1 == reference_block.height:
                # We create a new block object that has the same height/hash,
                # but uses the node's current tip as the parent, to simulate "catching up."
                adopted = Block(reference_block.height, node.chain[-1].hash)
                adopted.hash = reference_block.hash
                node.add_block(adopted)

        elif node.current_height() == majority_height:
            # Same height, but possibly a different hash
            local_hash = node.chain[-1].hash
            if local_hash != majority_hash:
                print(f"Node {node.node_id} is at majority_height but with a different hash ({local_hash[:6]}), adopting majority ({majority_hash[:6]})")
                # Discard the last block
                node.discard_last_block()
                # Then add the majority block
                # (Again, in a real system we'd do a full sync from common ancestor.)
                if node.current_height() + 1 == reference_block.height:
                    adopted = Block(reference_block.height, node.chain[-1].hash)
                    adopted.hash = reference_block.hash
                    node.add_block(adopted)


def main():
    """
    Creates 5 nodes, runs the simplified random consensus mechanism for 5 rounds,
    then prints each node's chain after each round.
    """
    nodes = [Node(node_id=i) for i in range(5)]

    ROUNDS = 5
    for r in range(ROUNDS):
        print(f"=== Round {r} ===")
        random_consensus_round(nodes)

        # Display the state of each node
        for node in nodes:
            print(f"Node {node.node_id} | height={node.current_height()} | chain={node.chain}")
        print("")

if __name__ == "__main__":
    main()
