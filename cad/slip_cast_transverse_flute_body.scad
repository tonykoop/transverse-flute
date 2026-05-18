// Slip-cast transverse flute body concept model.
// Units: inches. Convert to mm in slicer/CAD if needed.
// This is a geometry starter, not a final mold with draft analysis.
// Dimensions are first-pass prototype targets from family-spec.csv and
// data/fired-dimension-targets.csv; they are not measured tuning proof.

instrument_id = "SCF-G4-01";
family_spec_source = "family-spec.csv";
design_table_source = "data/fired-dimension-targets.csv";
fired_length = 18.388;
fired_bore = 0.669;
fired_wall = 0.130;
shrink_x = 0.12;
shrink_y = 0.12;
shrink_z = 0.12;

master_length = fired_length / (1 - shrink_x);
master_bore_y = fired_bore / (1 - shrink_y);
master_bore_z = fired_bore / (1 - shrink_z);
master_od_y = (fired_bore + 2*fired_wall) / (1 - shrink_y);
master_od_z = (fired_bore + 2*fired_wall) / (1 - shrink_z);

inch = 25.4;

module flute_outer() {
  scale([1, master_od_y/master_od_z, 1])
    rotate([0,90,0])
      cylinder(h=master_length*inch, d=master_od_z*inch, $fn=96);
}

module flute_bore() {
  scale([1, master_bore_y/master_bore_z, 1])
    translate([-0.01*inch,0,0])
      rotate([0,90,0])
        cylinder(h=(master_length+0.02)*inch, d=master_bore_z*inch, $fn=96);
}

difference() {
  flute_outer();
  flute_bore();
}
