# Sketch Operations Reference

## Übersicht

Diese Referenz dokumentiert alle verfügbaren 2D-Skizzenoperationen für die SolidWorks-Automatisierung.

## Wichtige Hinweise

### Einheiten
- **SolidWorks API verwendet Meter, nicht Millimeter!**
- Immer `mm / 1000` rechnen
- Das Script `sw_automation.py` macht diese Konvertierung automatisch

### Sketch-Zustand
- Ein Sketch muss **aktiv** sein, bevor Elemente gezeichnet werden können
- `InsertSketch(True)` startet einen neuen Sketch ODER beendet den aktuellen
- Immer Ebene auswählen vor `InsertSketch()`

### Koordinatensystem
- Z-Koordinate ist normalerweise 0 für 2D-Skizzen
- Ursprung (0,0) ist die Mitte der Skizzenebene

### Ebenen (Planes)
Die Standard-Ebenen haben unterschiedliche Namen je nach Spracheinstellung:

| Englisch | Deutsch |
|----------|---------|
| Front Plane | Ebene vorne |
| Top Plane | Ebene oben |
| Right Plane | Ebene rechts |

Das Script unterstützt beide Sprachen über Aliase.

---

## Grundlegende Formen

### Linie (CreateLine)

```python
# API-Methode
SketchManager.CreateLine(X1, Y1, Z1, X2, Y2, Z2)

# Mit sw_automation.py
sw.sketch.line(x1, y1, x2, y2)  # Koordinaten in mm
```

**Parameter:**
| Parameter | Typ | Beschreibung |
|-----------|-----|--------------|
| X1, Y1, Z1 | double | Startpunkt (Meter) |
| X2, Y2, Z2 | double | Endpunkt (Meter) |

**Beispiel:**
```python
# Linie von (0,0) nach (100,50) mm
sw.sketch.line(0, 0, 100, 50)
```

---

### Kreis (CreateCircle)

```python
# API-Methode
SketchManager.CreateCircle(Xc, Yc, Zc, Xp, Yp, Zp)

# Mit sw_automation.py
sw.sketch.circle(cx, cy, diameter=100)  # oder radius=50
```

**Parameter:**
| Parameter | Typ | Beschreibung |
|-----------|-----|--------------|
| Xc, Yc, Zc | double | Zentrum (Meter) |
| Xp, Yp, Zp | double | Punkt auf dem Kreis (Meter) |

**Beispiel:**
```python
# Kreis mit Durchmesser 100mm im Ursprung
sw.sketch.circle(diameter=100)

# Kreis mit Radius 25mm bei (50, 30)
sw.sketch.circle(cx=50, cy=30, radius=25)
```

---

### Rechteck (CreateCornerRectangle)

```python
# API-Methode
SketchManager.CreateCornerRectangle(X1, Y1, Z1, X2, Y2, Z2)

# Mit sw_automation.py
sw.sketch.rectangle(x1, y1, x2, y2)
sw.sketch.rectangle_centered(width, height)
```

**Parameter:**
| Parameter | Typ | Beschreibung |
|-----------|-----|--------------|
| X1, Y1, Z1 | double | Erste Ecke (Meter) |
| X2, Y2, Z2 | double | Gegenüberliegende Ecke (Meter) |

**Beispiele:**
```python
# Rechteck von (0,0) nach (100,50)
sw.sketch.rectangle(0, 0, 100, 50)

# Zentriertes Rechteck 100x50mm
sw.sketch.rectangle_centered(width=100, height=50)

# Zentriertes Rechteck bei (20,30)
sw.sketch.rectangle_centered(width=80, height=40, cx=20, cy=30)
```

---

### Bogen (CreateArc)

```python
# API-Methode
SketchManager.CreateArc(Xc, Yc, Zc, Xs, Ys, Zs, Xe, Ye, Ze, Direction)

# Mit sw_automation.py
sw.sketch.arc(cx, cy, radius, start_angle, end_angle)
```

**Parameter:**
| Parameter | Typ | Beschreibung |
|-----------|-----|--------------|
| Xc, Yc, Zc | double | Bogenzentrum (Meter) |
| Xs, Ys, Zs | double | Startpunkt (Meter) |
| Xe, Ye, Ze | double | Endpunkt (Meter) |
| Direction | short | 1 = gegen Uhrzeigersinn, -1 = im Uhrzeigersinn |

