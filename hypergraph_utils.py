from random import random, sample, randint, choice
from hypernetx import Hypergraph
from networkx import Graph, is_connected, connected_components


def find_minimal_clique_separators(hg: Hypergraph) -> set[frozenset[str]]:
    try:
        # строим обычный граф для заданного гиперграфа
        # (если пара вершин в гиперграфе смежны, то в обычном графе между ними есть ребро)
        g = hypergraph_to_graph(hg)

        # находим:
        #   1) минимальную триангуляцию этого графа (хордальный граф [одно и то же])
        #   2) minimal elimination ordering
        #   3) вершины, которые образуют минимальные сепараторы
        h, meo, generators = find_minimal_triangulation(g)

        # находим минимальные кликовые сепараторы
        cliques = _find_clique_minimal_separators(g, h, meo, generators)

        return cliques
    except ValueError as e:
        raise ValueError(f"Не удалось найти минимальный кликовый сепаратор: {e}")


def hypergraph_to_graph(hg: Hypergraph) -> Graph:
    """
    У гиперграфа есть матрица смежности вершин, по которой можно построить обычный граф.

    Любая клика обычного графа является кликой гиперграфа.

    @param hg: гиперграф
    @return: граф смежности этого гиперграфа
    """
    g_edges = []
    for edge in hg.edges:
        nodes = hg.edges[edge]
        for i, n1 in enumerate(nodes):
            for j, n2 in enumerate(nodes):
                if i <= j:
                    continue
                g_edges.append((n1, n2))
    g = Graph(g_edges)
    return g


def find_minimal_triangulation(g: Graph) -> tuple[Graph, list[str], list[str]]:
    """
    Реализация алгоритма MCS-M+.

    источник:
    https://hal-lirmm.ccsd.cnrs.fr/lirmm-00485851/document#:~:text=Clique%20minimal%20separator%20decomposition%20is,be%20explained%20in%20detail%20further.

    @param g: связный неправленный граф
    @return:
        1) его минимальная триангуляция (хордальный граф [это одно и то же])
        2) minimal elimination ordering
        3) вершины, которые образуют минимальные сепараторы
    """
    if not is_connected(g):
        raise ValueError("граф несвязный")
    if g.is_directed():
        raise ValueError("граф направленный")

    n = len(g.nodes)

    g_ = Graph(g)  # копия оригинального графа, с которым мы далее работаем
    h = Graph(g)  # хордальный граф, который мы пытаемся построить

    meo = []  # minimal elimination ordering
    generators = []  # вершины, которые образуют минимальные сепараторы

    label = {node: 0 for node in g_.nodes}  # метки вершин
    s = -1

    for i in range(1, n + 1):
        x = max(label.items(), key=lambda p: p[1])[0]  # находим вершину с максимальной меткой
        Y = set(g_.neighbors(x))  # находим соседние вершины этой вершины

        if label[x] <= s:
            generators.append(x)

        s = label[x]

        # помечаем x и всех ее соседей как достигнутые
        reached = {x, *Y}
        reach = {}
        for y in Y:
            if label[y] not in reach:
                reach[label[y]] = set()
            reach[label[y]].add(y)

        for j in range(0, n):
            if j not in reach:
                continue
            while reach[j] != set():
                y = reach[j].pop()  # удаляем вершину

                for z in g_.neighbors(y):
                    if z not in reached:
                        reached.add(z)
                        if label[z] > j:
                            Y.add(z)
                            reach[label[z]].add(z)
                        else:
                            reach[j].add(y)
        for y in Y:
            h.add_edge(x, y)  # добавляем ребро к хордальному графу
            label[y] += 1

        meo.append(x)
        g_.remove_node(x)
        del label[x]

    return h, meo, generators


def is_clique(g: Graph, nodes: set[str]) -> bool:
    """
    @param g: граф
    @param nodes: подмножество его вершин
    @return: является ли это подмножество вершин кликой
    """
    for n1 in nodes:
        for n2 in nodes:
            if n1 == n2:
                continue
            if not g.has_edge(n1, n2):
                return False
    return True


def _find_clique_minimal_separators(
        g: Graph,
        h: Graph,
        meo: list[str],
        generators: list[str]
) -> set[frozenset[str]]:
    """
    источник:
    https://hal-lirmm.ccsd.cnrs.fr/lirmm-00485851/document#:~:text=Clique%20minimal%20separator%20decomposition%20is,be%20explained%20in%20detail%20further.

    @param g: исходный граф
    @param h: его минимальная триангуляция(хордальный граф)
    @param meo: minimal elimination ordering
    @param generators: вершины, которые образуют минимальные сепараторы
    @return: множество всех кликовых минимальных сепараторов
    """
    g_ = Graph(g)  # копия исходного графа
    h_ = Graph(h)  # копия хордального графа
    separators = set()  # сепараторы графа

    for x in meo[::-1]:
        if x in generators:
            separator = set(h_.neighbors(x))

            if is_clique(g, separator):
                if len(separator) == 0:
                    continue
                separators.add(frozenset(separator))

                tmp_g = Graph(g_)
                tmp_g.remove_nodes_from(separator)
                components = [*connected_components(tmp_g)]
                if len(components) == 1:
                    raise RuntimeError("сепаратор не разделяет граф :(")

                for component in components:
                    if x in component:
                        g_.remove_nodes_from(component)
                        component.update(separator)
                        if len(component) == 0:
                            raise RuntimeError
                        break
        h_.remove_node(x)

    return separators


def generate_hypergraph(n: int, k: int) -> Hypergraph:
    """
    :param n: количество вершин
    :param k: количество гиперребер
    :return: случайный гиперграф
    """
    nodes = [
        f"v{i + 1}"
        for i in range(n)
    ]
    edges_labels = [
        f"e{i + 1}"
        for i in range(k)
    ]
    edges = {
        label: sample(nodes, randint(1, _max_nodes(n)))
        for label in edges_labels
    }

    used_nodes = set()
    for edge_nodes in edges.values():
        used_nodes.update(edge_nodes)

    # изолированные вершины нам не нужны, поэтому каждую изолированную вершину
    # необходимо добавить в одно из ребер
    isolated_nodes = set(nodes) - used_nodes
    for isolated_node in isolated_nodes:
        hyperedge = choice(edges_labels)
        edges[hyperedge].append(isolated_node)

    h = Hypergraph()

    # необходимо для того, чтобы вершины в объекте гиперграфа были упорядочены
    # в необходимом для нас порядке
    fix_label = "fix_label"
    h.add_edge(fix_label)
    for node in nodes:
        h.add_node_to_edge(node, fix_label)

    # добавление гиперребер
    for edge, nodes in edges.items():
        h.add_edge(edge)
        for node in nodes:
            h.add_node_to_edge(node, edge)

    # это ребро больше не нужно
    h.remove_edge(fix_label)

    return h


def _max_nodes(n: int) -> int:
    r = random()
    if r < 0.2:
        return n
    elif r < 0.6:
        return int(0.6 * n)
    else:
        return int(0.3 * n)
