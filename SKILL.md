---
name: solidworks-automation
description: |
  Automatisiert SolidWorks CAD-Software über Python und COM-Schnittstelle.
  Verwende diesen Skill wenn der Nutzer:
  - 2D Skizzen erstellen möchte (Linien, Kreise, Rechtecke, Ellipsen, Bögen, Splines)
  - 3D Features erstellen möchte (Extrusionen, Schnitte, Bohrungen, Fasen, Verrundungen)
  - Drehkörper erstellen möchte (Revolve - Zylinder, Kegel, Kugeln, Torus)
  - Muster erstellen möchte (Linear Pattern, Circular Pattern, Mirror)
  - Referenzgeometrie erstellen möchte (Ebenen, Achsen)
  - SolidWorks-Modelle automatisieren möchte
  - CAD-Operationen in natürlicher Sprache beschreibt (Deutsch oder Englisch)
  Trigger-Phrasen: "zeichne", "erstelle", "extrudiere", "bohre", "drehe", "rotiere", "spiegele", "draw", "create", "extrude", "hole", "revolve", "mirror", "SolidWorks", "CAD", "Skizze", "sketch", "Welle", "Zylinder", "Kegel"
  Voraussetzungen: Windows, SolidWorks 2015+, Python mit pywin32
---

# SolidWorks Automation Skill

Dieser Skill ermöglicht die Automatisierung von SolidWorks über natürliche Sprache.

## Voraussetzungen

- Windows-Betriebssystem
- SolidWorks 2015 oder neuer (muss laufen)
- Python 3.x mit pywin32: `pip install pywin32`
- Ein geöffnetes Part-Dokument in SolidWorks

## Workflow

1. **Nutzer beschreibt** was erstellt werden soll (z.B. "Zeichne ein Rechteck 100x50mm und extrudiere es 20mm")
2. **Claude generiert** Python-Code basierend auf diesem Skill
3. **Code wird ausgeführt** in SolidWorks
4. **Ergebnis** erscheint im SolidWorks-Modell

## Wichtige API-Hinweise

### Einheiten
- SolidWorks API verwendet **Meter**, nicht Millimeter
- Immer `mm / 1000` rechnen vor API-Aufruf
- Beispiel: 100mm = 0.1 Meter

### Sketch-Operationen
- Sketch muss **aktiv** sein vor Zeichenoperationen
- `InsertSketch()` startet neuen Sketch auf ausgewählter Ebene
- `InsertSketch()` beendet auch aktiven Sketch

### Feature-Operationen
- Features brauchen geschlossene Skizzen
- Nach Sketch: `InsertSketch()` zum Beenden
- Dann Feature-Methode aufrufen

## Verfügbare Operationen

### 2D Skizzen (SketchManager)

| Operation | Methode | Beispiel |
|-----------|---------|----------|
| Linie | `sw.sketch.line(x1, y1, x2, y2)` | Gerade zwischen zwei Punkten |
| Kreis | `sw.sketch.circle(diameter=100)` | Kreis mit Durchmesser |
| Rechteck | `sw.sketch.rectangle_centered(width, height)` | Zentriertes Rechteck |
| Ellipse | `sw.sketch.ellipse(major_radius, minor_radius)` | Ellipse |
| Bogen | `sw.sketch.arc(cx, cy, radius, start, end)` | Kreisbogen |
| 3-Punkt-Bogen | `sw.sketch.three_point_arc(x1,y1,x2,y2,x3,y3)` | Bogen durch 3 Punkte |
| Spline | `sw.sketch.spline(points, closed)` | Freiformkurve |
| Polygon | `sw.sketch.polygon(cx, cy, radius, sides)` | Regelmäßiges Vieleck |
| Langloch | `sw.sketch.slot(x1, y1, x2, y2, width)` | Slot/Langloch |
| Beziehung | `sw.sketch.add_relation("horizontal")` | Sketch-Constraints |

### 3D Features (FeatureManager)

| Operation | Methode | Beschreibung |
|-----------|---------|--------------|
| Extrusion | `sw.feature.extrude(depth)` | Profil in Tiefe ziehen |
| Schnitt | `sw.feature.cut(depth)` | Material entfernen |
| Drehkörper | `sw.feature.revolve(angle)` | Rotation um Achse |
| Dreh-Schnitt | `sw.feature.revolve_cut(angle)` | Rotationsschnitt |
| Fase | `sw.feature.chamfer(distance)` | Kante abschrägen |
| Verrundung | `sw.feature.fillet(radius)` | Kante abrunden |
| Linear Pattern | `sw.feature.linear_pattern(dir, count, spacing)` | Lineares Muster |
| Bohrungsmuster | `sw.feature.circular_hole_pattern(...)` | Kreisförmiges Lochmuster |
| Spiegeln | `sw.feature.mirror(plane)` | Feature spiegeln |
| Referenzebene | `sw.feature.reference_plane(offset)` | Neue Ebene erstellen |

