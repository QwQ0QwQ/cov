import sys
import matplotlib
import networkx
import networkx as nx
import requests
from collections import deque, defaultdict
from pprint import pprint, pformat
import matplotlib.pyplot as plt

matplotlib.use('TkAgg')
DEFAULT_COMPARISON_EDGE_ATTRIBUTES = [
    "unevalResult",
    "isSealed",
    "isFrozen",
    "isExtensible",
    "isPrimitive",
    "isToStringSuccessful",
    "isAboutBlankDOM",
    "toStringErrorMessage",
]

DEFAULT_COMPARISON_NODE_ATTRIBUTES = [
    "nodevalue",
    "nodetype",
    "readErrorMessage",
    "isSelfEqualTripleEqual",
    "isSelfEqualObjectIs",
    "isReferenceSelfEqualObjectIs",
    "isReferenceSelfEqualTripleEqual",
    "isDeterministic",
    # "readTime",
]


def urldecode(text):
    return requests.utils.unquote(text)  # .decode('utf8')


def is_wellformed_DEG(nxgraph):
    try:
        assert_DEG_wellformity(nxgraph)
        return True
    except:
        return False


def assert_DEG_wellformity(nxgraph):
    if int(nxgraph.graph['number_of_nodes']) != nxgraph.number_of_nodes():
        raise ValueError(
            "The defragmented graph does not contain the number of nodes indicated by the JavaScript Crawler (expected: %s, actual: %d, diff: %d)." % (
                nxgraph.graph['number_of_nodes'], nxgraph.number_of_nodes(),
                int(nxgraph.graph['number_of_nodes']) - nxgraph.number_of_nodes()
            ))
    if int(nxgraph.graph['number_of_edges']) != nxgraph.number_of_edges():
        raise ValueError(
            "The defragmented graph does not contain the number of edges indicated by the JavaScript Crawler (expected: %s, actual: %d, diff: %d)." % (
                nxgraph.graph['number_of_edges'], nxgraph.number_of_edges(),
                int(nxgraph.graph['number_of_edges']) - nxgraph.number_of_edges()
            ))
    for u, v, key, data in nxgraph.edges(data=True, keys=True):
        for edge_attribute_name in ['edgelabel', 'firstpath', 'traversaltype', 'traversaltype']:
            if edge_attribute_name not in data:
                raise ValueError(
                    "Edge (%s->%s, %s) of graph %s does not have the mandatory property '%s'\nData:\n%s" % (
                    u, v, key, nxgraph.name, edge_attribute_name, pformat(data)))
    for n, data in nxgraph.nodes(data=True):
        for node_attribute_name in ['nodetype']:
            if node_attribute_name not in data:
                raise ValueError("Node %s of graph %s does not have the mandatory property '%s'" % (
                n, nxgraph.name, node_attribute_name))
    if not nxgraph.has_node('0'):
        raise ValueError("The virtual entry node (id=0) is missing")
    if len(nxgraph.out_edges('0')) != 1:
        raise ValueError("The virtual entry edge is not present at node[id=0]")
    tree = nx.dfs_tree(nxgraph, '0')
    if set(tree.nodes()) != set(nxgraph.nodes()):
        raise ValueError("Graph %s does not have a spanning tree from the virtual start node!" % nxgraph.name)
    for n in nxgraph.nodes():
        outstar = nxgraph.out_edges(n, keys=True, data=True)
        labels = [(data['edgelabel'], data['traversaltype']) for _, _, _, data in outstar]
        if len(set(labels)) != len(labels):
            message = "\n".join(
                [" / ".join([data['edgelabel'], data['traversaltype'], data['firstpath']]) for _, _, _, data in outstar
                 if (data['edgelabel'], data['traversaltype']) in labels])
            raise ValueError("The list of out-labels of node %s contains duplicates: \n %s" % (n, message))


