from math import sqrt
from polyhedron import Polyhedron

def create_cube():
    faces = [
        [[-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1]],
        [[-1, -1,  1], [-1, 1,  1], [1, 1,  1], [1, -1, 1]],
        [[-1, -1, -1], [-1, -1, 1], [1, -1, 1], [1, -1, -1]],
        [[-1,  1, -1], [1,  1, -1], [1,  1, 1], [-1,  1, 1]],
        [[-1, -1, -1], [-1, 1, -1], [-1, 1, 1], [-1, -1, 1]],
        [[1, -1, -1], [1, -1, 1], [1, 1, 1], [1, 1, -1]],
            ]
    return Polyhedron(faces)

def create_dodecahedron():
    PHI = (1 + sqrt(5)) / 2

    dodec_vertices = [
        [-1, -1, -1], [1, -1, -1], [-1, 1, -1], [1, 1, -1],
        [-1, -1, 1],  [1, -1, 1],  [-1, 1, 1],  [1, 1, 1],
        [0, -1/PHI, -PHI], [0, 1/PHI, -PHI],
        [0, -1/PHI, PHI],  [0, 1/PHI, PHI],
        [-1/PHI, -PHI, 0], [1/PHI, -PHI, 0],
        [-1/PHI, PHI, 0],  [1/PHI, PHI, 0],
        [-PHI, 0, -1/PHI], [-PHI, 0, 1/PHI],
        [PHI, 0, -1/PHI],  [PHI, 0, 1/PHI],
    ]

    dodec_faces = [
        [0, 8, 9, 2, 16],
        [0, 16, 17, 4, 12],
        [0, 12, 13, 1, 8],
        [1, 8, 9, 3, 18],
        [1, 18, 19, 5, 13],
        [2, 14, 15, 3, 9],
        [2, 16, 17, 6, 14],
        [3, 15, 7, 19, 18],
        [4, 10, 11, 6, 17],
        [4, 12, 13, 5, 10],
        [5, 10, 11, 7, 19],
        [6, 14, 15, 7, 11],
    ]

    mapped_faces = [[dodec_vertices[v] for v in face] for face in dodec_faces]

    return Polyhedron(mapped_faces)

base_shapes = {
    'C': create_cube,
    'D': create_dodecahedron,
}

def kis(poly): return poly.kis()
def dual(poly): return poly.dual()

operations = {
    'k': kis,
    'd': dual,
}

