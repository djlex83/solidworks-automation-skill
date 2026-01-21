# Feature Operations Reference

## Übersicht

Diese Referenz dokumentiert alle verfügbaren 3D-Feature-Operationen für die SolidWorks-Automatisierung.

## Wichtige Hinweise

### Voraussetzungen für Features
1. Ein **geschlossener Sketch** muss existieren
2. Der Sketch muss **beendet** sein (nicht mehr aktiv)
3. Einheiten sind in **Metern** (automatisch konvertiert)

### Feature-Typen
- **Boss/Base**: Fügt Material hinzu
- **Cut**: Entfernt Material
- **Pattern**: Wiederholt Features

---

## Extrusion (Boss/Base)

### FeatureExtrusion3

Extrudiert einen Sketch in die Tiefe.

```python
# Mit sw_automation.py
sw.feature.extrude(depth=20)  # 20mm tief
sw.feature.extrude(depth=20, direction=-1)  # Umgekehrte Richtung
sw.feature.extrude(depth=20, direction=0)  # Beidseitig
sw.feature.extrude(depth=20, draft_angle=5)  # Mit Anzug
```

**Parameter:**
| Parameter | Typ | Beschreibung |
|-----------|-----|--------------|
| depth | float | Extrusionstiefe in mm |
| direction | int | 1=normal, -1=umgekehrt, 0=beidseitig |
| draft_angle | float | Anzugswinkel in Grad (optional) |

**Vollständiges Beispiel:**
```python
from sw_automation import SolidWorksAutomation

sw = SolidWorksAutomation()

# Sketch erstellen
sw.new_sketch("Front")
sw.sketch.rectangle_centered(100, 50)
sw.end_sketch()

# Extrudieren
sw.feature.extrude(depth=30)

sw.save()
```

### End-Typen (API-Konstanten)

| Typ | Wert | Beschreibung |
|-----|------|--------------|
| swEndCondBlind | 0 | Feste Tiefe |
| swEndCondThroughAll | 1 | Durch alles |
| swEndCondThroughAllBoth | 2 | Durch alles (beidseitig) |
| swEndCondUpToVertex | 3 | Bis zu Punkt |
| swEndCondUpToSurface | 4 | Bis zu Fläche |
| swEndCondOffsetFromSurface | 5 | Offset von Fläche |
| swEndCondMidPlane | 6 | Mittelebene |
| swEndCondUpToBody | 7 | Bis zu Körper |

---

## Schnitt (Cut)

### FeatureCut4

Entfernt Material durch Extrusion einer Skizze.

```python
# Mit sw_automation.py
sw.feature.cut(depth=10)  # 10mm tief schneiden
sw.feature.cut(depth=10, through_all=True)  # Durch alles
sw.feature.cut(depth=10, direction=-1)  # Umgekehrte Richtung
```

**Parameter:**
| Parameter | Typ | Beschreibung |
|-----------|-----|--------------|
| depth | float | Schnitttiefe in mm |
| direction | int | 1=normal, -1=umgekehrt |
| through_all | bool | True=durch alles schneiden |

**Beispiel: Tasche erstellen**
```python
sw = SolidWorksAutomation()

# Basis erstellen
sw.new_sketch("Front")
sw.sketch.rectangle_centered(100, 80)
sw.end_sketch()
sw.feature.extrude(depth=30)

# Tasche ausschneiden
sw.new_sketch("Front")
sw.sketch.rectangle_centered(60, 40)
sw.end_sketch()
sw.feature.cut(depth=15)

sw.save()
```

---

## Bohrungen

### Einfache Bohrung (als Cut)

```python
sw.new_sketch("Front")
sw.sketch.circle(cx=30, cy=0, diameter=10)
sw.end_sketch()
sw.feature.cut(depth=20)
```

### Kreisförmiges Bohrungsmuster

```python
# Mit sw_automation.py
sw.feature.circular_hole_pattern(
    num_holes=8,           # Anzahl der Bohrungen
    hole_diameter=10,      # Durchmesser in mm
    pitch_circle_diameter=100,  # Lochkreis in mm
    hole_depth=15,         # Tiefe in mm
    start_angle=0          # Startwinkel in Grad
)
```

**Beispiel: Flansch mit Bohrungen**
```python
sw = SolidWorksAutomation()

# Zylinder erstellen
sw.new_sketch("Front")
sw.sketch.circle(diameter=150)
sw.end_sketch()
sw.feature.extrude(depth=20)

# 6 Bohrungen auf Lochkreis
sw.feature.circular_hole_pattern(
    num_holes=6,
    hole_diameter=12,
    pitch_circle_diameter=120,
    hole_depth=20
)

sw.save()
```

---

## Fase (Chamfer)

### InsertFeatureChamfer

Fügt Fasen an Kanten hinzu.

```python
# Mit sw_automation.py
sw.feature.chamfer(distance=3)  # 45° Fase, 3mm
sw.feature.chamfer(distance=5, angle=30)  # 30° Fase, 5mm
```

