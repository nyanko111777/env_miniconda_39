__title__ = "isoCurves for FreeCAD"
__author__ = "Chris_G"
__license__ = "LGPL 2.1"
__doc__ = '''
import isocurves
single = isocurves.isoCurve(face,'U',0.5)
Part.show(single.toShape())
multi  = isocurves.multiIso(face,10,20)
Part.show(multi.toShape())
'''

from operator import itemgetter
import FreeCAD
from FreeCAD import Base
import Part
from freecad.Curves import _utils


class curve(object):
    '''Base class of nurbs curves'''
    def __init__(self, edge=None):
        if edge is None:
            v1 = FreeCAD.Vector(0, 0, 0)
            v2 = FreeCAD.Vector(1, 0, 0)
            b = Part.BezierCurve()
            b.setPoles([v1, v2])
            self.curve = b
        elif isinstance(edge, Part.Edge):
            c = edge.Curve
            if isinstance(c, (Part.BezierCurve, Part.BSplineCurve)):
                self.curve = c
            else:
                bs = c.toBSpline()
                self.curve = bs
        elif isinstance(edge, (Part.BezierCurve, Part.BSplineCurve)):
            self.curve = edge

    def length(self):
        return self.curve.length()


class curveOnSurface(curve):
    '''defines a curve on a surface'''


class isoCurve:
    '''isoCurve of a surface'''
    def __init__(self, face, direc='U', param=0):
        self.face = None
        self.direction = 'U'
        self.parameter = 0
        if not isinstance(face, Part.Face):
            FreeCAD.Console.PrintMessage("Error. Not a face")
        else:
            self.bounds = face.ParameterRange
            self.face = face
        if direc not in 'UV':
            FreeCAD.Console.PrintMessage("Direction error")
        else:
            self.direction = direc
        if not isinstance(param, (float, int)):
            FreeCAD.Console.PrintMessage("Parameter error")
        else:
            self.parameter = param

    def faceBounds2d(self):
        edges2d = []
        for edge3d in self.face.OuterWire.Edges:
            if edge3d.isSeam(self.face):
                for pc in _utils.get_pcurves(edge3d):
                    if _utils.geom_equal(pc[1], self.face.Surface):
                        edges2d.append((pc[0], pc[-2], pc[-1]))
            else:
                edges2d.append(self.face.curveOnSurface(edge3d))
        return(edges2d)

    def getIntersectionPoints(self, l2d, bounds):
        pts = []
        for c2d in bounds:
            try:
                inter = l2d.intersectCC(c2d[0])
                for pt in inter:
                    pts.append((pt.x, pt.y))
            except RuntimeError:
                pass
        return(pts)

    def toShape(self):
        bounds = self.faceBounds2d()
        prange = [0, 1]
        if self.direction == 'U':
            self.curve = self.face.Surface.uIso(self.parameter)
            v1 = Base.Vector2d(self.parameter, self.bounds[2])
            v2 = Base.Vector2d(self.parameter, self.bounds[3])
            l2d = Part.Geom2d.Line2dSegment(v1, v2)
            pts = self.getIntersectionPoints(l2d, bounds)
            if pts:
                sortedPts = sorted(pts, key=itemgetter(1))
                prange = [l2d.parameter(Base.Vector2d(sortedPts[0][0], sortedPts[0][1])), l2d.parameter(Base.Vector2d(sortedPts[-1][0], sortedPts[-1][1]))]
            else:
                FreeCAD.Console.PrintMessage("No intersection points")
        elif self.direction == 'V':
            self.curve = self.face.Surface.vIso(self.parameter)
            v1 = Base.Vector2d(self.bounds[0], self.parameter)
            v2 = Base.Vector2d(self.bounds[1], self.parameter)
            l2d = Part.Geom2d.Line2dSegment(v1, v2)
            pts = self.getIntersectionPoints(l2d, bounds)
            if pts:
                sortedPts = sorted(pts, key=itemgetter(0))
                prange = [l2d.parameter(Base.Vector2d(sortedPts[0][0], sortedPts[0][1])), l2d.parameter(Base.Vector2d(sortedPts[-1][0], sortedPts[-1][1]))]
            else:
                FreeCAD.Console.PrintMessage("No intersection points")
        e = l2d.toShape(self.face, prange[0], prange[1])
        if isinstance(e, Part.Edge):
            return(e)
        else:
            FreeCAD.Console.PrintMessage("Failed to create isoCurve shape")
            return(None)


class multiIso:
    '''defines a set of multiple iso curves on a face'''
    def __init__(self, face, numu=0, numv=0):
        self.face = None
        self.paramu = []
        self.paramv = []
        self.uiso = []
        self.viso = []
        if not isinstance(face, Part.Face):
            FreeCAD.Console.PrintMessage("Error. Not a face")
        else:
            self.bounds = face.ParameterRange
            self.face = face
        if numu:
            self.setNumberU(numu)
        if numv:
            self.setNumberV(numv)

    def computeU(self):
        self.uiso = []
        for u in self.paramu:
            self.uiso.append(isoCurve(self.face, 'U', u))

    def computeV(self):
        self.viso = []
        for v in self.paramv:
            self.viso.append(isoCurve(self.face, 'V', v))

    # def compute(self):
        # self.computeU()
        # self.computeV()

    def toShape(self):
        c = []
        for u in self.uiso:
            c.append(u.toShape())
        for v in self.viso:
            c.append(v.toShape())
        return(Part.Compound(c))

    def paramList(self, n, fp, lp):
        rang = lp-fp
        params = []
        if n == 1:
            params = [fp + rang / 2.0]
        elif n == 2:
            params = [fp, lp]
        elif n > 2:
            for i in range(n):
                params.append(fp + 1.0 * i * rang / (n - 1))
        return params

    def setNumberU(self, n):
        fp = self.bounds[0]
        lp = self.bounds[1]
        self.paramu = self.paramList(n, fp, lp)
        self.computeU()

    def setNumberV(self, n):
        fp = self.bounds[2]
        lp = self.bounds[3]
        self.paramv = self.paramList(n, fp, lp)
        self.computeV()

    def setNumbers(self, nu, nv):
        self.setNumberU(nu)
        self.setNumberV(nv)
