#!/usr/bin/env python3
"""
SolidWorks Automation - Python Bridge

Dieses Script stellt eine einfache Python-Schnittstelle zur SolidWorks API bereit.
Es verwendet pywin32 für die COM-Kommunikation.

Voraussetzungen:
- Windows
- SolidWorks 2015+ (muss laufen)
- Python 3.x
- pywin32: pip install pywin32

Verwendung:
    from sw_automation import SolidWorksAutomation

    sw = SolidWorksAutomation()
    sw.sketch.rectangle_centered(100, 50)
    sw.feature.extrude(20)
    sw.save()
"""

import math

try:
    import win32com.client
    import pythoncom
except ImportError:
    raise ImportError("pywin32 nicht installiert. Bitte ausführen: pip install pywin32")

# Null-IDispatch für COM-Aufrufe (ersetzt None bei Object-Parametern)
_COM_NULL = win32com.client.VARIANT(pythoncom.VT_DISPATCH, None)


def mm_to_m(mm: float) -> float:
    """Konvertiert Millimeter zu Meter (SolidWorks API verwendet Meter)."""
    return mm / 1000.0


def deg_to_rad(deg: float) -> float:
    """Konvertiert Grad zu Radiant."""
    return deg * math.pi / 180.0


# SolidWorks Konstanten (swconst)
class SwConst:
    """SolidWorks API Konstanten."""
    # Document Types
    swDocPART = 1
    swDocASSEMBLY = 2
    swDocDRAWING = 3

    # End Conditions
    swEndCondBlind = 0
    swEndCondThroughAll = 1
    swEndCondThroughAllBoth = 2
    swEndCondUpToVertex = 3
    swEndCondUpToSurface = 4
    swEndCondMidPlane = 6

    # Sketch Relations
    swConstraintType_HORIZONTAL = 6
    swConstraintType_VERTICAL = 7
    swConstraintType_COINCIDENT = 3
    swConstraintType_TANGENT = 4
    swConstraintType_PERPENDICULAR = 5
    swConstraintType_PARALLEL = 8
    swConstraintType_CONCENTRIC = 9
    swConstraintType_EQUAL = 10
    swConstraintType_FIX = 11

    # Selection Types
    swSelFACES = 2
    swSelEDGES = 1
    swSelVERTICES = 3


class SolidWorksConnection:
    """Verwaltet die Verbindung zu SolidWorks."""

    def __init__(self):
        self.app = None
        self.model = None
        self._connect()

    def _connect(self):
        """Stellt Verbindung zu laufender SolidWorks-Instanz her."""
        try:
            self.app = win32com.client.Dispatch("SldWorks.Application")
        except Exception as e:
            raise ConnectionError(
                f"Konnte nicht zu SolidWorks verbinden: {e}\n"
                "Stellen Sie sicher, dass SolidWorks läuft."
            )

        self.model = self.app.ActiveDoc
        if self.model is None:
            raise ValueError(
                "Kein aktives Dokument in SolidWorks.\n"
                "Bitte öffnen Sie ein Part-Dokument."
            )

        # Prüfen ob es ein Part ist
        doc_type = self.model.GetType
        if doc_type != 1:  # 1 = Part, 2 = Assembly, 3 = Drawing
            raise ValueError(
                f"Aktives Dokument ist kein Part (Typ: {doc_type}).\n"
                "Dieser Skill funktioniert nur mit Part-Dokumenten."
            )

    @property
    def sketch_manager(self):
        """Gibt den SketchManager zurück."""
        return self.model.SketchManager

    @property
    def feature_manager(self):
        """Gibt den FeatureManager zurück."""
        return self.model.FeatureManager

    @property
    def selection_manager(self):
        """Gibt den SelectionManager zurück."""
        return self.model.SelectionManager

    @property
    def extension(self):
        """Gibt die ModelDocExtension zurück."""
        return self.model.Extension