### Quick-Funktionen

| Funktion | Beschreibung |
|----------|--------------|
| `quick_box(w, h, d)` | Schnell einen Quader erstellen |
| `quick_cylinder(d, h)` | Schnell einen Zylinder erstellen |
| `quick_pipe(outer, inner, length)` | Rohr/Hohlzylinder |
| `quick_revolve(points, axis, angle)` | Drehkörper aus Profil |
| `quick_plate_with_holes(...)` | Platte mit Bohrungen |

## Code-Generierung

Wenn du Code generierst, verwende immer das Script aus `scripts/sw_automation.py`.

### Standard-Template

```python
from sw_automation import SolidWorksAutomation

# Verbindung herstellen
sw = SolidWorksAutomation()

# Operationen ausführen
# ... (spezifische Operationen hier)

# Speichern
sw.save()
```

### Beispiel: Rechteck extrudieren

```python
from sw_automation import SolidWorksAutomation

sw = SolidWorksAutomation()

# Rechteck zeichnen (100x50mm, zentriert)
sw.sketch.rectangle_centered(width=100, height=50)

# Extrudieren (20mm tief)
sw.feature.extrude(depth=20)

sw.save()
```

### Beispiel: Kreis mit Bohrungen

```python
from sw_automation import SolidWorksAutomation

sw = SolidWorksAutomation()

# Kreis zeichnen (Durchmesser 200mm)
sw.new_sketch("Front")
sw.sketch.circle(diameter=200)
sw.end_sketch()

# Extrudieren
sw.feature.extrude(depth=10)

# 8 Bohrungen auf Lochkreis
sw.feature.circular_hole_pattern(
    num_holes=8,
    hole_diameter=10,
    pitch_circle_diameter=150,
    hole_depth=10
)

sw.save()
```

### Beispiel: Drehkörper (Kegel)

```python
from sw_automation import SolidWorksAutomation

sw = SolidWorksAutomation()
sw.new_sketch("Front")

# Dreieckiges Profil für Kegel
sw.sketch.line(0, 0, 30, 0)   # Basis
sw.sketch.line(30, 0, 0, 60)  # Schräge
sw.sketch.line(0, 60, 0, 0)   # Schließen

# Mittellinie für Rotation
sw.sketch.line(0, -10, 0, 70)

sw.end_sketch()
sw.feature.revolve(angle=360)
sw.save()
```

### Beispiel: Quick-Funktionen

```python
from sw_automation import quick_box, quick_cylinder, quick_pipe

# Quader 100x50x30mm
quick_box(100, 50, 30)

# Zylinder Ø80mm, Höhe 50mm
quick_cylinder(80, 50)

# Rohr Außen Ø50, Innen Ø40, Länge 100mm
quick_pipe(50, 40, 100)
```

## Referenzen

Für detaillierte API-Dokumentation siehe:
- `references/sketch-operations.md` - Alle Skizzen-Methoden
- `references/feature-operations.md` - Alle Feature-Methoden
- `references/examples.md` - Weitere Beispiele

## Sprachunterstützung

Der Skill versteht Deutsch und Englisch:

**Deutsch:**
- "Zeichne ein Rechteck 100x50mm"
- "Erstelle eine Extrusion 20mm tief"
- "Füge 8 Bohrungen M10 auf Lochkreis 200mm hinzu"

**English:**
- "Draw a rectangle 100x50mm"
- "Create an extrusion 20mm deep"
- "Add 8 M10 holes on pitch circle 200mm"

## Fehlerbehandlung

Häufige Fehler und Lösungen:

| Fehler | Ursache | Lösung |
|--------|---------|--------|
| "Failed to connect" | SolidWorks nicht gestartet | SolidWorks starten |
| "No active document" | Kein Part geöffnet | Part-Dokument öffnen |
| "Sketch not active" | Sketch nicht gestartet | `InsertSketch()` aufrufen |
| "Feature creation failed" | Sketch nicht geschlossen | Sketch beenden vor Feature |
