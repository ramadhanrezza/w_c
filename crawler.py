from bs4 import BeautifulSoup
import requests
import json
import datetime
import os
import re

def company_index():
    print('Fetching company list.')
    page = requests.get('http://stock.vietnammarkets.com/vietnam-stock-market.php')
    soup = BeautifulSoup(page.content, 'html.parser')

    headers = ['ticker_symbol', 'url', 'company_name', 'business', 'listing_bourse', 'crawling_at']
    list_head = {}
    for i in range(len(headers)):
        list_head[i] = headers[i]
    
    rows = soup.find('div', {"class": "results"}).find_all('tr')
    data = []
    
    for row in rows:
        if row.attrs.get('bgcolor') is None:
            cells = row('td')
            if cells[0].find('a') is not None:
                cells.insert(1,cells[0].find('a'))

            items = {}
            for index in list_head:
                try:
                    items[list_head[index]] = cells[index].text if cells[index].attrs.get('href') is None else cells[index].attrs.get('href')
                except:
                    items[list_head[index]] = datetime.datetime.now().strftime("%Y-%m-%d")

            data.append(items)

    print('Fetching company list completed.')
    return data


def company_details():
    fileOpen = open('company_index.json', 'r')
    company_list = json.load(fileOpen)

    data = []
    try:
        for company_json in company_list:
            print('Get details company: {}'.format(company_json['ticker_symbol']))
            company_page = requests.get(company_json['url'])
            company_bs4 = BeautifulSoup(company_page.content, 'html.parser')

            first_td = company_bs4.find('div', {"class": "results"}).find('table').find('tr').find('td')
            second_td = company_bs4.find('div', {"class": "results"}).find('table').find('tr').find('td').find_next('td').find('table').find_all('tr')
            third_td = company_bs4.find('div', {"class": "results"}).find('table').contents[-2].find('td')

            selected_company = {
                'ticker_symbol': company_json['ticker_symbol'],
                'uid': company_json['url'],
                'country': 'Vietnam'
            }
            
            list_element = []
            regex = re.compile(r'[\n\r\t\xa0]')
            
            for ftd in first_td.contents[:-1]:
                if ftd.find('<br/>') == -1:
                    try:
                        list_element.append(regex.sub('', ftd).split(':')[1].strip())
                    except Exception:
                        list_element.append(regex.sub('', ftd))
                        

            # ticker_symbol, uid, country, company_name, company_address, company_phone_number, company_email, company_website, company_industry, company_description, revenue, financial_summary, business_registration, auditing_company
            details = ['company_name', 'company_street_address', 'company_phone_number', 'company_email', 'company_website', 'business']
            list_head = {}
            for i in range(len(details)):
                list_head[i] = details[i]

            company_details = {}
            for index in list_head:
                try:
                    if index == 2:
                        company_details[list_head[index]] = list_element[2:4]
                    else:
                        v = index
                        if index > 2:
                            v = index+1
                        company_details[list_head[index]] = list_element[v]

                except Exception:
                    pass
            selected_company.update(company_details)

            list_std = {}
            for std in second_td:
                contents = std.contents
                sindex = "_".join(contents[0].text.lower()[:-1].split())
                list_std[sindex] = contents[1].text
            revenue = {
                'revenue': list_std['market_cap']
            }
            financial = {
                'financial_summary': list_std
            }
            selected_company.update(revenue)
            selected_company.update(financial)
            
            tlist_element = []
            for ttd in third_td.contents:
                if ttd.find('<br/>') == -1:
                    tlist_element.append(regex.sub('', ttd))

            tlist = [i for i,x in enumerate(tlist_element) if x == '']
            
            tlist_element = tlist_element[1:-1]
            c_desc = {
                'company_description': ' '.join(tlist_element[tlist[0]:tlist[-3]-1])
            }
            selected_company.update(c_desc)
            
            blist = {}
            for i in tlist_element[tlist[-2]:tlist[-1]]:
                blist["_".join(i.split(':')[0].lower().split())] = i.split(':')[1].strip()
            b_reg = {
                'business_registration': blist
            }

            ahead = {
                0: 'company_name',
                1: 'address',
                2: 'phone_number',
                3: 'website'
            }
            alist = tlist_element[tlist[-3]:tlist[-2]]

            aa = {}
            for i in ahead:
                try:
                    aa[ahead[i]] = alist[i]
                except Exception:
                    aa[ahead[i]] = ''
            
            a_company = {
                'auditing_company': aa
            }
            selected_company.update(b_reg)
            selected_company.update(a_company)
            data.append(selected_company)

        return data
    except Exception:
        return data
    else:
        return data

if __name__ == "__main__":
    if os.path.isfile('company_index.json'):
        print('company_index.json exist::::')
        if os.path.isfile('company_profiles.json') is None:
            profiles = company_details()
            print('company_profiles.json complete::::')
            if profiles:
                with open('company_profiles.json', 'w') as outfile:
                    json.dump(profiles, outfile)
        print('company_profiles.json exist::::')
    else:
        print('company_index.json doesnt exist::::fetch company index::::')
        index = company_index()
        print('company_index.json complete::::')
        if index:
            with open('company_index.json', 'w') as outfile:
                json.dump(index, outfile)
            
            profiles = company_details()
            print('company_profiles.json complete::::')
            if profiles:
                with open('company_profiles.json', 'w') as outfile:
                    json.dump(profiles, outfile)