def is_isomorphic_DEG(nxgraph_A, nxgraph_B, skip_copy=False):
    if not skip_copy:
        nxgraph_A, nxgraph_B = nxgraph_A.copy(), nxgraph_B.copy()

    # Only allow wellformed DEGs to be processed
    if not is_wellformed_DEG(nxgraph_A) or not is_wellformed_DEG(nxgraph_B):
        return False  # not a DEG -> can't be DEG-isomorphic
    # Remove the VEN / VEE. It is irrelevant where in the DOM the crawler started.
    for G in [nxgraph_A, nxgraph_B]:
        ven = [n for n, data in G.nodes(data=True) if data["isVEN"] == "true"][0]
        G.remove_node(ven)  # Also removes V.E.E.

    success = nx.is_isomorphic(nxgraph_A, nxgraph_B, edge_match=_em, node_match=_nm)
    return success


def _em(e1, e2):
    if len(e1) != len(e2):
        # Number of parallel edges differs -> not a match
        return False

    isomorphism_edge_attribute_names = [
        'isBlacklisted', 'isReadable', 'isToStringSuccessful',
        'isSelfEqualTripleEqual', 'isSelfEqualObjectIs',
        'isReferenceSelfEqualObjectIs',
        'isReferenceSelfEqualTripleEqual', 'isDeterministic',
        'isPrimitive',
        'isSealed', 'isFrozen', 'isExtensible', 'isVEE',
        'readErrorMessage', 'toStringErrorMessage']

    vectors = []
    for edge in [e1, e2]:
        vectors.append({
            edge[parallel_edge]['edgelabel']: [
                edge[parallel_edge].get(fieldname, '') for fieldname in isomorphism_edge_attribute_names
            ] for parallel_edge in edge
        })
    return vectors[0] == vectors[1]


def _nm(n1, n2):
    strings_to_be_replaced = [
        'hd_so_edextraction', 'hd_so_hdextraction',
        'ed_extraction', 'ed_blank',
        'var CONFIG_CRAWLER_ENABLED = false;',
        'var CONFIG_CRAWLER_ENABLED = true;']

    match = True
    match &= n1['nodetype'] == n2['nodetype']
    match &= n1['isVEN'] == n2['isVEN']
    if match:
        nodetype = n1['nodetype']
        v1, v2 = n1.get('nodevalue', ''), n2.get('nodevalue', '')
        if nodetype in ['string', 'object']:
            v1 = requests.utils.unquote(v1).decode('utf8')
            v2 = requests.utils.unquote(v2).decode('utf8')
            for replace_string in strings_to_be_replaced:
                v1 = v1.replace(replace_string, 'REPLACED')
                v2 = v2.replace(replace_string, 'REPLACED')
            match &= v1 == v2
        elif nodetype == 'number':
            v1f, v2f = float(v1), float(v2)
            if v1 == v2:
                match = True
            else:
                match &= v1f > 1000000000 and v2f > 1000000000
        else:
            match &= v1 == v2
    return match


def bfs_tree_subtraction(graphs, roots=None):
    graphs = [g.copy() for g in graphs]
    bfs_tree_subtraction_inplace(graphs, roots=None)
    return graphs


