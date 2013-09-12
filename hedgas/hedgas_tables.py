import numpy
from django.template import Context, Template
from django.utils.safestring import mark_safe
from hedgas import hedgas_model,hedgas_parameters
import time
import datetime

def getheaderin():
	headings = ["Parameter", "Value", "Units"]
	return headings

def getheaderout():
	headings = [mark_safe("Respiratory <br>Tract Region"),mark_safe("NOAEL<sub>ADJ</sub>"),mark_safe("MV<sub>a</sub>"),"RGDR",mark_safe("HEC <br>(mg/m<sup>3</sup>)"),mark_safe("HEC <br>(ppm)")]
	return headings

def getheaderoutqaqc():
	headings = [mark_safe("Respiratory <br>Tract Region"),mark_safe("NOAEL<sub>ADJ</sub>"),mark_safe("NOAEL<sub>ADJ</sub> Expected"),mark_safe("MV<sub>a</sub>"),mark_safe("MV<sub>a</sub> Expected"),"RGDR","RGDR Expected",mark_safe("HEC <br>(mg/m<sup>3</sup>)"),mark_safe("HEC Expected <br>(mg/m<sup>3</sup>)"),mark_safe("HEC <br>(ppm)"),mark_safe("HEC Expected <br>(ppm)")]
	return headings

# def getheadersum():
#     headings = ["Parameter", "Mean", "Std", "Min", "Max", "Unit"]
#     return headings

def gethtmlrowsfromcols(data, headings):
	columns = [data[heading] for heading in headings]

	# get the length of the longest column
	max_len = len(max(columns, key=len))

	for col in columns:
		# padding the short columns with None
		col += [None,] * (max_len - len(col))

	# Then rotate the structure...
	rows = [[col[i] for col in columns] for i in range(max_len)]
	return rows

def getdjtemplate():
	dj_template ="""
	<table class="out_">
	{# headings #}
		<tr>
		{% for heading in headings %}
			<th>{{ heading }}</th>
		{% endfor %}
		</tr>
	{# data #}
	{% for row in data %}
	<tr>
		{% for val in row %}
		<td>{{ val|default:'' }}</td>
		{% endfor %}
	</tr>
	{% endfor %}
	</table>
	"""
	return dj_template


def table_all(hedgas_obj):
	html_all = div_input_start()
	check = 1
	if hedgas_obj.run_acuteNonOcc == '1':
		html_all = html_all + table_1(hedgas_obj)
		check = check + 1
	if hedgas_obj.run_stitNonOcc == '1':
		html_all = html_all + table_2(hedgas_obj)
		check = check + 1
	if hedgas_obj.run_ltNonOcc == '1':
		html_all = html_all + table_3(hedgas_obj)
		check = check + 1
	if hedgas_obj.run_acuteOcc == '1':
		html_all = html_all + table_4(hedgas_obj)
		check = check + 1
	if hedgas_obj.run_stitOcc == '1':
		html_all = html_all + table_5(hedgas_obj)
		check = check + 1
	if hedgas_obj.run_ltOcc == '1':
		html_all = html_all + table_6(hedgas_obj)
		check = check + 1

	html_all_out = html_all + div_output_start()
	
	if hedgas_obj.run_acuteNonOcc == '1':
		html_all_out = html_all_out + table_7(hedgas_obj)
	if hedgas_obj.run_stitNonOcc == '1':
		html_all_out = html_all_out + table_8(hedgas_obj)
	if hedgas_obj.run_ltNonOcc == '1':
		html_all_out = html_all_out + table_9(hedgas_obj)
	if hedgas_obj.run_acuteOcc == '1':
		html_all_out = html_all_out + table_10(hedgas_obj)
	if hedgas_obj.run_stitOcc == '1':
		html_all_out = html_all_out + table_11(hedgas_obj)
	if hedgas_obj.run_ltOcc == '1':
		html_all_out = html_all_out + table_12(hedgas_obj)

	if check <= 1:
		html_all = mark_safe("<br><div><h3>Error: No Model(s) selected</h3>") + div_end()
	else:
		html_all = html_all_out + div_end()
	return html_all

def table_all_qaqc(hedgas_obj):
	html_all = div_input_start()
	check = 1
	if hedgas_obj.run_acuteNonOcc == '1':
		html_all = html_all + table_1(hedgas_obj)
		check = check + 1
	if hedgas_obj.run_stitNonOcc == '1':
		html_all = html_all + table_2(hedgas_obj)
		check = check + 1
	if hedgas_obj.run_ltNonOcc == '1':
		html_all = html_all + table_3(hedgas_obj)
		check = check + 1
	if hedgas_obj.run_acuteOcc == '1':
		html_all = html_all + table_4(hedgas_obj)
		check = check + 1
	if hedgas_obj.run_stitOcc == '1':
		html_all = html_all + table_5(hedgas_obj)
		check = check + 1
	if hedgas_obj.run_ltOcc == '1':
		html_all = html_all + table_6(hedgas_obj)
		check = check + 1

	html_all_out = html_all + div_output_start()
	
	if hedgas_obj.run_acuteNonOcc == '1':
		html_all_out = html_all_out + table_7_qaqc(hedgas_obj)
	if hedgas_obj.run_stitNonOcc == '1':
		html_all_out = html_all_out + table_8_qaqc(hedgas_obj)
	if hedgas_obj.run_ltNonOcc == '1':
		html_all_out = html_all_out + table_9_qaqc(hedgas_obj)
	if hedgas_obj.run_acuteOcc == '1':
		html_all_out = html_all_out + table_10_qaqc(hedgas_obj)
	if hedgas_obj.run_stitOcc == '1':
		html_all_out = html_all_out + table_11_qaqc(hedgas_obj)
	if hedgas_obj.run_ltOcc == '1':
		html_all_out = html_all_out + table_12_qaqc(hedgas_obj)

	if check <= 1:
		html_all = mark_safe("<br><div><h3>Error: No Model(s) selected</h3>") + div_end()
	else:
		html_all = html_all_out + div_end()
	return html_all

def timestamp():
	ts = time.time()
	st = datetime.datetime.fromtimestamp(ts).strftime('%A, %Y-%B-%d %H:%M:%S')
	html="""
	<div class="out_">
		<b>HED Gas Calculator (Beta)<br>
	"""
	html = html + st
	html = html + " (UTC)</b>"
	html = html + """
	</div>"""
	return html