class SketchOperations:
    """2D Skizzen-Operationen."""

    def __init__(self, connection: SolidWorksConnection):
        self.conn = connection

    def start_sketch(self, plane: str = "Front"):
        """
        Startet einen neuen Sketch auf der angegebenen Ebene.

        Args:
            plane: "Front", "Top", "Right" oder Feature-Name
        """
        # Ebene auswählen
        plane_map = {
            "Front": "Front Plane",
            "Top": "Top Plane",
            "Right": "Right Plane",
            "Vorne": "Front Plane",
            "Oben": "Top Plane",
            "Rechts": "Right Plane"
        }

        plane_name = plane_map.get(plane, plane)

        # Ebene selektieren
        self.conn.model.Extension.SelectByID2(
            plane_name, "PLANE", 0.0, 0.0, 0.0, False, 0, _COM_NULL, 0
        )

        # Sketch starten
        self.conn.sketch_manager.InsertSketch(True)

    def end_sketch(self):
        """Beendet den aktiven Sketch."""
        self.conn.sketch_manager.InsertSketch(True)

    def line(self, x1: float, y1: float, x2: float, y2: float):
        """
        Zeichnet eine Linie.

        Args:
            x1, y1: Startpunkt in mm
            x2, y2: Endpunkt in mm
        """
        self.conn.sketch_manager.CreateLine(
            mm_to_m(x1), mm_to_m(y1), 0,
            mm_to_m(x2), mm_to_m(y2), 0
        )

    def circle(self, cx: float = 0, cy: float = 0, diameter: float = None, radius: float = None):
        """
        Zeichnet einen Kreis.

        Args:
            cx, cy: Zentrum in mm (Standard: Ursprung)
            diameter: Durchmesser in mm
            radius: Radius in mm (alternativ zu diameter)
        """
        if diameter is not None:
            r = diameter / 2
        elif radius is not None:
            r = radius
        else:
            raise ValueError("Entweder diameter oder radius muss angegeben werden.")

        # CreateCircle braucht Zentrum und einen Punkt auf dem Kreis
        self.conn.sketch_manager.CreateCircle(
            mm_to_m(cx), mm_to_m(cy), 0,
            mm_to_m(cx + r), mm_to_m(cy), 0
        )

    def rectangle(self, x1: float, y1: float, x2: float, y2: float):
        """
        Zeichnet ein Rechteck aus zwei Eckpunkten.

        Args:
            x1, y1: Erste Ecke in mm
            x2, y2: Gegenüberliegende Ecke in mm
        """
        self.conn.sketch_manager.CreateCornerRectangle(
            mm_to_m(x1), mm_to_m(y1), 0,
            mm_to_m(x2), mm_to_m(y2), 0
        )

    def rectangle_centered(self, width: float, height: float, cx: float = 0, cy: float = 0):
        """
        Zeichnet ein zentriertes Rechteck.

        Args:
            width: Breite in mm
            height: Höhe in mm
            cx, cy: Zentrum in mm (Standard: Ursprung)
        """
        half_w = width / 2
        half_h = height / 2
        self.rectangle(
            cx - half_w, cy - half_h,
            cx + half_w, cy + half_h
        )

    def arc(self, cx: float, cy: float, radius: float,
            start_angle: float, end_angle: float):
        """
        Zeichnet einen Kreisbogen.

        Args:
            cx, cy: Zentrum in mm
            radius: Radius in mm
            start_angle: Startwinkel in Grad
            end_angle: Endwinkel in Grad
        """
        # Berechne Start- und Endpunkte
        start_rad = deg_to_rad(start_angle)
        end_rad = deg_to_rad(end_angle)

        sx = cx + radius * math.cos(start_rad)
        sy = cy + radius * math.sin(start_rad)
        ex = cx + radius * math.cos(end_rad)
        ey = cy + radius * math.sin(end_rad)

        # Direction: 1 = counter-clockwise, -1 = clockwise
        direction = 1 if end_angle > start_angle else -1

        self.conn.sketch_manager.CreateArc(
            mm_to_m(cx), mm_to_m(cy), 0,
            mm_to_m(sx), mm_to_m(sy), 0,
            mm_to_m(ex), mm_to_m(ey), 0,
            direction
        )

    def polygon(self, cx: float, cy: float, radius: float, sides: int):
        """
        Zeichnet ein regelmäßiges Polygon.

        Args:
            cx, cy: Zentrum in mm
            radius: Radius (Umkreis) in mm
            sides: Anzahl der Seiten (3 = Dreieck, 6 = Sechseck, etc.)
        """
        points = []
        for i in range(sides):
            angle = 2 * math.pi * i / sides - math.pi / 2  # Start oben
            x = cx + radius * math.cos(angle)
            y = cy + radius * math.sin(angle)
            points.append((x, y))

        # Linien zeichnen
        for i in range(sides):
            x1, y1 = points[i]
            x2, y2 = points[(i + 1) % sides]
            self.line(x1, y1, x2, y2)

    def slot(self, x1: float, y1: float, x2: float, y2: float, width: float):
        """
        Zeichnet ein Langloch (Slot).

        Args:
            x1, y1: Startpunkt der Mittellinie in mm
            x2, y2: Endpunkt der Mittellinie in mm
            width: Breite des Langlochs in mm
        """
        # SolidWorks hat CreateSketchSlot, aber Parameter sind komplex
        # Vereinfachte Version mit Linien und Bögen

        dx = x2 - x1
        dy = y2 - y1
        length = math.sqrt(dx*dx + dy*dy)

        if length == 0:
            raise ValueError("Start- und Endpunkt dürfen nicht identisch sein.")

        # Normalisierte Richtung
        nx = dx / length
        ny = dy / length

        # Senkrechte Richtung
        px = -ny
        py = nx

        r = width / 2

        # Vier Eckpunkte
        p1 = (x1 + px * r, y1 + py * r)
        p2 = (x1 - px * r, y1 - py * r)
        p3 = (x2 - px * r, y2 - py * r)
        p4 = (x2 + px * r, y2 + py * r)

        # Linien
        self.line(p1[0], p1[1], p4[0], p4[1])
        self.line(p2[0], p2[1], p3[0], p3[1])

        # Halbkreise an den Enden
        # Start-Ende
        start_angle = math.degrees(math.atan2(py, px))
        self.arc(x1, y1, r, start_angle, start_angle + 180)
        self.arc(x2, y2, r, start_angle + 180, start_angle + 360)

    def ellipse(self, cx: float = 0, cy: float = 0,
                major_radius: float = None, minor_radius: float = None,
                major_diameter: float = None, minor_diameter: float = None):
        """
        Zeichnet eine Ellipse.

        Args:
            cx, cy: Zentrum in mm
            major_radius: Hauptachsen-Radius in mm
            minor_radius: Nebenachsen-Radius in mm
            major_diameter: Hauptachsen-Durchmesser in mm (alternativ)
            minor_diameter: Nebenachsen-Durchmesser in mm (alternativ)
        """
        # Konvertiere Durchmesser zu Radien
        if major_diameter is not None:
            major_r = major_diameter / 2
        elif major_radius is not None:
            major_r = major_radius
        else:
            raise ValueError("major_radius oder major_diameter muss angegeben werden.")

        if minor_diameter is not None:
            minor_r = minor_diameter / 2
        elif minor_radius is not None:
            minor_r = minor_radius
        else:
            raise ValueError("minor_radius oder minor_diameter muss angegeben werden.")

        # CreateEllipse(Xc, Yc, Zc, Xa, Ya, Za, Xb, Yb, Zb)
        # Xa, Ya, Za = Punkt auf Hauptachse
        # Xb, Yb, Zb = Punkt auf Nebenachse
        self.conn.sketch_manager.CreateEllipse(
            mm_to_m(cx), mm_to_m(cy), 0,
            mm_to_m(cx + major_r), mm_to_m(cy), 0,
            mm_to_m(cx), mm_to_m(cy + minor_r), 0
        )

    def center_rectangle(self, cx: float, cy: float, width: float, height: float):
        """
        Zeichnet ein Rechteck um einen Mittelpunkt (API: CreateCenterRectangle).

        Args:
            cx, cy: Zentrum in mm
            width: Breite in mm
            height: Höhe in mm
        """
        half_w = width / 2
        half_h = height / 2

        # CreateCenterRectangle(Xc, Yc, Zc, Xp, Yp, Zp)
        # Xc, Yc, Zc = Zentrum
        # Xp, Yp, Zp = Eckpunkt
        self.conn.sketch_manager.CreateCenterRectangle(
            mm_to_m(cx), mm_to_m(cy), 0,
            mm_to_m(cx + half_w), mm_to_m(cy + half_h), 0
        )

    def three_point_arc(self, x1: float, y1: float, x2: float, y2: float,
                        x3: float, y3: float):
        """
        Zeichnet einen Bogen durch drei Punkte.

        Args:
            x1, y1: Startpunkt in mm
            x2, y2: Mittelpunkt (auf dem Bogen) in mm
            x3, y3: Endpunkt in mm
        """
        self.conn.sketch_manager.Create3PointArc(
            mm_to_m(x1), mm_to_m(y1), 0,
            mm_to_m(x2), mm_to_m(y2), 0,
            mm_to_m(x3), mm_to_m(y3), 0
        )

    def spline(self, points: list, closed: bool = False):
        """
        Zeichnet einen Spline durch Punktliste.

        Args:
            points: Liste von (x, y) Tupeln in mm
            closed: True für geschlossenen Spline
        """
        # Punktarray für API erstellen (x, y, z, x, y, z, ...)
        point_data = []
        for x, y in points:
            point_data.extend([mm_to_m(x), mm_to_m(y), 0])

        # CreateSpline2 erwartet ein Variant-Array
        self.conn.sketch_manager.CreateSpline2(point_data, closed)

    def add_relation(self, relation_type: str):
        """
        Fügt eine Beziehung zu ausgewählten Sketch-Elementen hinzu.

        Args:
            relation_type: "horizontal", "vertical", "coincident", "tangent",
                          "perpendicular", "parallel", "concentric", "equal", "fix"

        Hinweis: Sketch-Elemente müssen vorher selektiert sein!
        """
        relation_map = {
            "horizontal": SwConst.swConstraintType_HORIZONTAL,
            "vertical": SwConst.swConstraintType_VERTICAL,
            "coincident": SwConst.swConstraintType_COINCIDENT,
            "tangent": SwConst.swConstraintType_TANGENT,
            "perpendicular": SwConst.swConstraintType_PERPENDICULAR,
            "parallel": SwConst.swConstraintType_PARALLEL,
            "concentric": SwConst.swConstraintType_CONCENTRIC,
            "equal": SwConst.swConstraintType_EQUAL,
            "fix": SwConst.swConstraintType_FIX,
            # Deutsche Begriffe
            "horizontal": SwConst.swConstraintType_HORIZONTAL,
            "vertikal": SwConst.swConstraintType_VERTICAL,
            "koinzident": SwConst.swConstraintType_COINCIDENT,
            "tangential": SwConst.swConstraintType_TANGENT,
            "senkrecht": SwConst.swConstraintType_PERPENDICULAR,
            "gleich": SwConst.swConstraintType_EQUAL,
            "fixiert": SwConst.swConstraintType_FIX
        }

        rel_const = relation_map.get(relation_type.lower())
        if rel_const is None:
            raise ValueError(f"Unbekannte Beziehung: {relation_type}")

        self.conn.model.SketchAddConstraints(rel_const)