def bfs_tree_subtraction_inplace(graphs, roots=None, edge_match_attributes=["edgelabel"],
                                 node_match_attributes=["nodevalue", "nodetype"], continue_after_divergence=False):
    if not roots:
        roots = [getVEN(g) for g in graphs]

    assert (type(graphs) == type(roots) == list)
    assert (len(graphs) == len(roots))

    current_position = roots
    current_path = ""
    queue = deque()
    visited_positions = set()
    divergence_roots = []

    while current_position:

        # the neighborhoods, the "out-stars", for the current positions in all graphs.
        outstars = [list(g.out_edges(n, keys=True)) for g, n in zip(graphs, current_position)]

        # union the labels of the edges in alll out-stars
        all_edgelabels = set([k for outstar in outstars for u, v, k in outstar])
        for current_edgelabel in all_edgelabels:

            # for all target nodes, mark the last common accessor path
            if current_position == roots:
                new_path = ""
            else:
                new_path = current_path + "." + str(current_edgelabel) if current_path else str(current_edgelabel)

            edge_matches = [[edge for edge in outstar if edge[2] == current_edgelabel] for outstar in outstars]
            if not all(edge_matches):
                divergence_roots.append({
                    "path": new_path,
                    "type": "property existence"
                })
            else:
                edge_matches = [m[0] for m in edge_matches]
                target_nodevalue_of_edge_matches = [
                    tuple(g.nodes[v].get(attrname, '') for attrname in node_match_attributes)
                    for g, (u, v, k) in zip(graphs, edge_matches)
                ]
                for g, (u, v, k), n in zip(graphs, edge_matches, target_nodevalue_of_edge_matches):
                    g.nodes[v]['nodevalue'] = n

                traversed_edges = [g[u][v][k] for g, (u, v, k) in zip(graphs, edge_matches)]
                traversed_edge_attributes = [
                    tuple(e.get(attrname) for attrname in edge_match_attributes)
                    for e in traversed_edges
                ]
                if len(set(traversed_edge_attributes)) != 1:
                    divergence_roots.append({
                        "path": new_path,
                        "type": "edge attribute value",
                        "divergence_data": traversed_edge_attributes
                    })
                else:
                    queue.append(([v for u, v, k in edge_matches], new_path))
                    visited_positions.update(edge_matches)
                    continue_after_divergence = False

        if queue:
            current_position, current_path = queue.popleft()
        else:
            current_position = None

    return graphs


def getVEN(nxgraph):
    for n, data in nxgraph.nodes(data=True):
        if data.get('isVEN', 'false') == 'true':
            return n
    raise ValueError("VEN node not found")


def diff(graphs, exclude_path_keywords=None, include_path_keywords=None, exclude_node_labels=None,
         include_node_labels=None, output_directory="/tmp", report_filename="diff.json", ):
    import json
    import os
    from itertools import chain
    from collections import defaultdict

    output_directory = os.path.join(output_directory, '')
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    graphs = [g.copy() for g in graphs]

    exclude_path_keywords = exclude_path_keywords if exclude_path_keywords else []
    include_path_keywords = include_path_keywords if include_path_keywords else []
    exclude_node_labels = exclude_node_labels if exclude_node_labels else []
    include_node_labels = include_node_labels if include_node_labels else []

    roots = [getVEN(g) for g in graphs]

    diff = defaultdict(dict)
    all_path_counts = defaultdict(int)
    for g in graphs:
        bfs_tree_subtraction_inplace([g], roots=[getVEN(g)])

    filtered_subgraphs = []
    filtered_divergence_roots = []
    filtered_path_counts = defaultdict(int)
    for root, graph in zip(roots, graphs):
        divergence_root_set = set()
        subgraph_nodes = set()
        for path, divergence_type in chain(graph.graph['bfs_tree_divergence_roots'].items(),
                                           graph.graph['bfs_tree_divergence_roots_dominated_by'].items()):
            path = urldecode(path)
            include = all([k in path for k in include_path_keywords]) if include_path_keywords else True
            exclude = any([k in path for k in exclude_path_keywords])
            if include and not exclude:
                divergence_root_set.add(path)
                filtered_divergence_roots.append((path, divergence_type))
                for n in nx.dfs_tree(graph, root):
                    subgraph_nodes.add(n)
                    filtered_path_counts[path] += 1
        subgraph = graph.subgraph(subgraph_nodes)
        filtered_subgraphs.append(subgraph)

    filtered_diff_graph = nx.union_all(filtered_subgraphs)
    filtered_diff_graph.graph['divergence_roots'] = filtered_divergence_roots
    filtered_diff_graph.graph['path_counts'] = dict(filtered_path_counts)

    nx.write_gml(filtered_diff_graph, os.path.join(output_directory, "diff_graph.gml"))
    if report_filename:
        with open(os.path.join(output_directory, report_filename), "w") as f:
            json.dump(filtered_diff_graph.graph, f, indent=2)

    return filtered_diff_graph


def split_dompath_into_labels(path):
    return path.split('.')


