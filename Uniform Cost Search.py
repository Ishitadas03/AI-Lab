import heapq
import networkx as nx
import matplotlib.pyplot as plt

graph = {
    1: [(2, 7), (3, 9), (6, 14)],
    2: [(1, 7), (3, 10), (4, 15)],
    3: [(1, 9), (2, 10), (4, 11), (6, 2)],
    4: [(2, 15), (3, 11), (5, 6)],
    5: [(4, 6), (6, 9)],
    6: [(1, 14), (3, 2), (5, 9)]
}

pos = {
    1: (0, 0),
    2: (2, -1),
    3: (2, 1),
    4: (5, 1),
    5: (4, 3),
    6: (0, 3)
}

labels = {
    1: "1\n(a)",
    2: "2",
    3: "3",
    4: "4",
    5: "5\n(b)",
    6: "6"
}

G = nx.Graph()

for u in graph:
    for v, w in graph[u]:
        if not G.has_edge(u, v):
            G.add_edge(u, v, weight=w)


def draw(current, visited, frontier, path, costs, title):
    plt.clf()

    colors = []

    for node in G.nodes():
        if node in path:
            colors.append("red")
        elif node == current:
            colors.append("deepskyblue")
        elif node in visited:
            colors.append("lightgreen")
        elif node in frontier:
            colors.append("yellow")
        else:
            colors.append("white")

    nx.draw(
        G,
        pos,
        with_labels=False,
        labels=labels,
        node_color=colors,
        node_size=900,
        edgecolors="black"
    )

    nx.draw_networkx_labels(G, pos, labels)

    nx.draw_networkx_edge_labels(
        G,
        pos,
        edge_labels=nx.get_edge_attributes(G, "weight")
    )

    text = "\n".join(
        f"g({node}) = {cost}"
        for node, cost in sorted(costs.items())
    )

    plt.gcf().text(
        0.80,
        0.50,
        text,
        bbox=dict(facecolor="white")
    )

    plt.title(title)
    plt.pause(2)


def uniform_cost_search(start, goal):
    pq = [(0, start, [start])]
    best_cost = {start: 0}
    visited = {}

    while pq:
        frontier = {node for _, node, _ in pq}
        cost, node, path = heapq.heappop(pq)

        if cost > best_cost[node]:
            continue

        if node in visited:
            continue

        visited[node] = cost

        draw(
            node,
            visited,
            frontier,
            [],
            best_cost,
            f"Expand Node {node}   Cost = {cost}"
        )

        if node == goal:
            draw(
                None,
                visited,
                set(),
                path,
                best_cost,
                f"Goal Found\nPath = {path}\nCost = {cost}"
            )
            return path, cost

        for neighbor, weight in graph[node]:
            new_cost = cost + weight

            if new_cost < best_cost.get(neighbor, float("inf")):
                best_cost[neighbor] = new_cost
                heapq.heappush(
                    pq,
                    (new_cost, neighbor, path + [neighbor])
                )

    draw(
        None,
        visited,
        set(),
        [],
        best_cost,
        "Goal Not Reachable"
    )

    return None, float("inf")


plt.figure(figsize=(9, 6))

path, cost = uniform_cost_search(1, 5)

print("Shortest Path:", path)
print("Total Cost:", cost)

plt.show()