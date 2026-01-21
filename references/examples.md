# Beispiele für SolidWorks Automation

Diese Datei enthält praktische Beispiele für die SolidWorks-Automatisierung.

---

## Einfache Beispiele

### 1. Quader (Box)

**Natürliche Sprache:**
> "Erstelle einen Quader 100x50x30mm"

**Code:**
```python
from sw_automation import SolidWorksAutomation

sw = SolidWorksAutomation()

# Rechteck zeichnen
sw.new_sketch("Front")
sw.sketch.rectangle_centered(width=100, height=50)
sw.end_sketch()

# Extrudieren
sw.feature.extrude(depth=30)

sw.save()
```

**Oder schnell:**
```python
from sw_automation import quick_box
quick_box(100, 50, 30)
```

---

### 2. Zylinder

**Natürliche Sprache:**
> "Erstelle einen Zylinder mit Durchmesser 80mm und Höhe 50mm"

**Code:**
```python
from sw_automation import SolidWorksAutomation

sw = SolidWorksAutomation()

sw.new_sketch("Front")
sw.sketch.circle(diameter=80)
sw.end_sketch()

sw.feature.extrude(depth=50)

sw.save()
```

**Oder schnell:**
```python
from sw_automation import quick_cylinder
quick_cylinder(80, 50)
```

---

### 3. Rohr (Hohlzylinder)

**Natürliche Sprache:**
> "Erstelle ein Rohr: Außendurchmesser 60mm, Innendurchmesser 40mm, Höhe 100mm"

**Code:**
```python
from sw_automation import SolidWorksAutomation

sw = SolidWorksAutomation()

# Außenkreis
sw.new_sketch("Front")
sw.sketch.circle(diameter=60)
sw.end_sketch()
sw.feature.extrude(depth=100)

# Innenkreis ausschneiden
sw.new_sketch("Front")
sw.sketch.circle(diameter=40)
sw.end_sketch()
sw.feature.cut(through_all=True)

sw.save()
```

---

## Mittlere Beispiele

### 4. Platte mit Bohrungen

**Natürliche Sprache:**
> "Erstelle eine Platte 200x100x10mm mit 4 Bohrungen Ø12mm in den Ecken (20mm vom Rand)"

**Code:**
```python
from sw_automation import SolidWorksAutomation

sw = SolidWorksAutomation()

# Grundplatte
sw.new_sketch("Front")
sw.sketch.rectangle_centered(width=200, height=100)
sw.end_sketch()
sw.feature.extrude(depth=10)

# Positionen für Bohrungen (20mm vom Rand)
holes = [
    (200/2 - 20, 100/2 - 20),   # Oben rechts
    (-200/2 + 20, 100/2 - 20),  # Oben links
    (200/2 - 20, -100/2 + 20),  # Unten rechts
    (-200/2 + 20, -100/2 + 20)  # Unten links
]

# Bohrungen erstellen
for x, y in holes:
    sw.new_sketch("Front")
    sw.sketch.circle(cx=x, cy=y, diameter=12)
    sw.end_sketch()
    sw.feature.cut(through_all=True)

sw.save()
```

---

### 5. Flansch mit Lochkreis

**Natürliche Sprache:**
> "Erstelle einen Flansch: Ø150mm, 15mm dick, mit 8 Bohrungen M8 auf Lochkreis Ø120mm"

**Code:**
```python
from sw_automation import SolidWorksAutomation

sw = SolidWorksAutomation()

# Flanschkörper
sw.new_sketch("Front")
sw.sketch.circle(diameter=150)
sw.end_sketch()
sw.feature.extrude(depth=15)

# Zentralbohrung
sw.new_sketch("Front")
sw.sketch.circle(diameter=40)
sw.end_sketch()
sw.feature.cut(through_all=True)

# 8 Bohrungen auf Lochkreis
sw.feature.circular_hole_pattern(
    num_holes=8,
    hole_diameter=8,  # M8
    pitch_circle_diameter=120,
    hole_depth=15
)

sw.save()
```

---

### 6. L-Profil (Winkel)

**Natürliche Sprache:**
> "Erstelle ein L-Profil: Schenkel 50x50mm, Wandstärke 5mm, Länge 200mm"

**Code:**
```python
from sw_automation import SolidWorksAutomation

sw = SolidWorksAutomation()

sw.new_sketch("Front")

# Außenkontur
sw.sketch.line(0, 0, 50, 0)      # Unten
sw.sketch.line(50, 0, 50, 5)    # Rechts unten
sw.sketch.line(50, 5, 5, 5)     # Innen horizontal
sw.sketch.line(5, 5, 5, 50)     # Innen vertikal
sw.sketch.line(5, 50, 0, 50)    # Oben
sw.sketch.line(0, 50, 0, 0)     # Links

sw.end_sketch()
sw.feature.extrude(depth=200)

sw.save()
```

---

## Komplexe Beispiele

### 7. Zahnrad (vereinfacht)

**Natürliche Sprache:**
> "Erstelle ein einfaches Zahnrad: 20 Zähne, Modul 3, Breite 15mm, Bohrung Ø20mm"

