# webscraping for cvedetails.com #for updating vulnerabilities
import requests
from bs4 import BeautifulSoup
import re
import sqlite3
from datetime import datetime
import os


# function for returning the lxml parsing data
def funforparsing(val):
    response = requests.get(val).text
    parsing = BeautifulSoup(response, "lxml")
    return parsing


# pages links#storing all required info in lists
fpl = []
Cve_id = []
Description = []
dates = []
Publish_Date = []
Update_Date = []
# loop for getting data from all 12months in an year
for i in range(1, 13):
    urldum = "https://www.cvedetails.com/vulnerability-list/year-2021/month-{}"
    url = urldum.format(i)
    monthurl = funforparsing(url)
    for pl in monthurl.find_all('div', 'paging'):
        for pll in pl.find_all('a', attrs={'href': re.compile("^/vulnerability-list")}):
            fml = (pll.get('href'))
            # fpl.append(fml)
            originalurl = "https://www.cvedetails.com{}"
            originalpageurl = originalurl.format(fml)
            fpl.append(originalpageurl)
            pagedataofparsing = funforparsing(originalpageurl)
            for dm in pagedataofparsing.find_all('a', attrs={'title': re.compile("^CVE")}):
                cveid_ = re.sub('<[A-Za-z\/][^>]*>', '', str(dm))
                # got cveid's and append to list
                Cve_id.append(cveid_)
            for cvesum in pagedataofparsing.find_all('td', 'cvesummarylong'):
                cvesu = cvesum.prettify()
                cvesumf = re.sub('<[A-Za-z\/][^>]*>', '', str(cvesu))
                # got description of cve and append to list
                Description.append(cvesumf)
            for docveid in pagedataofparsing.find_all('tr', 'srrowns'):
                for tag in docveid.find_all("td"):

                    try:
                        match_str = re.search(r'\d{4}-\d{2}-\d{2}', str(tag))
                        res = datetime.strptime(match_str.group(), '%Y-%m-%d').date()
                        # got all dates
                        dates.append(str(res))
                    except AttributeError:
                        continue

# for getting update dates #got all dates in one list so divided them using even and odd and seperated them as update date and publish date in to seperate lists
for num in range(len(dates)):
    if num % 2 != 0:
        Update_Date.append(dates[num])
# print(len(Update_Date))
# print(Update_Date)
# for getting publish dates
for numm in range(len(dates)):
    if numm % 2 == 0:
        Publish_Date.append(dates[numm])
# print(len(Publish_Date))
# print(Publish_Date)
# print(len(Cve_id))
# print(len(Description))

# inserting to database #creating a db file
conn = sqlite3.connect('cvedata2021new')
c = conn.cursor()


def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS cvedata2021(Cve_id INT,Description TEXT,Publish_Date  INT,Update_Date INT)')
    print("table was created")


create_table()

try:
    for i in range(len(Cve_id)):
        I = Cve_id[i]
        II = Description[i]
        III = Publish_Date[i]
        IV = Update_Date[i]
        c.execute("INSERT INTO cvedata2021(Cve_id, Description, Publish_Date, Update_Date) VALUES  (?,?,?,?) ",
                  (I, II, III, IV))
        conn.commit()
except Exception as err:
    print("Error:" + str(err))
# done
#last updated file size
size = os.path.getsize('cvedata2021')
print('Size of file is', size, 'bytes')
#latest updated file size
newfilesize = os.path.getsize('cvedata2021new')
print('size of file is', newfilesize, 'bytes')

if newfilesize > size:
    os.remove('cvedata2021')
    os.renames('cvedata2021new', 'cvedata2021')
else:
    print("Error: %s file not found")

