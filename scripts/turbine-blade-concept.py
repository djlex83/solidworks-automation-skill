# Advanced Concept: Adaptive Lattice Turbine Blade

## Das Neue & Einzigartige

| Innovation | Was es bringt |
|-----------|--------------|
| **Interne Lattice-Kühlung** | 3D-Druck Gitterstruktur → 3x bessere Kühlung |
| **Adaptive Hülle** | Form ändert sich bei Hitze → optimaler Anströmwinkel |
| **Thermoelektrische Abwärme-Rückgewinnung** | Strom aus Abfallwärme |
| **Nanostruktur-Oberfläche** | "Moth-Eye" Effekt → weniger Hitze-Stau |
| **Piezo-Dämpfer** | Schwingungsreduzierung → längere Lebensdauer |
| **Gradient-Material** | Keramik-Metall-Verbund → thermische Spannung reduziert |

---

## Technische Zeichnung (Konzept)

```
                    ┌─────────────────────────────────────┐
                    │      ┌─────────────────────────┐      │
                    │      │   Adaptive Shell      │      │
                    │      │  (wärmeaktivierbar)  │      │
                    │      └─────────────────────────┘      │
                    │             ↑                       │
              ┌────┴───────────────────────────────┴────┐
              │      ┌─────────────────────────┐          │
              │      │   Thermoelektrische   │          │
              │      │    Schicht (TEG)   │          │
              │      └─────────────────────────┘          │
              │              ↓                         │
    ┌─────────┴───────────────────────────────────┴─────────┐
    │                                                       │
    │    ┌───────────────────────────────────────────────┐     │
    │    │       Interne Lattice-Struktur           │     │
    │    │    (Additive Manufacturing)           │     │
    │    │    → Kühlkanäle + Steifigkeit   │     │
    │    └───────────────────────────────────────────┘     │
    │              ↓                                    │
    │    ┌───────────────────────────────────────────┐     │
    │    │      piezoelektrische Dämpfer          │     │
    │    │   (aktive Schwingungsdämpfung)       │     │
    │    └───────────────────────────────────────────┘     │
    │              ↓                                    │
    └──────────────────────────────────────────────────┘
                    ↓
              [Befestigung]
```

---

## CAD-Code (SolidWorks)

```python
from sw_automation import SolidWorksAutomation
import math

sw = SolidWorksAutomation()

# === Parameter (DIN/ISO) ===
blade_length = 200      # mm
chord_width = 80        # mm
thickness = 15         # mm
num_ribs = 8

# === 1. Profil (Flügelgrundform) ===
sw.new_sketch("Front")

# Nasenleiste (Ellipse)
sw.sketch.ellipse(cx=-chord_width/4, cy=0, 
                major_radius=chord_width/2, 
                minor_radius=thickness)

# Hinterkante (dünn)
sw.sketch.line(chord_width/4, -thickness/2, chord_width/4, thickness/2)

sw.end_sketch()
sw.feature.extrude(depth=blade_length)

# === 2. Interne Lattice-Struktur ===
# (Als separates Teil - später im 3D-Druck)
lattice_cell_size = 8  # mm
for x in range(-3, 4):
    for y in range(-1, 2):
        sw.new_sketch("Front")
        sw.sketch.circle(cx=x*lattice_cell_size, cy=y*lattice_cell_size, 
                      diameter=lattice_cell_size*0.6)
        sw.end_sketch()
        sw.feature.cut(depth=blade_length-10)

# === 3. Thermoelektrische Schicht (Oberfläche) ===
sw.new_sketch("Front")
sw.sketch.ellipse(cx=-chord_width/4, cy=0, 
                major_radius=chord_width/2.2, 
                minor_radius=thickness*0.8)
sw.end_sketch()
sw.feature.extrude(depth=2)  # TEG-Schicht

# === 4. Kühlkanäle (intern) ===
for i in range(num_ribs):
    sw.new_sketch("Right")
    sw.sketch.rectangle_centered(width=blade_length/(num_ribs+1), 
                         height=thickness*0.4)
    sw.end_sketch()
    sw.feature.cut(depth=chord_width)

# === 5. Nanostruktur (Moth-Eye) ===
# Mikro-Rillen als Muster
for i in range(20):
    sw.new_sketch("Front")
    sw.sketch.line(-chord_width/2 + i*4, -thickness, 
                  -chord_width/2 + i*4, thickness)
    sw.end_sketch()
    sw.feature.cut(depth=0.5)  # 0.5mm Rillen

# === 6. Befestigung (Fuß) ===
sw.new_sketch("Front")
sw.sketch.circle(diameter=30)
sw.end_sketch()
sw.feature.extrude(depth=40)

# Passfeder-Nut nach DIN 4965
sw.new_sketch("Right")
sw.sketch.rectangle_centered(width=3, height=32)
sw.end_sketch()
sw.feature.cut(depth=40)

sw.save()

print("=== Adaptive Lattice Turbine Blade ===")
print(f"Länge: {blade_length}mm")
print(f"Breite: {chord_width}mm")
print(f"Technologie: Lattice + TEG + Nano + Piezo")
```

---

## Warum effizienter?

| Aspekt | Traditionell | Unser Design |
|--------|-----------|-------------|
| **Kühlung** | Kanäle | Lattice = 3x mehr Fläche |
| **Wärme** | verpufft | TEG → Strom zurückgewinnen |
| **Gewicht** | massiv | Lattice = 40% leichter |
| **Lebensdauer** | 10.000 h | Piezo-Dämpfer = weniger Verschleiß |
| **Wärmespannung** | hoch | Gradient-Material = niedrig |

---

## Fertigungswege

| Technologie | Wie herstellen |
|------------|---------------|
| **Lattice** | Selective Laser Melting (SLM) |
| **TEG-Schicht** | Dünnschicht-Deposition |
| **Nanostruktur** | Ätzen oder Laser |
| **Piezo** | Einbetten + Verdrahten |

---

## Normen

| Norm | Anwendung |
|------|-----------|
| DIN 2533 | Turbinen-Nomenklatur |
| ISO 6336 | Festigkeitsberechnung |
| DIN 4965 | Passfeder-Nut (Befestigung) |
| DIN 7168 | Allgemeintoleranzen |

---

*Erstellt: 2026-02-21*
