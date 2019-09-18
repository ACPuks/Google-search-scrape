from selenium import webdriver
from selenium.webdriver.firefox import options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
import requests
import click


def createProfile(access_token, key):
    create_profile_url = 'https://api.multiloginapp.com/v2/profile?token=' + access_token
    name = 'search-' + key.rstrip()
    data = {
        'name': name,
        'browser': 'mimic',
        'os': 'win'
    }

    response = requests.post(create_profile_url, json=data)

    profile_id = response.json()
    print('Created profile ' + name + ' with the ID of ' + profile_id['uuid'])
    return profile_id['uuid']

@click.command()
@click.option(
    '-input_file',
    required=True,
    help='File in which there is the text you want to search'
)
@click.option(
    '-port',
    required=True,
    help='Port where Multilogin is running locally'
)
@click.option(
    '-token',
    required=True,
    help='Your access token to for Multilogin'
)

def runTime(input_file,port, token):
    try:
        file=open(input_file, 'r')
        print('Opened file: '+input_file)
        outputfile=open('output.txt','w')

    except:
        sys.exit('Unable to open file')

    for keyword in file:
        try:
            mla_url = 'http://127.0.0.1:'+port+'/api/v1/profile/start?automation=true&profileId=' + createProfile(token, keyword)
        except:
            sys.exit('Unable to create profile - Double check whether Multilogin is running on the correct port and that the token is valid - Terminating')

        # Launch browser
        response = requests.get(mla_url)
        json = response.json()
        opts = options.DesiredCapabilities()

        # Connect Selenium to launched browser
        browser = webdriver.Remote(command_executor=json['value'], desired_capabilities={})

        browser.get('https://google.com/')

        # Waits for browser to load google, time can be reduced by changing the variable in seconds
        WebDriverWait(browser, 5)
        try:
            search = browser.find_element_by_name('q')
        except:
            print('Unable to find search box on Google - Perhaps try increasing the wait? - Terminating program')
            sys.exit()

        if keyword[-1:] != '\n':
            search.send_keys(keyword + '\n')
        else:
            search.send_keys(keyword)

        try:
            # Waits for browser to load search results page, time can be reduced by changing the variable in seconds
            WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.ID, 'reviewDialog')))
        except:
            browser.quit()
            print('Search timed out - Terminating - Keyword: ' + keyword)

        try:
            link = browser.find_element_by_xpath('//*[@id="search"]/div/div/div/div/div/div/div/div/a').get_attribute(
                'href')
            outputfile.write(keyword.rstrip()+'\n')
            outputfile.write(link+'\n')
        except:
            print('Failed finding link for keyword: ' + keyword)

        browser.close()

    print('Ending search and terminating program')
    file.close()
    outputfile.close()

if __name__ == "__main__":
    runTime()