**Beispiel:**
```python
# Halbkreis oben
sw.sketch.arc(cx=0, cy=0, radius=50, start_angle=0, end_angle=180)

# Viertelkreis
sw.sketch.arc(cx=0, cy=0, radius=30, start_angle=0, end_angle=90)
```

---

### Drei-Punkt-Bogen (Create3PointArc)

```python
# API-Methode
SketchManager.Create3PointArc(X1, Y1, Z1, X2, Y2, Z2, X3, Y3, Z3)

# Mit sw_automation.py
sw.sketch.three_point_arc(x1, y1, x2, y2, x3, y3)
```

**Parameter:**
| Parameter | Typ | Beschreibung |
|-----------|-----|--------------|
| X1, Y1, Z1 | double | Startpunkt (Meter) |
| X2, Y2, Z2 | double | Punkt auf dem Bogen (Meter) |
| X3, Y3, Z3 | double | Endpunkt (Meter) |

**Beispiel:**
```python
# Bogen durch drei Punkte
sw.sketch.three_point_arc(0, 0, 25, 25, 50, 0)
```

---

### Ellipse (CreateEllipse)

```python
# API-Methode
SketchManager.CreateEllipse(Xc, Yc, Zc, Xa, Ya, Za, Xb, Yb, Zb)

# Mit sw_automation.py
sw.sketch.ellipse(cx, cy, major_radius, minor_radius)
# oder
sw.sketch.ellipse(cx, cy, major_diameter=100, minor_diameter=50)
```

**Parameter:**
| Parameter | Typ | Beschreibung |
|-----------|-----|--------------|
| Xc, Yc, Zc | double | Zentrum (Meter) |
| Xa, Ya, Za | double | Punkt auf Hauptachse (Meter) |
| Xb, Yb, Zb | double | Punkt auf Nebenachse (Meter) |

**Beispiele:**
```python
# Ellipse mit Radien
sw.sketch.ellipse(cx=0, cy=0, major_radius=50, minor_radius=25)

# Ellipse mit Durchmessern
sw.sketch.ellipse(cx=0, cy=0, major_diameter=100, minor_diameter=50)

# Ellipse an anderer Position
sw.sketch.ellipse(cx=30, cy=20, major_radius=40, minor_radius=20)
```

---

### Center Rectangle (CreateCenterRectangle)

```python
# API-Methode
SketchManager.CreateCenterRectangle(Xc, Yc, Zc, Xp, Yp, Zp)

# Mit sw_automation.py
sw.sketch.center_rectangle(cx, cy, width, height)
```

**Beschreibung:** Erstellt ein Rechteck zentriert um einen Mittelpunkt.

**Beispiel:**
```python
# Zentriertes Rechteck 80x40mm bei Ursprung
sw.sketch.center_rectangle(cx=0, cy=0, width=80, height=40)

# Zentriertes Rechteck bei (50, 30)
sw.sketch.center_rectangle(cx=50, cy=30, width=60, height=30)
```

---

## Erweiterte Formen

### Polygon

```python
# Mit sw_automation.py
sw.sketch.polygon(cx, cy, radius, sides)
```

**Parameter:**
| Parameter | Typ | Beschreibung |
|-----------|-----|--------------|
| cx, cy | float | Zentrum in mm |
| radius | float | Umkreisradius in mm |
| sides | int | Anzahl der Seiten |

**Beispiele:**
```python
# Sechseck mit Umkreisradius 50mm
sw.sketch.polygon(cx=0, cy=0, radius=50, sides=6)

# Dreieck
sw.sketch.polygon(cx=0, cy=0, radius=40, sides=3)

# Achteck
sw.sketch.polygon(cx=0, cy=0, radius=60, sides=8)
```

---

### Langloch (Slot)

```python
# Mit sw_automation.py
sw.sketch.slot(x1, y1, x2, y2, width)
```

**Parameter:**
| Parameter | Typ | Beschreibung |
|-----------|-----|--------------|
| x1, y1 | float | Start der Mittellinie in mm |
| x2, y2 | float | Ende der Mittellinie in mm |
| width | float | Breite des Langlochs in mm |

