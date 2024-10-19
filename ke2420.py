import pyvisa
import time

rm = pyvisa.ResourceManager('@py') # Linux pyvisa-py backend
#rm = pyvisa.ResourceManager()     # Windows NIVISA

class ke2420:
	
	# Constructor
	def __init__(self):
		self.instr = rm.open_resource('ASRL/dev/ttyUSB0::INSTR', baud_rate=9600, read_termination  = '\r', write_termination = '\r', timeout=4000) # Linux USB<->rs232
		#self.instr = rm.open_resource('ASRL6::INSTR', baud_rate=9600, read_termination  = '\r', write_termination = '\r', timeout=4000) # Windows COM6 USB<->rs232
		#self.instr = rm.open_resource('GPIB::15::INSTR') # GPIB

	def source_i_meas_v(self, current=-0.6, voltage_limit=21.0, samples=1, delay=0.0): # source current, measure voltage
		smu1_setting_list = ['SOURCe:CURRent:RANGe:AUTO 1', 'SOURce:FUNCtion CURR', 'SENSe:FUNCtion "VOLT:DC"', 'SENSe:VOLTage:RANGe:AUTO 1']
		for setting in smu1_setting_list:
			self.instr.write(setting)
		self.instr.write('SENSe:VOLTage:PROTection {:f}'.format(voltage_limit))
		self.instr.write('SOURce:CURRent {0}'.format(current))
		self.instr.write('OUTPut:STATe 1')
		time.sleep(delay)
		meas_res = 0.0
		for x in range(samples):
			result_list = self.instr.query("MEASure:VOLTage?").split(",")
			meas_res += float(result_list[0])
		return meas_res / samples
	
	def source_v_meas_i(self, voltage=0.1, current_limit=0.01, samples=1, delay=0.0):
		smu1_setting_list = ['SOURCe:VOLTage:RANGe:AUTO 1', 'SOURce:FUNCtion VOLT', 'SENSe:FUNCtion "CURR:DC"', 'SENSe:CURRent:RANGe:AUTO 1']
		for setting in smu1_setting_list:
			self.instr.write(setting)
		self.instr.write('SENSe:CURRent:PROTection {:f}'.format(current_limit))
		self.instr.write('SOURce:VOLTage {0}'.format(voltage))
		self.instr.write('OUTPut:STATe 1')
		time.sleep(delay)
		meas_res = 0.0
		for x in range(samples):
			result_list = self.instr.query("MEASure:CURRent?").split(",")
			meas_res += float(result_list[1])
		return meas_res / samples
		

	def output_off(self):
		self.instr.write('OUTPut:SMODe HIMPedance')
		self.instr.write('OUTPut:STATe 0')

	def output_on(self):
		self.instr.write('OUTPut:STATe 1')
	
	def reset(self):
		self.instr.write('*RST')
		time.sleep(2)
