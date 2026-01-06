def label_depan(data):
    return f"""
^XA
^PW640
^LL400

^FO30,25^A0N,34,34^FDGeoAssay Laboratory - CIKARANG^FS

^FO30,85^A0N,28,28^FDJob No : {data['job_no']}^FS
^FO30,130^A0N,28,28^FDBox No : {data['box_no']}^FS
^FO30,175^A0N,28,28^FDFirst : {data['first']}^FS
^FO30,220^A0N,28,28^FDLast  : {data['last']}^FS
^FO30,265^A0N,28,28^FDDate Rec'd : {data['date_received']}^FS

^XZ
"""


def label_belakang(data):
    return f"""
^XA
^PW640
^LL400

^FO30,25^A0N,34,34^FDGEOASSAY LABORATORY^FS

^FO30,85^A0N,28,28^FDJob No : {data['job_no']}^FS
^FO30,130^A0N,28,28^FDLSN    : {data['lsn']}^FS
^FO30,175^A0N,28,28^FDSID    : {data['sid']}^FS
^FO30,220^A0N,28,28^FDDate Rec'd : {data['date_received']}^FS
^FO30,270^A0N,28,28^FDBox No : {data['box_no']}^FS

^XZ
"""
