import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
import sys

def analyze_graphml(filepath):
    node_types = Counter()
    edge_types = Counter()
    node_degree = defaultdict(int)

    context = ET.iterparse(filepath, events=('start', 'end'))
    _, root = next(context)

    in_node = False
    in_edge = False
    current_node_id = None
    current_node_type = None
    current_edge_source = None
    current_edge_target = None
    current_edge_type = None

    for event, elem in context:
        if event == 'start':
            if elem.tag.endswith('node'):
                in_node = True
                current_node_id = elem.get('id')
                labels_attr = elem.get('labels')
                if labels_attr:
                    current_node_type = labels_attr.lstrip(':')
                else:
                    current_node_type = 'Unknown'
            elif elem.tag.endswith('edge'):
                in_edge = True
                current_edge_source = elem.get('source')
                current_edge_target = elem.get('target')
                current_edge_type = elem.get('label')

        elif event == 'end':
            if elem.tag.endswith('node'):
                node_types[current_node_type] += 1
                in_node = False
                elem.clear()
            elif elem.tag.endswith('edge'):
                if current_edge_type:
                    edge_types[current_edge_type] += 1
                if current_edge_source:
                    node_degree[current_edge_source] += 1
                if current_edge_target:
                    node_degree[current_edge_target] += 1
                in_edge = False
                elem.clear()

            if len(root) > 0 and root[0].tag.endswith(('node', 'edge')):
                root.clear()

    print(f"Tipi di nodo ({len(node_types)}):")
    for t, cnt in node_types.most_common():
        print(f"  {t}: {cnt}")
    print(f"\nTipi di relazione ({len(edge_types)}):")
    for t, cnt in edge_types.most_common():
        print(f"  {t}: {cnt}")
    print(f"\nGrado dei nodi:")
    if node_degree:
        degrees = list(node_degree.values())
        print(f"  Min: {min(degrees)}")
        print(f"  Max: {max(degrees)}")
        print(f"  Media: {sum(degrees)/len(degrees):.2f}")
        print(f"  Mediana: {sorted(degrees)[len(degrees)//2]}")
    else:
        print("Nessun grado registrato.")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f"Uso: {sys.argv[0]} <file.graphml>")
        sys.exit(1)
    analyze_graphml(sys.argv[1])