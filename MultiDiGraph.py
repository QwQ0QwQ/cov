class MultiDiGraph:
    def __init__(self):
        self.edges = {}
        self.nodes = {}
        self.node_keys_sorted_by_time = []
        self.edge_keys_sorted_by_time = []
        self.metadata = {}
        self.write_blocked = False
        self.number_of_edges = 0
        self.number_of_nodes = 0
        self.is_frozen = False
        self.prevent_unfrozen_iteration = True
        self.node_addition_observers = []
        self.edge_addition_observers = []

    def add_node(self, node_id, node_data=None):
        if self.is_frozen:
            print("Graph is frozen, unable to add node")
            return

        node_data = node_data or {}
        node_data['nodeid'] = node_id
        if node_id not in self.nodes:
            self.number_of_nodes += 1
            self.nodes[node_id] = node_data
            self.node_keys_sorted_by_time.append(node_id)
            for observer in self.node_addition_observers:
                observer(node_id, node_data)
        else:
            print("Node id already exists in the graph!")

    def add_edge(self, source_id, target_id, edge_label, edge_data=None):
        if self.is_frozen:
            print("Graph is frozen, unable to add edge")
            return

        edge_data = edge_data or {}
        prefixed_edge_label = "[graph]:" + str(type(edge_label)) + str(edge_label)
        if source_id not in self.edges:
            self.edges[source_id] = {}
        next_level = self.edges[source_id]

        if target_id not in next_level:
            next_level[target_id] = {}
        next_level = next_level[target_id]

        if prefixed_edge_label not in next_level:
            self.number_of_edges += 1
            edge_data['sourceid'] = source_id
            edge_data['targetid'] = target_id
            next_level[prefixed_edge_label] = edge_data
            self.edge_keys_sorted_by_time.append([source_id, target_id, prefixed_edge_label])
            for observer in self.edge_addition_observers:
                observer(source_id, target_id, prefixed_edge_label, edge_data)
        else:
            print("Duplicate write access on graph[{}][{}][{}] was denied: edge already exists.".format(source_id, target_id, edge_label))

    def remove_edge(self, source, target, key):
        if source in self.edges:
            if target in self.edges[source]:
                if key in self.edges[source][target]:
                    del self.edges[source][target][key]
                if len(self.edges[source][target]) == 0:
                    del self.edges[source][target]
            if len(self.edges[source]) == 0:
                del self.edges[source]

    def iter_nodes(self):
        if not self.is_frozen and self.prevent_unfrozen_iteration:
            print("Do not iterate over non-frozen graph!")
        for node_id in self.node_keys_sorted_by_time:
            yield self.nodes[node_id]

    def iter_edges(self):
        if not self.is_frozen and self.prevent_unfrozen_iteration:
            print("Do not iterate over non-frozen graph!")
        for uvk in self.edge_keys_sorted_by_time:
            u, v, k = uvk
            yield {
                'u': u,
                'v': v,
                'k': k,
                'data': self.edges[u][v][k]
            }

    def freeze(self):
        self.is_frozen = True

    def to_json(self):
        nodes_flat = []
        edges_flat = []
        for uvk in self.edge_keys_sorted_by_time:
            edge = self.edges[uvk[0]][uvk[1]][uvk[2]]
            edge['key'] = edge.get('edgelabel', '')  # 使用 get 方法获取键值，如果不存在则返回空字符串
            edge['source'] = edge['sourceid']
            edge['target'] = edge['targetid']
            edges_flat.append(edge)
        for node_id in self.node_keys_sorted_by_time:
            node = self.nodes[node_id]
            node['name'] = node['nodeid']
            nodes_flat.append(node)
        return {
            'directed': True,
            'multigraph': True,
            'graph_uuid': self.metadata.get('graph_uuid', ''),
            'graph': self.metadata,
            'nodes': nodes_flat,
            'links': edges_flat
        }