class FeatureOperations:
    """3D Feature-Operationen."""

    def __init__(self, connection: SolidWorksConnection):
        self.conn = connection

    def extrude(self, depth: float, direction: int = 1, draft_angle: float = 0):
        """
        Extrudiert den aktuellen Sketch.

        Args:
            depth: Tiefe in mm
            direction: 1 = normal, -1 = umgekehrt, 0 = beidseitig
            draft_angle: Anzugswinkel in Grad (optional)
        """
        # FeatureExtrusion3 Parameter:
        # Sd (Single direction), Flip, Dir (direction),
        # T1 (end type 1), T2 (end type 2), D1 (depth 1), D2 (depth 2),
        # Dchk1, Dchk2, Ddir1, Ddir2, Dang1, Dang2,
        # OffsetReverse1, OffsetReverse2, TranslateSurface1, TranslateSurface2,
        # Merge, UseFeatScope, UseAutoSelect, T0 (start type), StartOffset, FlipStartOffset

        depth_m = mm_to_m(depth)
        draft_rad = deg_to_rad(draft_angle)

        if direction == 0:
            # Beidseitig
            self.conn.feature_manager.FeatureExtrusion3(
                False,  # Sd - not single direction
                False,  # Flip
                False,  # Dir
                0,      # T1 - Blind
                0,      # T2 - Blind
                depth_m / 2,  # D1
                depth_m / 2,  # D2
                draft_angle != 0,  # Dchk1
                draft_angle != 0,  # Dchk2
                False,  # Ddir1
                False,  # Ddir2
                draft_rad,  # Dang1
                draft_rad,  # Dang2
                False, False, False, False,
                True,   # Merge
                True,   # UseFeatScope
                True,   # UseAutoSelect
                0,      # T0 - Sketch plane
                0,      # StartOffset
                False   # FlipStartOffset
            )
        else:
            # Einseitig
            self.conn.feature_manager.FeatureExtrusion3(
                True,   # Sd - single direction
                direction < 0,  # Flip
                False,  # Dir
                0,      # T1 - Blind
                0,      # T2 - not used
                depth_m,  # D1
                0,      # D2 - not used
                draft_angle != 0,  # Dchk1
                False,  # Dchk2
                False,  # Ddir1
                False,  # Ddir2
                draft_rad,  # Dang1
                0,      # Dang2
                False, False, False, False,
                True,   # Merge
                True,   # UseFeatScope
                True,   # UseAutoSelect
                0,      # T0 - Sketch plane
                0,      # StartOffset
                False   # FlipStartOffset
            )

    def cut(self, depth: float = 10.0, direction: int = 1, through_all: bool = False):
        """
        Erstellt einen Schnitt (entfernt Material).

        Args:
            depth: Tiefe in mm (ignoriert wenn through_all=True)
            direction: 1 = normal, -1 = umgekehrt
            through_all: True = durch alles schneiden
        """
        depth_m = mm_to_m(depth)

        # End type: 0 = Blind, 1 = Through All
        end_type = 1 if through_all else 0

        flip = 1 if direction < 0 else 0
        fm = self.conn.model.FeatureManager
        fm.FeatureCut(
            1,          # Sd - single direction
            flip,       # Flip
            0,          # Dir
            end_type,   # T1
            0,          # T2
            depth_m,    # D1
            0.0,        # D2
            0, 0, 0, 0, # Dchk1, Dchk2, Ddir1, Ddir2
            0.0, 0.0    # Dang1, Dang2
        )

    def chamfer(self, distance: float, angle: float = 45):
        """
        Fügt eine Fase zu ausgewählten Kanten hinzu.

        Args:
            distance: Fasenabstand in mm
            angle: Fasenwinkel in Grad (Standard: 45)

        Hinweis: Kanten müssen vorher selektiert sein!
        """
        distance_m = mm_to_m(distance)
        angle_rad = deg_to_rad(angle)

        # InsertFeatureChamfer Parameter:
        # Options, ChamferType, Distance, Angle, OtherDistance,
        # VertexChamDist1, VertexChamDist2, VertexChamDist3

        self.conn.feature_manager.InsertFeatureChamfer(
            2,  # Options: 2 = use selections
            1,  # ChamferType: 1 = Angle-Distance
            distance_m,
            angle_rad,
            0,  # OtherDistance (for symmetric)
            0, 0, 0  # Vertex distances
        )

    def fillet(self, radius: float):
        """
        Fügt eine Verrundung zu ausgewählten Kanten hinzu.

        Args:
            radius: Verrundungsradius in mm

        Hinweis: Kanten müssen vorher selektiert sein!
        """
        radius_m = mm_to_m(radius)

        # FeatureFillet3 Parameter sind komplex
        # Vereinfachte Version mit SimpleFilletFeature
        self.conn.feature_manager.FeatureFillet3(
            195,    # Options
            radius_m,
            0,      # Fillet type
            0,      # Overflow type
            0, 0, 0,  # Additional radii
            0, 0, 0,
            0, 0, 0,
            True,   # TangentPropagation
            False,  # FullPreview
            False,  # PartialPreview
            False,  # Isocurves
            False,  # Curvature
            False,  # Zebra
            False   # Faceted
        )

    def circular_hole_pattern(self, num_holes: int, hole_diameter: float,
                               pitch_circle_diameter: float, hole_depth: float,
                               start_angle: float = 0):
        """
        Erstellt ein kreisförmiges Bohrungsmuster.

        Args:
            num_holes: Anzahl der Bohrungen
            hole_diameter: Bohrungsdurchmesser in mm
            pitch_circle_diameter: Lochkreisdurchmesser in mm
            hole_depth: Bohrtiefe in mm
            start_angle: Startwinkel in Grad
        """
        r = pitch_circle_diameter / 2
        angle_step = 360 / num_holes

        for i in range(num_holes):
            angle = start_angle + i * angle_step
            angle_rad = deg_to_rad(angle)

            # Position berechnen
            x = r * math.cos(angle_rad)
            y = r * math.sin(angle_rad)

            # Sketch für diese Bohrung
            self.conn.model.Extension.SelectByID2(
                "Front Plane", "PLANE", 0.0, 0.0, 0.0, False, 0, _COM_NULL, 0
            )
            self.conn.sketch_manager.InsertSketch(True)

            # Kreis zeichnen
            hole_r = hole_diameter / 2
            self.conn.sketch_manager.CreateCircle(
                mm_to_m(x), mm_to_m(y), 0,
                mm_to_m(x + hole_r), mm_to_m(y), 0
            )

            # Sketch beenden
            self.conn.sketch_manager.InsertSketch(True)

            # Cut erstellen
            self.cut(hole_depth)

    def linear_pattern(self, direction: str, count: int, spacing: float):
        """
        Erstellt ein lineares Muster des zuletzt erstellten Features.

        Args:
            direction: "X", "Y" oder "Z"
            count: Anzahl der Kopien
            spacing: Abstand zwischen Kopien in mm

        Hinweis: Feature muss vorher selektiert sein!
        """
        spacing_m = mm_to_m(spacing)

        # Richtungsvektor
        dir_map = {
            "X": (1, 0, 0),
            "Y": (0, 1, 0),
            "Z": (0, 0, 1)
        }

        dx, dy, dz = dir_map.get(direction.upper(), (1, 0, 0))

        # FeatureLinearPattern4 ist komplex, hier vereinfacht
        self.conn.feature_manager.FeatureLinearPattern4(
            count, spacing_m,  # D1Num, D1Spacing
            1, spacing_m,      # D2Num, D2Spacing (nur 1 in zweite Richtung)
            True, False,       # D1Reverse, D2Reverse
            dx, dy, dz,        # D1X, D1Y, D1Z (Richtung 1)
            0, 1, 0,           # D2X, D2Y, D2Z (Richtung 2)
            False, False,      # GeometryPattern, VarySketch
            True               # CreateSeeds
        )

    def revolve(self, angle: float = 360, axis: str = "Y", direction: int = 1):
        """
        Erstellt einen Drehkörper aus dem aktuellen Sketch.

        Args:
            angle: Drehwinkel in Grad (Standard: 360 für Vollrotation)
            axis: Drehachse - "X", "Y", "Z" oder Achsenname
            direction: 1 = normal, -1 = umgekehrt, 0 = beidseitig

        Hinweis: Sketch muss eine Mittellinie oder Achse enthalten!
        """
        angle_rad = deg_to_rad(angle)

        # Achse auswählen (falls nicht bereits selektiert)
        axis_map = {
            "X": "X-Achse",
            "Y": "Y-Achse",
            "Z": "Z-Achse"
        }

        if direction == 0:
            # Beidseitig (MidPlane)
            self.conn.feature_manager.FeatureRevolve2(
                False,  # SingleDir
                True,   # IsSolid
                False,  # IsThin
                False,  # IsCut
                False,  # ReverseDir
                False,  # BothDirectionUpToSameEntity
                SwConst.swEndCondMidPlane,  # Dir1Type
                SwConst.swEndCondBlind,     # Dir2Type
                angle_rad,  # Dir1Angle
                0,          # Dir2Angle
                False, False, 0, 0,  # Offsets
                0, 0, 0,             # ThinType, Thickness1, Thickness2
                True,   # Merge
                True,   # UseFeatScope
                True    # UseAutoSelect
            )
        else:
            # Einseitig
            self.conn.feature_manager.FeatureRevolve2(
                True,   # SingleDir
                True,   # IsSolid
                False,  # IsThin
                False,  # IsCut
                direction < 0,  # ReverseDir
                False,  # BothDirectionUpToSameEntity
                SwConst.swEndCondBlind,  # Dir1Type
                SwConst.swEndCondBlind,  # Dir2Type
                angle_rad,  # Dir1Angle
                0,          # Dir2Angle
                False, False, 0, 0,  # Offsets
                0, 0, 0,             # ThinType, Thickness1, Thickness2
                True,   # Merge
                True,   # UseFeatScope
                True    # UseAutoSelect
            )

    def revolve_cut(self, angle: float = 360, direction: int = 1):
        """
        Erstellt einen Rotationsschnitt (entfernt Material durch Drehung).

        Args:
            angle: Drehwinkel in Grad (Standard: 360)
            direction: 1 = normal, -1 = umgekehrt
        """
        angle_rad = deg_to_rad(angle)

        self.conn.feature_manager.FeatureRevolve2(
            True,   # SingleDir
            True,   # IsSolid
            False,  # IsThin
            True,   # IsCut - WICHTIG: True für Schnitt!
            direction < 0,  # ReverseDir
            False,  # BothDirectionUpToSameEntity
            SwConst.swEndCondBlind,  # Dir1Type
            SwConst.swEndCondBlind,  # Dir2Type
            angle_rad,  # Dir1Angle
            0,          # Dir2Angle
            False, False, 0, 0,  # Offsets
            0, 0, 0,             # ThinType, Thickness1, Thickness2
            True,   # Merge
            True,   # UseFeatScope
            True    # UseAutoSelect
        )

    def reference_plane(self, offset: float, base_plane: str = "Front"):
        """
        Erstellt eine neue Referenzebene.

        Args:
            offset: Abstand von der Basisebene in mm
            base_plane: "Front", "Top", "Right" oder Ebenenname
        """
        # Basisebene auswählen
        plane_map = {
            "Front": "Front Plane",
            "Top": "Top Plane",
            "Right": "Right Plane",
            "Vorne": "Front Plane",
            "Oben": "Top Plane",
            "Rechts": "Right Plane"
        }

        plane_name = plane_map.get(base_plane, base_plane)

        self.conn.model.Extension.SelectByID2(
            plane_name, "PLANE", 0.0, 0.0, 0.0, False, 0, _COM_NULL, 0
        )

        offset_m = mm_to_m(offset)

        # InsertRefPlane erstellt Referenzebene mit Offset
        self.conn.feature_manager.InsertRefPlane(
            8,  # Constraint type: Offset
            offset_m,
            0, 0,
            0, 0
        )

    def mirror(self, plane: str = "Right"):
        """
        Spiegelt ausgewählte Features an einer Ebene.

        Args:
            plane: Spiegelebene - "Front", "Top", "Right" oder Ebenenname

        Hinweis: Features müssen vorher selektiert sein!
        """
        plane_map = {
            "Front": "Front Plane",
            "Top": "Top Plane",
            "Right": "Right Plane",
            "Vorne": "Front Plane",
            "Oben": "Top Plane",
            "Rechts": "Right Plane"
        }

        plane_name = plane_map.get(plane, plane)

        # Spiegelebene zur Selektion hinzufügen
        self.conn.model.Extension.SelectByID2(
            plane_name, "PLANE", 0.0, 0.0, 0.0, True, 0, _COM_NULL, 0
        )

        # Mirror Feature erstellen
        self.conn.feature_manager.InsertMirrorFeature2(
            True,   # MirrorBody
            False,  # GeometryPattern
            True,   # PropagateVisualProps
            True    # FullPreview
        )


