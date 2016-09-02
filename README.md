# GmailBot
This bot will be used for keeping track of individual progress on a spreadsheet.
It will take emails from an email account and parse for emails specifically forwarded
from open kattis

# Setting up
####Python version:
- 3.0 and up 

### Guide:
1. Clone the git repo to your desired location 
2. Use ``pip install -r requirements.txt`` to install dependecies
3. Make sure you have recieved OAuth2 credentials from google, use the following
   as a guide: http://gspread.readthedocs.io/en/latest/oauth2.html 
4. Remember to share the spreadsheet with the email proved from the OAuth2
   process
5. Assuming you're on linux use do the following command in the terminal:
   ``cp details-example.yaml details.yaml`` then edit the ``details.yaml`` file
   as the detailed instructions inquire.
6. Make sure that you have shared 
7. Run using ``python3 app.py``

# Lisence

This is distributed under the terms of the [MIT License][1].
   [1]: https://github.com/csecutsc/GmailBot/blob/master/LICENSE 
