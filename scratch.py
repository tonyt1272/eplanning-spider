data = {'__RequestVerificationToken': '_TsflNEGy3wtCDg64_OI_IOANL2riTKFd0OW9uen1zveG8ak3vg0o9zIoaEYbIGxxKQP3R4eqHFjjyQQhPjETDbdA-Zg46W1owI0nqpyXu81',
        'AppStatus': '0',
        'CheckBoxList[0].Id': '0',
        'CheckBoxList[0].Name': 'Leitrim County Council',
        'CheckBoxList[0].IsSelected': 'true',
        'CheckBoxList[0].IsSelected': 'false',
        'RdoTimeLimit': '0',
        'SearchType': 'Listing',
        'CountyTownCount': '1',
        'CountyTownCouncilNames': 'Leitrim County Council:0,'}

http://www.eplanning.ie/LeitrimCC/searchresults


form = FormRequest.from_response(response, formdata=data, dont_filter=True, formxpath='(//form)[2]')