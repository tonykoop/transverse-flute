# Slip-Cast Transverse Flute Family Print Packet

Generated: 2026-05-02
Packet folder: `/mnt/c/Users/Tony/Documents/GitHub/transverse-flute`

## File Map

| File | Purpose |
| --- | --- |
| `design.md` | Project intent, catalog metadata, assumptions, and validation plan. |
| `bom.csv` | Starter bill of materials with part categories, quantities, drawing refs, and notes. |
| `sourcing.csv` | Supplier/search tracker with specs, price/date fields, lead time, substitutes, and risks. |
| `cut-list.csv` | Rough/final stock sizes, material, grain/orientation, operations, yield, and offcuts. |
| `drawing-brief.md` | Manufacturing drawing and technical product sketch brief. |
| `assembly-manual.md` | Shop-facing sequence, tools, fixtures, safety, tuning, finishing, and maintenance notes. |
| `validation.csv` | Target/measured values, tolerance, environment, result, and tuning/build action log. |
| `supplier-rfq.md` | Supplier email/request-for-quote starter. |
| `visual-bom-brief.md` | Art direction for an image-forward visual BOM. |
| `wolfram-starter.wl` | Wolfram starter for physics, optimization, visualization, and validation. |
| `README.md` | Project artifact. |
| `doe-plan.md` | Project artifact. |
| `mold-workflow.md` | Project artifact. |

<div class="page-break"></div>

## design.md

Project intent, catalog metadata, assumptions, and validation plan.

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

<div class="page-break"></div>

## bom.csv

Starter bill of materials with part categories, quantities, drawing refs, and notes.

| item_id | subsystem | item | qty | unit | material_spec | make_buy | drawing_ref | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SCF-BOM-001 | CAD/master | Parametric flute body master set | 5 | masters | Sealed 3D print or machined master, scaled by X/Y/Z shrink factors | Make | drawings/SCF-*-body.svg; cad/slip_cast_transverse_flute_body.scad | Use as mold masters or CAD reference. Add mold split before production tooling. |
| SCF-BOM-002 | Mold | Two-piece or three-piece plaster molds | 5+ | molds | Pottery plaster, registration keys, pour/drain reservoir | Make | drawings/mold-stack.svg | D4 may need sectional mold or reinforced cradle due to length. |
| SCF-BOM-003 | Material | Cone 6 stoneware casting slip | TBD | gallons | Casting slip with known fired shrinkage and absorption | Buy/mix | data/doe-build-matrix.csv | Date-check supplier and record batch number. |
| SCF-BOM-004 | Material | Cone 6 porcelain casting slip | TBD | gallons | Porcelain slip for comparison runs | Buy/mix | data/doe-build-matrix.csv | Higher shrink/warpage risk, better density and surface. |
| SCF-BOM-005 | Tuning | Diamond needle files and small diamond burrs | 1 | set | Fine files for bisque and fired ceramic hole tuning | Buy | assembly-manual.md | Avoid glazing acoustic edges after tuning. |
| SCF-BOM-006 | Validation | Measurement kit | 1 | kit | Calipers, bore gauges/pin gauges, tuner, mic, thermometer/hygrometer, scale | Use/buy | validation.csv | Use the same tuner/mic distance for all response tests. |
| SCF-BOM-007 | Voicing | Cork/stopper test kit | 5 | sets | Cork, silicone, or printed plug for head-end tuning experiments | Make/buy | drawing-brief.md | Treat head-stopper position as an adjustable variable before ceramic-integral solutions. |
| SCF-BOM-008 | Finish | Wax resist and glaze test set | 1 | set | Food-safe/contact-safe glaze where mouth contact occurs; acoustic edges waxed clear | Buy | mold-workflow.md | Keep glaze out of embouchure, bore, tone holes, and stopper fit surfaces. |

<div class="page-break"></div>

## sourcing.csv

Supplier/search tracker with specs, price/date fields, lead time, substitutes, and risks.

