from delaunay import *

def test_intersects():
    e1 = Edge(Vertex(1, 1), Vertex(10, 1))
    e2 = Edge(Vertex(1, 2), Vertex(10, 2))
    assert(intersects(e1, e2) == 0)

    e3 = Edge(Vertex(-5, -5), Vertex(0, 0))
    e4 = Edge(Vertex(1, 1), Vertex(10, 10))
    assert(intersects(e3, e4) == 0)

    e5 = Edge(Vertex(10, 0), Vertex(0, 10))
    e6 = Edge(Vertex(0, 0), Vertex(10, 10))
    assert(intersects(e5, e6) == 1)

def test_contains():
    c1 = Vertex(0, 0)
    r1 = 1
    p1 = Vertex(.5, .5)
    assert(contains(c1, r1, p1) == True)
    
    p2 = Vertex(1, 1)
    assert(contains(c1, r1, p2) == False)

    p3 = Vertex(2, 1)
    assert(contains(c1, r1, p3) == False)

    c1 = Vertex(1, 1)
    r1 = 0.5
    p1 = Vertex(1.1, 1.1)
    assert(contains(c1, r1, p1) == True)

def test_get_circumcircle():
    p1 = Vertex(-1, 0)
    p2 = Vertex(0, 1)
    p3 = Vertex(0, -1)

    assert(get_circumcircle(p1, p2, p3) == (Vertex(0, 0), 1.0))

def test_triangulate():
    p1 = Vertex(0, 0)
    p2 = Vertex(1, 1)
    assert(triangulate([p1, p2]) == set([Edge(p1, p2)]))

    p3 = Vertex(-1, -1)
    assert(triangulate([p1, p2, p3]) == set([Edge(p1, p2), Edge(p2, p3), Edge(p3, p1)]))

def test_edge_equality():
    p1 = Vertex(0, 0)
    p2 = Vertex(1, 0)
    assert(Edge(p1, p2) == Edge(p2, p1))

def test_angle_between():
    p1 = Vertex(0, 0)
    p2 = Vertex(0, 1)
    p3 = Vertex(-1, 0)
    p4 = Vertex(10, 0)
    assert(angle_between(Edge(p1, p2), Edge(p3, p4)) == 90)

def test_candidate_theta():
    l_anchor = Vertex(0, 0)
    r_anchor = Vertex(1, 0)
    candidate = Vertex(1, 1)
    baseline = Edge(l_anchor, r_anchor)
    assert(candidate_theta(baseline, Edge(r_anchor, candidate)) == 90)
    assert(candidate_theta(Edge(r_anchor, l_anchor), Edge(l_anchor, candidate)) == 45)
    l_anchor = Vertex(0, 0)
    r_anchor = Vertex(1, 0)
    candidate = Vertex(1, 1.554131203081)
    assert(candidate_theta(baseline, Edge(r_anchor, candidate)) == 90)

def test_get_edges():
    pt = Vertex(0, 0)
    pt2 = Vertex(10, 10)
    pt3 = Vertex(20, 20)
    pt4 = Vertex(15, 5)
    edges = set([Edge(pt, pt2), Edge(pt2, pt3), Edge(pt, pt3), Edge(pt2, pt4)])
    assert(get_edges(pt2, edges) == set([Edge(pt, pt2), Edge(pt2, pt3), Edge(pt2, pt4)]))
    assert(get_neighbors(pt2, edges) == set([pt, pt3, pt4]))

def run_tests():
    test_contains()
    test_get_circumcircle()
    test_intersects()
    test_triangulate()
    test_edge_equality()
    test_angle_between()
    test_candidate_theta()
    test_get_edges()

if __name__ == '__main__':
    run_tests()
