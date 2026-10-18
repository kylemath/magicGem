"""
gem_geometry.py — exact geometry of Magic Gems.

Conventions (paper): N = n^2, p_ij = (x,y,z) with
    x = j - (n-1)/2,  y = (n-1)/2 - i,  z = s_ij - (N+1)/2.
Internally we use the doubled lattice  P = 2 p  so that all coordinates are
integers; lengths are divided by 2, areas by 4, volumes by 8 at the end.

Provides
    scaled_points(S)            -> (N,3) int array (doubled coordinates)
    exact_hull(S)               -> dict with vertices, faces (exact planes), edges,
                                   f-vector, exact volume (Fraction), area (float);
                                   every hull is certified in exact integer arithmetic
                                   (certify_closure): pairwise distinct facet planes, all points
                                   satisfy all facet inequalities, each facet is the exact 2D hull
                                   of the points on its plane (2-dimensional), every facet edge lies
                                   in exactly two facets, strict convexity at every edge, V - E + F = 2
    bipartite_graph(hull)       -> networkx graph of vertex-facet incidences
    combinatorial_hash(hull)    -> WL hash (first pass)
    congruent(P, Q)             -> exact test: distance-preserving bijection exists
"""
from fractions import Fraction
from math import gcd
from itertools import combinations
import numpy as np
from scipy.spatial import ConvexHull
import networkx as nx


def scaled_points(S):
    S = np.asarray(S, dtype=np.int64)
    n = S.shape[0]
    N = n * n
    pts = []
    for i in range(n):
        for j in range(n):
            pts.append((2 * j - (n - 1), (n - 1) - 2 * i, 2 * int(S[i, j]) - (N + 1)))
    return np.array(pts, dtype=np.int64)


def _plane(p0, p1, p2):
    """Exact integer plane through three integer points: (a,b,c,d) with
    a x + b y + c z + d = 0, primitive, orientation from the cross product."""
    u = p1 - p0
    v = p2 - p0
    nrm = np.array([u[1] * v[2] - u[2] * v[1],
                    u[2] * v[0] - u[0] * v[2],
                    u[0] * v[1] - u[1] * v[0]], dtype=object)
    a, b, c = int(nrm[0]), int(nrm[1]), int(nrm[2])
    g = gcd(gcd(abs(a), abs(b)), abs(c))
    a, b, c = a // g, b // g, c // g
    d = -(a * int(p0[0]) + b * int(p0[1]) + c * int(p0[2]))
    return a, b, c, d


