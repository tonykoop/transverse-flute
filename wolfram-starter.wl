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
