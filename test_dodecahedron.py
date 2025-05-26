from math import sqrt
from polyhedron import Polyhedron
from base_shapes import *

dodecahedron = create_dodecahedron()
print("Manifold:", dodecahedron.is_manifold())
print("All faces convex:", dodecahedron.is_all_faces_convex())

kis_dodec = dodecahedron.kis()
print("Kis dodecahedron manifold:", kis_dodec.is_manifold())
print("Kis dodecahedron all faces convex:", kis_dodec.is_all_faces_convex())

dual_dodec = dodecahedron.dual()
print("Dual dodec manifold:", dual_dodec.is_manifold())
print("Dual dodec all faces convex:", dual_dodec.is_all_faces_convex())

bucky = dodecahedron.kis().dual()
print("Buckyball manifold:", bucky.is_manifold())
print("Buckyball all faces convex:", bucky.is_all_faces_convex())

dual_dual_dodec = dodecahedron.dual().dual()
print("Dual dual dodec manifold:", dual_dual_dodec.is_manifold())
print("Dual dual dodec all faces convex:", dual_dual_dodec.is_all_faces_convex())
