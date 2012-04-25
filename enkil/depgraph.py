"""

   Tarjan's algorithm and topological sorting implementation in Python

   by Paul Harrison

   Public domain, do with it as you will

   http://www.logarithmic.net/pfh/blog/01208083168

"""


def strongly_connected_components(graph):
    """
    Tarjan's Algorithm (named for its discoverer, Robert Tarjan) is a graph
    theory algorithm for finding the strongly connected components of a graph.

    Based on:
    http://en.wikipedia.org/wiki/Tarjan%27s_strongly_connected_components_algorithm
    """

    index_counter = [0]
    stack = []
    lowlinks = {}
    index = {}
    result = []

    def strongconnect(node):
        # set the depth index for this node to the smallest unused index
        index[node] = index_counter[0]
        lowlinks[node] = index_counter[0]
        index_counter[0] += 1
        stack.append(node)

        # Consider successors of `node`
        try:
            successors = graph[node]
        except:
            successors = []

        for successor in successors:
            if successor not in lowlinks:
                # Successor has not yet been visited; recurse on it
                strongconnect(successor)
                lowlinks[node] = min(lowlinks[node], lowlinks[successor])
            elif successor in stack:
                # The successor is in the stack and hence in the current
                # strongly connected component (SCC)
                lowlinks[node] = min(lowlinks[node], index[successor])

        # If `node` is a root node, pop the stack and generate an SCC
        if lowlinks[node] == index[node]:
            connected_component = []

            while True:
                successor = stack.pop()
                connected_component.append(successor)
                if successor == node:
                    break

            component = tuple(connected_component)

            # Store the result
            result.append(component)

    for node in graph:
        if node not in lowlinks:
            strongconnect(node)

    return result


def topological_sort(graph):
    count = {}
    for node in graph:
        count[node] = 0
    for node in graph:
        for successor in graph[node]:
            count[successor] += 1

    ready = [node for node in graph if count[node] == 0]

    result = []
    while ready:
        node = ready.pop(-1)
        result.append(node)

        for successor in graph[node]:
            count[successor] -= 1
            if count[successor] == 0:
                ready.append(successor)

    return result


def robust_topological_sort(graph):
    """ First identify strongly connected components,
        then perform a topological sort on these components. """

    components = strongly_connected_components(graph)

    node_component = {}
    for component in components:
        for node in component:
            node_component[node] = component

    component_graph = {}
    for component in components:
        component_graph[component] = []

    for node in graph:
        node_c = node_component[node]
        for successor in graph[node]:
            successor_c = node_component[successor]
            if node_c != successor_c:
                component_graph[node_c].append(successor_c)

    return topological_sort(component_graph)


class DependencyGraph(object):
    """
    This class implements a simple dependency graph with support for nodes
    and multiple dependencies.
    """

    def __init__(self):
        self.nodes = {}

    def add_node(self, node):
        self.nodes[node] = []

    def add_nodes(self, nodes):
        for n in nodes:
            self.add_node(n)

    def add_dependency(self, node, dependency):
        self.nodes[node].append(dependency)

    def add_dependencies(self, node, dependencies):
        for dep in dependencies:
            self.add_dependency(node, dep)

    def get_traversal(self):
        top_sorted = robust_topological_sort(self.nodes)
        top_sorted.reverse()

        return top_sorted