def gett1data(hedgas_obj):
	data = { 
		"Parameter": ['Molecular Weight','NOAEL','Hours animal study','Hours human','Days of week animal','Days of week human','Body Weight (animal)',mark_safe('b<sub>0</sub>'),mark_safe('b<sub>1</sub>'),'SAa','TB','PU'],
		"Value": ['%.3f'%hedgas_obj.mw_acuteNonOcc,'%.2f'%hedgas_obj.noael_acuteNonOcc,'%.1f'%hedgas_obj.hrs_animal_acuteNonOcc,'%.1f'%hedgas_obj.hrs_human_acuteNonOcc,'%.1f'%hedgas_obj.dow_animal_acuteNonOcc,'%.1f'%hedgas_obj.dow_human_acuteNonOcc,'N/A','%.2f'%hedgas_obj.b0_acuteNonOcc,'%.2f'%hedgas_obj.b1_acuteNonOcc,'%.2f'%hedgas_obj.SAa_acuteNonOcc,'%.2f'%hedgas_obj.tb_acuteNonOcc,'%.2f'%hedgas_obj.pu_acuteNonOcc,],
		"Units": ['g',mark_safe('mg/m<sup>3</sup>'),'Hrs (acute)','Hrs (acute)','Days (acute)','Days (acute)','kg','','','',mark_safe('cm<sup>2</sup>'),mark_safe('m<sup>2</sup>')],
	}
	return data

def gett2data(hedgas_obj):
	data = { 
		"Parameter": ['Molecular Weight','NOAEL','Hours animal study','Hours human','Days of week animal','Days of week human','Body Weight (animal)',mark_safe('b<sub>0</sub>'),mark_safe('b<sub>1</sub>'),'SAa','TB','PU'],
		"Value": ['%.3f'%hedgas_obj.mw_stitNonOcc,'%.2f'%hedgas_obj.noael_stitNonOcc,'%.1f'%hedgas_obj.hrs_animal_stitNonOcc,'%.1f'%hedgas_obj.hrs_human_stitNonOcc,'%.1f'%hedgas_obj.dow_animal_stitNonOcc,'%.1f'%hedgas_obj.dow_human_stitNonOcc,'%.3f'%hedgas_obj.BWa_stitNonOcc,'%.2f'%hedgas_obj.b0_stitNonOcc,'%.2f'%hedgas_obj.b1_stitNonOcc,'%.2f'%hedgas_obj.SAa_stitNonOcc,'%.2f'%hedgas_obj.tb_stitNonOcc,'%.2f'%hedgas_obj.pu_stitNonOcc,],
		"Units": ['g',mark_safe('mg/m<sup>3</sup>'),'Hrs (subchronic)','Hrs (subchronic)','Days*','Days','kg','','','',mark_safe('cm<sup>2</sup>'),mark_safe('m<sup>2</sup>')],
	}
	return data

def gett3data(hedgas_obj):
	data = { 
		"Parameter": ['Molecular Weight','NOAEL','Hours animal study','Hours human','Days of week animal','Days of week human','Body Weight (animal)',mark_safe('b<sub>0</sub>'),mark_safe('b<sub>1</sub>'),'SAa','TB','PU'],
		"Value": ['%.3f'%hedgas_obj.mw_ltNonOcc,'%.2f'%hedgas_obj.noael_ltNonOcc,'%.1f'%hedgas_obj.hrs_animal_ltNonOcc,'%.1f'%hedgas_obj.hrs_human_ltNonOcc,'%.1f'%hedgas_obj.dow_animal_ltNonOcc,'%.1f'%hedgas_obj.dow_human_ltNonOcc,'%.3f'%hedgas_obj.BWa_ltNonOcc,'%.2f'%hedgas_obj.b0_ltNonOcc,'%.2f'%hedgas_obj.b1_ltNonOcc,'%.2f'%hedgas_obj.SAa_ltNonOcc,'%.2f'%hedgas_obj.tb_ltNonOcc,'%.2f'%hedgas_obj.pu_ltNonOcc,],
		"Units": ['g',mark_safe('mg/m<sup>3</sup>'),'Hrs (chronic)','Hrs (chronic)','Days (chronic)','Days (chronic)','kg','','','',mark_safe('cm<sup>2</sup>'),mark_safe('m<sup>2</sup>')],
	}
	return data

def gett4data(hedgas_obj):
	data = { 
		"Parameter": ['Molecular Weight','NOAEL','Hours animal study','Hours human','Days of week animal','Days of week human','Body Weight (animal)',mark_safe('b<sub>0</sub>'),mark_safe('b<sub>1</sub>'),'SAa','TB','PU'],
		"Value": ['%.3f'%hedgas_obj.mw_acuteOcc,'%.2f'%hedgas_obj.noael_acuteOcc,'%.1f'%hedgas_obj.hrs_animal_acuteOcc,'%.1f'%hedgas_obj.hrs_human_acuteOcc,'%.1f'%hedgas_obj.dow_animal_acuteOcc,'%.1f'%hedgas_obj.dow_human_acuteOcc,'%.3f'%hedgas_obj.BWa_acuteOcc,'%.2f'%hedgas_obj.b0_acuteOcc,'%.2f'%hedgas_obj.b1_acuteOcc,'%.2f'%hedgas_obj.SAa_acuteOcc,'%.2f'%hedgas_obj.tb_acuteOcc,'%.2f'%hedgas_obj.pu_acuteOcc,],
		"Units": ['g',mark_safe('mg/m<sup>3</sup>'),'Hrs (acute)','Hrs (acute)','Days (acute)','Days (acute)','kg','','','',mark_safe('cm<sup>2</sup>'),mark_safe('m<sup>2</sup>')],
	}
	return data

def gett5data(hedgas_obj):
	data = { 
		"Parameter": ['Molecular Weight','NOAEL','Hours animal study','Hours human','Days of week animal','Days of week human','Body Weight (animal)',mark_safe('b<sub>0</sub>'),mark_safe('b<sub>1</sub>'),'SAa','TB','PU'],
		"Value": ['%.3f'%hedgas_obj.mw_stitOcc,'%.2f'%hedgas_obj.noael_stitOcc,'%.1f'%hedgas_obj.hrs_animal_stitOcc,'%.1f'%hedgas_obj.hrs_human_stitOcc,'%.1f'%hedgas_obj.dow_animal_stitOcc,'%.1f'%hedgas_obj.dow_human_stitOcc,'%.3f'%hedgas_obj.BWa_stitOcc,'%.2f'%hedgas_obj.b0_stitOcc,'%.2f'%hedgas_obj.b1_stitOcc,'%.2f'%hedgas_obj.SAa_stitOcc,'%.2f'%hedgas_obj.tb_stitOcc,'%.2f'%hedgas_obj.pu_stitOcc,],
		"Units": ['g',mark_safe('mg/m<sup>3</sup>'),'Hrs (subchronic)','Hrs (subchronic)','Days','Days','kg','','','',mark_safe('cm<sup>2</sup>'),mark_safe('m<sup>2</sup>')],
	}
	return data

