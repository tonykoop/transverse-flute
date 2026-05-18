# Slip-Cast Transverse Flute Family Build Packet

## Source And Scope

- Date: `2026-05-02`
- Source workbook inspected: `/mnt/c/Users/Tony/Documents/Claude/Projects/Career/flutes-staging/Flutes-AI.xlsx`
- Relevant sheet: `Irish Flute`, which uses open-open flute math, D4 sanity dimensions, end correction, and 6-hole diatonic placement.
- Ceramic workflow references inspected: `Ocarina`, `Udu Drum Family`, and `vessel-flute-lab` build packets.

This packet is for unkeyed transverse ceramic flute prototypes made by slip casting. The acoustic dimensions below are final fired targets. Master and mold dimensions are scaled from those targets using provisional X/Y/Z shrink factors.

## Design Intent

Build a family across D4, F4, G4, A4, and C5 so the study sees both long-body casting behavior and smaller higher-key behavior. Round 1 is not trying to prove a finished product. It is meant to produce a clean data set:

- actual X/Y/Z fired shrink by material, wall, and mold orientation,
- actual bore roundness and wall buildup,
- pitch and response error against the open-open first-pass model,
- embouchure and bore-profile preferences before Round 2.

## Governing Model

First-pass open-open transverse flute model:

```text
f = c / (2 * L_eff)
L_acoustic = c / (2 * f)
end_correction_total ~= 0.6 * bore_ID
sounding_length ~= L_acoustic - end_correction_total
hole_distance_from_foot ~= L_acoustic * (fundamental_frequency / hole_frequency)
```

The hole positions are first-pass acoustic stations. Ceramic wall thickness, hole chimney height, undercutting, bore ovalization, embouchure geometry, and stopper position will move real pitch. The packet therefore makes hole cuts undersize and expects bisque-stage tuning.

The V5 acoustic-law summary is tracked in [`family-spec.csv`](family-spec.csv).
Every family row declares `acoustic_law=open_open`,
`end_condition=both_ends_open`, and `dimension_provenance=physics_derived`.
Those fields describe the first-pass planning model only; measured prototype
pitch, bore roundness, shrink, and tone-hole correction data are still required
before the dimensions become validated tuning authority.

## Initial Family Targets

| ID | Key | Bore ID | OD | Sounding length | Pre-trim fired length | Master X length @12% |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| SCF-D4-01 | D4 | 0.748 in | 1.028 in | 22.625 in | 24.247 in | 27.554 in |
| SCF-F4-01 | F4 | 0.669 in | 0.939 in | 19.001 in | 20.505 in | 23.301 in |
| SCF-G4-01 | G4 | 0.669 in | 0.929 in | 16.885 in | 18.388 in | 20.895 in |
| SCF-A4-01 | A4 | 0.591 in | 0.841 in | 15.045 in | 16.432 in | 18.673 in |
| SCF-C5-01 | C5 | 0.512 in | 0.742 in | 12.643 in | 13.911 in | 15.808 in |

## Shrinkage Model

Coordinate convention:

- X = flute length/bore axis/hole stations.
- Y = side-to-side bore and outside width.
- Z = vertical height, wall buildup, and ovalization direction.

```text
master_x = fired_target_x / (1 - shrink_x)
master_y = fired_target_y / (1 - shrink_y)
master_z = fired_target_z / (1 - shrink_z)
observed_shrink_axis = 1 - fired_measured_axis / master_measured_axis
round2_master_axis = round1_master_axis * fired_target_axis / fired_measured_axis
```

Initial assumption is `shrink_x = shrink_y = shrink_z = 0.12`. This is a placeholder, not a material claim.

## Round 1 Success Criteria

- No full-length cracking through drying, bisque, or glaze fire.
- Bore remains measurable and cleanable.
- Embouchure speaks a stable fundamental and octave on at least the G4 or C5 prototypes.
- Hole tuning can be brought within +/-35 cents after bisque without grotesque hole enlargement.
- X/Y/Z shrink measurements have enough consistency to choose Round 2 scale factors.

## Round 2 Decision Path

1. Fit shrink_x, shrink_y, and shrink_z from bars, bore rings, and flute features.
2. Choose the best material/profile/embouchure combination from the DoE.
3. Update the workbook inputs and regenerate master dimensions.
4. Rebuild the full five-key family using corrected X/Y/Z scale factors.
5. Tighten acceptance to +/-10 cents for tuned notes and +/-0.010 to +/-0.030 in on critical fired dimensions.

## Open Assumptions

- Bore diameters are adapted from the existing Irish/simple-system flute design range, then made ceramic-friendly with thinner walls than wood.
- A removable head stopper or cork test plug is assumed for Round 1 because it gives a reversible tuning variable.
- All prices, supplier availability, and exact clay data must be date-checked before buying.
- CAD mold release and split lines need confirmation in the actual CAD model before cutting production molds.
