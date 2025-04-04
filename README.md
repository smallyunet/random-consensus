```markdown
# README

## Overview

This repository demonstrates a **Random-Consensus** mechanism in Python, along with a basic web visualization using D3.js. It has two main parts:

1. **Command-Line / Console Demos**:  
   - **main.py**: The original command-line demo code for random consensus.
   - **simulate_consensus.py**: A script that simulates the consensus across multiple rounds and produces JSON output for visualization.

2. **Web Visualization**:  
   - **index.html**: A D3.js-powered web page that reads `consensus_data.json` (generated by `simulate_consensus.py`) and displays node states as an animated sequence.
   - **consensus_data.json**: The output file from `simulate_consensus.py` containing the data for each node after each round.

## File Structure

- **demo/**
  - **index.html**: A simple HTML file using D3.js to visualize node heights and block hashes over multiple rounds.
  - **consensus_data.json**: A JSON file generated by `simulate_consensus.py` that stores each node’s state (height, hash, etc.) for each round.
  - **simulate_consensus.py**: A Python script that runs a certain number of rounds, simulating random block proposals and updates, then writes the resulting data to `consensus_data.json`.
  - **main.py**: The original console-based demonstration of the random consensus mechanism, without JSON export or visualization.

## How to Use

1. **Run the Simulation**  
   In your terminal or command line, navigate to the folder containing the scripts and run:
   ```bash
   python simulate_consensus.py
   ```
   This will create or update **consensus_data.json** with the state of each node after every consensus round.

2. **View the Visualization**  
   - Start a local web server in the same directory, for example:
     ```bash
     python -m http.server 8000
     ```
   - Open your browser to:
     ```text
     http://localhost:8000/index.html
     ```
   - You will see circles (one per node) move up or down to reflect the current chain height each round, and the text label will show a short hash identifier.

## Customization

- **Number of Nodes / Rounds**: Adjust in `simulate_consensus.py` to run more nodes or more rounds.
- **Consensus Logic**: Feel free to extend or modify the random selection, block creation, or “majority wins” approach.
- **Visualization**: Tweak `index.html` to change animation speeds, styling, or data presentation.

## License

These demos are for educational purposes only. You may adapt or integrate them into other projects under the license or terms of your choice.