def gett6data(hedgas_obj):
	data = { 
		"Parameter": ['Molecular Weight','NOAEL','Hours animal study','Hours human','Days of week animal','Days of week human','Body Weight (animal)',mark_safe('b<sub>0</sub>'),mark_safe('b<sub>1</sub>'),'SAa','TB','PU'],
		"Value": ['%.3f'%hedgas_obj.mw_ltOcc,'%.2f'%hedgas_obj.noael_ltOcc,'%.1f'%hedgas_obj.hrs_animal_ltOcc,'%.1f'%hedgas_obj.hrs_human_ltOcc,'%.1f'%hedgas_obj.dow_animal_ltOcc,'%.1f'%hedgas_obj.dow_human_ltOcc,'%.3f'%hedgas_obj.BWa_ltOcc,'%.2f'%hedgas_obj.b0_ltOcc,'%.2f'%hedgas_obj.b1_ltOcc,'%.2f'%hedgas_obj.SAa_ltOcc,'%.2f'%hedgas_obj.tb_ltOcc,'%.2f'%hedgas_obj.pu_ltOcc,],
		"Units": ['g',mark_safe('mg/m<sup>3</sup>'),'Hrs (chronic)','Hrs (chronic)','Days (chronic)','Days (chronic)','kg','','','',mark_safe('cm<sup>2</sup>'),mark_safe('m<sup>2</sup>')],
	}
	return data

def gett7data(hedgas_obj):
	data = { 
		mark_safe("Respiratory <br>Tract Region"): ['Acute ET','Acute TB','Acute PB','Systemic'],
		mark_safe("NOAEL<sub>ADJ</sub>"): ['%.3f'%hedgas_obj.noael_adj_acuteNonOccET,'','',''],
		mark_safe("MV<sub>a</sub>"): ['%.3f'%hedgas_obj.mv_a_acuteNonOccET,'','',''],
		"RGDR": ['%.3f'%hedgas_obj.rgdr_acuteNonOccET,'%.2f'%hedgas_obj.rgdr_acuteNonOccTB,'%.2f'%hedgas_obj.rgdr_acuteNonOccPU,''],
		mark_safe("HEC <br>(mg/m<sup>3</sup>)"): ['%.2f'%hedgas_obj.hec_acuteNonOccET,'%.2f'%hedgas_obj.hec_acuteNonOccTB,'%.2f'%hedgas_obj.hec_acuteNonOccPU,'%.2f'%hedgas_obj.hec_acuteNonOccSYS],
		mark_safe("HEC <br>(ppm)"): ['%.2f'%hedgas_obj.hec_acuteNonOccET_ppm,'%.2f'%hedgas_obj.hec_acuteNonOccTB_ppm,'%.2f'%hedgas_obj.hec_acuteNonOccPU_ppm,'%.2f'%hedgas_obj.hec_acuteNonOccSYS_ppm],
	}
	return data

def gett8data(hedgas_obj):
	data = { 
		mark_safe("Respiratory <br>Tract Region"): ['ST/IT ET','ST/IT TB','ST/IT PB','Systemic'],
		mark_safe("NOAEL<sub>ADJ</sub>"): ['%.3f'%hedgas_obj.noael_adj_stitNonOccET,'','',''],
		mark_safe("MV<sub>a</sub>"): ['%.3f'%hedgas_obj.mv_a_stitNonOccET,'','',''],
		"RGDR": ['%.3f'%hedgas_obj.rgdr_stitNonOccET,'%.2f'%hedgas_obj.rgdr_stitNonOccTB,'%.2f'%hedgas_obj.rgdr_stitNonOccPU,''],
		mark_safe("HEC <br>(mg/m<sup>3</sup>)"): ['%.2f'%hedgas_obj.hec_stitNonOccET,'%.2f'%hedgas_obj.hec_stitNonOccTB,'%.2f'%hedgas_obj.hec_stitNonOccPU,'%.2f'%hedgas_obj.hec_stitNonOccSYS],
		mark_safe("HEC <br>(ppm)"): ['%.2f'%hedgas_obj.hec_stitNonOccET_ppm,'%.2f'%hedgas_obj.hec_stitNonOccTB_ppm,'%.2f'%hedgas_obj.hec_stitNonOccPU_ppm,'%.2f'%hedgas_obj.hec_stitNonOccSYS_ppm],
	}
	return data

def gett9data(hedgas_obj):
	data = { 
		mark_safe("Respiratory <br>Tract Region"): ['LT ET','LT TB','LT PB','Systemic'],
		mark_safe("NOAEL<sub>ADJ</sub>"): ['%.3f'%hedgas_obj.noael_adj_ltNonOccET,'','',''],
		mark_safe("MV<sub>a</sub>"): ['%.3f'%hedgas_obj.mv_a_ltNonOccET,'','',''],
		"RGDR": ['%.3f'%hedgas_obj.rgdr_ltNonOccET,'%.2f'%hedgas_obj.rgdr_ltNonOccTB,'%.2f'%hedgas_obj.rgdr_ltNonOccPU,''],
		mark_safe("HEC <br>(mg/m<sup>3</sup>)"): ['%.2f'%hedgas_obj.hec_ltNonOccET,'%.2f'%hedgas_obj.hec_ltNonOccTB,'%.2f'%hedgas_obj.hec_ltNonOccPU,'%.2f'%hedgas_obj.hec_ltNonOccSYS],
		mark_safe("HEC <br>(ppm)"): ['%.2f'%hedgas_obj.hec_ltNonOccET_ppm,'%.2f'%hedgas_obj.hec_ltNonOccTB_ppm,'%.2f'%hedgas_obj.hec_ltNonOccPU_ppm,'%.2f'%hedgas_obj.hec_ltNonOccSYS_ppm],
	}
	return data