class SelectionHelper:
    """Hilfsklasse für Objektselektion (Kanten, Flächen, Körper)."""

    def __init__(self, connection: SolidWorksConnection):
        self.conn = connection

    def select_by_id(self, name: str, obj_type: str, append: bool = False):
        """
        Selektiert ein Objekt nach Name und Typ.

        Args:
            name: Name des Objekts (z.B. "Front Plane", "Boss-Extrude1")
            obj_type: Typ ("PLANE", "FACE", "EDGE", "VERTEX", "BODYFEATURE")
            append: True = zur Selektion hinzufügen, False = ersetzen
        """
        return self.conn.model.Extension.SelectByID2(
            name, obj_type, 0.0, 0.0, 0.0, append, 0, _COM_NULL, 0
        )

    def select_by_ray(self, x: float, y: float, z: float,
                      dx: float = 0, dy: float = 0, dz: float = -1,
                      obj_type: str = "FACE"):
        """
        Selektiert ein Objekt durch Raycast an einer Position.

        Args:
            x, y, z: Startpunkt des Rays in mm
            dx, dy, dz: Richtung des Rays (Standard: -Z)
            obj_type: "FACE", "EDGE", oder "VERTEX"
        """
        type_map = {
            "FACE": SwConst.swSelFACES,
            "EDGE": SwConst.swSelEDGES,
            "VERTEX": SwConst.swSelVERTICES
        }

        sel_type = type_map.get(obj_type.upper(), SwConst.swSelFACES)

        return self.conn.model.Extension.SelectByRay(
            mm_to_m(x), mm_to_m(y), mm_to_m(z),
            dx, dy, dz,
            0.001,  # Radius
            sel_type,
            False,  # Append
            0,      # Mark
            0       # Action
        )

    def select_face_at(self, x: float, y: float, z: float):
        """Selektiert eine Fläche an der angegebenen Position."""
        return self.select_by_ray(x, y, z, obj_type="FACE")

    def select_edge_at(self, x: float, y: float, z: float):
        """Selektiert eine Kante an der angegebenen Position."""
        return self.select_by_ray(x, y, z, obj_type="EDGE")

    def select_all_edges(self):
        """
        Selektiert alle Kanten des aktiven Körpers.

        Hinweis: Dies ist eine vereinfachte Version.
        Für komplexe Selektion B-Rep traversieren.
        """
        # Alle Körper durchlaufen
        bodies = self.conn.model.GetBodies2(0, True)  # 0 = Solid bodies
        if bodies:
            for body in bodies:
                edges = body.GetEdges()
                if edges:
                    for edge in edges:
                        edge.Select4(True, _COM_NULL)

    def get_selection_count(self) -> int:
        """Gibt die Anzahl der selektierten Objekte zurück."""
        return self.conn.selection_manager.GetSelectedObjectCount2(-1)

    def clear_selection(self):
        """Hebt alle Selektionen auf."""
        self.conn.model.ClearSelection2(True)

    def get_body(self):
        """Gibt den ersten Solid-Körper zurück."""
        bodies = self.conn.model.GetBodies2(0, True)
        if bodies and len(bodies) > 0:
            return bodies[0]
        return None