def exact_hull(S):
    P = scaled_points(S)
    N = len(P)
    hull = ConvexHull(P.astype(float))
    # --- exact facet planes, oriented outward (all points have value <= 0) ---
    planes = {}
    for simplex in hull.simplices:
        p0, p1, p2 = P[simplex[0]], P[simplex[1]], P[simplex[2]]
        a, b, c, d = _plane(p0, p1, p2)
        # orientation: evaluate at centroid of all points (interior) -> must be < 0
        val = a * int(P[:, 0].sum()) + b * int(P[:, 1].sum()) + c * int(P[:, 2].sum()) + d * N
        assert val != 0, "degenerate plane through the centroid"
        if val > 0:
            a, b, c, d = -a, -b, -c, -d
        key = (a, b, c, d)
        planes.setdefault(key, set()).update(int(k) for k in simplex)
    # exact incidence: which points lie ON each plane (value == 0); sanity: none > 0
    face_pts = {}
    for key in planes:
        a, b, c, d = key
        vals = a * P[:, 0] + b * P[:, 1] + c * P[:, 2] + d
        assert (vals <= 0).all(), "point strictly outside a hull plane (qhull inconsistency)"
        face_pts[key] = frozenset(int(k) for k in np.nonzero(vals == 0)[0])
    # vertices: points lying on >= 3 facet planes (extreme points of a 3-polytope)
    count = np.zeros(N, dtype=int)
    for pts in face_pts.values():
        for k in pts:
            count[k] += 1
    vertices = sorted(int(k) for k in np.nonzero(count >= 3)[0])
    vset = set(vertices)
    qh_vertices = sorted(int(k) for k in hull.vertices)
    assert vertices == qh_vertices, (vertices, qh_vertices)
    # facets as vertex sets (restrict to extreme points)
    faces = {key: frozenset(k for k in pts if k in vset) for key, pts in face_pts.items()}
    # edges: pairs of vertices sharing >= 2 facets
    edges = set()
    face_list = list(faces.values())
    for u, v in combinations(vertices, 2):
        shared = sum(1 for f in face_list if u in f and v in f)
        if shared >= 2:
            edges.add((u, v))
    V, E, F = len(vertices), len(edges), len(faces)
    assert V - E + F == 2, (V, E, F)
    certify_closure(P, faces, edges)
    # face sizes
    face_sizes = sorted(len(f) for f in face_list)
    # exact volume: signed tetrahedra from the (integer) first vertex over qhull triangles
    ref = P[vertices[0]]
    vol6 = 0
    for simplex in hull.simplices:
        a = P[simplex[0]] - ref
        b = P[simplex[1]] - ref
        c = P[simplex[2]] - ref
        det = (int(a[0]) * (int(b[1]) * int(c[2]) - int(b[2]) * int(c[1]))
               - int(a[1]) * (int(b[0]) * int(c[2]) - int(b[2]) * int(c[0]))
               + int(a[2]) * (int(b[0]) * int(c[1]) - int(b[1]) * int(c[0])))
        vol6 += abs(det)
    volume = Fraction(vol6, 6) / 8  # undo the doubling
    assert abs(float(volume) - hull.volume / 8) <= 1e-9 * max(1.0, float(volume))  # relative: volumes reach 1e7 for n ~ 60
    area = hull.area / 4.0
    return dict(P=P, vertices=vertices, faces=faces, edges=sorted(edges),
                f_vector=(V, E, F), face_sizes=face_sizes,
                volume=volume, area=area)


