# Overview
The script will open up the designated text file, create a browser fingerprint for each keyword, take the first result link and save it to a text file called output.txt.
The format for the output will be alternating lines of the keyword used and then the link.
The browser profiles will be saved as search-keyword
# Requirements
In order to use this script, you would need to have the following installed:
* Multilogin 
* Python 3
* Python libraries: requests, selenium and click 
## Installing Python libraries
In order to install the libraries, open up a Windows command prompt/PowerShell and run the following command:

`pip install requests selenium click`

## Access token & Ports
For the script to run properly, you need to launch the Multilogin application first and login in order to get an access token and designate the port to be used later on.

After you have logged in, follow these steps:
1. Please go to `C:\Users\%username%\.multiloginapp.com` directory and open app.properies file
2. Add the following line: multiloginapp.port=[PORT_NUMBER]
3. Save the app.properties file

> An example port would be 45000

Make sure to copy the token from the app.properties file to someplace accessible.

Next, restart the Multilogin application and you should be all set to run the script.

## Running the script
For the script to run, you need to have the text file with the keywords and the script file in the same folder.

To run the script execute the following command:

 `python googlescrape.py -input_file [FILENAME] -port [PORT_NUMBER] -token [ACCESS TOKEN]`

An example would be 

 `python googlescrape.py -input_file example.txt -port 45000 -token 12345678-abcd-1234-abcd-123456789012`