def gett10data(hedgas_obj):
	data = { 
		mark_safe("Respiratory <br>Tract Region"): ['Acute ET','Acute TB','Acute PB','Systemic'],
		mark_safe("NOAEL<sub>ADJ</sub>"): ['%.3f'%hedgas_obj.noael_adj_acuteOccET,'','',''],
		mark_safe("MV<sub>a</sub>"): ['%.3f'%hedgas_obj.mv_a_acuteOccET,'','',''],
		"RGDR": ['%.3f'%hedgas_obj.rgdr_acuteOccET,'%.2f'%hedgas_obj.rgdr_acuteOccTB,'%.2f'%hedgas_obj.rgdr_acuteOccPU,''],
		mark_safe("HEC <br>(mg/m<sup>3</sup>)"): ['%.2f'%hedgas_obj.hec_acuteOccET,'%.2f'%hedgas_obj.hec_acuteOccTB,'%.2f'%hedgas_obj.hec_acuteOccPU,'%.2f'%hedgas_obj.hec_acuteOccSYS],
		mark_safe("HEC <br>(ppm)"): ['%.2f'%hedgas_obj.hec_acuteOccET_ppm,'%.2f'%hedgas_obj.hec_acuteOccTB_ppm,'%.2f'%hedgas_obj.hec_acuteOccPU_ppm,'%.2f'%hedgas_obj.hec_acuteOccSYS_ppm],
	}
	return data

def gett11data(hedgas_obj):
	data = { 
		mark_safe("Respiratory <br>Tract Region"): ['ST/IT ET','ST/IT TB','ST/IT PB','Systemic'],
		mark_safe("NOAEL<sub>ADJ</sub>"): ['%.3f'%hedgas_obj.noael_adj_stitOccET,'','',''],
		mark_safe("MV<sub>a</sub>"): ['%.3f'%hedgas_obj.mv_a_stitOccET,'','',''],
		"RGDR": ['%.3f'%hedgas_obj.rgdr_stitOccET,'%.2f'%hedgas_obj.rgdr_stitOccTB,'%.2f'%hedgas_obj.rgdr_stitOccPU,''],
		mark_safe("HEC <br>(mg/m<sup>3</sup>)"): ['%.2f'%hedgas_obj.hec_stitOccET,'%.2f'%hedgas_obj.hec_stitOccTB,'%.2f'%hedgas_obj.hec_stitOccPU,'%.2f'%hedgas_obj.hec_stitOccSYS],
		mark_safe("HEC <br>(ppm)"): ['%.2f'%hedgas_obj.hec_stitOccET_ppm,'%.2f'%hedgas_obj.hec_stitOccTB_ppm,'%.2f'%hedgas_obj.hec_stitOccPU_ppm,'%.2f'%hedgas_obj.hec_stitOccSYS_ppm],
	}
	return data

def gett12data(hedgas_obj):
	data = { 
		mark_safe("Respiratory <br>Tract Region"): ['LT ET','LT TB','LT PB','Systemic'],
		mark_safe("NOAEL<sub>ADJ</sub>"): ['%.3f'%hedgas_obj.noael_adj_ltOccET,'','',''],
		mark_safe("MV<sub>a</sub>"): ['%.3f'%hedgas_obj.mv_a_ltOccET,'','',''],
		"RGDR": ['%.3f'%hedgas_obj.rgdr_ltOccET,'%.2f'%hedgas_obj.rgdr_ltOccTB,'%.2f'%hedgas_obj.rgdr_ltOccPU,''],
		mark_safe("HEC <br>(mg/m<sup>3</sup>)"): ['%.2f'%hedgas_obj.hec_ltOccET,'%.2f'%hedgas_obj.hec_ltOccTB,'%.2f'%hedgas_obj.hec_ltOccPU,'%.2f'%hedgas_obj.hec_ltOccSYS],
		mark_safe("HEC <br>(ppm)"): ['%.2f'%hedgas_obj.hec_ltOccET_ppm,'%.2f'%hedgas_obj.hec_ltOccTB_ppm,'%.2f'%hedgas_obj.hec_ltOccPU_ppm,'%.2f'%hedgas_obj.hec_ltOccSYS_ppm],
	}
	return data

def gett7dataqaqc(hedgas_obj):
	data = { 
		mark_safe("Respiratory <br>Tract Region"): ['Acute ET','Acute TB','Acute PB','Systemic'],
		mark_safe("NOAEL<sub>ADJ</sub>"): ['%.3f'%hedgas_obj.noael_adj_acuteNonOccET,'','',''],
		mark_safe("NOAEL<sub>ADJ</sub> Expected"): ['%.3f'%hedgas_obj.noael_adj_acuteNonOccET_exp,'','',''],
		mark_safe("MV<sub>a</sub>"): ['%.3f'%hedgas_obj.mv_a_acuteNonOccET,'','',''],
		mark_safe("MV<sub>a</sub> Expected"): ['%.3f'%hedgas_obj.mv_a_acuteNonOccET_exp,'','',''],
		"RGDR": ['%.3f'%hedgas_obj.rgdr_acuteNonOccET,'%.2f'%hedgas_obj.rgdr_acuteNonOccTB,'%.2f'%hedgas_obj.rgdr_acuteNonOccPU,''],
		"RGDR Expected": ['%.3f'%hedgas_obj.rgdr_acuteNonOccET_exp,'%.2f'%hedgas_obj.rgdr_acuteNonOccTB_exp,'%.2f'%hedgas_obj.rgdr_acuteNonOccPU_exp,''],
		mark_safe("HEC <br>(mg/m<sup>3</sup>)"): ['%.2f'%hedgas_obj.hec_acuteNonOccET,'%.2f'%hedgas_obj.hec_acuteNonOccTB,'%.2f'%hedgas_obj.hec_acuteNonOccPU,'%.2f'%hedgas_obj.hec_acuteNonOccSYS],
		mark_safe("HEC Expected <br>(mg/m<sup>3</sup>)"): ['%.2f'%hedgas_obj.hec_acuteNonOccET_exp,'%.2f'%hedgas_obj.hec_acuteNonOccTB_exp,'%.2f'%hedgas_obj.hec_acuteNonOccPU_exp,'%.2f'%hedgas_obj.hec_acuteNonOccSYS_exp],
		mark_safe("HEC <br>(ppm)"): ['%.2f'%hedgas_obj.hec_acuteNonOccET_ppm,'%.2f'%hedgas_obj.hec_acuteNonOccTB_ppm,'%.2f'%hedgas_obj.hec_acuteNonOccPU_ppm,'%.2f'%hedgas_obj.hec_acuteNonOccSYS_ppm],
		mark_safe("HEC Expected <br>(ppm)"): ['%.2f'%hedgas_obj.hec_acuteNonOccET_ppm_exp,'%.2f'%hedgas_obj.hec_acuteNonOccTB_ppm_exp,'%.2f'%hedgas_obj.hec_acuteNonOccPU_ppm_exp,'%.2f'%hedgas_obj.hec_acuteNonOccSYS_ppm_exp],
	}
	return data

