# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.http import Request, FormRequest
from scrapy.utils.response import open_in_browser


class EplanningSpider(Spider):
    index = 0
    name = 'eplanning'
    allowed_domains = ['eplanning.ie']
    start_urls = ['http://eplanning.ie/']

    def parse(self, response):
        urls = response.xpath('//td/a[@target="_blank"]/@href').extract()           #From the start page select the
                                                                                    #branch urls to be scraped
        for url in urls:
            try:
                yield Request(url,callback=self.parse_application)  #request and send each branch to parse function
            except:
                pass                                                #if the request fails move on to next url

    def parse_application(self, response):
        app_url = response.xpath('//*[@class="glyphicon glyphicon-inbox btn-lg"]/'   #From the branch, getting the url
                                 'following-sibling::a/@href').extract_first()      #for the next level down we want to
        try:                                                                        #go to.
            yield Request(response.urljoin(app_url), callback=self.parse_form)  #Requesting a response from the next
        except:                                                                 #next level down.  If we get a 200 reply
            pass                                                                #send the response to the next parse, if
                                                                                #an exception, pass an move on to the
                                                                                #next url in the main parse.

    def parse_form(self, response):
        # data = {
        #     '__RequestVerificationToken': '_tKY_i9PFt8URRfshZmJdsqc-puRzoiBksFzV2csKzA6rj1MTuiap'
        #                                   'YaqzM2HaiWoC85-T3OL1QjlP4S_dKKqCFxOsBjFp7E8zK0SiamOS8Y1',
        #     'AppStatus': '0',
        #     'CheckBoxList[0].Id': '0',
        #     'CheckBoxList[0].Name': 'Leitrim County Council',
        #     'CheckBoxList[0].IsSelected': 'true',
        #     'CheckBoxList[0].IsSelected': 'false',
        #     'RdoTimeLimit': '42',
        #     'SearchType': 'Listing',
        #     'CountyTownCount': '1',
        #     'CountyTownCouncilNames': 'Leitrim County Council:0,'}
        # token = response.xpath('//*[@name="__RequestVerificationToken"]/@value').extract_first()  #token is dynamically
        #                                                                                 #generated, this extracts the
        #                                                                                 #current token before submitting
        #                                                                                 #Form request
        # data['__RequestVerificationToken'] = token
        #data = {'RdoTimeLimit': '42'}  #this just sets the data for at time limit to the value we need
                                       #and leaves the rest of the form at the default values

        data2 = {'RdoTimeLimit': '42','AppStatus': '2'} #passing two arguments to the form dictionary at once

        yield FormRequest.from_response(response,
                                        formdata=data2,
                                        dont_filter=True,#if response is same url, accept it
                                        formxpath='(//form)[2]',    #multiple forms on page, choosing the second form
                                        callback=self.parse_pages)

    def parse_pages(self,response):
        application_urls = response.xpath('//tr/td[1]//@href').extract()

        for url in application_urls:
            url = response.urljoin(url)
            yield Request(url, callback=self.parse_items)

        next_page_url = response.xpath('//*[@class="PagedList-skipToNext"]/a/@href').extract_first()
        abs_next_page_url = response.urljoin(next_page_url)

        try:
            yield Request(abs_next_page_url, callback=self.parse_pages)
        except:
            pass

    def parse_items(self,response):
        agent_button = response.xpath('//input[@title="Show Agents Popup"]/@style').extract_first()

        if 'display: inline;  visibility: visible;' in agent_button:

            name = response.xpath('//tr//th[text()="Name :"]/following-sibling::td/text()').extract_first()

            address_p1 = response.xpath('//tr[th="Address :"]/td/text()').extract()
            address_p2 = response.xpath('//tr[th="Address :"]/following-sibling::tr/td/text()')[0:3].extract()
            address = address_p1+address_p2

            Phone = response.xpath('//tr[th="Phone :"]/td/text()').extract_first()

            Fax = response.xpath('//tr[th="Fax :"]/td/text()').extract_first()

            e_mail = response.xpath('//tr[th="e-mail :"]/td/a/text()').extract()

            url = response.url

            attributes = {'name': name,
                          'address': address,
                          'Phone': Phone,
                          'Fax': Fax,
                          'e_mail': e_mail,
                          'url': url}

            yield attributes

        else:
            self.logger.info('Agent button not found on page, passing invalid url.')



