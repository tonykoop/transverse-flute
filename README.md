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
