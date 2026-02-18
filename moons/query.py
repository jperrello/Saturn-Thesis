import json, sys

with open("moons/graph.json") as f:
    g = json.load(f)

nodes = {n["id"]: n for n in g["nodes"]}
cmd = sys.argv[1] if len(sys.argv) > 1 else "help"

if cmd == "node":
    nid = sys.argv[2]
    n = nodes.get(nid)
    if n:
        print(json.dumps(n, indent=2))
    else:
        print(f"not found: {nid}")

elif cmd == "type":
    t = sys.argv[2]
    for n in g["nodes"]:
        if n["type"] == t:
            print(f"  {n['id']}: {n['desc']}")

elif cmd == "edges-to":
    target = sys.argv[2]
    for n in g["nodes"]:
        for e in n.get("edges", []):
            if e["to"] == target:
                print(f"  {n['id']} --{e['rel']}--> {target}")

elif cmd == "edges-from":
    nid = sys.argv[2]
    n = nodes.get(nid)
    if n:
        for e in n.get("edges", []):
            print(f"  {nid} --{e['rel']}--> {e['to']}")

elif cmd == "types":
    from collections import Counter
    c = Counter(n["type"] for n in g["nodes"])
    for t, count in c.most_common():
        print(f"  {t}: {count}")

elif cmd == "search":
    q = sys.argv[2].lower()
    for n in g["nodes"]:
        if q in n["id"].lower() or q in n["desc"].lower():
            print(f"  {n['id']} ({n['type']}): {n['desc']}")

else:
    print("usage: python moons/query.py <cmd> [arg]")
    print("  node <id>       - show full node")
    print("  type <type>     - list nodes of type")
    print("  edges-to <id>   - find all edges pointing to node")
    print("  edges-from <id> - find all edges from node")
    print("  types           - count nodes by type")
    print("  search <text>   - search ids and descriptions")
