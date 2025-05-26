import numpy as np

class HalfEdge:
    def __init__(self, origin, twin=None, next_edge=None):
        self.origin = origin        # np.array([x, y, z])
        self.twin = twin            # HalfEdge
        self.next = next_edge       # HalfEdge

    def end(self):
        return self.next.origin if self.next else None

class Polygon:
    def __init__(self, vertices):
        self.vertices = [np.array(v) for v in vertices]
        self.half_edges = self._build_half_edges()

    def _build_half_edges(self):
        n = len(self.vertices)
        half_edges = []
        for i in range(n):
            he = HalfEdge(self.vertices[i])
            half_edges.append(he)
        for i in range(n):
            half_edges[i].next = half_edges[(i + 1) % n]
        return half_edges

    def edges(self):
        return [(he.origin, he.end()) for he in self.half_edges]

    def to_gl_lines(self):
        lines = []
        for he in self.half_edges:
            lines.append(he.origin.tolist())
            lines.append(he.end().tolist())
        return np.array(lines, dtype=np.float32)

    # ------------------ Validation Tests ------------------

    def is_convex(self):
        # Compute cross products of edge vectors and compare normal directions
        def normal(a, b, c):
            return np.cross(b - a, c - b)

        normals = []
        n = len(self.vertices)
        for i in range(n):
            a, b, c = self.vertices[i], self.vertices[(i + 1) % n], self.vertices[(i + 2) % n]
            nrm = normal(a, b, c)
            if np.linalg.norm(nrm) != 0:
                normals.append(nrm / np.linalg.norm(nrm))

        if not normals:
            return False

        # All normals should point in the same general direction
        ref = normals[0]
        return all(np.dot(ref, nrm) > 0.999 for nrm in normals[1:])

    def has_consistent_winding(self):
        # Assuming convexity, we can compare all triangle normals with the first
        ref_normal = np.cross(self.vertices[1] - self.vertices[0],
                              self.vertices[2] - self.vertices[1])
        for i in range(len(self.vertices)):
            a = self.vertices[i]
            b = self.vertices[(i + 1) % len(self.vertices)]
            c = self.vertices[(i + 2) % len(self.vertices)]
            n = np.cross(b - a, c - b)
            if np.dot(n, ref_normal) < 0:
                return False
        return True

    def is_manifold(self):
        edge_count = {}
        for start, end in self.edges():
            key = tuple(map(tuple, sorted([tuple(start), tuple(end)])))
            edge_count[key] = edge_count.get(key, 0) + 1
        return all(count <= 2 for count in edge_count.values())

