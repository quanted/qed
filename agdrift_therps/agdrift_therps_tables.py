import datetime

def timestamp(agdrift_trex_obj):
    st = datetime.datetime.strptime(agdrift_trex_obj.jid, '%Y%m%d%H%M%S%f').strftime('%A, %Y-%B-%d %H:%M:%S')
    html="""
    <div class="out_">
    <b>Agdrift-Therps<br>
    """
    html = html + st
    html = html + " (EST)</b>"
    html = html + """
    </div>"""
    return html