class DocumentManager:
    """Verwaltet SolidWorks-Dokumente (Erstellen, Öffnen, Schließen)."""

    def __init__(self, app):
        self.app = app
        # Standard-Templates (können je nach Installation variieren)
        self._templates = {
            "part": r"C:\ProgramData\SolidWorks\SOLIDWORKS 2023\templates\Part.prtdot",
            "assembly": r"C:\ProgramData\SolidWorks\SOLIDWORKS 2023\templates\Assembly.asmdot",
            "drawing": r"C:\ProgramData\SolidWorks\SOLIDWORKS 2023\templates\Drawing.drwdot"
        }

    def set_template_path(self, doc_type: str, path: str):
        """
        Setzt den Pfad für ein Dokumenttemplate.

        Args:
            doc_type: "part", "assembly", oder "drawing"
            path: Vollständiger Pfad zur Template-Datei
        """
        self._templates[doc_type.lower()] = path

    def new_part(self, template: str = None):
        """
        Erstellt ein neues Part-Dokument.

        Args:
            template: Optionaler Pfad zum Template

        Returns:
            ModelDoc2 Objekt
        """
        template_path = template or self._templates.get("part", "")

        # Versuche Standard-Template oder leeres Dokument
        try:
            model = self.app.NewDocument(template_path, 0, 0, 0)
        except:
            # Fallback: Versuche ohne spezifisches Template
            model = self.app.NewPart()

        if model:
            print(f"Neues Part erstellt: {model.GetTitle}")
        return model

    def new_assembly(self, template: str = None):
        """
        Erstellt ein neues Assembly-Dokument.

        Args:
            template: Optionaler Pfad zum Template

        Returns:
            ModelDoc2 Objekt
        """
        template_path = template or self._templates.get("assembly", "")

        try:
            model = self.app.NewDocument(template_path, 0, 0, 0)
        except:
            model = self.app.NewAssembly()

        if model:
            print(f"Neue Baugruppe erstellt: {model.GetTitle}")
        return model

    def open(self, file_path: str):
        """
        Öffnet ein bestehendes Dokument.

        Args:
            file_path: Pfad zur Datei (.sldprt, .sldasm, .slddrw)

        Returns:
            ModelDoc2 Objekt
        """
        # Dateityp erkennen
        ext = file_path.lower().split('.')[-1]
        type_map = {
            "sldprt": SwConst.swDocPART,
            "sldasm": SwConst.swDocASSEMBLY,
            "slddrw": SwConst.swDocDRAWING
        }

        doc_type = type_map.get(ext, SwConst.swDocPART)

        errors = 0
        warnings = 0
        model = self.app.OpenDoc6(
            file_path,
            doc_type,
            1,  # Silent mode
            "",
            errors,
            warnings
        )

        if model:
            print(f"Dokument geöffnet: {model.GetTitle}")
        else:
            print(f"Fehler beim Öffnen: Error={errors}, Warning={warnings}")

        return model

    def close(self, save: bool = False):
        """
        Schließt das aktive Dokument.

        Args:
            save: True = vor dem Schließen speichern
        """
        model = self.app.ActiveDoc
        if model:
            if save:
                model.Save3(1, 0, 0)
            title = model.GetTitle
            self.app.CloseDoc(title)
            print(f"Dokument geschlossen: {title}")

    def close_all(self, save: bool = False):
        """Schließt alle geöffneten Dokumente."""
        while self.app.ActiveDoc:
            self.close(save)