def gett8dataqaqc(hedgas_obj):
	data = { 
		mark_safe("Respiratory <br>Tract Region"): ['Acute ET','Acute TB','Acute PB','Systemic'],
		mark_safe("NOAEL<sub>ADJ</sub>"): ['%.3f'%hedgas_obj.noael_adj_stitNonOccET,'','',''],
		mark_safe("NOAEL<sub>ADJ</sub> Expected"): ['%.3f'%hedgas_obj.noael_adj_stitNonOccET_exp,'','',''],
		mark_safe("MV<sub>a</sub>"): ['%.3f'%hedgas_obj.mv_a_stitNonOccET,'','',''],
		mark_safe("MV<sub>a</sub> Expected"): ['%.3f'%hedgas_obj.mv_a_stitNonOccET_exp,'','',''],
		"RGDR": ['%.3f'%hedgas_obj.rgdr_stitNonOccET,'%.2f'%hedgas_obj.rgdr_stitNonOccTB,'%.2f'%hedgas_obj.rgdr_stitNonOccPU,''],
		"RGDR Expected": ['%.3f'%hedgas_obj.rgdr_stitNonOccET_exp,'%.2f'%hedgas_obj.rgdr_stitNonOccTB_exp,'%.2f'%hedgas_obj.rgdr_stitNonOccPU_exp,''],
		mark_safe("HEC <br>(mg/m<sup>3</sup>)"): ['%.2f'%hedgas_obj.hec_stitNonOccET,'%.2f'%hedgas_obj.hec_stitNonOccTB,'%.2f'%hedgas_obj.hec_stitNonOccPU,'%.2f'%hedgas_obj.hec_stitNonOccSYS],
		mark_safe("HEC Expected <br>(mg/m<sup>3</sup>)"): ['%.2f'%hedgas_obj.hec_stitNonOccET_exp,'%.2f'%hedgas_obj.hec_stitNonOccTB_exp,'%.2f'%hedgas_obj.hec_stitNonOccPU_exp,'%.2f'%hedgas_obj.hec_stitNonOccSYS_exp],
		mark_safe("HEC <br>(ppm)"): ['%.2f'%hedgas_obj.hec_stitNonOccET_ppm,'%.2f'%hedgas_obj.hec_stitNonOccTB_ppm,'%.2f'%hedgas_obj.hec_stitNonOccPU_ppm,'%.2f'%hedgas_obj.hec_stitNonOccSYS_ppm],
		mark_safe("HEC Expected <br>(ppm)"): ['%.2f'%hedgas_obj.hec_stitNonOccET_ppm_exp,'%.2f'%hedgas_obj.hec_stitNonOccTB_ppm_exp,'%.2f'%hedgas_obj.hec_stitNonOccPU_ppm_exp,'%.2f'%hedgas_obj.hec_stitNonOccSYS_ppm_exp],
	}
	return data

def gett9dataqaqc(hedgas_obj):
	data = { 
		mark_safe("Respiratory <br>Tract Region"): ['Acute ET','Acute TB','Acute PB','Systemic'],
		mark_safe("NOAEL<sub>ADJ</sub>"): ['%.3f'%hedgas_obj.noael_adj_ltNonOccET,'','',''],
		mark_safe("NOAEL<sub>ADJ</sub> Expected"): ['%.3f'%hedgas_obj.noael_adj_ltNonOccET_exp,'','',''],
		mark_safe("MV<sub>a</sub>"): ['%.3f'%hedgas_obj.mv_a_ltNonOccET,'','',''],
		mark_safe("MV<sub>a</sub> Expected"): ['%.3f'%hedgas_obj.mv_a_ltNonOccET_exp,'','',''],
		"RGDR": ['%.3f'%hedgas_obj.rgdr_ltNonOccET,'%.2f'%hedgas_obj.rgdr_ltNonOccTB,'%.2f'%hedgas_obj.rgdr_ltNonOccPU,''],
		"RGDR Expected": ['%.3f'%hedgas_obj.rgdr_ltNonOccET_exp,'%.2f'%hedgas_obj.rgdr_ltNonOccTB_exp,'%.2f'%hedgas_obj.rgdr_ltNonOccPU_exp,''],
		mark_safe("HEC <br>(mg/m<sup>3</sup>)"): ['%.2f'%hedgas_obj.hec_ltNonOccET,'%.2f'%hedgas_obj.hec_ltNonOccTB,'%.2f'%hedgas_obj.hec_ltNonOccPU,'%.2f'%hedgas_obj.hec_ltNonOccSYS],
		mark_safe("HEC Expected <br>(mg/m<sup>3</sup>)"): ['%.2f'%hedgas_obj.hec_ltNonOccET_exp,'%.2f'%hedgas_obj.hec_ltNonOccTB_exp,'%.2f'%hedgas_obj.hec_ltNonOccPU_exp,'%.2f'%hedgas_obj.hec_ltNonOccSYS_exp],
		mark_safe("HEC <br>(ppm)"): ['%.2f'%hedgas_obj.hec_ltNonOccET_ppm,'%.2f'%hedgas_obj.hec_ltNonOccTB_ppm,'%.2f'%hedgas_obj.hec_ltNonOccPU_ppm,'%.2f'%hedgas_obj.hec_ltNonOccSYS_ppm],
		mark_safe("HEC Expected <br>(ppm)"): ['%.2f'%hedgas_obj.hec_ltNonOccET_ppm_exp,'%.2f'%hedgas_obj.hec_ltNonOccTB_ppm_exp,'%.2f'%hedgas_obj.hec_ltNonOccPU_ppm_exp,'%.2f'%hedgas_obj.hec_ltNonOccSYS_ppm_exp],
	}
	return data

