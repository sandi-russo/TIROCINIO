import xml.etree.ElementTree as ET, csv, random, os, tracemalloc

INPUT_FILE    = "data/raw/PharMeBiNet_finished.graphml"
OUTPUT_BASE   = "data/sampled"
SCALES        = [25, 50, 75, 100]
RANDOM_SEED   = 42
MAX_EDGES_100 = 6_611_711
MAX_NODES_100 = 2_428_718


def local_name(elem):
    return elem.tag.split('}')[-1]


def phase1_sample_edges():
    random.seed(RANDOM_SEED)

    writers        = {}
    files          = {}
    selected_nodes = {s: set() for s in SCALES}
    edge_count     = {s: 0 for s in SCALES}

    for s in SCALES:
        d = os.path.join(OUTPUT_BASE, f"scale_{s}")
        os.makedirs(d, exist_ok=True)
        f = open(os.path.join(d, "edges.csv"), 'w', newline='', encoding='utf-8')
        w = csv.writer(f)
        w.writerow(['source', 'target', 'label'])
        writers[s] = w
        files[s]   = f

    print("Campionamento archi...")

    context    = ET.iterparse(INPUT_FILE, events=('end',))
    total_read = 0
    done       = False

    for event, elem in context:
        tag = local_name(elem)

        if tag == 'edge':
            if edge_count[100] >= MAX_EDGES_100:
                done = True

            if not done:
                total_read += 1
                src   = elem.get('source')
                tgt   = elem.get('target')
                label = elem.get('label', '')
                r     = random.random()

                for s in SCALES:
                    if r < s / 100.0:
                        writers[s].writerow([src, tgt, label])
                        selected_nodes[s].add(src)
                        selected_nodes[s].add(tgt)
                        edge_count[s] += 1

                if total_read % 500_000 == 0:
                    print(f"  Archi letti: {total_read:,}  |  " + "  ".join(f"{s}%:{edge_count[s]:,}" for s in SCALES))

        elem.clear()

        if done:
            break

    for f in files.values():
        f.close()

    print(f"\nArchi letti in totale: {total_read:,}")
    for s in SCALES:
        print(f"  scale_{s:3d}: {edge_count[s]:>9,} archi | "
              f"{len(selected_nodes[s]):>9,} nodi unici")

    return selected_nodes


def phase2_extract_nodes(selected_nodes_per_scale):
    print("\nEstrazione nodi...")
    writers    = {}
    files      = {}
    node_count = {s: 0 for s in SCALES}

    for s in SCALES:
        d = os.path.join(OUTPUT_BASE, f"scale_{s}")
        f = open(os.path.join(d, "nodes.csv"), 'w', newline='', encoding='utf-8')
        w = csv.writer(f)
        w.writerow(['id', 'label', 'name'])
        writers[s] = w
        files[s]   = f

    context    = ET.iterparse(INPUT_FILE, events=('end',))
    total_read = 0

    for event, elem in context:
        tag = local_name(elem)

        if tag == 'node':
            if node_count[100] >= MAX_NODES_100:
                elem.clear()
                break

            total_read += 1
            node_id = elem.get('id')
            labels  = elem.get('labels', ':Unknown').lstrip(':')
            name    = node_id
            for child in elem:
                if local_name(child) == 'data':
                    if child.get('key') in ('name', 'displayName'):
                        name = child.text or node_id
                        break

            for s in SCALES:
                if node_id in selected_nodes_per_scale[s]:
                    writers[s].writerow([node_id, labels, name])
                    node_count[s] += 1

            if total_read % 500_000 == 0:
                print(f"  Nodi letti: {total_read:,}  |  " + "  ".join(f"{s}%:{node_count[s]:,}" for s in SCALES))

        elem.clear()

    for f in files.values():
        f.close()

    print(f"\nNodi scritti per scala:")
    for s in SCALES:
        print(f"  scale_{s:3d}: {node_count[s]:>9,} nodi")


if __name__ == "__main__":
    if not os.path.exists(INPUT_FILE):
        print(f"Errore: {INPUT_FILE} non trovato!")
        exit(1)

    tracemalloc.start()
    selected = phase1_sample_edges()
    phase2_extract_nodes(selected)
    curr, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"Dataset salvati in {OUTPUT_BASE}/scale_{{25,50,75,100}}/")