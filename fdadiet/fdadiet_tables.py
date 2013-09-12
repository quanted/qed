import numpy
from django.template import Context, Template
from django.utils.safestring import mark_safe
from fdadiet import fdadiet_model,fdadiet_parameters
import time
import datetime

def getheader():
	headings = ["Parameter", "Value", "Units"]
	return headings

def getheaderqaqc():
	headings = ["Parameter", "Value", "Expected Value", "Units"]
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


def table_all(fdadiet_obj):
	if fdadiet_obj.run_use == '0':
		html_all = table_1(fdadiet_obj)
		html_all = html_all + table_2(fdadiet_obj)
	else:
		html_all = table_1b(fdadiet_obj)
		html_all = html_all + table_2b(fdadiet_obj)
	return html_all

def table_all_qaqc(fdadiet_obj):
	if fdadiet_obj.run_use == '0':
		html_all = table_1(fdadiet_obj)
		html_all = html_all + table_2_qaqc(fdadiet_obj)
	else:
		html_all = table_1b(fdadiet_obj)
		html_all = html_all + table_2b_qaqc(fdadiet_obj)
	return html_all

def timestamp():
	ts = time.time()
	st = datetime.datetime.fromtimestamp(ts).strftime('%A, %Y-%B-%d %H:%M:%S')
	html="""
	<div class="out_">
		<b>FDA Dietary Exposure Model (Beta)<br>
	"""
	html = html + st
	html = html + " (UTC)</b>"
	html = html + """
	</div>"""
	return html


def gett1data(fdadiet_obj):
	data = { 
		"Parameter": ['Chemical Name','Commercial or Trade Names','"At-Use" Concentration','Sanitizer Residue','"Worst-Case" Estimate of Exposure'],
		"Value": [fdadiet_obj.chemical_name,fdadiet_obj.trade_name,'%.2f'%fdadiet_obj.atuse_conc,'%.2f'%fdadiet_obj.residue,'%.1f'%fdadiet_obj.worst_case_est],
		"Units": ['','',mark_safe('ppm, &#956;g/mg'),mark_safe('mg/cm<sup>2</sup>'),mark_safe('cm<sup>2</sup>/person/day')]
	}
	return data

def gett2data(fdadiet_obj):
	data = { 
		"Parameter": ['Estimated Daily Intake (EDI)'],
		"Value": ['%.1f'%fdadiet_obj.edi],
		"Units": [mark_safe('&#956;g/person/day')]
	}
	return data

def gett2dataqaqc(fdadiet_obj):
	data = { 
		"Parameter": ['Estimated Daily Intake (EDI)'],
		"Value": ['%.1f'%fdadiet_obj.edi],
		"Expected Value": ['%.1f'%fdadiet_obj.edi_exp],
		"Units": [mark_safe('&#956;g/person/day')]
	}
	return data

def gett1bdata(fdadiet_obj):
	data = { 
		"Parameter": ['Chemical Name','Commercial or Trade Names','"At-Use" Concentration','Volume of tank','Cross-sectional diameter of tank','Lenth of tank','Surface Area of tank','Average Intake','90th Percentile Intake'],
		"Value": [fdadiet_obj.chemical_name,fdadiet_obj.trade_name,'%.2f'%fdadiet_obj.atuse_conc,'%.2f'%fdadiet_obj.vol,fdadiet_obj.d,fdadiet_obj.h,fdadiet_obj.sa,'%.2f'%fdadiet_obj.intake_avg,'%.2f'%fdadiet_obj.intake_90th],
		"Units": ['','',mark_safe('ppm, &#956;g/mg'),'gal','ft','ft',mark_safe('ft<sup>2</sup>'),'g/person/day','g/person/day']
	}
	return data

def gett2bdata(fdadiet_obj):
	data = { 
		"Parameter": ['Surface Area of tank','Concentration of %s'%fdadiet_obj.chemical_name,'Average EDI','90th Percentile EDI'],
		"Value": ['%.2f'%fdadiet_obj.sa_cylinder,'%.2f'%fdadiet_obj.conc_unit_conv,'%.1f'%fdadiet_obj.edi_avg_vol,'%.1f'%fdadiet_obj.edi_90th_vol],
		"Units": [mark_safe('ft<sup>2</sup>'),mark_safe('&#956;g/L'),mark_safe('&#956;g/person/day'),mark_safe('&#956;g/person/day')]
	}
	return data