def gett10dataqaqc(hedgas_obj):
	data = { 
		mark_safe("Respiratory <br>Tract Region"): ['Acute ET','Acute TB','Acute PB','Systemic'],
		mark_safe("NOAEL<sub>ADJ</sub>"): ['%.3f'%hedgas_obj.noael_adj_acuteOccET,'','',''],
		mark_safe("NOAEL<sub>ADJ</sub> Expected"): ['%.3f'%hedgas_obj.noael_adj_acuteOccET_exp,'','',''],
		mark_safe("MV<sub>a</sub>"): ['%.3f'%hedgas_obj.mv_a_acuteOccET,'','',''],
		mark_safe("MV<sub>a</sub> Expected"): ['%.3f'%hedgas_obj.mv_a_acuteOccET_exp,'','',''],
		"RGDR": ['%.3f'%hedgas_obj.rgdr_acuteOccET,'%.2f'%hedgas_obj.rgdr_acuteOccTB,'%.2f'%hedgas_obj.rgdr_acuteOccPU,''],
		"RGDR Expected": ['%.3f'%hedgas_obj.rgdr_acuteOccET_exp,'%.2f'%hedgas_obj.rgdr_acuteOccTB_exp,'%.2f'%hedgas_obj.rgdr_acuteOccPU_exp,''],
		mark_safe("HEC <br>(mg/m<sup>3</sup>)"): ['%.2f'%hedgas_obj.hec_acuteOccET,'%.2f'%hedgas_obj.hec_acuteOccTB,'%.2f'%hedgas_obj.hec_acuteOccPU,'%.2f'%hedgas_obj.hec_acuteOccSYS],
		mark_safe("HEC Expected <br>(mg/m<sup>3</sup>)"): ['%.2f'%hedgas_obj.hec_acuteOccET_exp,'%.2f'%hedgas_obj.hec_acuteOccTB_exp,'%.2f'%hedgas_obj.hec_acuteOccPU_exp,'%.2f'%hedgas_obj.hec_acuteOccSYS_exp],
		mark_safe("HEC <br>(ppm)"): ['%.2f'%hedgas_obj.hec_acuteOccET_ppm,'%.2f'%hedgas_obj.hec_acuteOccTB_ppm,'%.2f'%hedgas_obj.hec_acuteOccPU_ppm,'%.2f'%hedgas_obj.hec_acuteOccSYS_ppm],
		mark_safe("HEC Expected <br>(ppm)"): ['%.2f'%hedgas_obj.hec_acuteOccET_ppm_exp,'%.2f'%hedgas_obj.hec_acuteOccTB_ppm_exp,'%.2f'%hedgas_obj.hec_acuteOccPU_ppm_exp,'%.2f'%hedgas_obj.hec_acuteOccSYS_ppm_exp],
	}
	return data

def gett11dataqaqc(hedgas_obj):
	data = { 
		mark_safe("Respiratory <br>Tract Region"): ['Acute ET','Acute TB','Acute PB','Systemic'],
		mark_safe("NOAEL<sub>ADJ</sub>"): ['%.3f'%hedgas_obj.noael_adj_stitOccET,'','',''],
		mark_safe("NOAEL<sub>ADJ</sub> Expected"): ['%.3f'%hedgas_obj.noael_adj_stitOccET_exp,'','',''],
		mark_safe("MV<sub>a</sub>"): ['%.3f'%hedgas_obj.mv_a_stitOccET,'','',''],
		mark_safe("MV<sub>a</sub> Expected"): ['%.3f'%hedgas_obj.mv_a_stitOccET_exp,'','',''],
		"RGDR": ['%.3f'%hedgas_obj.rgdr_stitOccET,'%.2f'%hedgas_obj.rgdr_stitOccTB,'%.2f'%hedgas_obj.rgdr_stitOccPU,''],
		"RGDR Expected": ['%.3f'%hedgas_obj.rgdr_stitOccET_exp,'%.2f'%hedgas_obj.rgdr_stitOccTB_exp,'%.2f'%hedgas_obj.rgdr_stitOccPU_exp,''],
		mark_safe("HEC <br>(mg/m<sup>3</sup>)"): ['%.2f'%hedgas_obj.hec_stitOccET,'%.2f'%hedgas_obj.hec_stitOccTB,'%.2f'%hedgas_obj.hec_stitOccPU,'%.2f'%hedgas_obj.hec_stitOccSYS],
		mark_safe("HEC Expected <br>(mg/m<sup>3</sup>)"): ['%.2f'%hedgas_obj.hec_stitOccET_exp,'%.2f'%hedgas_obj.hec_stitOccTB_exp,'%.2f'%hedgas_obj.hec_stitOccPU_exp,'%.2f'%hedgas_obj.hec_stitOccSYS_exp],
		mark_safe("HEC <br>(ppm)"): ['%.2f'%hedgas_obj.hec_stitOccET_ppm,'%.2f'%hedgas_obj.hec_stitOccTB_ppm,'%.2f'%hedgas_obj.hec_stitOccPU_ppm,'%.2f'%hedgas_obj.hec_stitOccSYS_ppm],
		mark_safe("HEC Expected <br>(ppm)"): ['%.2f'%hedgas_obj.hec_stitOccET_ppm_exp,'%.2f'%hedgas_obj.hec_stitOccTB_ppm_exp,'%.2f'%hedgas_obj.hec_stitOccPU_ppm_exp,'%.2f'%hedgas_obj.hec_stitOccSYS_ppm_exp],
	}
	return data

def gett12dataqaqc(hedgas_obj):
	data = { 
		mark_safe("Respiratory <br>Tract Region"): ['Acute ET','Acute TB','Acute PB','Systemic'],
		mark_safe("NOAEL<sub>ADJ</sub>"): ['%.3f'%hedgas_obj.noael_adj_ltOccET,'','',''],
		mark_safe("NOAEL<sub>ADJ</sub> Expected"): ['%.3f'%hedgas_obj.noael_adj_ltOccET_exp,'','',''],
		mark_safe("MV<sub>a</sub>"): ['%.3f'%hedgas_obj.mv_a_ltOccET,'','',''],
		mark_safe("MV<sub>a</sub> Expected"): ['%.3f'%hedgas_obj.mv_a_ltOccET_exp,'','',''],
		"RGDR": ['%.3f'%hedgas_obj.rgdr_ltOccET,'%.2f'%hedgas_obj.rgdr_ltOccTB,'%.2f'%hedgas_obj.rgdr_ltOccPU,''],
		"RGDR Expected": ['%.3f'%hedgas_obj.rgdr_ltOccET_exp,'%.2f'%hedgas_obj.rgdr_ltOccTB_exp,'%.2f'%hedgas_obj.rgdr_ltOccPU_exp,''],
		mark_safe("HEC <br>(mg/m<sup>3</sup>)"): ['%.2f'%hedgas_obj.hec_ltOccET,'%.2f'%hedgas_obj.hec_ltOccTB,'%.2f'%hedgas_obj.hec_ltOccPU,'%.2f'%hedgas_obj.hec_ltOccSYS],
		mark_safe("HEC Expected <br>(mg/m<sup>3</sup>)"): ['%.2f'%hedgas_obj.hec_ltOccET_exp,'%.2f'%hedgas_obj.hec_ltOccTB_exp,'%.2f'%hedgas_obj.hec_ltOccPU_exp,'%.2f'%hedgas_obj.hec_ltOccSYS_exp],
		mark_safe("HEC <br>(ppm)"): ['%.2f'%hedgas_obj.hec_ltOccET_ppm,'%.2f'%hedgas_obj.hec_ltOccTB_ppm,'%.2f'%hedgas_obj.hec_ltOccPU_ppm,'%.2f'%hedgas_obj.hec_ltOccSYS_ppm],
		mark_safe("HEC Expected <br>(ppm)"): ['%.2f'%hedgas_obj.hec_ltOccET_ppm_exp,'%.2f'%hedgas_obj.hec_ltOccTB_ppm_exp,'%.2f'%hedgas_obj.hec_ltOccPU_ppm_exp,'%.2f'%hedgas_obj.hec_ltOccSYS_ppm_exp],
	}
	return data


