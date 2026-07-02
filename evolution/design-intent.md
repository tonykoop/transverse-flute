# Design Intent — transverse-flute rev A

- Master CAD: `cad/slip_cast_transverse_flute_body.scad` (sha256: 09559ce3695fb347a80539320d67dd08b2f200aac15d973c2522a8109cbf1eda), driven by `Slip-Cast-Transverse-Flute-Family.xlsx` (sha256: 8956d4db48cb64065a868b3e6a1f89d63ca9b68a0c0be8512c7b77fd6ee7f224)
- Function: Experimental slip-cast ceramic transverse flute family (D4/F4/G4/A4/C5). Open-open flute model: both ends open, side-blown embouchure; pitch from sounding length + bore + end corrections. Tone-hole stations are first-pass open-open ratios and require prototype tuning. First-pass workflow: fired target dims → scale masters for shrinkage → cast/fire Round 1 → measure → correct.
- Environment: Cone-6 slip-cast ceramic via master + plaster mold; long thin tubes are warp/crack-prone in firing; shrinkage is an assumption until a clay test bar is measured. Embouchure/voicing geometry is empirical and outside the model.
- Target qty: 1 (Round 1 prototype, G4 first). Deadline: TBD. Budget/unit ceiling: TBD.

## Critical dimensions (carry tolerances)

| Feature | Nominal | Tolerance | Why critical | Source |
| --- | --- | --- | --- | --- |
| G4 packet sounding length | 428.88 mm | tune to pitch after firing | fundamental pitch (G4 = 391.995 Hz) | family-spec.csv SCF-G4-01 (physics_derived) |
| G4 fired bore ID | 16.99 mm | measure after fire | bore governs pitch/response | family-spec.csv SCF-G4-01 (physics_derived) |
| G4 total end correction | 10.19 mm | recompute from measured bore | open-open end effect | family-spec.csv SCF-G4-01 |
| G4 master overall length (initial) | 530.73 mm | recompute from measured shrinkage | fired size vs master | family-spec.csv SCF-G4-01 (first-pass scaling) |
| Tone-hole stations | per data/hole-schedule.csv (first-pass ratios) | undersize; tune post-bisque | scale intonation | data/hole-schedule.csv (measurement_required) |
| A4 reference | 440.000 Hz | ±cents logged in validation.csv | tuning correctness | family-spec.csv SCF-A4-01 |

## Incidental (free for DFM)

- Body exterior styling, decorative banding, glaze color/family, non-mating surface finish, headjoint cosmetic contour.

## Must-nots (DFM may never violate)

- Embouchure/voicing cut is tuning-sensitive: never freeze it from the table or a lossy mesh export — refine by hand and log (risks.md / README).
- Keep tone holes undersized before empirical bisque-stage tuning (data/hole-schedule.csv; risks.md Acoustic).
- Do not treat any dimension as proven until logged in validation.csv; no build/tune/fire has occurred (README validation warning).
- Do not scale to the full family before Round 1 (G4) measured shrinkage + tuning corrections (doe-plan.md / risks.md Structural).

## Material intent

- Preferred: Cone-6 slip-cast ceramic; master + two-piece plaster mold (per bom.csv / mold-workflow.md).
- Acceptable subs: per sourcing.csv / supplier-rfq.md (spec-first; live prices unverified; mouth-safe finishes only).
- Forbidden: non-mouth-safe interior finishes on blown bodies.

## Stage status

Stage 0 intake complete 2026-07-01. Gate A (Alpha shop compile) NOT yet run — no concessions logged, nothing presented as shippable. Design is experimental/unvalidated; fabrication authority remains measurement-gated (L2 candidate for review).
