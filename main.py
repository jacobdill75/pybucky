import sys
from view import View
from controller import Controller
from base_shapes import *

def parse_input():
    if len(sys.argv) < 2:
        print("Usage: python main.py <operations><shape>")
        print("Example: python main.py kdC")
        sys.exit(1)

    notation = sys.argv[1]
    shape_key = notation[-1].upper()
    ops = notation[:-1].lower()

    if shape_key not in base_shapes:
        print(f"Unknown shape: {shape_key}")
        sys.exit(1)

    poly = base_shapes[shape_key]()

    for op in ops:
        if op not in operations:
            print(f"Unknown operation: {op}")
            sys.exit(1)
        poly = operations[op](poly)
    
    if len(sys.argv) > 2 and sys.argv[2] == "-f":
        print(f"Resolution {len(ops) // 2} face Count: {len(poly.faces)}")

    return poly

def main():
    poly = parse_input()
    controller = Controller()
    view = View(controller)

    while not view.should_close() and not controller.should_exit:
        view.render_polyhedron(poly)
        view.update()

    view.terminate()

if __name__ == "__main__":
    main()

