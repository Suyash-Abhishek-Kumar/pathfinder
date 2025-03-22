
# PathFinder

## Overview

PathFinder is a simulation program that demonstrates Dijkstra's pathfinding algorithm using a shopping complex as an example. This project visualizes how the algorithm computes the shortest path between nodes in a graph, making it a valuable educational tool for understanding pathfinding concepts.

## Features

- **Dijkstra's Algorithm Simulation:** Visual representation of the algorithm's process in finding the shortest path.
- **Shopping Complex Layout:** Uses a shopping complex scenario to illustrate real-world applications.
- **Interactive Visualization:** Allows users to observe the step-by-step execution of the algorithm.

## Installation

To run the PathFinder simulation locally, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Suyash-Abhishek-Kumar/pathfinder.git
   cd pathfinder
   ```

2. **Set up a virtual environment (optional but recommended):**
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows, use 'env\Scripts\activate'
   ```

## Usage

To start the simulation:

```bash
python python_display.py
```

This command will launch the visualization of Dijkstra's algorithm applied to the shopping complex layout.

## Project Structure

- `Graph.py`: Contains the implementation of the graph data structure and Dijkstra's algorithm.
- `node.py`: Defines the node structure used in the graph.
- `setLayout.py`: Sets up the layout of the shopping complex for the simulation.
- `python_display.py`: Manages the graphical display of the simulation.
- `graphics/`: Directory containing graphical assets used in the visualization.

## Contact

For questions or suggestions, please open an issue in this repository.