class SolidWorksAutomation:
    """
    Hauptklasse für SolidWorks-Automatisierung.

    Verwendung:
        sw = SolidWorksAutomation()
        sw.sketch.rectangle_centered(100, 50)
        sw.feature.extrude(20)
        sw.save()
    """

    def __init__(self, require_document: bool = True):
        """
        Initialisiert die SolidWorks-Verbindung.

        Args:
            require_document: True = Fehler wenn kein Dokument offen
                              False = Erlaubt Start ohne offenes Dokument
        """
        self._connection = SolidWorksConnection() if require_document else None
        self._app = None

        if self._connection:
            self._app = self._connection.app
            self._sketch = SketchOperations(self._connection)
            self._feature = FeatureOperations(self._connection)
            self._selection = SelectionHelper(self._connection)
            print("Verbunden mit SolidWorks")
            print(f"Aktives Dokument: {self._connection.model.GetTitle}")
        else:
            # Nur App-Verbindung ohne Dokument
            try:
                self._app = win32com.client.Dispatch("SldWorks.Application")
                print("Verbunden mit SolidWorks (kein Dokument)")
            except Exception as e:
                raise ConnectionError(f"Konnte nicht zu SolidWorks verbinden: {e}")

        self._documents = DocumentManager(self._app)

    @property
    def sketch(self) -> SketchOperations:
        """Zugriff auf Sketch-Operationen."""
        return self._sketch

    @property
    def feature(self) -> FeatureOperations:
        """Zugriff auf Feature-Operationen."""
        return self._feature

    @property
    def selection(self) -> SelectionHelper:
        """Zugriff auf Selektions-Hilfsfunktionen."""
        return self._selection

    @property
    def documents(self) -> DocumentManager:
        """Zugriff auf Dokument-Management."""
        return self._documents

    @property
    def model(self):
        """Direkter Zugriff auf das ModelDoc2 Objekt."""
        if self._connection:
            return self._connection.model
        return self._app.ActiveDoc

    @property
    def app(self):
        """Direkter Zugriff auf die SolidWorks Application."""
        return self._app

    def new_sketch(self, plane: str = "Front"):
        """
        Startet einen neuen Sketch.

        Args:
            plane: "Front", "Top", "Right"
        """
        self._sketch.start_sketch(plane)

    def end_sketch(self):
        """Beendet den aktuellen Sketch."""
        self._sketch.end_sketch()

    def rebuild(self):
        """Baut das Modell neu auf."""
        self._connection.model.ForceRebuild3(False)

    def save(self, path: str = None):
        """
        Speichert das Modell.

        Args:
            path: Optionaler Speicherpfad. Wenn None, wird überschrieben.
        """
        if path:
            self._connection.model.SaveAs(path)
        else:
            self._connection.model.Save3(1, 0, 0)
        print("Modell gespeichert")

    def select_face(self, face_name: str):
        """Selektiert eine Fläche nach Name."""
        self._connection.model.Extension.SelectByID2(
            face_name, "FACE", 0.0, 0.0, 0.0, False, 0, _COM_NULL, 0
        )

    def select_edge(self, edge_index: int = 0):
        """
        Selektiert eine Kante.

        Hinweis: Kanten haben keine Namen in SolidWorks.
        Dies erfordert manuelle Selektion oder Ray-Casting.
        """
        # Vereinfacht - normalerweise würde man SelectByRay verwenden
        pass

    def clear_selection(self):
        """Hebt alle Selektionen auf."""
        self._connection.model.ClearSelection2(True)