| source_id | category | spec | supplier_or_search_terms | qty | date_checked | unit_price | lead_time | substitution_rule | risk_notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SRC-SLIP-STONEWARE | Ceramic slip | Cone 6 stoneware casting slip, published shrinkage and absorption data | local ceramic supplier cone 6 stoneware casting slip shrinkage data sheet | TBD |  |  |  | Must have measured or published shrinkage; color can vary. | Live price and availability intentionally blank until purchase planning. |
| SRC-SLIP-PORCELAIN | Ceramic slip | Cone 6 porcelain casting slip, low warpage preferred | cone 6 porcelain casting slip shrinkage casting data sheet | TBD |  |  |  | Substitute only with data-backed shrink and firing schedule. | Porcelain may move more; use bars and rings before long D4 molds. |
| SRC-PLASTER | Mold material | Pottery plaster or high-strength mold plaster | USG pottery plaster No. 1 local ceramic supplier | TBD |  |  |  | Must be absorbent mold plaster, not general patching plaster. | Mold drying time affects casting wall thickness and repeatability. |
| SRC-PRINT | Master fabrication | High-resolution sealed print or machined master; smooth bore core strategy | SLA print service large format resin smooth finish or in-house FDM sealed master | 5 masters plus coupons |  |  |  | Any method is acceptable if master dimensions are measured and sealed. | Layer lines transfer to plaster and may disturb mold release. |
| SRC-TUNING | Tuning tools | Diamond needle files, small diamond burrs, tuner/mic | diamond needle file set ceramic tuning burr chromatic tuner measurement microphone | 1 kit |  |  |  | Prefer fine controlled abrasion over aggressive rotary cutting. | Over-opening holes is not reversible. |

<div class="page-break"></div>

## cut-list.csv

Rough/final stock sizes, material, grain/orientation, operations, yield, and offcuts.

| cut_id | part | qty | rough_dimensions | final_dimensions | material | orientation | operation | yield_or_notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CUT-SCF-D4-01 | Scaled master body blank/envelope | 1 | 28.55 x 1.67 x 1.67 in | 27.554 x 1.168 x 1.168 in | Sealed printed/machined master | X along bore axis; mark top/embouchure datum | Print/machine, sand, seal, measure, then mold | Add handles/sprues outside acoustic envelope only. |
| CUT-SCF-F4-01 | Scaled master body blank/envelope | 1 | 24.3 x 1.57 x 1.57 in | 23.301 x 1.067 x 1.067 in | Sealed printed/machined master | X along bore axis; mark top/embouchure datum | Print/machine, sand, seal, measure, then mold | Add handles/sprues outside acoustic envelope only. |
| CUT-SCF-G4-01 | Scaled master body blank/envelope | 1 | 21.9 x 1.56 x 1.56 in | 20.895 x 1.056 x 1.056 in | Sealed printed/machined master | X along bore axis; mark top/embouchure datum | Print/machine, sand, seal, measure, then mold | Add handles/sprues outside acoustic envelope only. |
| CUT-SCF-A4-01 | Scaled master body blank/envelope | 1 | 19.67 x 1.46 x 1.46 in | 18.673 x 0.956 x 0.956 in | Sealed printed/machined master | X along bore axis; mark top/embouchure datum | Print/machine, sand, seal, measure, then mold | Add handles/sprues outside acoustic envelope only. |
| CUT-SCF-C5-01 | Scaled master body blank/envelope | 1 | 16.81 x 1.34 x 1.34 in | 15.808 x 0.843 x 0.843 in | Sealed printed/machined master | X along bore axis; mark top/embouchure datum | Print/machine, sand, seal, measure, then mold | Add handles/sprues outside acoustic envelope only. |
| CUT-SHRINK-BAR-X | Shrinkage bar set | 12 | 6.5 x 0.5 x 0.25 in master or cast bars | Measure fired length, width, thickness | Each slip body | Label X, Y, Z and casting direction | Cast alongside every flute run | Primary anisotropic shrink data. |
| CUT-BORE-RING | Bore/roundness ring coupons | 12 | OD/ID matching each bore family | Measure fired ID/OD in Y and Z | Each slip body | Same drain orientation as flute | Cast with flute body | Detect ovalization and wall-thickness drift. |

<div class="page-break"></div>

## drawing-brief.md

Manufacturing drawing and technical product sketch brief.

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

<div class="page-break"></div>

## assembly-manual.md

Shop-facing sequence, tools, fixtures, safety, tuning, finishing, and maintenance notes.

# Slip-Cast Transverse Flute Assembly Manual

## Tools