**Code:**
```python
from sw_automation import SolidWorksAutomation
import math

sw = SolidWorksAutomation()

# Zahnradparameter
z = 20       # Zähnezahl
m = 3        # Modul
b = 15       # Breite

# Berechnete Werte
d = m * z                    # Teilkreisdurchmesser
da = d + 2 * m               # Kopfkreisdurchmesser
df = d - 2.5 * m             # Fußkreisdurchmesser

# Vereinfachtes Zahnrad (Polygon mit Zähnen)
sw.new_sketch("Front")

# Fußkreis als Basis
sw.sketch.circle(diameter=df)

sw.end_sketch()
sw.feature.extrude(depth=b)

# Zentralbohrung
sw.new_sketch("Front")
sw.sketch.circle(diameter=20)
sw.end_sketch()
sw.feature.cut(through_all=True)

sw.save()

print(f"Zahnrad erstellt:")
print(f"  Teilkreis: Ø{d}mm")
print(f"  Kopfkreis: Ø{da}mm")
print(f"  Fußkreis: Ø{df}mm")
```

---

### 8. Gehäuse mit Tasche

**Natürliche Sprache:**
> "Erstelle ein Gehäuse 120x80x40mm mit Tasche 100x60x30mm, Wandstärke 10mm, 4 Befestigungsbohrungen M6"

**Code:**
```python
from sw_automation import SolidWorksAutomation

sw = SolidWorksAutomation()

# Außenmaße
L, B, H = 120, 80, 40
# Tasche
tL, tB, tH = 100, 60, 30
# Bohrungen
d_bolt = 6  # M6
edge = 10   # Abstand vom Rand

# Grundkörper
sw.new_sketch("Front")
sw.sketch.rectangle_centered(width=L, height=B)
sw.end_sketch()
sw.feature.extrude(depth=H)

# Tasche
sw.new_sketch("Top")
sw.sketch.rectangle_centered(width=tL, height=tB)
sw.end_sketch()
sw.feature.cut(depth=tH)

# 4 Befestigungsbohrungen
positions = [
    (L/2 - edge, B/2 - edge),
    (-L/2 + edge, B/2 - edge),
    (L/2 - edge, -B/2 + edge),
    (-L/2 + edge, -B/2 + edge)
]

for x, y in positions:
    sw.new_sketch("Top")
    sw.sketch.circle(cx=x, cy=y, diameter=d_bolt)
    sw.end_sketch()
    sw.feature.cut(through_all=True)

sw.save()
```

---

### 9. Stufenwelle

**Natürliche Sprache:**
> "Erstelle eine Stufenwelle: Ø40mm x 50mm, dann Ø30mm x 80mm, dann Ø25mm x 40mm"

**Code:**
```python
from sw_automation import SolidWorksAutomation

sw = SolidWorksAutomation()

# Stufen (Durchmesser, Länge)
stufen = [
    (40, 50),
    (30, 80),
    (25, 40)
]

# Erste Stufe (Basis)
sw.new_sketch("Front")
sw.sketch.circle(diameter=stufen[0][0])
sw.end_sketch()
sw.feature.extrude(depth=sum(l for d, l in stufen))

# Material entfernen für Stufen
offset = stufen[0][1]
for i in range(1, len(stufen)):
    d, l = stufen[i]
    d_prev = stufen[i-1][0]

    # Ring ausschneiden
    sw.new_sketch("Right")  # Von der Seite
    sw.sketch.circle(diameter=d_prev)
    # Innerer Kreis
    sw.sketch.circle(diameter=d)
    sw.end_sketch()

    # Tiefe berechnen...
    # (Vereinfacht - echte Implementierung komplexer)

    offset += l

sw.save()
```

---

## Deutsche Befehle → Code-Übersetzung

| Natürliche Sprache | Code |
|--------------------|------|
| "Zeichne ein Rechteck 100x50mm" | `sw.sketch.rectangle_centered(100, 50)` |
| "Erstelle einen Kreis Ø80mm" | `sw.sketch.circle(diameter=80)` |
| "Extrudiere 20mm tief" | `sw.feature.extrude(depth=20)` |
| "Schneide durch alles" | `sw.feature.cut(through_all=True)` |
| "Füge 8 Bohrungen M10 hinzu" | `sw.feature.circular_hole_pattern(num_holes=8, hole_diameter=10, ...)` |
| "3mm Fase" | `sw.feature.chamfer(distance=3)` |
| "5mm Radius verrunden" | `sw.feature.fillet(radius=5)` |

---

## English Commands → Code Translation

| Natural Language | Code |
|------------------|------|
| "Draw a rectangle 100x50mm" | `sw.sketch.rectangle_centered(100, 50)` |
| "Create a circle Ø80mm" | `sw.sketch.circle(diameter=80)` |
| "Extrude 20mm deep" | `sw.feature.extrude(depth=20)` |
| "Cut through all" | `sw.feature.cut(through_all=True)` |
| "Add 8 M10 holes on pitch circle" | `sw.feature.circular_hole_pattern(num_holes=8, hole_diameter=10, ...)` |
| "3mm chamfer" | `sw.feature.chamfer(distance=3)` |
| "5mm fillet" | `sw.feature.fillet(radius=5)` |

