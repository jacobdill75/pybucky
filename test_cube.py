from polyhedron import Polyhedron
from base_shapes import *

cube = create_cube()
print("Manifold:", cube.is_manifold())
print("All faces convex:", cube.is_all_faces_convex())

kis_cube = cube.kis()
print("Kis cube manifold:", kis_cube.is_manifold())
print("Kis cube all faces convex:", kis_cube.is_all_faces_convex())

dual_cube = cube.dual()
print("Dual cube manifold:", dual_cube.is_manifold())
print("Dual cube all faces convex:", dual_cube.is_all_faces_convex())

dual_kis_cube = cube.kis().dual()
print("dual kis cube manifold:", dual_kis_cube.is_manifold())
print("dual kis cube all faces convex:", dual_kis_cube.is_all_faces_convex())

dual_dual_cube = cube.dual().dual()
print("dual dual cube manifold:", dual_dual_cube.is_manifold())
print("dual dual cube all faces convex:", dual_dual_cube.is_all_faces_convex())
