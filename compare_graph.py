import matplotlib
import networkx as nx
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')
def compare_graphs(graph1, graph2):
    # 检查两个图是否同构
    isomorphic = nx.is_isomorphic(graph1, graph2)

    if isomorphic:
        print("Graphs are isomorphic.")
    else:
        print("Graphs are not isomorphic.")

    # 找出差异
    if not isomorphic:
        # 比较节点
        print("Nodes:")
        for node1, node2 in zip(graph1.nodes(), graph2.nodes()):
            if node1 != node2:
                print(f"Difference in node attributes: {node1} - {node2}")

        # 比较边
        print("Edges:")
        for edge1, edge2 in zip(graph1.edges(), graph2.edges()):
            if edge1 != edge2:
                print(f"Difference in edge attributes: {edge1} - {edge2}")

        # 比较连接组件
        print("Connected components:")
        cc1 = nx.connected_components(graph1)
        cc2 = nx.connected_components(graph2)
        for cc1_component, cc2_component in zip(cc1, cc2):
            if cc1_component != cc2_component:
                print(f"Difference in connected components: {cc1_component} - {cc2_component}")

# 示例用法
# 创建两个图
graph1 = nx.Graph()
graph1.add_edges_from([(1, 2), (2, 3)])
print(graph1)
# nx.draw(graph1, with_labels=True) # 画图
# plt.axis('on')
# plt.xticks([])
# plt.yticks([])
# plt.show() #

graph2 = nx.Graph()
graph2.add_edges_from([(1, 2), (3, 4)])
print(graph2)
nx.draw(graph2, with_labels=True) # 画图
plt.axis('on')
plt.xticks([])
plt.yticks([])
plt.show() #
# 比较图
compare_graphs(graph1, graph2)