inheadings = getheaderin()
outheadings = getheaderout()
outheadingsqaqc = getheaderoutqaqc()
# sumheadings = getheadersum()
djtemplate = getdjtemplate()
tmpl = Template(djtemplate)


def div_input_start():
	html = """
	<H3 class="out_1 collapsible" id="section1"><span></span>RfC Methodology: User Inputs</H3>
		<div class="out_">
	"""
	return html

def table_1(hedgas_obj):
		html = """
			<H4 class="out_1 collapsible" id="section2"><span></span>Acute HEC Non-Occupational Inputs</H4>
				<div class="out_ container_output">
		"""
		t1data = gett1data(hedgas_obj)
		t1rows = gethtmlrowsfromcols(t1data,inheadings)
		html = html + tmpl.render(Context(dict(data=t1rows, headings=inheadings)))
		html = html + """
				</div>
		"""
		return html

def table_2(hedgas_obj):
		html = """
			<H4 class="out_1 collapsible" id="section2"><span></span>ST/IT HEC Non-Occupational Inputs</H4>
				<div class="out_ container_output">
		"""
		t1data = gett2data(hedgas_obj)
		t1rows = gethtmlrowsfromcols(t1data,inheadings)
		html = html + tmpl.render(Context(dict(data=t1rows, headings=inheadings)))
		html = html + """
				<p>*Developmental studies are 7 days per week for animal exposure whereas 13-week studies are 5 days a week.</p>
				</div>
		"""
		return html

def table_3(hedgas_obj):
		html = """
			<H4 class="out_1 collapsible" id="section2"><span></span>LT HEC Non-Occupational Inputs</H4>
				<div class="out_ container_output">
		"""
		t1data = gett3data(hedgas_obj)
		t1rows = gethtmlrowsfromcols(t1data,inheadings)
		html = html + tmpl.render(Context(dict(data=t1rows, headings=inheadings)))
		html = html + """
				</div>
		"""
		return html

def table_4(hedgas_obj):
		html = """
			<H4 class="out_1 collapsible" id="section2"><span></span>Acute HEC Occupational Inputs</H4>
				<div class="out_ container_output">
		"""
		t1data = gett4data(hedgas_obj)
		t1rows = gethtmlrowsfromcols(t1data,inheadings)
		html = html + tmpl.render(Context(dict(data=t1rows, headings=inheadings)))
		html = html + """
				</div>
		"""
		return html

def table_5(hedgas_obj):
		html = """
			<H4 class="out_1 collapsible" id="section2"><span></span>ST/IT HEC Occupational Inputs</H4>
				<div class="out_ container_output">
		"""
		t1data = gett5data(hedgas_obj)
		t1rows = gethtmlrowsfromcols(t1data,inheadings)
		html = html + tmpl.render(Context(dict(data=t1rows, headings=inheadings)))
		html = html + """
				</div>
		"""
		return html

def table_6(hedgas_obj):
		html = """
			<H4 class="out_1 collapsible" id="section2"><span></span>LT HEC Occupational Inputs</H4>
				<div class="out_ container_output">
		"""
		t1data = gett6data(hedgas_obj)
		t1rows = gethtmlrowsfromcols(t1data,inheadings)
		html = html + tmpl.render(Context(dict(data=t1rows, headings=inheadings)))
		html = html + """
				</div>
		"""
		return html

def div_output_start():
	html = """
	</div>

	<br>
	<H3 class="out_1 collapsible" id="section1"><span></span>Model Outputs</H3>
		<div class="out_">
	"""
	return html

def table_7(hedgas_obj):
		html = """
			<H4 class="out_1 collapsible" id="section2"><span></span>Acute HEC Non-Occupational</H4>
				<div class="out_ container_output">
		"""
		t1data = gett7data(hedgas_obj)
		t1rows = gethtmlrowsfromcols(t1data,outheadings)
		html = html + tmpl.render(Context(dict(data=t1rows, headings=outheadings)))
		html = html + """
				</div>
		"""
		return html

def table_8(hedgas_obj):
		html = """
			<H4 class="out_1 collapsible" id="section2"><span></span>ST/IT HEC Non-Occupational</H4>
				<div class="out_ container_output">
		"""
		t1data = gett8data(hedgas_obj)
		t1rows = gethtmlrowsfromcols(t1data,outheadings)
		html = html + tmpl.render(Context(dict(data=t1rows, headings=outheadings)))
		html = html + """
				</div>
		"""
		return html

def table_9(hedgas_obj):
		html = """
			<H4 class="out_1 collapsible" id="section2"><span></span>LT HEC Non-Occupational</H4>
				<div class="out_ container_output">
		"""
		t1data = gett9data(hedgas_obj)
		t1rows = gethtmlrowsfromcols(t1data,outheadings)
		html = html + tmpl.render(Context(dict(data=t1rows, headings=outheadings)))
		html = html + """
				</div>
		"""
		return html

def table_10(hedgas_obj):
		html = """
			<H4 class="out_1 collapsible" id="section2"><span></span>Acute HEC Occupational</H4>
				<div class="out_ container_output">
		"""
		t1data = gett10data(hedgas_obj)
		t1rows = gethtmlrowsfromcols(t1data,outheadings)
		html = html + tmpl.render(Context(dict(data=t1rows, headings=outheadings)))
		html = html + """
				</div>
		"""
		return html

def table_11(hedgas_obj):
		html = """
			<H4 class="out_1 collapsible" id="section2"><span></span>ST/IT HEC Occupational</H4>
				<div class="out_ container_output">
		"""
		t1data = gett11data(hedgas_obj)
		t1rows = gethtmlrowsfromcols(t1data,outheadings)
		html = html + tmpl.render(Context(dict(data=t1rows, headings=outheadings)))
		html = html + """
				</div>
		"""
		return html

def table_12(hedgas_obj):
		html = """
			<H4 class="out_1 collapsible" id="section2"><span></span>LT HEC Occupational</H4>
				<div class="out_ container_output">
		"""
		t1data = gett12data(hedgas_obj)
		t1rows = gethtmlrowsfromcols(t1data,outheadings)
		html = html + tmpl.render(Context(dict(data=t1rows, headings=outheadings)))
		html = html + """
				</div>
		"""
		return html

