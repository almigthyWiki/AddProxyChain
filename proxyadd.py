from bs4 import BeautifulSoup
import ipaddress
import requests

"""
Extracting data from Socks Proxy
finding all 'td' label  where are the proxy data
"""
data= requests.get('https://socks-proxy.net')
soup = BeautifulSoup(data.content,'html.parser')
proxyData = soup.find_all('td')
parserData=[]

"""
extraction, filtering and adding "td" label to a list
"""
for td in proxyData:
    metaData= str(td).lstrip('<td>').strip('</td>')
    parserData.append(metaData)

# Counter
counter=0
"""
reading list and extract metadata
Country Code and Country Name for add more verbose
but is not in for now
"""
for object in parserData:
    try:
        # Filterting data and call
        if ipaddress.IPv4Address(object):
            counter+=1
            # Proxy Port
            portProxy=parserData.index(object) + 1
            # Country Code
            codeProxy=parserData.index(object) + 2
            # Country Name
            countryProxy=parserData.index(object) + 3
            # Socks Type - always socks4
            sockProxy=parserData.index(object) + 4

            # Open proxychains.conf in append mode for update with socks-proxy info
            file=open('/etc/proxychains.conf', 'a')
            SocksProxy='\n{} {} {}'.format(parserData[sockProxy].lower(),object,parserData[portProxy])
            file.writelines(SocksProxy.lstrip(' '))
        else:
            pass
        # Close file proxychains.conf
        file.close()
    except ipaddress.AddressValueError:
        pass
print(counter,"Proxy's was added to proxychains.conf")
