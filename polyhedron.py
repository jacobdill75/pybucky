from polygon import Polygon
import numpy as np
from collections import defaultdict

class Polyhedron:
    def __init__(self, face_vertex_lists):
        # face_vertex_lists: list of faces, each a list of 3D points
        self.faces = [Polygon(face) for face in face_vertex_lists]
        self.vertices = self._extract_unique_vertices()
        self.edge_map = self._build_edge_map()  # for manifold test and dual

    def _extract_unique_vertices(self):
        seen = {}
        index = 0
        unique = []
        for poly in self.faces:
            for v in poly.vertices:
                vt = tuple(v)
                if vt not in seen:
                    seen[vt] = index
                    unique.append(v)
                    index += 1
        return unique

    def _build_edge_map(self):
        edge_faces = defaultdict(list)
        for i, face in enumerate(self.faces):
            for start, end in face.edges():
                key = tuple(sorted([tuple(start), tuple(end)]))
                edge_faces[key].append(i)
        return edge_faces

    def is_manifold(self):
        return all(len(faces) == 2 for faces in self.edge_map.values())

    def is_all_faces_convex(self):
        return all(face.is_convex() for face in self.faces)

    def to_gl_lines(self):
        lines = []
        for face in self.faces:
            lines.extend(face.to_gl_lines())
        return np.array(lines, dtype=np.float32)

    def to_line_vertex_buffer(self):
        # Returns a flat list of line segments for GL_LINES
        lines = []
        for face in self.faces:
            verts = face.vertices
            n = len(verts)
            for i in range(n):
                lines.extend(verts[i])
                lines.extend(verts[(i + 1) % n])
        return np.array(lines, dtype=np.float32)

    def to_triangle_vertex_buffer(self):
        # Returns a fanned triangle list for drawing polygons with GL_TRIANGLES
        triangles = []
        for face in self.faces:
            verts = face.vertices
            if len(verts) < 3:
                continue
            for i in range(1, len(verts) - 1):
                triangles.extend(verts[0])
                triangles.extend(verts[i])
                triangles.extend(verts[i + 1])
        return np.array(triangles, dtype=np.float32)

    def kis(self):
        new_faces = []

        for face in self.faces:
            center = np.mean(face.vertices, axis=0)

            # Triangulate by connecting each edge to the center
            n = len(face.vertices)
            for i in range(n):
                v1 = face.vertices[i]
                v2 = face.vertices[(i + 1) % n]
                triangle = [v1, v2, center]
                new_faces.append(triangle)

        return Polyhedron(new_faces)

    def dual(self):
        # Step 1: Compute centroids and normals of all faces
        face_centroids = []
        face_normals = []
        for face in self.faces:
            verts = np.array(face.vertices)
            centroid = np.mean(verts, axis=0)
            normal = np.cross(verts[1] - verts[0], verts[2] - verts[0]).astype(float)
            normal /= np.linalg.norm(normal)
            face_centroids.append(centroid)
            face_normals.append(normal)

        # Step 2: Build vertex → incident face indices map
        vertex_face_map = defaultdict(list)
        for face_idx, face in enumerate(self.faces):
            for v in face.vertices:
                vertex_face_map[tuple(v)].append(face_idx)

        # Step 3: For each vertex, create a face from centroids of incident faces (ordered)
        new_faces = []
        for v_key, face_indices in vertex_face_map.items():
            v = np.array(v_key)

            # Compute average normal (approximate vertex normal)
            avg_normal = np.mean([face_normals[i] for i in face_indices], axis=0)
            avg_normal /= np.linalg.norm(avg_normal)

            # Build local basis for tangent plane
            u = np.cross([0, 0, 1], avg_normal)
            if np.linalg.norm(u) < 1e-6:
                u = np.cross([0, 1, 0], avg_normal)
            u /= np.linalg.norm(u)
            v_axis = np.cross(avg_normal, u)

            # Sort centroids around the vertex in tangent plane
            def sort_key(i):
                vec = face_centroids[i] - v
                x = np.dot(vec, u)
                y = np.dot(vec, v_axis)
                return np.arctan2(y, x)

            sorted_indices = sorted(face_indices, key=sort_key)
            face = [face_centroids[i] for i in sorted_indices]
            new_faces.append(face)

        return Polyhedron(new_faces)