def div_end():
	html = """
	</div>
	"""
	return html

# def table_1_qaqc(hedgas_obj):
# 		html = """
# 			<H4 class="out_1 collapsible" id="section2"><span></span>Acute HEC Non-Occupational Inputs</H4>
# 				<div class="out_ container_output">
# 		"""
# 		t1data = gett1dataqaqc(hedgas_obj)
# 		t1rows = gethtmlrowsfromcols(t1data,inheadings)
# 		html = html + tmpl.render(Context(dict(data=t1rows, headings=inheadings)))
# 		html = html + """
# 				</div>
# 		"""
# 		return html

# def table_2_qaqc(hedgas_obj):
# 		html = """
# 			<H4 class="out_1 collapsible" id="section2"><span></span>ST/IT HEC Non-Occupational Inputs</H4>
# 				<div class="out_ container_output">
# 		"""
# 		t1data = gett2dataqaqc(hedgas_obj)
# 		t1rows = gethtmlrowsfromcols(t1data,inheadings)
# 		html = html + tmpl.render(Context(dict(data=t1rows, headings=inheadings)))
# 		html = html + """
# 				<p>*Developmental studies are 7 days per week for animal exposure whereas 13-week studies are 5 days a week.</p>
# 				</div>
# 		"""
# 		return html

# def table_3_qaqc(hedgas_obj):
# 		html = """
# 			<H4 class="out_1 collapsible" id="section2"><span></span>LT HEC Non-Occupational Inputs</H4>
# 				<div class="out_ container_output">
# 		"""
# 		t1data = gett3dataqaqc(hedgas_obj)
# 		t1rows = gethtmlrowsfromcols(t1data,inheadings)
# 		html = html + tmpl.render(Context(dict(data=t1rows, headings=inheadings)))
# 		html = html + """
# 				</div>
# 		"""
# 		return html

# def table_4_qaqc(hedgas_obj):
# 		html = """
# 			<H4 class="out_1 collapsible" id="section2"><span></span>Acute HEC Occupational Inputs</H4>
# 				<div class="out_ container_output">
# 		"""
# 		t1data = gett4dataqaqc(hedgas_obj)
# 		t1rows = gethtmlrowsfromcols(t1data,inheadings)
# 		html = html + tmpl.render(Context(dict(data=t1rows, headings=inheadings)))
# 		html = html + """
# 				</div>
# 		"""
# 		return html

# def table_5_qaqc(hedgas_obj):
# 		html = """
# 			<H4 class="out_1 collapsible" id="section2"><span></span>ST/IT HEC Occupational Inputs</H4>
# 				<div class="out_ container_output">
# 		"""
# 		t1data = gett5dataqaqc(hedgas_obj)
# 		t1rows = gethtmlrowsfromcols(t1data,inheadings)
# 		html = html + tmpl.render(Context(dict(data=t1rows, headings=inheadings)))
# 		html = html + """
# 				</div>
# 		"""
# 		return html

# def table_6_qaqc(hedgas_obj):
# 		html = """
# 			<H4 class="out_1 collapsible" id="section2"><span></span>LT HEC Occupational Inputs</H4>
# 				<div class="out_ container_output">
# 		"""
# 		t1data = gett6dataqaqc(hedgas_obj)
# 		t1rows = gethtmlrowsfromcols(t1data,inheadings)
# 		html = html + tmpl.render(Context(dict(data=t1rows, headings=inheadings)))
# 		html = html + """
# 				</div>
# 		"""
# 		return html

def table_7_qaqc(hedgas_obj):
		html = """
			<H4 class="out_1 collapsible" id="section2"><span></span>Acute HEC Non-Occupational</H4>
				<div class="out_ container_output">
		"""
		t1data = gett7dataqaqc(hedgas_obj)
		t1rows = gethtmlrowsfromcols(t1data,outheadingsqaqc)
		html = html + tmpl.render(Context(dict(data=t1rows, headings=outheadingsqaqc)))
		html = html + """
				</div>
		"""
		return html

def table_8_qaqc(hedgas_obj):
		html = """
			<H4 class="out_1 collapsible" id="section2"><span></span>ST/IT HEC Non-Occupational</H4>
				<div class="out_ container_output">
		"""
		t1data = gett8dataqaqc(hedgas_obj)
		t1rows = gethtmlrowsfromcols(t1data,outheadingsqaqc)
		html = html + tmpl.render(Context(dict(data=t1rows, headings=outheadingsqaqc)))
		html = html + """
				</div>
		"""
		return html

def table_9_qaqc(hedgas_obj):
		html = """
			<H4 class="out_1 collapsible" id="section2"><span></span>LT HEC Non-Occupational</H4>
				<div class="out_ container_output">
		"""
		t1data = gett9dataqaqc(hedgas_obj)
		t1rows = gethtmlrowsfromcols(t1data,outheadingsqaqc)
		html = html + tmpl.render(Context(dict(data=t1rows, headings=outheadingsqaqc)))
		html = html + """
				</div>
		"""
		return html

def table_10_qaqc(hedgas_obj):
		html = """
			<H4 class="out_1 collapsible" id="section2"><span></span>Acute HEC Occupational</H4>
				<div class="out_ container_output">
		"""
		t1data = gett10dataqaqc(hedgas_obj)
		t1rows = gethtmlrowsfromcols(t1data,outheadingsqaqc)
		html = html + tmpl.render(Context(dict(data=t1rows, headings=outheadingsqaqc)))
		html = html + """
				</div>
		"""
		return html

def table_11_qaqc(hedgas_obj):
		html = """
			<H4 class="out_1 collapsible" id="section2"><span></span>ST/IT HEC Occupational</H4>
				<div class="out_ container_output">
		"""
		t1data = gett11dataqaqc(hedgas_obj)
		t1rows = gethtmlrowsfromcols(t1data,outheadingsqaqc)
		html = html + tmpl.render(Context(dict(data=t1rows, headings=outheadingsqaqc)))
		html = html + """
				</div>
		"""
		return html

def table_12_qaqc(hedgas_obj):
		html = """
			<H4 class="out_1 collapsible" id="section2"><span></span>LT HEC Occupational</H4>
				<div class="out_ container_output">
		"""
		t1data = gett12dataqaqc(hedgas_obj)
		t1rows = gethtmlrowsfromcols(t1data,outheadingsqaqc)
		html = html + tmpl.render(Context(dict(data=t1rows, headings=outheadingsqaqc)))
		html = html + """
				</div>
		"""
		return html