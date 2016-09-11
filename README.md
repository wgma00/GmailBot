# GmailBot
This bot will be used for keeping track of individual progress on a spreadsheet.
It will take emails from an email account and parse for emails specifically forwarded
from open kattis

# Setting up proper environment 
####Python version:
- 3.0 and up 

### Guide:
1. Clone the git repo to your desired location 
2. If you do not have pip installed I recommend using the following guide 
   `https://pip.pypa.io/en/stable/installing/`, specficially you will have to 
   run ``python3 get-pip.py`` under a super user status i.e. sudo or su -. Note
   that simply running something similar to apt-get may give you old modules.
3. Use ``pip install -r requirements.txt`` to install dependecies
4. Make sure you have recieved OAuth2 credentials from google for the use of
   the GoogleSheets API(gspread), use the following as a guide:
   `http://gspread.readthedocs.io/en/latest/oauth2.html` 
5. Remember to share the spreadsheet with the email proved from the OAuth2
   process
6. Make sure you have recieved OAuth credentials from google for hte use of the
   Gmail API, use the following as a guide:
   `https://developers.google.com/gmail/api/quickstart/python`

6. Assuming you're on unix/linux do the following command in the terminal:
   ``cp details-example.yaml details.yaml`` then edit the ``details.yaml`` file
   as the detailed instructions inquire.
7. Run using ``python3 app.py``

# Lisence

This is distributed under the terms of the [MIT License][1].
   [1]: https://github.com/csecutsc/GmailBot/blob/master/LICENSE 