def gett2bdataqaqc(fdadiet_obj):
	data = { 
		"Parameter": ['Surface Area of tank','Concentration of %s'%fdadiet_obj.chemical_name,'Average EDI','90th Percentile EDI'],
		"Value": ['%.2f'%fdadiet_obj.sa_cylinder,'%.2f'%fdadiet_obj.conc_unit_conv,'%.1f'%fdadiet_obj.edi_avg_vol,'%.1f'%fdadiet_obj.edi_90th_vol],
		"Expected Value": ['%.2f'%fdadiet_obj.sa_cylinder_exp,'%.2f'%fdadiet_obj.conc_unit_conv_exp,'%.1f'%fdadiet_obj.edi_avg_vol_exp,'%.1f'%fdadiet_obj.edi_90th_vol_exp],
		"Units": [mark_safe('ft<sup>2</sup>'),mark_safe('&#956;g/L'),mark_safe('&#956;g/person/day'),mark_safe('&#956;g/person/day')]
	}
	return data


headings = getheader()
headingsqaqc = getheaderqaqc()
# sumheadings = getheadersum()
djtemplate = getdjtemplate()
tmpl = Template(djtemplate)


def table_1(fdadiet_obj):
		html = """
		<H3 class="out_1 collapsible" id="section1"><span></span>User Inputs</H3>
        <div class="out_">
			<H4 class="out_1 collapsible" id="section2"><span></span>Sanitizer Properties</H4>
				<div class="out_ container_output">
		"""
		t1data = gett1data(fdadiet_obj)
		t1rows = gethtmlrowsfromcols(t1data,headings)
		html = html + tmpl.render(Context(dict(data=t1rows, headings=headings)))
		html = html + """
				</div>
		</div>
		"""
		return html

def table_1b(fdadiet_obj):
		html = """
		<H3 class="out_1 collapsible" id="section1"><span></span>User Inputs</H3>
        <div class="out_">
			<H4 class="out_1 collapsible" id="section2"><span></span>Sanitizer Properties</H4>
				<div class="out_ container_output">
		"""
		t1data = gett1bdata(fdadiet_obj)
		t1rows = gethtmlrowsfromcols(t1data,headings)
		html = html + tmpl.render(Context(dict(data=t1rows, headings=headings)))
		html = html + """
				</div>
		</div>
		"""
		return html

def table_2(fdadiet_obj):
		html = """
		<br>
		<H3 class="out_1 collapsible" id="section1"><span></span>Model Output</H3>
        <div class="out_">
			<H4 class="out_1 collapsible" id="section2"><span></span>Surface Residue Exposure Estimate of %s</H4>
				<div class="out_ container_output">
		"""%fdadiet_obj.chemical_name
		t1data = gett2data(fdadiet_obj)
		t1rows = gethtmlrowsfromcols(t1data,headings)
		html = html + tmpl.render(Context(dict(data=t1rows, headings=headings)))
		html = html + """
				</div>
		</div>
		"""
		return html

def table_2_qaqc(fdadiet_obj):
		html = """
		<br>
		<H3 class="out_1 collapsible" id="section1"><span></span>Model Output</H3>
        <div class="out_">
			<H4 class="out_1 collapsible" id="section2"><span></span>Surface Residue Exposure Estimate of %s</H4>
				<div class="out_ container_output">
		"""%fdadiet_obj.chemical_name
		t1data = gett2dataqaqc(fdadiet_obj)
		t1rows = gethtmlrowsfromcols(t1data,headingsqaqc)
		html = html + tmpl.render(Context(dict(data=t1rows, headings=headingsqaqc)))
		html = html + """
				</div>
		</div>
		"""
		return html

def table_2b(fdadiet_obj):
		html = """
		<br>
		<H3 class="out_1 collapsible" id="section1"><span></span>Model Output</H3>
        <div class="out_">
			<H4 class="out_1 collapsible" id="section2"><span></span>Tank Residue Exposure Estimate of %s</H4>
				<div class="out_ container_output">
		"""%fdadiet_obj.chemical_name
		t1data = gett2bdata(fdadiet_obj)
		t1rows = gethtmlrowsfromcols(t1data,headings)
		html = html + tmpl.render(Context(dict(data=t1rows, headings=headings)))
		html = html + """
				</div>
		</div>
		"""
		return html

def table_2b_qaqc(fdadiet_obj):
		html = """
		<br>
		<H3 class="out_1 collapsible" id="section1"><span></span>Model Output</H3>
        <div class="out_">
			<H4 class="out_1 collapsible" id="section2"><span></span>Tank Residue Exposure Estimate of %s</H4>
				<div class="out_ container_output">
		"""%fdadiet_obj.chemical_name
		t1data = gett2bdataqaqc(fdadiet_obj)
		t1rows = gethtmlrowsfromcols(t1data,headingsqaqc)
		html = html + tmpl.render(Context(dict(data=t1rows, headings=headingsqaqc)))
		html = html + """
				</div>
		</div>
		"""
		return html