import ke2420

smu1 = ke2420.ke2420()

print("Place resistor between two-wire connections") # I used a 27 Ohm resistor
smu1.reset()
print("Forced 1.0V on resistor and measured {:.6f}A".format(smu1.source_v_meas_i(voltage=1.0, current_limit=0.1)))
smu1.output_off()
print("Forced 0.36657A on resistor and measured {:.6f}V".format(smu1.source_i_meas_v(current=0.036657)))
smu1.output_off()
