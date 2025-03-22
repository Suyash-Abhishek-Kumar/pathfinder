from heapq import heapify, heappop, heappush


class Graph:
    def __init__(self, graph: dict = {}):
        self.graph = graph  # A dictionary for the adjacency list

    def print_graph(self):
        for i in self.graph.keys():
            print(i, end=":- ")
            val = self.graph.get(i)
            for j in val: print(f"{j}: {val[j]} ", end="")
            print()

    def add_edge(self, node1, node2, weight):
        if node1 not in self.graph:  # Check if the node is already added
            self.graph[node1] = {}  # If not, create the node
        self.graph[node1][node2] = weight  # Else, add a connection to its neighbor
        if node2 not in self.graph:
            self.graph[node2] = {}
        self.graph[node2][node1] = weight  # Connect it the other way around too

    def remove_edge(self, node):
        if node not in self.graph:
            print("Node not in graph")
        else:
            for i in self.graph.get(node):
                loc = self.graph.get(i)
                loc.pop(node)
            self.graph.pop(node)

    def shortest_distances(self, source: str):
        distancess = {node: float("inf") for node in self.graph}  # Initialize the values of all nodes with infinity
        distancess[source] = 0  # Set the source value to 0

        # Initialize a priority queue
        pq = [(0, source)]
        heapify(pq)

        # Create a set to hold visited nodes
        visited = set()

        while pq:  # While the priority queue isn't empty
            current_distance, current_node = heappop(pq)

            if current_node in visited:
                continue
            visited.add(current_node)

            for neighbor, weight in self.graph[current_node].items():
                # Calculate the distance from current_node to the neighbor
                tentative_distance = current_distance + weight
                if tentative_distance < distancess[neighbor]:
                    distancess[neighbor] = tentative_distance
                    heappush(pq, (tentative_distance, neighbor))

        predecessorss = {node: None for node in self.graph}

        for node, distance in distancess.items():
            for neighbor, weight in self.graph[node].items():
                if distancess[neighbor] == distance + weight:
                    predecessorss[neighbor] = node

        return distancess, predecessorss

    def shortest_path(self, source: str, target: str):
        # Generate the predecessors dict
        _, predecessorss = self.shortest_distances(source)

        path = []
        current_node = target

        # Backtrack from the target node using predecessors
        while current_node:
            path.append(current_node)
            current_node = predecessorss[current_node]

        # Reverse the path and return it
        path.reverse()

        return path

if __name__ == '__main__':
    graph = {
    "A": {"B": 3, "C": 3},
    "B": {"A": 3, "D": 3.5, "E": 2.8},
    "C": {"A": 3, "E": 2.8, "F": 3.5},
    "D": {"B": 3.5, "E": 3.1, "G": 10},
    "E": {"B": 2.8, "C": 2.8, "D": 3.1, "G": 7},
    "F": {"G": 2.5, "C": 3.5},
    "G": {"F": 2.5, "E": 7, "D": 10},
    }

    g = Graph(graph=graph)
    g.print_graph()
    g.remove_edge("B")
    print()
    g.print_graph()
