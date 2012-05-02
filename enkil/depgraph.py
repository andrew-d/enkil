import copy


class CycleException(Exception):
    pass


class DependencyGraph(object):
    """
    This class implements a simple dependency graph with support for nodes
    and multiple dependencies.
    """

    def __init__(self):
        self.nodes = {}

    def add_node(self, node):
        self.nodes[node] = [0]

    def add_nodes(self, nodes):
        for n in nodes:
            self.add_node(n)

    def add_dependency(self, node, dependency):
        self.nodes[node].append(dependency)

    def add_dependencies(self, node, dependencies):
        for dep in dependencies:
            self.add_dependency(node, dep)

    def get_traversal(self):
        # Copy our graph.
        graph = copy.copy(self.nodes)

        # Find all roots.
        # Original topological sort code written by Ofer Faigon (www.bitformation.com) and used with permission.
        roots = [node for (node, nodeinfo) in graph.items() if nodeinfo[0] == 0]

        sorted_items = []
        while len(roots) != 0:
            # If len(roots) is always 1 when we get here, it means that
            # the input describes a complete ordering and there is only
            # one possible output.
            #
            # When len(roots) > 1, we can choose any root to send to the
            # output; this freedom represents the multiple complete orderings
            # that satisfy the input restrictions. We arbitrarily take one of
            # the roots using pop(). Note that for the algorithm to be efficient,
            # this operation must be done in O(1) time.
            root = roots.pop()
            sorted_items.append(root)

            for child in graph[root][1:]:
                graph[child][0] = graph[child][0] - 1

                if graph[child][0] == 0:
                    roots.append(child)

            del graph[root]

        if len(graph.items()) != 0:
            # There is a loop in the input.
            raise CycleException("Cycle in dependencies: %r" % (graph.items()))

        return sorted_items
