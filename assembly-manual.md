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
