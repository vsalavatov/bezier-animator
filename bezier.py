import pygame

class Bezier(object):
    def __init__(self, pivots):
        if len(pivots) == 0:
            raise Exception("Bezier curve with no pivots")
        self.pivots = pivots

    def reduce(self, t):
        if self.is_final():
            return Bezier(self.pivots)
        points = []
        for (p1, p2) in zip(self.pivots, self.pivots[1:]):
            vec = (p2[0] - p1[0], p2[1] - p1[1])
            vec = (vec[0] * t, vec[1] * t)
            pt = (int(p1[0] + vec[0]), int(p1[1] + vec[1]))
            points.append(pt)
        return Bezier(points)

    def is_final(self):
        return len(self.pivots) == 1


class BezierCurves(object):
    def __init__(self, filename = None):
        self.pivots_color = (0, 0, 0, 255)
        self.pivots_radius = 5
        self.lines_color = (0, 0, 0, 255)
        self.lines_thickness = 1
        self.point_color = (0, 0, 0, 255)
        self.point_radius = 7

        self.curves = []
        if filename:
            with open(filename, 'r') as src:
                raw_curves = list(filter(None, [x.strip() for x in src.readlines()]))
                for raw_curve in raw_curves:
                    curve = []
                    vals = list(map(int, raw_curve.split()))
                    if len(vals) % 2 == 1:
                        raise Exception("invalid format: " + raw_curve)
                    for i in range(len(vals) // 2):
                        curve.append((vals[2 * i], vals[2 * i + 1]))
                    self.curves.append(Bezier(curve))

    def inherit(self, bc):
        self.pivots_color = bc.pivots_color
        self.pivots_radius = bc.pivots_radius
        self.lines_color = bc.lines_color
        self.lines_thickness = bc.lines_thickness
        self.point_color = bc.point_color
        self.point_radius = bc.point_radius

    def reduce(self, t):
        bc = BezierCurves()
        bc.inherit(self)
        for c in self.curves:
            bc.curves.append(c.reduce(t))
        return bc

    def is_final(self):
        return all([c.is_final() for c in self.curves])

    def draw(self, surface: pygame.Surface, t, draw_pivots=False, draw_lines=False, draw_evolution=False):
        if self.is_final() or draw_evolution:
            if draw_lines:
                for c in self.curves:
                    for (p1, p2) in zip(c.pivots, c.pivots[1:]):
                        pygame.draw.line(surface, self.lines_color, p1, p2, self.lines_thickness)
            if draw_pivots:
                for c in self.curves:
                    for p in c.pivots:
                        pygame.draw.circle(surface, self.pivots_color, p, self.pivots_radius)
        if not self.is_final():
            bc = self.reduce(t)
            bc.draw(surface, t, draw_pivots, draw_lines, draw_evolution)