def _hull2d(pts):
    """Exact 2D convex hull (Andrew's monotone chain, integer cross products) of [(u, v, idx)]:
    the indices of the strict hull vertices in counter-clockwise order (collinear points dropped)."""
    pts = sorted(set(pts))
    if len(pts) < 3:
        return [p[2] for p in pts]
    cross = lambda o, a, b: (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lower, upper = [], []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return [p[2] for p in lower[:-1] + upper[:-1]]


def certify_closure(P, faces, edges):
    """Exact closure certificate (integer arithmetic only), for faces = {outward primitive plane (a,b,c,d): vertex set}:
    (1) the planes are pairwise distinct and every point satisfies every facet inequality;
    (2) each facet is 2-dimensional: the exact 2D convex hull of ALL points on its plane (projected to the coordinate
        plane dropping a coordinate with nonzero normal component) has >= 3 vertices, and these are exactly the facet's
        vertices; its cyclic order gives the facet polygon;
    (3) every polygon edge lies in exactly two facets, and these edges are exactly the edges found from the incidences;
    (4) local strict convexity: at every edge, the vertices of each of the two facets not on the edge satisfy the
        other facet's inequality strictly (so no true facet is split into coplanar pieces).
    Returns the dict edge -> (plane, plane)."""
    from collections import defaultdict
    # a plane has exactly one outward representation with primitive (a,b,c), so distinct keys = distinct planes
    keys = list(faces)
    assert len(set(keys)) == len(keys), "facet planes not pairwise distinct"
    for (a, b, c, d) in keys:
        assert gcd(gcd(abs(a), abs(b)), abs(c)) == 1, "normal not primitive"
    Pi = [tuple(int(t) for t in p) for p in P]
    val = lambda key, p: key[0] * p[0] + key[1] * p[1] + key[2] * p[2] + key[3]
    efaces = defaultdict(list)
    for key, fv in faces.items():
        assert all(val(key, p) <= 0 for p in Pi), "point strictly outside a facet plane"
        on = [k for k, p in enumerate(Pi) if val(key, p) == 0]
        drop = next(i for i in (2, 0, 1) if key[i] != 0)        # coordinate with nonzero normal component
        cyc = _hull2d([tuple(Pi[k][i] for i in range(3) if i != drop) + (k,) for k in on])
        assert len(cyc) >= 3, "facet is not 2-dimensional"
        assert set(cyc) == set(fv), "facet vertices differ from the exact 2D hull of the points on its plane"
        for i in range(len(cyc)):
            efaces[frozenset((cyc[i], cyc[(i + 1) % len(cyc)]))].append(key)
    assert all(len(f) == 2 for f in efaces.values()), "facet edge not in exactly two facets"
    assert sorted(tuple(sorted(e)) for e in efaces) == sorted(tuple(sorted(e)) for e in edges), "edge sets differ"
    for e, (k1, k2) in efaces.items():
        assert k1 != k2
        for ka, kb in ((k1, k2), (k2, k1)):
            assert all(val(kb, Pi[v]) < 0 for v in faces[ka] if v not in e), "not strictly convex at an edge"
    return dict(efaces)


def classify_points(h):
    """Split the points of a gem into (vertices, strictly interior points, non-vertex boundary points), all as index lists.
    A non-vertex point is strictly interior iff it satisfies every facet inequality strictly (exact integer test)."""
    P = h['P']; V = set(h['vertices']); interior, boundary = [], []
    for k in range(len(P)):
        if k in V: continue
        slack = max(a * int(P[k, 0]) + b * int(P[k, 1]) + c * int(P[k, 2]) + d for a, b, c, d in h['faces'])
        assert slack <= 0
        (interior if slack < 0 else boundary).append(k)
    return sorted(V), interior, boundary


def bipartite_graph(h):
    G = nx.Graph()
    for v in h['vertices']:
        G.add_node(('v', v), kind=0)
    for idx, (key, f) in enumerate(h['faces'].items()):
        G.add_node(('f', idx), kind=1)
        for v in f:
            G.add_edge(('v', v), ('f', idx))
    return G


def combinatorial_hash(h, G=None):
    if G is None:
        G = bipartite_graph(h)
    return nx.weisfeiler_lehman_graph_hash(G, node_attr='kind', iterations=4)


def same_combinatorial_type(G1, G2):
    return nx.is_isomorphic(G1, G2, node_match=lambda a, b: a['kind'] == b['kind'])


# ---------------------------------------------------------------- congruence
def sqdist_multiset(P):
    """Sorted list of squared distances between all pairs of points (ints)."""
    P = np.asarray(P, dtype=np.int64)
    d = []
    for i in range(len(P)):
        for j in range(i + 1, len(P)):
            v = P[i] - P[j]
            d.append(int(v @ v))
    return tuple(sorted(d))


def distance_graph(P):
    """Complete graph with squared-distance edge labels."""
    P = np.asarray(P, dtype=np.int64)
    G = nx.Graph()
    G.add_nodes_from(range(len(P)))
    for i in range(len(P)):
        for j in range(i + 1, len(P)):
            v = P[i] - P[j]
            G.add_edge(i, j, w=int(v @ v))
    return G


def congruent(P, Q):
    """Exact congruence test for finite point sets in R^3 (reflections allowed):
    congruent  <=>  there is a bijection preserving all pairwise distances
    (any such bijection extends to an isometry of R^3)."""
    if len(P) != len(Q):
        return False
    if sqdist_multiset(P) != sqdist_multiset(Q):
        return False
    return nx.is_isomorphic(distance_graph(P), distance_graph(Q),
                            edge_match=lambda a, b: a['w'] == b['w'])


def kabsch_check(P, Q):
    """Numerical confirmation: find the best proper/improper rotation after a
    distance-preserving bijection. Returns the RMSD (should be ~0)."""
    GP, GQ = distance_graph(P), distance_graph(Q)
    gm = nx.algorithms.isomorphism.GraphMatcher(GP, GQ, edge_match=lambda a, b: a['w'] == b['w'])
    m = next(gm.isomorphisms_iter())
    A = np.asarray(P, float)
    B = np.asarray([Q[m[i]] for i in range(len(P))], float)
    A0 = A - A.mean(0)
    B0 = B - B.mean(0)
    U, s, Vt = np.linalg.svd(A0.T @ B0)
    R = (U @ Vt).T  # may be a reflection; that's allowed
    return float(np.sqrt(((A0 @ R.T - B0) ** 2).sum(1).mean()))
