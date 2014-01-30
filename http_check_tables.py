from django.template import Context, Template
from django.utils.safestring import mark_safe
import logging
import time
import datetime

def gethttpheader():
	headings = ["#", "Page", "Status", "Reason"]
	return headings

def gethttpdata(counter, page, status, reason):
    data = { 
        "#": counter,
        "Page": page,
        "Status": status,
        "Reason": reason,
    }
    return data

def timestamp():
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%A, %Y-%B-%d %H:%M:%S')
    html="""
    <div class="out_">
        Web Page Functionality Check<br>
    """
    html = html + st
    html = html + " (UTC)</b>"
    html = html + """
    </div>"""
    return html

def table_1(httpheadings, counter, page, status, reason):
    html = """
    <H3 class="out_1 collapsible" id="section1"><span></span>User Inputs</H3>
    <div class="out_">
        <H4 class="out_1 collapsible" id="section2"><span></span>Application and Chemical Information</H4>
            <div class="out_ container_output">
    """
    t1data = gett1data(counter, page, status, reason)
    t1rows = gethtmlrowsfromcols(t1data,httpheadings)
    html = html + tmpl.render(Context(dict(data=t1rows, headings=httpheadings)))
    html = html + """
            </div>
    </div>
    """
    return html