def labelpath_to_graphcomponents(path, graph, return_node=False):
    labels = split_dompath_into_labels(path)
    current = getVEN(graph)
    for label in labels:
        outstar = graph.out_edges(current, data=True)
        candidates = [v for u, v, data in outstar if data['edgelabel'] == label]
        if not candidates:
            raise ValueError("Path '%s' not found in graph %s" % (path, graph.name))
        if len(candidates) > 1:
            raise ValueError("Path '%s' is ambiguous in graph %s" % (path, graph.name))
        current = candidates[0]
    return current if return_node else (current, labels[-1])


def walk_path(graph, path):
    labels = split_dompath_into_labels(path)
    current_node = getVEN(graph)
    for label in labels:
        out_edges = list(graph.out_edges(current_node, data=True))
        next_node = None
        for u, v, data in out_edges:
            if data['edgelabel'] == label:
                next_node = v
                break
        if next_node is None:
            raise ValueError(f"Path {path} not found in the graph.")
        current_node = next_node
    return current_node


def autocomplete(graph, prefix):
    labels = split_dompath_into_labels(prefix)
    current_node = getVEN(graph)
    for label in labels:
        out_edges = list(graph.out_edges(current_node, data=True))
        next_node = None
        for u, v, data in out_edges:
            if data['edgelabel'] == label:
                next_node = v
                break
        if next_node is None:
            return []  # No completions available
        current_node = next_node

    out_edges = list(graph.out_edges(current_node, data=True))
    completions = [data['edgelabel'] for u, v, data in out_edges]
    return completions


class AbstractGraphBuilder(object):

    def __init__(self, *args, **kwargs):
        super(AbstractGraphBuilder, self).__init__()

    def add_nodes(self, *args, **kwargs):
        raise NotImplementedError("This method should be implemented by subclasses.")

    def add_edges(self, *args, **kwargs):
        raise NotImplementedError("This method should be implemented by subclasses.")

    def build_graph(self, *args, **kwargs):
        raise NotImplementedError("This method should be implemented by subclasses.")


class JSONNetworkXGraphBuilder(AbstractGraphBuilder):

    def __init__(self):
        super(JSONNetworkXGraphBuilder, self).__init__()

    def add_nodes(self, graph, nodes):
        for node in nodes:
            graph.add_node(node['id'], **node['properties'])

    def add_edges(self, graph, edges):
        for edge in edges:
            graph.add_edge(edge['source'], edge['target'], **edge['properties'])

    def build_graph(self, fragmented_jsons):
        graph = nx.MultiDiGraph()
        for fragment in fragmented_jsons:
            self.add_nodes(graph, fragment['nodes'])
            self.add_edges(graph, fragment['edges'])
        return graph


class JSONNeo4JGraphBuilder(AbstractGraphBuilder):

    def __init__(self, neo4j_driver):
        super(JSONNeo4JGraphBuilder, self).__init__()
        self.neo4j_driver = neo4j_driver

    def add_nodes(self, graph, nodes):
        with self.neo4j_driver.session() as session:
            for node in nodes:
                session.run("CREATE (n {id: $id, properties: $properties})", id=node['id'],
                            properties=node['properties'])

    def add_edges(self, graph, edges):
        with self.neo4j_driver.session() as session:
            for edge in edges:
                session.run("MATCH (a {id: $source}), (b {id: $target}) CREATE (a)-[r {properties: $properties}]->(b)",
                            source=edge['source'], target=edge['target'], properties=edge['properties'])

    def build_graph(self, fragmented_jsons):
        graph = None
        for fragment in fragmented_jsons:
            self.add_nodes(graph, fragment['nodes'])
            self.add_edges(graph, fragment['edges'])
        return graph


def process_fragmented_jsons(fragmented_jsons, builder_class):
    builder = builder_class()
    return builder.build_graph(fragmented_jsons)

def save_graph_to_neo4j(graph, neo4j_driver):
    builder = JSONNeo4JGraphBuilder(neo4j_driver)
    fragmented_jsons = [{
        'nodes': [{'id': n, 'properties': graph.nodes[n]} for n in graph.nodes()],
        'edges': [{'source': u, 'target': v, 'properties': data} for u, v, data in graph.edges(data=True)]
    }]
    builder.build_graph(fragmented_jsons)