# Schnellzugriff-Funktionen für einfache Operationen
def quick_box(width: float, height: float, depth: float):
    """
    Erstellt schnell einen einfachen Quader.

    Args:
        width: Breite in mm
        height: Höhe in mm
        depth: Tiefe in mm
    """
    sw = SolidWorksAutomation()
    sw.new_sketch("Front")
    sw.sketch.rectangle_centered(width, height)
    sw.end_sketch()
    sw.feature.extrude(depth)
    sw.save()
    print(f"Quader erstellt: {width}x{height}x{depth}mm")
    return sw


def quick_cylinder(diameter: float, height: float):
    """
    Erstellt schnell einen Zylinder.

    Args:
        diameter: Durchmesser in mm
        height: Höhe in mm
    """
    sw = SolidWorksAutomation()
    sw.new_sketch("Front")
    sw.sketch.circle(diameter=diameter)
    sw.end_sketch()
    sw.feature.extrude(height)
    sw.save()
    print(f"Zylinder erstellt: Ø{diameter}x{height}mm")
    return sw


def quick_revolve(profile_points: list, axis: str = "Y", angle: float = 360):
    """
    Erstellt schnell einen Drehkörper aus Profilpunkten.

    Args:
        profile_points: Liste von (x, y) Punkten in mm (Halbprofil)
        axis: Drehachse "X" oder "Y"
        angle: Drehwinkel in Grad

    Beispiel:
        # Kegel erstellen
        quick_revolve([(0, 0), (20, 0), (0, 50)], axis="Y")
    """
    sw = SolidWorksAutomation()
    sw.new_sketch("Front")

    # Profil zeichnen
    for i in range(len(profile_points) - 1):
        x1, y1 = profile_points[i]
        x2, y2 = profile_points[i + 1]
        sw.sketch.line(x1, y1, x2, y2)

    # Profil schließen (zum Ursprung)
    if profile_points[0] != profile_points[-1]:
        x1, y1 = profile_points[-1]
        x2, y2 = profile_points[0]
        sw.sketch.line(x1, y1, x2, y2)

    # Mittellinie für Drehachse (als Konstruktionslinie)
    if axis.upper() == "Y":
        sw.sketch.line(0, -100, 0, 100)  # Vertikale Achse
    else:
        sw.sketch.line(-100, 0, 100, 0)  # Horizontale Achse

    sw.end_sketch()
    sw.feature.revolve(angle, axis)
    sw.save()
    print(f"Drehkörper erstellt: {angle}°")
    return sw