**Parameter:**
| Parameter | Typ | Beschreibung |
|-----------|-----|--------------|
| distance | float | Fasenabstand in mm |
| angle | float | Fasenwinkel in Grad (Standard: 45) |

**Hinweis:** Kanten müssen vorher selektiert werden!

```python
# Manuelle Kantenselektion erforderlich
# In SolidWorks: Kante anklicken, dann:
sw.feature.chamfer(distance=2)
```

### Fasen-Typen (API)

| Typ | Wert | Beschreibung |
|-----|------|--------------|
| swChamferSymmetric | 0 | Symmetrisch (eine Distanz) |
| swChamferTwoDistances | 1 | Zwei Distanzen |
| swChamferDistanceAngle | 2 | Distanz und Winkel |

---

## Verrundung (Fillet)

### FeatureFillet3

Rundet Kanten ab.

```python
# Mit sw_automation.py
sw.feature.fillet(radius=5)  # 5mm Radius
```

**Parameter:**
| Parameter | Typ | Beschreibung |
|-----------|-----|--------------|
| radius | float | Verrundungsradius in mm |

**Hinweis:** Kanten müssen vorher selektiert werden!

```python
# Nach Kantenselektion:
sw.feature.fillet(radius=3)
```

---

## Muster (Patterns)

### Linear Pattern

Wiederholt ein Feature in einer Linie.

```python
# Mit sw_automation.py
sw.feature.linear_pattern(
    direction="X",  # oder "Y", "Z"
    count=5,        # Anzahl inkl. Original
    spacing=20      # Abstand in mm
)
```

**Parameter:**
| Parameter | Typ | Beschreibung |
|-----------|-----|--------------|
| direction | str | "X", "Y" oder "Z" |
| count | int | Anzahl der Kopien |
| spacing | float | Abstand zwischen Kopien in mm |

### Circular Pattern (API)

```python
# API-Methode
FeatureManager.FeatureCirPattern4(
    Number,        # Anzahl
    Spacing,       # Winkelabstand in Radiant
    FlipDirection, # Richtung umkehren
    ...
)
```

---

## Drehkörper (Revolve)

### Revolve (FeatureRevolve2)

Erstellt einen Rotationskörper aus einem Profil.

```python
# Mit sw_automation.py
sw.feature.revolve(angle=360, axis="Y", direction=1)
```

**Parameter:**
| Parameter | Typ | Beschreibung |
|-----------|-----|--------------|
| angle | float | Drehwinkel in Grad (Standard: 360) |
| axis | str | Drehachse "X", "Y", "Z" |
| direction | int | 1=normal, -1=umgekehrt, 0=beidseitig |

**Wichtig:** Der Sketch muss eine Mittellinie oder Achse enthalten!

**Beispiel: Zylinder durch Rotation**
```python
sw = SolidWorksAutomation()
sw.new_sketch("Front")

# Rechteckiges Profil (Hälfte des Zylinders)
sw.sketch.rectangle(0, 0, 25, 50)

# Mittellinie für Rotation (Y-Achse)
sw.sketch.line(0, -10, 0, 60)

sw.end_sketch()
sw.feature.revolve(angle=360, axis="Y")
sw.save()
```

### Revolve Cut

Entfernt Material durch Rotation.

```python
sw.feature.revolve_cut(angle=360, direction=1)
```

**Beispiel: Nut in Welle**
```python
# Profil für die Nut
sw.new_sketch("Front")
sw.sketch.rectangle(20, 10, 25, 15)
sw.sketch.line(0, 0, 0, 50)  # Mittellinie
sw.end_sketch()

sw.feature.revolve_cut(angle=360)
```

---

## Referenzgeometrie

### Reference Plane (Referenzebene)

Erstellt eine neue Ebene parallel zu einer bestehenden.

```python
# Mit sw_automation.py
sw.feature.reference_plane(offset=50, base_plane="Front")
```

**Parameter:**
| Parameter | Typ | Beschreibung |
|-----------|-----|--------------|
| offset | float | Abstand in mm |
| base_plane | str | "Front", "Top", "Right" oder Ebenenname |

**Beispiel:**
```python
# Neue Ebene 50mm vor der Front-Ebene
sw.feature.reference_plane(offset=50, base_plane="Front")

# Deutsche Bezeichnung funktioniert auch
sw.feature.reference_plane(offset=30, base_plane="Vorne")
```

---

## Spiegeln (Mirror)

### Mirror Feature

Spiegelt Features an einer Ebene.

```python
# Mit sw_automation.py
sw.feature.mirror(plane="Right")
```

**Parameter:**
| Parameter | Typ | Beschreibung |
|-----------|-----|--------------|
| plane | str | Spiegelebene - "Front", "Top", "Right" |

**Hinweis:** Features müssen vorher selektiert sein!

**Beispiel:**
```python
# Feature erstellen
sw.new_sketch("Front")
sw.sketch.rectangle(10, 10, 40, 30)
sw.end_sketch()
sw.feature.extrude(20)

# Feature selektieren und spiegeln
# (Selektion über Feature-Name oder UI)
sw.feature.mirror(plane="Right")
```

