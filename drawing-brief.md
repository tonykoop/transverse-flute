# Drawing Brief

## Required Views

- Family overview showing D4, F4, G4, A4, and C5 fired target lengths.
- Individual body plan view for each key with X-axis datum, embouchure, tone holes, bore ID, OD, and fired/master length notes.
- Section view at embouchure showing wall thickness, bore, hole edge, undercut zone, and stopper relationship.
- Section view through a tone hole showing chimney height and allowed tuning/undercut area.
- Mold stack view showing split line, registration keys, pour/drain direction, seam cleanup zone, and optional three-piece D4 strategy.
- Shrink coupon drawing with X/Y/Z labels and measurement flats.

## Critical Dimensions

| Dimension | Source | Tolerance Intent |
| --- | --- | --- |
| Fired sounding length | `data/fired-dimension-targets.csv` and workbook | Tuning critical |
| Embouchure center from head | workbook, initial 1.5 x bore ID | Response and tuning |
| Bore ID Y/Z | workbook and bore ring measurement | Tuning, response, shrink fit |
| Tone-hole stations X | `data/hole-schedule.csv` | Tuning critical; first-pass only |
| Tone-hole diameters | `data/hole-schedule.csv` | Cut undersize; tune after bisque |
| Wall thickness | DoE wall target and measured coupons | Durability, weight, hole chimney |
| Master X/Y/Z scale | shrink model | Process critical |

## Existing Drawings

- `drawings/family-overview.svg`
- `drawings/mold-stack.svg`
- `drawings/SCF-D4-01-body.svg`
- `drawings/SCF-F4-01-body.svg`
- `drawings/SCF-G4-01-body.svg`
- `drawings/SCF-A4-01-body.svg`
- `drawings/SCF-C5-01-body.svg`

These are SVG shop-review drawings. They are not a substitute for final CAD mold drawings with draft and release analysis.