def quick_pipe(outer_diameter: float, inner_diameter: float, length: float):
    """
    Erstellt schnell ein Rohr (Hohlzylinder).

    Args:
        outer_diameter: Außendurchmesser in mm
        inner_diameter: Innendurchmesser in mm
        length: Länge in mm
    """
    sw = SolidWorksAutomation()

    # Außenzylinder
    sw.new_sketch("Front")
    sw.sketch.circle(diameter=outer_diameter)
    sw.end_sketch()
    sw.feature.extrude(length)

    # Innenbohrung
    sw.new_sketch("Front")
    sw.sketch.circle(diameter=inner_diameter)
    sw.end_sketch()
    sw.feature.cut(through_all=True)

    sw.save()
    print(f"Rohr erstellt: Ø{outer_diameter}/Ø{inner_diameter} x {length}mm")
    return sw


def quick_plate_with_holes(length: float, width: float, thickness: float,
                           hole_diameter: float, hole_positions: list):
    """
    Erstellt schnell eine Platte mit Bohrungen.

    Args:
        length: Länge in mm
        width: Breite in mm
        thickness: Dicke in mm
        hole_diameter: Bohrungsdurchmesser in mm
        hole_positions: Liste von (x, y) Positionen der Bohrungen

    Beispiel:
        quick_plate_with_holes(100, 50, 10, 8, [(20, 15), (80, 15), (20, 35), (80, 35)])
    """
    sw = SolidWorksAutomation()

    # Grundplatte
    sw.new_sketch("Front")
    sw.sketch.rectangle(0, 0, length, width)
    sw.end_sketch()
    sw.feature.extrude(thickness)

    # Bohrungen
    for x, y in hole_positions:
        sw.new_sketch("Front")
        sw.sketch.circle(cx=x, cy=y, diameter=hole_diameter)
        sw.end_sketch()
        sw.feature.cut(through_all=True)

    sw.save()
    print(f"Platte mit {len(hole_positions)} Bohrungen erstellt")
    return sw


if __name__ == "__main__":
    # Test-Modus
    print("=" * 60)
    print("SolidWorks Automation - Test")
    print("=" * 60)

    try:
        sw = SolidWorksAutomation()
        print("\nVerbindung erfolgreich!")
        print(f"SolidWorks Version: {sw.app.RevisionNumber()}")
        print(f"Dokument: {sw.model.GetTitle}")
        print("\nBereit für Operationen.")
    except Exception as e:
        print(f"\nFehler: {e}")
        print("\nStellen Sie sicher, dass:")
        print("  1. SolidWorks läuft")
        print("  2. Ein Part-Dokument geöffnet ist")
        print("  3. pywin32 installiert ist")
