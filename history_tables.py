import numpy
from django.template import Context, Template
from django.utils.safestring import mark_safe
import datetime

def table_all(user_hist_obj):
    table1_out = table_1(user_hist_obj)
    html_all = table1_out
    return html_all

def table_1(user_hist_obj):
        # #pre-table 1
        html = '''<table>
                    <tr><th style="display:none">Model</th><th>Index</th><th>User</th><th>Time</th><th style="display:none">jid</th><th>Run Type</th><th>Link</th><tr><tbody id="itemContainer">
               '''
        for i in range(int(user_hist_obj.total_num)):
            html = html + '''<form method="post" action="history_revisit.html" target="_blank">'''
            html = html + '''<tr><td style="display:none"><input name="model_name" id="model_name" value=%s type="text"></td>'''%(user_hist_obj.model_name)
            html = html + "<td>%s</td>"%(i+1)
            html = html + "<td>%s</td>"%(user_hist_obj.user_id[i])
            html = html + "<td>%s</td>"%(user_hist_obj.time_id[i])
            html = html + '''<td style="display:none"><input name="jid" id="jid" value=%s type="text"></td>'''%(user_hist_obj.jid[i])
            html = html + '''<td>%s</td>'''%(user_hist_obj.run_type[i])
            html = html + '''<td><input type="submit" value="View" Class="input_button_%s" ></td></tr>'''%(i+1)
            html = html + "</form>"

        html = html + '''<tr style="display:none"><td id="total_num">%s</td></tr>'''%(user_hist_obj.total_num)
        html = html + '''
                </tbody></table><br>
                <div id="holder_pagination"></div>
            </div>
        '''
        return html

 # 
