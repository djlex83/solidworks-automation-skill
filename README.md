# SolidWorks Automation Skill

A Python-based automation interface for SolidWorks CAD software, designed to work with Claude AI for natural language CAD commands.

## Features

- **2D Sketching**: Lines, circles, rectangles, ellipses, arcs, splines, polygons
- **3D Features**: Extrusions, cuts, revolves, chamfers, fillets, patterns
- **Natural Language**: Supports both German and English commands
- **Quick Functions**: Pre-built functions for common shapes (box, cylinder, pipe, plate with holes)

## Requirements

- Windows OS
- SolidWorks 2015 or newer
- Python 3.x
- pywin32

## Installation

1. Clone this repository:
```bash
git clone https://github.com/YOUR_USERNAME/solidworks-automation-skill.git
```

2. Install dependencies:
```bash
pip install pywin32
```

3. Start SolidWorks and open a Part document

## Quick Start

```python
from scripts.sw_automation import SolidWorksAutomation

# Connect to SolidWorks
sw = SolidWorksAutomation()

# Create a simple box
sw.new_sketch("Front")
sw.sketch.rectangle_centered(100, 50)  # 100x50mm
sw.end_sketch()
sw.feature.extrude(depth=30)  # 30mm deep

sw.save()
```

## Quick Functions

```python
from scripts.sw_automation import quick_box, quick_cylinder, quick_pipe

# Create a box 100x50x30mm
quick_box(100, 50, 30)

# Create a cylinder diameter 80mm, height 50mm
quick_cylinder(80, 50)

# Create a pipe (outer 50mm, inner 40mm, length 100mm)
quick_pipe(50, 40, 100)
```

## Available Operations

### 2D Sketch Operations

| Operation | Method | Description |
|-----------|--------|-------------|
| Line | `sw.sketch.line(x1, y1, x2, y2)` | Draw a line |
| Circle | `sw.sketch.circle(diameter=100)` | Draw a circle |
| Rectangle | `sw.sketch.rectangle_centered(w, h)` | Centered rectangle |
| Ellipse | `sw.sketch.ellipse(major_r, minor_r)` | Draw an ellipse |
| Arc | `sw.sketch.arc(cx, cy, r, start, end)` | Draw an arc |
| Polygon | `sw.sketch.polygon(cx, cy, r, sides)` | Regular polygon |
| Spline | `sw.sketch.spline(points)` | Freeform curve |

### 3D Feature Operations

| Operation | Method | Description |
|-----------|--------|-------------|
| Extrude | `sw.feature.extrude(depth)` | Extrude a profile |
| Cut | `sw.feature.cut(depth)` | Remove material |
| Revolve | `sw.feature.revolve(angle)` | Create revolve body |
| Chamfer | `sw.feature.chamfer(distance)` | Add chamfer to edges |
| Fillet | `sw.feature.fillet(radius)` | Round edges |
| Mirror | `sw.feature.mirror(plane)` | Mirror features |
| Linear Pattern | `sw.feature.linear_pattern(...)` | Create linear pattern |
| Hole Pattern | `sw.feature.circular_hole_pattern(...)` | Create circular hole pattern |

## Examples

### Create a Cone (Revolve)

```python
sw = SolidWorksAutomation()
sw.new_sketch("Front")

# Triangle profile
sw.sketch.line(0, 0, 30, 0)   # Base
sw.sketch.line(30, 0, 0, 60)  # Slope
sw.sketch.line(0, 60, 0, 0)   # Close

# Centerline for rotation
sw.sketch.line(0, -10, 0, 70)

sw.end_sketch()
sw.feature.revolve(angle=360)
sw.save()
```

### Create a Flange with Holes

```python
sw = SolidWorksAutomation()

# Base cylinder
sw.new_sketch("Front")
sw.sketch.circle(diameter=150)
sw.end_sketch()
sw.feature.extrude(depth=20)

# Center hole
sw.new_sketch("Front")
sw.sketch.circle(diameter=40)
sw.end_sketch()
sw.feature.cut(through_all=True)

# 8 holes on pitch circle
sw.feature.circular_hole_pattern(
    num_holes=8,
    hole_diameter=10,
    pitch_circle_diameter=120,
    hole_depth=20
)

sw.save()
```

## Project Structure

```
solidworks-automation-skill/
├── SKILL.md              # Claude skill definition
├── README.md             # This file
├── scripts/
│   └── sw_automation.py  # Main Python module
└── references/
    ├── sketch-operations.md    # 2D operations reference
    ├── feature-operations.md   # 3D operations reference
    └── examples.md             # More examples
```

## Using with Claude AI

This repository is designed as a Claude Code Skill. Claude can use the SKILL.md file to understand how to generate SolidWorks automation code from natural language requests.

Example prompts:
- "Create a box 100x50x30mm"
- "Draw a circle diameter 80mm and extrude it 50mm"
- "Make a flange with 8 M10 holes on pitch circle 200mm"
- "Erstelle einen Kegel mit Durchmesser 60mm und Höhe 80mm"

## API Reference

The SolidWorks API uses **meters** internally. This module automatically converts millimeters to meters, so all dimensions you specify are in **millimeters**.

### Important Notes

1. **SolidWorks must be running** before executing scripts
2. **A Part document must be open** (not Assembly or Drawing)
3. **Sketches must be closed** before creating features
4. **For Revolve features**, always include a centerline in the sketch

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Acknowledgments

- SolidWorks API Documentation
- pywin32 library
- Claude AI by Anthropic
