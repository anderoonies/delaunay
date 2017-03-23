from random import uniform
import itertools
import math
import numpy as np
from cmath import *

from draw import draw_triangle, draw_edges, draw_edge, draw_vertices, draw_vertex, draw_circle, clear_window

WIDTH = 200
HEIGHT = 200
N_POINTS = 10

class Vertex(object):
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def __repr__(self):
        return "<{}, {}>".format(self.x, self.y)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.x == other.x and self.y == other.y
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.x) * hash(self.y)

    def as_list(self):
        return [self.x, self.y]

class Edge(object):
    def __init__(self, p, q):
        self.p = p
        self.q = q

    def __repr__(self):
        return "{} -> {}".format(self.p, self.q)
    
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return ((self.p == other.p and self.q == other.q) or
                    (self.q == other.p and self.p == other.q))
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.p) * hash(self.q)

    def as_list(self):
        return [self.p.as_list(), self.q.as_list()]

    def vector(self):
        return [self.q.x - self.p.x, self.q.y - self.p.y]

def random_vertices():
    return [Vertex(uniform(0, WIDTH), uniform(0, HEIGHT)) for i in range(N_POINTS)]

def sort_vertices(vertices):
    # sort on x
    return sorted(vertices, key = lambda vertex: vertex.x)

def delaunay(vertices, edges = set()):
    # recursively creates the edge set
    if len(vertices) <= 3:
        # create a triangle from these vertices
        edges.update(triangulate(vertices))
        draw_edges(edges)
        return vertices, edges
    else:
        # split the vertices into halves
        l_verts = vertices[0:len(vertices)/2]
        draw_vertices(l_verts, 'red')
        r_verts = vertices[len(vertices)/2:]
        draw_vertices(r_verts, 'blue')
        l, l_edges = delaunay(l_verts, set(edges))
        r, r_edges = delaunay(r_verts, set(edges))
        merged_edges = merge_triangles(l, r, l_edges, r_edges)
        return vertices, merged_edges

def triangulate(vertices):
    shape_edges = edges(vertices) 
    return shape_edges

def edges(vertices):
    # given a pair or triple of vertices, get the edges that fully connect them
    edges = set()
    if len(vertices) == 3:
        a = vertices[0]
        b = vertices[1]
        c = vertices[2]
        edges.update([Edge(a, b), Edge(b, c), Edge(a, c)])
    elif len(vertices) == 2:
        a = vertices[0]
        b = vertices[1]
        edges.update([Edge(a, b)])
    else:
        print "should not be making edges for non-lines/triangles"

    return edges

def merge_triangles(l, r, l_edges, r_edges):
    # sort low to high
    merged_edges = set()
    l_set = sorted(l, key = lambda vertex: vertex.y)
    r_set = sorted(r, key = lambda vertex: vertex.y)
    l_anchor = l_set[0]
    r_anchor = r_set[0]
    base_lr = Edge(l_anchor, r_anchor)
    merged_edges.add(base_lr)
    l_candidates = get_left_candidates(l_anchor, r_anchor, l_edges)
    r_candidates = get_right_candidates(l_anchor, r_anchor, r_edges)
    draw_vertex(l_anchor, 'green')
    draw_vertex(r_anchor, 'green')
    lr = None
    draw_edge(base_lr, 'green')
    l_candidate = 1
    r_candidate = 1

    while (r_candidates or l_candidates):
        l_candidate = None
        r_candidate = None
        while len(r_candidates):
            r_candidate = r_candidates.pop(0)
            if candidate_theta(base_lr, Edge(r_anchor, r_candidate)) < 180:
                next_r_candidate = r_candidates[0] if len(r_candidates) > 0 else None
                circum_center, circum_radius = get_circumcircle(l_anchor, r_anchor, r_candidate)
                if contains(circum_center, circum_radius, next_r_candidate):
                    draw_edge(Edge(r_candidate, r_anchor), 'white')
                    r_edges.remove(Edge(r_candidate, r_anchor))
                else:
                    break

        while len(l_candidates):
            l_candidate = l_candidates.pop(0)
            if candidate_theta(Edge(r_anchor, l_anchor), Edge(l_anchor, l_candidate)) < 180:
                next_l_candidate = l_candidates[0] if len(l_candidates) > 0 else None
                circum_center, circum_radius = get_circumcircle(l_anchor, r_anchor, l_candidate)
                if contains(circum_center, circum_radius, next_l_candidate):
                    draw_edge(Edge(l_candidate, l_anchor), 'white')
                    l_edges.remove(Edge(l_candidate, l_anchor))
                else:
                    break

        if l_candidate and r_candidate:
           circum_center, circum_radius = get_circumcircle(l_anchor, r_anchor, r_candidate)
           if not contains(circum_center, circum_radius, l_candidate):
               lr = Edge(l_anchor, r_candidate)
               l_candidates.insert(0, l_candidate)
               r_anchor = r_candidate
               r_candidate = None
           else:
               circum_center, circum_radius = get_circumcircle(l_anchor, r_anchor, l_candidate)
               if not contains(circum_center, circum_radius, r_candidate):
                   lr = Edge(r_anchor, l_candidate)
                   r_candidates.insert(0, r_candidate)
                   l_anchor = l_candidate
                   l_candidate = None
        elif l_candidate:
            lr = Edge(r_anchor, l_candidate)
            l_anchor = l_candidate
            l_candidate = None
        elif r_candidate:
            lr = Edge(l_anchor, r_candidate)
            r_anchor = r_candidate
            r_candidate = None
        else:
            break

        if lr:
            merged_edges.add(lr)
            l_candidates = get_left_candidates(l_anchor, r_anchor, l_edges)
            r_candidates = get_right_candidates(l_anchor, r_anchor, r_edges)
            draw_edge(lr, 'red')

    merged_edges = merged_edges.union(l_edges.union(r_edges))
    return merged_edges