- CAD or OpenSCAD/SolidWorks for master geometry.
- 3D printer or machining route for sealed masters.
- Plaster mold supplies, cottle boards, scale, mixing bucket, release, clamps.
- Casting slip, deflocculant tools if mixing, and slip hydrometer if available.
- Needle tools, hole cutters, small round cutters, ribs, sponges, fettling knife.
- Calipers, bore gauges or pin gauges, scale, tuner, microphone, thermometer/hygrometer.
- Diamond needle files and fine diamond burrs.
- Wax resist, glaze, kiln access, and kiln-safe supports.

## Build Sequence

1. Pick a build row from `data/doe-build-matrix.csv`.
2. Confirm workbook shrink inputs and export the master dimensions for that run.
3. Print or machine the master, then sand, seal, and measure it.
4. Build the plaster mold with marked datums and registration keys.
5. Dry the mold completely enough for repeatable casting.
6. Pour slip, hold for the planned drain time, drain in the assigned orientation, and log the run.
7. Demold at leather hard and clean seams while preserving datums.
8. Cut embouchure and pilot tone holes undersize.
9. Dry slowly with support under the long body.
10. Bisque fire.
11. Measure X/Y/Z features, bore, mass, and first tuning.
12. Tune holes and embouchure in small steps using diamond tools.
13. Wax resist acoustic edges and glaze only after tuning is understood.
14. Final fire, then remeasure dimensions and tuning.
15. Enter data into `data/prototype-measurements.csv` and update `data/shrinkage-fit.csv`.

## Tuning Notes

- Enlarge an open tone hole to raise that note.
- Undercutting can raise pitch and improve response, but it changes the correction model.
- A head stopper gives a reversible global tuning lever; use it in Round 1 before committing to an integral ceramic head solution.
- Do not glaze the embouchure edge, tone-hole chimneys, bore interior, or stopper seating surface during the data rounds.

## Safety And Handling

- Fired ceramic edges and dust need care; use wet sanding or dust control.
- Long greenware bodies need full support while drying and moving.
- Label every prototype before it enters the kiln so the DoE data survives the shop day.

<div class="page-break"></div>

## validation.csv

Target/measured values, tolerance, environment, result, and tuning/build action log.

| build_id | instrument_id | stage | measurement | target_value | unit | tolerance | measured_value | environment | result | action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | SCF-D4-01 | final fired | fundamental | 293.665 | Hz | +/-10 cents after tuning; Round 1 accepts +/-35 cents before correction |  | Record temp F / humidity / tuner distance |  | Move stopper, file embouchure/tone holes, or update Round 2 CAD factor. |
|  | SCF-D4-01 | final fired | overall length X | 24.247 | in | +/-0.030 in before trim |  | Room temp; calipers/tape ID |  | Use target/measured as Round 2 X scale correction. |
|  | SCF-D4-01 | final fired | bore ID Y/Z | 0.748 | in | +/-0.010 in; record Y and Z separately |  | Pin gauge or bore gauge |  | Use Y/Z shrink correction and check ovalization. |
|  | SCF-F4-01 | final fired | fundamental | 349.228 | Hz | +/-10 cents after tuning; Round 1 accepts +/-35 cents before correction |  | Record temp F / humidity / tuner distance |  | Move stopper, file embouchure/tone holes, or update Round 2 CAD factor. |
|  | SCF-F4-01 | final fired | overall length X | 20.505 | in | +/-0.030 in before trim |  | Room temp; calipers/tape ID |  | Use target/measured as Round 2 X scale correction. |
|  | SCF-F4-01 | final fired | bore ID Y/Z | 0.669 | in | +/-0.010 in; record Y and Z separately |  | Pin gauge or bore gauge |  | Use Y/Z shrink correction and check ovalization. |
|  | SCF-G4-01 | final fired | fundamental | 391.995 | Hz | +/-10 cents after tuning; Round 1 accepts +/-35 cents before correction |  | Record temp F / humidity / tuner distance |  | Move stopper, file embouchure/tone holes, or update Round 2 CAD factor. |
|  | SCF-G4-01 | final fired | overall length X | 18.388 | in | +/-0.030 in before trim |  | Room temp; calipers/tape ID |  | Use target/measured as Round 2 X scale correction. |
|  | SCF-G4-01 | final fired | bore ID Y/Z | 0.669 | in | +/-0.010 in; record Y and Z separately |  | Pin gauge or bore gauge |  | Use Y/Z shrink correction and check ovalization. |
|  | SCF-A4-01 | final fired | fundamental | 440.0 | Hz | +/-10 cents after tuning; Round 1 accepts +/-35 cents before correction |  | Record temp F / humidity / tuner distance |  | Move stopper, file embouchure/tone holes, or update Round 2 CAD factor. |
|  | SCF-A4-01 | final fired | overall length X | 16.432 | in | +/-0.030 in before trim |  | Room temp; calipers/tape ID |  | Use target/measured as Round 2 X scale correction. |
|  | SCF-A4-01 | final fired | bore ID Y/Z | 0.591 | in | +/-0.010 in; record Y and Z separately |  | Pin gauge or bore gauge |  | Use Y/Z shrink correction and check ovalization. |
|  | SCF-C5-01 | final fired | fundamental | 523.251 | Hz | +/-10 cents after tuning; Round 1 accepts +/-35 cents before correction |  | Record temp F / humidity / tuner distance |  | Move stopper, file embouchure/tone holes, or update Round 2 CAD factor. |
|  | SCF-C5-01 | final fired | overall length X | 13.911 | in | +/-0.030 in before trim |  | Room temp; calipers/tape ID |  | Use target/measured as Round 2 X scale correction. |
|  | SCF-C5-01 | final fired | bore ID Y/Z | 0.512 | in | +/-0.010 in; record Y and Z separately |  | Pin gauge or bore gauge |  | Use Y/Z shrink correction and check ovalization. |

