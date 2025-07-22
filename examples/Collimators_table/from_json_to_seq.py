import xtrack as xt

# Full path to the input JSON file
input_path = "/home/dogibellieri/fcc_ee_pywit_model/examples/Collimators_table/fccee_collimation_lattice_forimpedance/FCCee_z_V92a_107_LCC_aper_collimators_xtrack.json"

# Load the JSON as a Line object
line = xt.Line.from_json(input_path)

# Convert the Line object to a MAD-X sequence
madx_sequence = line.to_madx_sequence("fcc_ee_ring")

# Full path to save the output .seq file
output_path = "/home/dogibellieri/fcc_ee_pywit_model/examples/Collimators_table/fccee_collimation_lattice_forimpedance/FCCee_z_V92a_107_LCC_aper_collimators.seq"

# Write the MAD-X sequence to a .seq file
with open(output_path, "w") as f:
    f.write(madx_sequence)


print(f"MAD-X sequence saved to: {output_path}")
