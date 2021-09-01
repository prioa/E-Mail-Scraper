import re
import requests
from bs4 import BeautifulSoup



subpages = set()

emailList = []
valid_emailList = []

#wait for target page input
input_url = str(input('Enter Target URL: '))

#email syntax
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


#function to get page html as plain text
def get_subpages(page_url):
    global count
    global user_url
    pattern = re.compile("^(/)")
    page_html = requests.get(page_url).text
    soup = BeautifulSoup(page_html, "html.parser")
    count = 0

    for link in soup.find_all("a", href=pattern):
        count += 1
        new_subpage_sub = link.attrs["href"]
        new_subpage_full = input_url + new_subpage_sub
        subpages.add(new_subpage_full)


get_subpages(input_url)
print('[i] subsites found: ' + str(count))

#find emails in subpages and pages
for subpage in subpages:
    print('scanning site: ' + subpage)
    getH = requests.get(subpage)
    h = getH.content
    soup_mailto = BeautifulSoup(h, 'html.parser')
    mailtos = soup_mailto.select('a[href^=mailto]')
    for i in mailtos:
        href = i['href']
        try:
            if href in emailList:
                print('Duplicate found')
            else:
                print('New Adress found')
                str1, str2 = href.split(':')
        except ValueError:
            break

        emailList.append(str2)




if not emailList:
    print("No E-Mails found")
else:
    without_duplicates = list(dict.fromkeys(emailList))
    valid_count = 0
    valid_count_total = 0
    for email in without_duplicates:
        valid_count_total += 1
        if (re.fullmatch(regex, email)):
            valid_count += 1
            valid_emailList.append(email)
        else:
            print()

print('\n\n#####################################################\nResults:\n' + str(valid_emailList) + '\n_____________________________________________________________')
print(str(valid_count) + ' out of ' + str(valid_count_total) + ' adresses are valid')
