import requests
import json
import xlwt
import os

doc_name = "complete.xls"

#그냥 그대로 따라한 excel 설정
workbook = xlwt.Workbook(encoding='utf-8')
workbook.default_style.font.height = 20*11   #font설정 11pt

#그냥 그대로 따라한 사용자 정의 색깔 설정
xlwt.add_palette_colour("lightgray", 0x21)
workbook.set_colour_RGB(0x21, 216, 216, 216)
xlwt.add_palette_colour("lightgreen", 0x22)
workbook.set_colour_RGB(0x22, 216,228,188)

apikey= '17676e1221128d0f94607400591df0406ad85fba8eb24ffda413781e9e36d5e6'
gparams = {'apikey': apikey}

for root, dirs, files in os.walk('./'):
    for file in files:
        if file != 'complete.py':
            worksheet = workbook.add_sheet(file)
            col_width_0 = 256*20
            col_width_1 = 256*18
            col_width_2 = 256*20
            col_width_3 = 256*50
            col_height_content = 48
            worksheet.col(0).width = col_width_0
            worksheet.col(1).width = col_width_1
            worksheet.col(2).width = col_width_2
            worksheet.col(3).width = col_width_3
            content_style = "font:height 180; align: wrap on"
            detect_style = "font:height 180; pattern: pattern solid, fore_color lightgreen; align: wrap on, horiz left"
            list_style = "font:height 180,bold on; pattern: pattern solid, fore_color lightgray; align: wrap on, vert centre, horiz center"
            doc_name = file
            files = {'file': ('D:/python/'+file, open('D:/python/'+file, 'rb'))}
            response = requests.post('https://www.virustotal.com/vtapi/v2/file/scan', files=files, params=gparams)
            json_response = response.json()
            pparams = {'apikey' : apikey, 'resource' : json_response['sha256']}
            headers = {
            "Accept-Encoding": "gzip, deflate",
            "User-Agent" : "gzip,  My Python requests library example client or username"
            }
            response2 = requests.get('https://www.virustotal.com/vtapi/v2/file/report',
            params=pparams, headers=headers)
            json_res = response2.json()
            a = list(json_res['scans'].keys())
            b = list(json_res['scans'].values())
            worksheet.write_merge(0,0,0,3,file,xlwt.easyxf(list_style))
            worksheet.write(1,0,u"sha5", xlwt.easyxf(content_style))
            worksheet.write_merge(1,1,1,3,json_response['sha256'], xlwt.easyxf(content_style))
            worksheet.write(2,0,u"Vaccine", xlwt.easyxf(list_style))
            worksheet.write(2,1,u"Version", xlwt.easyxf(list_style))
            worksheet.write(2,2,u"Update", xlwt.easyxf(list_style))
            worksheet.write(2,3,u"Detect", xlwt.easyxf(list_style))
            for t in range(0,len(a)):
                worksheet.write(3+t,0,a[t],xlwt.easyxf(content_style))
                worksheet.write(3+t,1,b[t]['version'],xlwt.easyxf(content_style))
                worksheet.write(3+t,2,b[t]['update'],xlwt.easyxf(content_style))
                if b[t]['result']==None:
                    worksheet.write(3+t,3,"None",xlwt.easyxf(detect_style))
                else:
                    worksheet.write(3+t,3,b[t]['result'],xlwt.easyxf(detect_style))
            workbook.save(os.path.join(os.path.abspath("."),doc_name)+'.xls')
