# Transverse Flute Risks

Scaffolded during the 2026-07-01 V5 refresh to satisfy the baseline-file
contract. All items are first-pass and unvalidated; this is an experimental
slip-cast ceramic flute lab (see README). Replace/expand with measured findings
after Round 1 firing.

## Acoustic

- Open-open flute math sets first-pass tone-hole stations only. Actual pitch
  depends on embouchure cut, bore taper, wall/undercut, and fired shrinkage —
  treat every `data/hole-schedule.csv` position as a starting point, not tuning
  authority (TBD until bisque-stage tuning). Keep holes undersized and tune up.
- Embouchure/voicing geometry is empirical and out of scope for the design
  table and the OpenSCAD envelope master; it must be refined by hand.

## Structural

- Ceramic shrinkage (X/Y/Z) is an assumption until a clay test bar is measured;
  master scaling (`master_overall_length_x_mm_initial` in family-spec.csv) is
  provisional. Firing warp/ovality on long thin tubes (D4/F4) is a real risk —
  measure straightness and bore ID after each fire (TBD).
- Thin-wall long bores may crack during drying/bisque; wall targets are
  unvalidated.

## Supply

- Live sourcing (slip, plaster, consumables) has not been checked; costs and
  lead times in sourcing.csv / bom.csv are placeholders (TBD).

## Fit/Finish

- Interior finish on a played/blown instrument must be mouth-safe; glaze/seal
  choice is unresolved (TBD).

## Process

- No physical build, tuning, firing, or validation has occurred. Do not treat
  any dimension as proven until logged in validation.csv. Remain at L2 until
  CAD, mold, and prototype tuning validation are complete.