---

---

## Drehkörper-Beispiele (NEU)

### 10. Welle (einfacher Zylinder durch Rotation)

**Natürliche Sprache:**
> "Erstelle eine Welle Ø30mm, 150mm lang durch Rotation"

**Code:**
```python
from sw_automation import SolidWorksAutomation

sw = SolidWorksAutomation()
sw.new_sketch("Front")

# Halbes Rechteck (Profil)
sw.sketch.rectangle(0, 0, 15, 150)  # Radius 15 = Ø30

# Mittellinie (Y-Achse)
sw.sketch.line(0, -10, 0, 160)

sw.end_sketch()
sw.feature.revolve(angle=360, axis="Y")
sw.save()
```

---

### 11. Kegel

**Natürliche Sprache:**
> "Erstelle einen Kegel mit Basisdurchmesser 60mm und Höhe 80mm"

**Code:**
```python
from sw_automation import SolidWorksAutomation

sw = SolidWorksAutomation()
sw.new_sketch("Front")

# Dreieckiges Profil
sw.sketch.line(0, 0, 30, 0)   # Basis (Radius 30)
sw.sketch.line(30, 0, 0, 80)  # Schräge
sw.sketch.line(0, 80, 0, 0)   # Schließen (Achse)

# Mittellinie
sw.sketch.line(0, -10, 0, 90)

sw.end_sketch()
sw.feature.revolve(angle=360)
sw.save()
```

**Oder mit quick_revolve:**
```python
from sw_automation import quick_revolve

quick_revolve([(0, 0), (30, 0), (0, 80)], axis="Y", angle=360)
```

---

### 12. Kugel

**Natürliche Sprache:**
> "Erstelle eine Kugel mit Durchmesser 100mm"

**Code:**
```python
from sw_automation import SolidWorksAutomation

sw = SolidWorksAutomation()
sw.new_sketch("Front")

# Halbkreis-Profil
sw.sketch.arc(cx=0, cy=0, radius=50, start_angle=-90, end_angle=90)
sw.sketch.line(0, -50, 0, 50)  # Schließen entlang Achse

# Mittellinie
sw.sketch.line(0, -60, 0, 60)

sw.end_sketch()
sw.feature.revolve(angle=360)
sw.save()
```

---

### 13. Torus (Donut)

**Natürliche Sprache:**
> "Erstelle einen Torus mit Hauptdurchmesser 100mm und Rohrdurchmesser 20mm"

**Code:**
```python
from sw_automation import SolidWorksAutomation

sw = SolidWorksAutomation()
sw.new_sketch("Front")

# Kreisprofil (versetzt vom Ursprung)
# Mittelpunkt bei x=50 (Hauptradius), Rohrradius=10
sw.sketch.circle(cx=50, cy=0, diameter=20)

# Mittellinie (Y-Achse)
sw.sketch.line(0, -20, 0, 20)

sw.end_sketch()
sw.feature.revolve(angle=360, axis="Y")
sw.save()
```

---

## Ellipsen-Beispiele (NEU)

### 14. Elliptischer Zylinder

**Natürliche Sprache:**
> "Erstelle einen elliptischen Zylinder 80x40mm, 50mm hoch"

**Code:**
```python
from sw_automation import SolidWorksAutomation

sw = SolidWorksAutomation()
sw.new_sketch("Front")

sw.sketch.ellipse(cx=0, cy=0, major_radius=40, minor_radius=20)

sw.end_sketch()
sw.feature.extrude(depth=50)
sw.save()
```

---

## Quick-Funktionen (NEU)

### Rohr erstellen

```python
from sw_automation import quick_pipe

# Rohr: Außen Ø50, Innen Ø40, Länge 100mm
quick_pipe(outer_diameter=50, inner_diameter=40, length=100)
```

### Platte mit Bohrungen

```python
from sw_automation import quick_plate_with_holes

# Platte 200x100x10mm mit 4 Bohrungen Ø12mm
quick_plate_with_holes(
    length=200,
    width=100,
    thickness=10,
    hole_diameter=12,
    hole_positions=[(30, 30), (170, 30), (30, 70), (170, 70)]
)
```

### Drehkörper aus Profil

```python
from sw_automation import quick_revolve

# Vase-Form
profile = [
    (0, 0),
    (30, 0),
    (35, 20),
    (25, 50),
    (30, 80),
    (20, 100),
    (0, 100)
]
quick_revolve(profile, axis="Y", angle=360)
```

---

## Tipps für Claude

1. **Immer mit `from sw_automation import SolidWorksAutomation` beginnen**
2. **Sketch vor Zeichenoperationen starten**: `sw.new_sketch("Front")`
3. **Sketch vor Features beenden**: `sw.end_sketch()`
4. **Am Ende speichern**: `sw.save()`
5. **Einheiten sind immer mm** (Konvertierung geschieht automatisch)
6. **Für komplexe Formen mehrere Sketches verwenden**
7. **Für Drehkörper**: Immer Mittellinie hinzufügen!
8. **Quick-Funktionen** für häufige Formen nutzen