---

## Weitere Feature-Methoden

### Revolve (Drehkörper)

```python
# API-Methode
FeatureManager.FeatureRevolve2(
    SingleDir,     # Einzelrichtung
    IsSolid,       # Als Volumenkörper
    IsThin,        # Dünnwandig
    IsCut,         # Als Schnitt
    ReverseDir,    # Richtung umkehren
    BothDirectionUpToSameEntity,
    Dir1Type,      # End-Typ Richtung 1
    Dir2Type,      # End-Typ Richtung 2
    Dir1Angle,     # Winkel Richtung 1 (Radiant)
    Dir2Angle,     # Winkel Richtung 2 (Radiant)
    OffsetReverse1,
    OffsetReverse2,
    OffsetDistance1,
    OffsetDistance2,
    ThinType,
    ThinThickness1,
    ThinThickness2,
    Merge,
    UseFeatScope,
    UseAutoSelect
)
```

### Sweep (Austragung)

```python
# API-Methode (vereinfacht)
FeatureManager.InsertProtrusionSwept4(
    Propagate,        # Tangentiale Propagation
    Alignment,        # Ausrichtung
    TwistCtrlOption,  # Verdrehungskontrolle
    ...
)
```

### Loft (Ausformung)

```python
# API-Methode (vereinfacht)
FeatureManager.InsertProtrusionLoft(
    Closed,           # Geschlossenes Profil
    Thin,             # Dünnwandig
    ...
)
```

---

## Workflow: Komplexes Teil

```python
from sw_automation import SolidWorksAutomation

sw = SolidWorksAutomation()

# 1. Grundkörper
sw.new_sketch("Front")
sw.sketch.rectangle_centered(100, 60)
sw.end_sketch()
sw.feature.extrude(depth=40)

# 2. Tasche oben
sw.new_sketch("Top")  # Oben-Ebene
sw.sketch.rectangle_centered(60, 30)
sw.end_sketch()
sw.feature.cut(depth=20)

# 3. Durchgangsbohrung
sw.new_sketch("Front")
sw.sketch.circle(cx=0, cy=0, diameter=15)
sw.end_sketch()
sw.feature.cut(through_all=True)

# 4. Fasen (nach manueller Kantenselektion)
# sw.feature.chamfer(distance=3)

sw.save()
```

---

## Selektion (SelectionHelper)

Die `SelectionHelper`-Klasse erleichtert die Auswahl von Geometrie.

### Methoden

```python
# Objekt nach Name auswählen
sw.selection.select_by_id("Boss-Extrude1", "BODYFEATURE")
sw.selection.select_by_id("Front Plane", "PLANE")

# Fläche/Kante an Position auswählen (Raycast)
sw.selection.select_face_at(x=50, y=25, z=10)
sw.selection.select_edge_at(x=0, y=0, z=20)

# Alle Kanten auswählen
sw.selection.select_all_edges()

# Selektion aufheben
sw.selection.clear_selection()

# Anzahl selektierter Objekte
count = sw.selection.get_selection_count()
```

### Objekttypen für select_by_id

| Typ | Beschreibung |
|-----|--------------|
| PLANE | Ebene |
| FACE | Fläche |
| EDGE | Kante |
| VERTEX | Eckpunkt |
| BODYFEATURE | Feature (Extrusion, Cut, etc.) |
| SKETCH | Skizze |

---

## Dokument-Management (DocumentManager)

### Neues Dokument erstellen

```python
sw = SolidWorksAutomation(require_document=False)

# Neues Part
sw.documents.new_part()

# Neue Baugruppe
sw.documents.new_assembly()
```

### Dokument öffnen

```python
sw.documents.open(r"C:\Pfad\zur\Datei.sldprt")
```

### Dokument schließen

```python
# Ohne Speichern
sw.documents.close()

# Mit Speichern
sw.documents.close(save=True)

# Alle schließen
sw.documents.close_all()
```

---

## Fehlersuche

| Problem | Ursache | Lösung |
|---------|---------|--------|
| Feature wird nicht erstellt | Sketch nicht geschlossen | Konturen schließen |
| Extrusion in falsche Richtung | Direction falsch | direction=-1 versuchen |
| Cut schneidet nichts | Sketch außerhalb des Körpers | Sketch-Position prüfen |
| Chamfer/Fillet versagt | Keine Kanten selektiert | Kanten vorher auswählen |
| Pattern inkorrekt | Feature nicht selektiert | Feature auswählen vor Pattern |
| Revolve versagt | Keine Mittellinie | Linie auf Achse hinzufügen |
| Mirror versagt | Keine Features selektiert | Features vorher auswählen |

---

## API-Konstanten (Auswahl)

### End Conditions
```
swEndCondBlind = 0
swEndCondThroughAll = 1
swEndCondMidPlane = 6
```

### Feature Types
```
swTnExtrude = 1
swTnCut = 2
swTnFillet = 3
swTnChamfer = 4
swTnPattern = 5
```

### Pattern Types
```
swLinearPattern = 0
swCircularPattern = 1
```