def get_edges(pt, edge_set):
    # get edges connected to point
    return set(filter(lambda edge: (edge.p == pt or edge.q == pt), edge_set))

def get_neighbors(pt, edge_set):
    neighbors = set()
    for edge in edge_set:
        if edge.p == pt:
            neighbors.add(edge.q)
        elif edge.q == pt:
            neighbors.add(edge.p)
    return neighbors

def get_left_candidates(l_anchor, r_anchor, l_edges):
    base_lr = Edge(r_anchor, l_anchor)
    candidates = sorted(get_neighbors(l_anchor, l_edges),
        key = lambda n: candidate_theta(base_lr, Edge(l_anchor, n)))
    candidates = filter(lambda c: c.y > l_anchor.y, candidates)
    return candidates

def get_right_candidates(l_anchor, r_anchor, r_edges):
    base_lr = Edge(l_anchor, r_anchor)
    candidates = sorted(get_neighbors(r_anchor, r_edges),
        key = lambda n: candidate_theta(base_lr, Edge(r_anchor, n)))
    candidates = filter(lambda c: c.y > r_anchor.y, candidates)
    return candidates

def candidate_theta(baseline, candidate_line):
    theta = 180 - angle_between(baseline, candidate_line)
    return theta

def unit_vector(vector):
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
    v1_u = unit_vector(v1.vector())
    v2_u = unit_vector(v2.vector())
    return np.degrees(np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0)))

def get_circumcircle(a, b, c):
    x = complex(a.x, a.y)
    y = complex(b.x, b.y)
    z = complex(c.x, c.y)
    w = z - x
    w /= y - x

    center = (x-y)*(w-abs(w)**2)/2j/w.imag-x
    return Vertex(-round(center.real, 2), -round(center.imag, 2)), abs(center + x)

def contains(center, radius, point):
    if not point:
        return False
    return (pow((point.x - center.x), 2) + 
            pow((point.y - center.y), 2) < pow(radius, 2))

def intersects(e1, e2):
    # check if two edges intersect
    def on_segment(p, q, r):
        if (q.x <= max(p.x, r.x) and q.x >= min(p.x, r.x) and
                q.y <= max(p.y, r.y) and q.y >= min(p.y, r.y)):
           return True
        return False
    
    def orientation(p, q, r):
        val = ((q.y - p.y) * (r.x - q.x) - 
                   (q.x - p.x) * (r.y - q.y))
 
        if (val == 0): return 0 # colinear
 
        return 1 if val > 0 else 2

    o1 = orientation(e1.p, e1.q, e2.p)
    o2 = orientation(e1.p, e1.q, e2.q)
    o3 = orientation(e2.p, e2.q, e1.p)
    o4 = orientation(e2.p, e2.q, e1.q)

    if (o1 != o2 and o3 != o4):
        return True
    elif (o1 == 0 and on_segment(e1.p, e2.p, e1.q)):
        return True
    elif (o2 == 0 and on_segment(e1.p, e2.p, e1.q)):
        return True
    elif (o3 == 0 and on_segment(e2.p, e1.p, e2.q)):
        return True
    elif (o4 == 0 and on_segment(e2.p, e1.q, e2.q)):
        return True
    else:
        return False

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return itertools.izip(a, b)

if __name__ == '__main__':
    vertices = sort_vertices(random_vertices())
    # vertices = sort_vertices([Vertex(0, 150), Vertex(30, 200), Vertex(30, 100), Vertex(30, 50),
    #                           Vertex(60, 150), Vertex(90, 50), Vertex(120, 100), Vertex(125, 200),
    #                           Vertex(150, 150), Vertex(150, 50)])
    draw_vertices(vertices, 'black')
    verts, edges = delaunay(vertices, set())
    clear_window()
    draw_edges(edges)
    draw_vertices(verts, 'black')
    raw_input("waitin fo ru")