**Beispiel:**
```python
# Horizontales Langloch 80mm lang, 20mm breit
sw.sketch.slot(x1=-40, y1=0, x2=40, y2=0, width=20)

# Vertikales Langloch
sw.sketch.slot(x1=0, y1=-30, x2=0, y2=30, width=15)
```

---

## Weitere API-Methoden

### CreateCenterRectangle
Rechteck um Zentrum mit Breite und Höhe.

```python
SketchManager.CreateCenterRectangle(Xc, Yc, Zc, Xp, Yp, Zp)
```

### CreateEllipse
Ellipse mit Zentrum und zwei Radien.

```python
SketchManager.CreateEllipse(Xc, Yc, Zc, Xa, Ya, Za, Xb, Yb, Zb)
```

### Spline (CreateSpline2)

```python
# API-Methode
SketchManager.CreateSpline2(PointData, Closed)

# Mit sw_automation.py
sw.sketch.spline(points, closed=False)
```

**Parameter:**
| Parameter | Typ | Beschreibung |
|-----------|-----|--------------|
| points | list | Liste von (x, y) Tupeln in mm |
| closed | bool | True für geschlossenen Spline |

**Beispiele:**
```python
# Offener Spline
points = [(0, 0), (20, 30), (50, 20), (80, 40), (100, 0)]
sw.sketch.spline(points)

# Geschlossener Spline (ergibt geschlossene Kurve)
points = [(0, 0), (50, 30), (100, 0), (50, -30)]
sw.sketch.spline(points, closed=True)
```

---

## Sketch-Beziehungen (Relations)

Beziehungen fixieren Sketch-Elemente zueinander.

### add_relation()

```python
sw.sketch.add_relation(relation_type)
```

**Verfügbare Beziehungen:**

| Deutsch | Englisch | Beschreibung |
|---------|----------|--------------|
| horizontal | horizontal | Linie/Punkte horizontal |
| vertikal | vertical | Linie/Punkte vertikal |
| koinzident | coincident | Punkte übereinander |
| tangential | tangent | Tangentiale Berührung |
| senkrecht | perpendicular | Rechtwinklig |
| parallel | parallel | Parallel zueinander |
| konzentrisch | concentric | Gleicher Mittelpunkt |
| gleich | equal | Gleiche Länge/Radius |
| fixiert | fix | Position fixieren |

**Wichtig:** Sketch-Elemente müssen vor dem Hinzufügen der Beziehung selektiert sein!

**Beispiel:**
```python
sw.new_sketch("Front")

# Zwei Linien zeichnen
sw.sketch.line(0, 0, 50, 0)
sw.sketch.line(50, 0, 50, 30)

# Linien selektieren und als senkrecht markieren
# (Selektion muss manuell oder per API erfolgen)
sw.sketch.add_relation("perpendicular")

sw.end_sketch()
```

---

## Workflow-Beispiel

```python
from sw_automation import SolidWorksAutomation

sw = SolidWorksAutomation()

# 1. Sketch auf Front-Ebene starten
sw.new_sketch("Front")

# 2. Formen zeichnen
sw.sketch.rectangle_centered(100, 80)  # Außenkontur
sw.sketch.circle(cx=30, cy=20, diameter=20)  # Bohrung 1
sw.sketch.circle(cx=-30, cy=20, diameter=20)  # Bohrung 2
sw.sketch.circle(cx=0, cy=-20, diameter=15)  # Bohrung 3

# 3. Sketch beenden
sw.end_sketch()

# 4. Speichern
sw.save()
```

---

## Tipps

1. **Geschlossene Konturen**: Für Extrusionen müssen Skizzen geschlossen sein
2. **Überschneidungen vermeiden**: Linien sollten sich nicht überschneiden
3. **Beziehungen**: API fügt automatisch Beziehungen hinzu (z.B. Horizonal/Vertikal)
4. **Performance**: `AddToDB = True` für schnelleres Zeichnen vieler Elemente

---

## Fehlersuche

| Problem | Ursache | Lösung |
|---------|---------|--------|
| Nichts gezeichnet | Sketch nicht aktiv | `new_sketch()` aufrufen |
| Falsche Größe | Einheiten nicht konvertiert | mm durch 1000 teilen |
| Sketch leer nach Feature | Sketch wurde verbraucht | Neuen Sketch starten |
| CreateLine gibt None | Ungültige Koordinaten | Punkte prüfen |