<div class="page-break"></div>

## supplier-rfq.md

Supplier email/request-for-quote starter.

# Supplier RFQ Starter

Subject: RFQ - slip-cast ceramic flute prototype materials and master/mold support

Hello,

I am prototyping a family of slip-cast ceramic transverse flutes and need materials or fabrication support with measured shrinkage and repeatability data.

Please quote the following where available:

- Cone 6 stoneware casting slip with shrinkage, absorption, and firing schedule data.
- Cone 6 porcelain casting slip with shrinkage, absorption, and firing schedule data.
- Pottery plaster suitable for slip-casting molds.
- Optional high-resolution master printing or machining for long cylindrical flute masters up to about 29 in master length.

Please include:

- unit price and minimum order,
- current availability and lead time,
- shipping or local pickup options,
- technical data sheets,
- recommended mold/drying/firing notes,
- any substitutions you recommend for thin-walled musical instrument bodies.

The prototypes will be measured for X/Y/Z shrinkage, bore roundness, wall thickness, and acoustic tuning after firing.

Thank you,

Tony

<div class="page-break"></div>

## visual-bom-brief.md

Art direction for an image-forward visual BOM.

# Visual BOM Brief

Create an image-forward BOM plate in Tony's Ashiko BOM style:

- Header: Slip-Cast Transverse Flute Family, quote date, material status, and Round 1 / Round 2 label.
- Hero image: family fan of the five fired target flutes or a clean CAD render.
- Table rows grouped by CAD/master, mold, ceramic material, tuning tools, validation tools, and finishing.
- Include thumbnails for: master, plaster mold halves, casting slip, shrink bars, bore rings, diamond files, tuner/mic, cork/stopper kit.
- Add callouts showing X/Y/Z shrink axes and where measurements are taken.
- Mark generated/CAD imagery as placeholders until replaced with shop photos or supplier images.

Important: the visual BOM should communicate process and parts, not invent unverified dimensions. Pull all numbers from the workbook and CSVs.

<div class="page-break"></div>

## wolfram-starter.wl

Wolfram starter for physics, optimization, visualization, and validation.

