from scdextractor import parse_file, extract_meta_information, extract_IEDs, extract_IP
from writer import Pandawriter
import PySimpleGUI as sg
import os

if __name__ == "__main__":
	# GUI initialization
	sg.theme('DarkBlue15')
	layout = [
		[sg.Text('Choose SCD file to process')],
		[sg.Input(background_color='black'), sg.FileBrowse(file_types=(("IEC 61850 SCD", "*.scd"),))],
		[sg.Text('Choose the output file')],
		[sg.Input(background_color='black'), sg.FileSaveAs(file_types=(("Excel 2013", "*.xlsx"),))],
		[sg.Checkbox('Include DataSet signals', key="_REPORT_")],
		[sg.Button('Report'), sg.Cancel()]
	]

	window = sg.Window('IEC 61850 SCD Report', layout)
	while True:
		event, values = window.read()

		if event == "Report":
			scd_file_path = values["Browse"]
			output_path = values["Save As..."]

			print(output_path)
			# check if file or a path
			if os.path.split(output_path)[1]:
				file = os.path.split(output_path)[1]
				if not os.path.split(file)[1]:
					# if path has no extension append with xlxx
					output_path += ".xlsx"

			if output_path.lower().endswith(('.xls', '.xlsx')):
				break
			else:
				output_path += ".xlsx"

			print(output_path)
			scd_content = parse_file(scd_file_path)

			scd_meta_info = extract_meta_information(scd_content)
			# find all IEDs
			extracted_devices = extract_IEDs(scd_content)
			extracted_devices = extract_IP(scd_content, extracted_devices)

			Pandawriter.load(scd_meta_info, extracted_devices)
			Pandawriter.write(output_path)
			break

		if event in (None, 'Cancel'):
			break

	print(values)
	print(output_path)
	window.close()

# TODO
#	Extract LN of CB and others based on the regex
#	Validate the file against the VTF
#	if not sbo raise flags
# 	if desc not filled raise flag
# 	if gateway not filled raise flag
