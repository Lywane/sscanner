from lxml import etree


a = """<get_reports_response status_text="OK" status="200"><report id="40d5f390-a3df-4bfa-8d16-f8dfb656f417" format_id="6c248850-1f62-11e1-b082-406186ea4fc5" extension="html" type="scan" content_type="text/html">PCFET0NUWVBFIGh0bWwgUFVCTElDICItLy9XM0MvL0RURCBIVE1MIDQuMDEvL0VOIiAiaHR0cDovL3d3dy53My5vcmcvVFIvaHRtbDQvc3RyaWN0LmR0ZCI+CjxodG1sPgo8aGVhZD4KPG1ldGEgaHR0cC1lcXVpdj0iQ29udGVudC1UeXBlIiBjb250ZW50PSJ0ZXh0L2h0bWw7IGNoYXJzZXQ9VVRGLTgiPgo8c3R5bGU+CmJvZHkgewogIGJhY2tncm91bmQtY29sb3I6ICNGRkZGRkY7CiAgbWFyZ2luOiAwcHg7CiAgZm9udDogc21hbGwgVmVyZGFuYSwgc2Fucy1zZXJpZjsKICBmb250LXNpemU6IDEycHg7CiAgY29sb3I6ICMxQTFBMUE7Cn0KCmRpdi5jb250ZW50IHsKICB3aWR0aDogOTglOwogIGFsaWduOiBjZW50ZXI7CiAgbWFyZ2luLWxlZnQ6IGF1dG87CiAgbWFyZ2luLXJpZ2h0OiBhdXRvOwp9Cgp0ci50YWJsZV9oZWFkIHsKICBiYWNrZ3JvdW5kLWNvbG9yOiAjZDVkNWQ1Owp9CgouZGlmZiB7CiAgd2hpdGUtc3BhY2U6IHByZTsKICBmb250LWZhbWlseTogbW9ub3NwYWNlOwp9CgouZGlmZi5hdCB7CiAgY29sb3I6ICM5OTMyQ0M7Cn0KCi5kaWZmLnBsdXMgewogIGNvbG9yOiAjMDA2NDAwOwp9CgouZGlmZi5taW51cyB7CiAgY29sb3I6ICNCMjIyMjI7Cn0KCmRpdi5mb290ZXIgewogIHRleHQtYWxpZ246IGNlbnRlcjsKfQoKZGl2Lm5vdGUsIGRpdi5vdmVycmlkZSB7CiAgcGFkZGluZzo0cHg7CiAgbWFyZ2luOjNweDsKICBtYXJnaW4tYm90dG9tOjBweDsKICBtYXJnaW4tdG9wOjBweDsKICBib3JkZXI6IDFweCBzb2xpZCAjQ0NDQ0NDOwogIGJvcmRlci10b3A6IDBweDsKICBiYWNrZ3JvdW5kLWNvbG9yOiAjZmZmZjkwOwp9CgoucmVzdWx0X2hlYWQgewogIHBhZGRpbmc6NHB4OwogIG1hcmdpbjozcHg7CiAgbWFyZ2luLWJvdHRvbTowcHg7CiAgY29sb3I6ICNGRkZGRkY7CiAgYm9yZGVyOiAxcHggc29saWQgI0NDQ0NDQzsKICBib3JkZXItYm90dG9tOiAwcHg7CiAgYmFja2dyb3VuZDojZDVkNWQ1Owp9CgoucmVzdWx0X2hlYWQubG93IHsKICBiYWNrZ3JvdW5kOiM1MzlkY2IKfQoKLnJlc3VsdF9oZWFkLm1lZGl1bSB7CiAgYmFja2dyb3VuZDojZjk5ZjMxCn0KCi5yZXN1bHRfaGVhZC5oaWdoIHsKICBiYWNrZ3JvdW5kOiNjYjFkMTcKfQoKLnJlc3VsdF9zZWN0aW9uIHsKICBwYWRkaW5nOjRweDsKICBtYXJnaW46M3B4OwogIG1hcmdpbi1ib3R0b206MHB4OwogIG1hcmdpbi10b3A6MHB4OwogIGJvcmRlcjogMXB4IHNvbGlkICNDQ0NDQ0M7CiAgYm9yZGVyLXRvcDogMHB4Owp9CgoubG9jYXRpb25fZmxvYXQgewogIGZsb2F0OiByaWdodDsKICB0ZXh0LWFsaWduOnJpZ2h0Owp9CgouZGVsdGFfZmxvYXQgewogIGZsb2F0OiBsZWZ0OwogIGZvbnQtc2l6ZTogMjRweDsKICBib3JkZXI6IDJweDsKICBwYWRkaW5nLWxlZnQ6IDJweDsKICBwYWRkaW5nLXJpZ2h0OiA4cHg7CiAgbWFyZ2luOjBweDsKfQoKLmZ1bGxfd2lkdGggewogIHdpZHRoOiAxMDAlOwp9CgpwcmUgewogd2hpdGUtc3BhY2U6IHByZS13cmFwOwogd29yZC13cmFwOiBicmVhay13b3JkOwp9CiAgICAgICAgPC9zdHlsZT4KPHRpdGxlPlNjYW4gUmVwb3J0PC90aXRsZT4KPC9oZWFkPgo8Ym9keT48ZGl2IGNsYXNzPSJjb250ZW50Ij4KPGgxPlN1bW1hcnk8L2gxPgo8cD4KICAgICAgICAgIFRoaXMgZG9jdW1lbnQgcmVwb3J0cyBvbiB0aGUgcmVzdWx0cyBvZiBhbiBhdXRvbWF0aWMgc2VjdXJpdHkgc2Nhbi4KICAgICAgICAgIFRoZSByZXBvcnQgZmlyc3Qgc3VtbWFyaXNlcyB0aGUgcmVzdWx0cyBmb3VuZC4gIFRoZW4sIGZvciBlYWNoIGhvc3QsCiAgICAgICAgICB0aGUgcmVwb3J0IGRlc2NyaWJlcyBldmVyeSBpc3N1ZSBmb3VuZC4gIFBsZWFzZSBjb25zaWRlciB0aGUKICAgICAgICAgIGFkdmljZSBnaXZlbiBpbiBlYWNoIGRlc2NyaXB0aW9uLCBpbiBvcmRlciB0byByZWN0aWZ5IHRoZSBpc3N1ZS4KICAgICAgICA8L3A+CjxwPgogICAgICAgICAgICAgIFZlbmRvciBzZWN1cml0eSB1cGRhdGVzIGFyZSBub3QgdHJ1c3RlZC4KICAgICAgICAgICAgPC9wPgo8cD4KICAgICAgICAgICAgICBPdmVycmlkZXMgYXJlIG9mZi4gIEV2ZW4gd2hlbiBhIHJlc3VsdCBoYXMgYW4gb3ZlcnJpZGUsIHRoaXMgcmVwb3J0IHVzZXMgdGhlIGFjdHVhbCB0aHJlYXQgb2YgdGhlIHJlc3VsdC4KICAgICAgICAgICAgPC9wPgo8cD4KICAgICAgICAgICAgICBJbmZvcm1hdGlvbiBvbiBvdmVycmlkZXMgaXMgaW5jbHVkZWQgaW4gdGhlIHJlcG9ydC4KICAgICAgICAgICAgPC9wPgo8cD4KICAgICAgICAgICAgICBOb3RlcyBhcmUgaW5jbHVkZWQgaW4gdGhlIHJlcG9ydC4KICAgICAgICAgICAgPC9wPgo8cD4KICAgICAgVGhpcyByZXBvcnQgbWlnaHQgbm90IHNob3cgZGV0YWlscyBvZiBhbGwgaXNzdWVzIHRoYXQgd2VyZSBmb3VuZC4KICAgICAgCiAgICAgICAgSXNzdWVzIHdpdGggdGhlIHRocmVhdCBsZXZlbCAiSGlnaCIgYXJlIG5vdCBzaG93bi4KICAgICAgCiAgICAgICAgSXNzdWVzIHdpdGggdGhlIHRocmVhdCBsZXZlbCAiTWVkaXVtIiBhcmUgbm90IHNob3duLgogICAgICAKICAgICAgICBJc3N1ZXMgd2l0aCB0aGUgdGhyZWF0IGxldmVsICJMb3ciIGFyZSBub3Qgc2hvd24uCiAgICAgIAogICAgICAgIElzc3VlcyB3aXRoIHRoZSB0aHJlYXQgbGV2ZWwgIkxvZyIgYXJlIG5vdCBzaG93bi4KICAgICAgCiAgICAgICAgSXNzdWVzIHdpdGggdGhlIHRocmVhdCBsZXZlbCAiRGVidWciIGFyZSBub3Qgc2hvd24uCiAgICAgIAogICAgICAgIElzc3VlcyB3aXRoIHRoZSB0aHJlYXQgbGV2ZWwgIkZhbHNlIFBvc2l0aXZlIiBhcmUgbm90IHNob3duLgogICAgICBPbmx5IHJlc3VsdHMgd2l0aCBhIG1pbmltdW0gUW9EIG9mIDcwIGFyZSBzaG93bi4gPC9wPgo8cD5UaGlzIHJlcG9ydCBjb250YWlucyAwIHJlc3VsdHMuICBCZWZvcmUgZmlsdGVyaW5nIHRoZXJlIHdlcmUgMCByZXN1bHRzLjwvcD4KPHA+QWxsIGRhdGVzIGFyZSBkaXNwbGF5ZWQgdXNpbmcgdGhlIHRpbWV6b25lICJDb29yZGluYXRlZCBVbml2ZXJzYWwgVGltZSIsIHdoaWNoIGlzIGFiYnJldmlhdGVkICJVVEMiLjwvcD4KPHRhYmxlPgo8dHI+Cjx0ZD5TY2FuIHN0YXJ0ZWQ6PC90ZD4KPHRkPjxiPlRodSBKYW4gMTggMDM6Mzc6MDEgMjAxOCBVVEM8L2I+PC90ZD4KPC90cj4KPHRyPgo8dGQ+U2NhbiBlbmRlZDo8L3RkPgo8dGQ+VGh1IEphbiAxOCAwMzozODoxMSAyMDE4IFVUQzwvdGQ+CjwvdHI+Cjx0cj4KPHRkPlRhc2s6PC90ZD4KPHRkPnRhc2tfNV9uZXdzLnNpbmEuY29tLmNuPC90ZD4KPC90cj4KPC90YWJsZT4KPGgyPkhvc3QgU3VtbWFyeTwvaDI+Cjx0YWJsZSB3aWR0aD0iMTAwJSI+Cjx0ciBjbGFzcz0idGFibGVfaGVhZCI+Cjx0ZD5Ib3N0PC90ZD4KPHRkPlN0YXJ0PC90ZD4KPHRkPkVuZDwvdGQ+Cjx0ZD5IaWdoPC90ZD4KPHRkPk1lZGl1bTwvdGQ+Cjx0ZD5Mb3c8L3RkPgo8dGQ+TG9nPC90ZD4KPHRkPkZhbHNlIFBvc2l0aXZlPC90ZD4KPC90cj4KPHRyPgo8dGQ+VG90YWw6IDA8L3RkPgo8dGQ+PC90ZD4KPHRkPjwvdGQ+Cjx0ZD4wPC90ZD4KPHRkPjA8L3RkPgo8dGQ+MDwvdGQ+Cjx0ZD4wPC90ZD4KPHRkPjA8L3RkPgo8L3RyPgo8L3RhYmxlPgo8aDE+UmVzdWx0cyBwZXIgSG9zdDwvaDE+CjxkaXYgY2xhc3M9ImZvb3RlciI+CiAgICAgICAgICAgICAgICAgIFRoaXMgZmlsZSB3YXMgYXV0b21hdGljYWxseSBnZW5lcmF0ZWQuCiAgICAgICAgICAgICAgICA8L2Rpdj4KPC9kaXY+PC9ib2R5Pgo8L2h0bWw+Cg==<owner><name>admin</name></owner><name>2018-01-18T03:37:01Z</name><comment></comment><creation_time>2018-01-18T03:37:01Z</creation_time><modification_time>2018-01-18T03:38:11Z</modification_time><writable>0</writable><in_use>0</in_use><task id="eecea0c3-9a73-4b50-a5a3-22a6cd604cc7"><name>task_5_news.sina.com.cn</name></task><report_format id="6c248850-1f62-11e1-b082-406186ea4fc5"><name>HTML</name></report_format></report><filters id=""><term>apply_overrides=0 min_qod=70 first=1 rows=10 sort=name</term><keywords><keyword><column>apply_overrides</column><relation>=</relation><value>0</value></keyword><keyword><column>min_qod</column><relation>=</relation><value>70</value></keyword><keyword><column>first</column><relation>=</relation><value>1</value></keyword><keyword><column>rows</column><relation>=</relation><value>10</value></keyword><keyword><column>sort</column><relation>=</relation><value>name</value></keyword></keywords></filters><sort><field>name<order>ascending</order></field></sort><reports max="1000" start="1"></reports><report_count>4<filtered>1</filtered><page>1</page></report_count></get_reports_response>"""
tree = etree.XML(a)

#n = tree.xpath("/get_tasks_response/task/name")
#q = tree.xpath("/get_tasks_response/task/status")
#z = tree.xpath("/get_tasks_response/task/@id")
#k = tree.xpath("/get_tasks_response/task/last_report/report/@id")

q = tree.xpath("/get_reports_response/report")

j = 0
for i in xrange(len(q)):
    print q[i].text