```wolfram
(* Slip-Cast Transverse Flute Family - Wolfram starter *)

a4 = 440;
cIn = 13552;
freq[midi_] := a4*2^((midi - 69)/12);
acousticLength[f_] := cIn/(2*f);
endCorrection[bore_] := 0.6*bore;
soundingLength[midi_, bore_] := acousticLength[freq[midi]] - endCorrection[bore];
holeDistanceFromFoot[midiFund_, interval_, bore_] :=
  acousticLength[freq[midiFund]] * freq[midiFund]/freq[midiFund + interval];
centsError[measured_, target_] := 1200*Log2[measured/target];
masterDim[fired_, shrink_] := fired/(1 - shrink);
observedShrink[master_, fired_] := 1 - fired/master;

family = {
  <|"ID" -> "SCF-D4-01", "MIDI" -> 62, "Bore" -> .748|>,
  <|"ID" -> "SCF-F4-01", "MIDI" -> 65, "Bore" -> .669|>,
  <|"ID" -> "SCF-G4-01", "MIDI" -> 67, "Bore" -> .669|>,
  <|"ID" -> "SCF-A4-01", "MIDI" -> 69, "Bore" -> .591|>,
  <|"ID" -> "SCF-C5-01", "MIDI" -> 72, "Bore" -> .512|>
};

Dataset[
  family /. inst_Association :> Join[
    inst,
    <|
      "FreqHz" -> freq[inst["MIDI"]],
      "SoundingLengthIn" -> soundingLength[inst["MIDI"], inst["Bore"]],
      "MasterXAt12PctIn" -> masterDim[soundingLength[inst["MIDI"], inst["Bore"]], .12]
    |>
  ]
]

Manipulate[
 Plot[
  Evaluate@Table[Sin[n*Pi*x/soundingLength[midi, bore]], {n, 1, 3}],
  {x, 0, soundingLength[midi, bore]},
  PlotRange -> {-1, 1},
  PlotLabel -> Row[{"Standing wave sketch, MIDI ", midi, ", bore ", bore, " in"}]
 ],
 {{midi, 62}, 62, 72, 1},
 {{bore, .748}, .45, .85, .001}
]
```

<div class="page-break"></div>

## README.md

Project artifact.

# Slip-Cast Transverse Flute Family

This folder is a build packet for a first-round family of slip-cast ceramic transverse flutes. It is set up for the workflow you described: target final fired dimensions first, build from shrink-scaled masters, measure the fired results, fit X/Y/Z shrinkage and acoustic correction factors, then run a second corrected round.

Start with:

- `Slip-Cast-Transverse-Flute-Family.xlsx` for the parametric workbook.
- `data/fired-dimension-targets.csv` for target fired dimensions.
- `data/hole-schedule.csv` for first-pass tone-hole stations.
- `data/doe-build-matrix.csv` for the Round 1 screening plan.
- `drawings/family-overview.svg` and individual `drawings/SCF-*-body.svg` files for shop review.
- `assembly-manual.md`, `mold-workflow.md`, and `validation.csv` for the actual build/measure loop.

All shrink factors are deliberately provisional: X=12%, Y=12%, Z=12%. Replace them with measured values after Round 1.

<div class="page-break"></div>

## doe-plan.md

Project artifact.

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

<div class="page-break"></div>

## mold-workflow.md

Project artifact.

# Slip-Cast Mold Workflow

## Master Strategy

1. Generate the master from the workbook/CAD dimensions using X/Y/Z scale factors.
2. Add external handling tabs, pour/drain reservoir geometry, and mold keys outside the final fired acoustic envelope.
3. Seal and polish the master. Measure master X/Y/Z dimensions before making plaster.
4. Mark datums permanently: head end, foot end, top/embouchure side, X/Y/Z axes, split line, and build ID.

## Mold Strategy

- Use a two-piece mold for G4/A4/C5 if release is clean.
- Consider a three-piece or sectional mold for D4 because length, sag, and demold stress are the main risks.
- Mold center marks or shallow dimples for holes are useful; avoid fully molded tone holes in Round 1 unless release testing proves they are clean.
- Keep registration keys away from the bore axis, embouchure edge, hole centers, and seam-cleanup surfaces.
- Include a pour/drain reservoir that can be removed without touching the fired trim target.

## Casting Controls

Record these for every run:

- slip body and batch,
- mold dry weight and mold age,
- pour time, drain time, and drain orientation,
- room temperature and humidity,
- leather-hard demold time,
- wall thickness at sacrificial rim/coupon,
- dry, bisque, and glaze firing schedules,
- fired mass, length, bore Y/Z, OD Y/Z, and note frequencies.

## Tuning-Friendly Hole Strategy

1. Cast the body with molded center marks only.
2. Cut pilot holes at leather hard, about 85% of the shrink-compensated target diameter.
3. Dry and bisque.
4. Tune by opening holes with diamond tools. Stop before final glaze.
5. Wax resist all acoustic edges before glaze.

## Failure Modes To Watch

- Long D4 body sags or twists while drying.
- Bore ovalizes differently in Y and Z.
- Mold seam intrudes into the embouchure or tone-hole region.
- Wall thickness drifts with drain time enough to change hole chimney height.
- Glaze softens, rounds, or chokes the embouchure and tone-hole edges.
