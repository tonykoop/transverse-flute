# Round 1 DoE Plan

## Purpose

Round 1 is a screening study for a slip-cast transverse flute family. It should answer:

- What are the actual X/Y/Z shrink factors for each clay/process condition?
- Which clay body and wall target survive long flute geometry?
- Does a cylindrical bore or mild taper give better response after ceramic firing?
- Which embouchure geometry speaks cleanly before excessive hand correction?
- Do shrink and acoustic errors interpolate across D4, G4, and C5 well enough to build F4 and A4 in Round 2?

## Factors

| Factor | Levels |
| --- | --- |
| Key/scale | D4, G4, C5 screening; F4 and A4 family fill-ins |
| Clay body | Cone 6 stoneware, Cone 6 porcelain |
| Wall target | thin drain, nominal drain, thick drain |
| Bore profile | cylindrical, mild taper |
| Embouchure | standard oval, longer oval |
| Mold orientation | horizontal drain, vertical drain |

## Responses

- X/Y/Z shrink from bars, bore rings, and flute features.
- Bore roundness: fired ID Y vs ID Z.
- Wall thickness at head, middle, foot.
- Fundamental and six-finger scale cents error.
- Octave response, breath threshold, tone stability, and subjective playability.
- Crack/warp/sag/seam cleanup outcomes.

## Round 1 Matrix

See `data/doe-build-matrix.csv`. It contains 20 planned runs including screening and family fill-in builds.

## Round 2 Fit

Use `data/prototype-measurements.csv` and `data/shrinkage-fit.csv` to compute:

```text
shrink_axis = 1 - fired_axis / master_axis
round2_axis_scale_multiplier = target_fired_axis / measured_fired_axis
cents_error = 1200 * log2(measured_frequency / target_frequency)
```

If material or orientation creates a strong interaction, keep separate shrink factors by material/orientation rather than forcing a single global X/Y/Z value.
