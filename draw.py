from graphics import *
win = GraphWin()

def draw_triangle(vertices):
    points = [Point(vertex[0], vertex[1]) for vertex in vertices]
    triangle = Polygon(points)
    triangle.setFill('gray')
    triangle.setOutline('cyan')
    triangle.setWidth(4) 
    triangle.draw(win) 

def draw_vertex(vertex, color):
    pt = Point(vertex.x, vertex.y)
    pt.setFill(color)
    pt.draw(win)

def draw_vertices(vertices, color):
    for vertex in vertices:
        pt = Point(vertex.x, vertex.y)
        pt.setFill(color)
        pt.draw(win)

def draw_edges(edge_set, color = 'black'):
    for edge in edge_set:
        draw_edge(edge, color)

def draw_edge(line, color = 'black'):
    pt1 = Point(line.p.x, line.p.y)
    pt2 = Point(line.q.x, line.q.y)
    line = Line(pt1, pt2)
    line.setFill(color)
    line.setWidth(1)
    line.draw(win)

def draw_circle(vertex, radius, color = 'black'):
    pt = Point(vertex.x, vertex.y)
    cir = Circle(pt, radius)
    cir.setWidth(1)
    cir.draw(win)

def clear_window():
    global win
    win.close()
    win = GraphWin()
