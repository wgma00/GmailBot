# The MIT License (MIT)
# 
# Copyright (c) 2016 Computer Science Enrichment Club 
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in 
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import gspread
import yaml
from oauth2client.service_account import ServiceAccountCredentials


class SpreadSheetTracker(object):
    """ Handles getting user data and uploading to a google spreadsheet.

    Uses the google sheets api to access and upload data.

    Attributes:
        details: map, maps variables to sensitive information.
        torn_api_key: string, api key provided by torn.
        google_creds_path: string, path to the credentials i.e. "*.json".
        google_sheets_key: string, code given to a google spreadsheet.
        wks: worksheet object, object representing the online spreadsheet.
        userbase: map, maps an email(str) to a the following collection:
                  {'first_name':str, 'last_name':str, 'problems_solved':
                  {'score':int, **} where ** are the list of problems they have
                  solved, as specified in the details.yaml.
        current_users: int, number of current users that should be in the
                       database.
    """
    def __init__(self):
        """Initializes basic contents required to access the service."""
        with open("details.yaml", 'r') as yaml_file:
           self.details = yaml.load(yaml_file)
           self.google_creds_path = str(self.details['google_creds_path'])
           self.google_sheets_key = str(self.details['google_sheets_key'])
           self.problem_ids = [i.split(',') for i in self.details['problem_ids']]
           self.wks = None
           self.googleSpreadSheetSetup()
           self.userbase = self.details['userbase']
           self.current_users = self.countNumberOfUsers()
           if(len(self.userbase) < self.current_users
               or current_users == self.wks.row_count):
               self.updateUserbase()

    def googleSpreadSheetSetup(self):
        """Authenticates user into google services and accesses spreadsheet.

        Returns:
            None
        Raises:
            gspread.SpreadsheetNotFound  
        """
        scope = ['https://spreadsheets.google.com/feeds']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(self.google_creds_path, scope)
        gc = gspread.authorize(credentials)
        self.wks = gc.open_by_key(self.google_sheets_key).sheet1

    def updateUserbase(self):
        """ Updates the local database with the entries on the spreadsheet.
        
        Queries the spreadsheet for each user's first name, last name, and
        email address. Note, that this process will take a long time.

        Returns:
            None
        Raises:
            None    
        """
        end_of_sheet = False
        # In this case, we will start from the newest users not added in our
        # currrent database.
        for i in range(len(self.userbase)+2, self.current_users+1):
            if end_of_sheet:
                break
            first_name = ''
            last_name = ''
            email = ''
            for j in 'ABC':
                if self.wks.acell(j+str(i)).value == '': 
                    end_of_sheet = True
                else:
                    # Mapping first three entries in spreadsheet to the 
                    # corresponding entries we need.
                    if j == 'A': first_name = self.wks.acell(j+str(i)).value
                    if j == 'B': last_name = self.wks.acell(j+str(i)).value
                    if j == 'C': email = self.wks.acell(j+str(i)).value
            self.userbase[email] = (first_name, last_name, {})
        # Now we'll be updating the yaml file so we don't have to redo this
        # slow procedure.
        self.details['userbase'] = self.userbase
        with open('details.yaml', 'w') as outfile:
            outfile.write(yaml.dump(self.details, default_flow_style=False))

    def countNumberOfUsers(self):
        """Finds the number of users in the google spreadsheet.
        
        Returns:
            an int that is, number of users in the google spreadsheet.
            If there are no current users in the spread sheet, this returns
            the maximum number of elements in the spreadsheet, i.e. 100
        """
        # We use binary search since this is the monotomic increasing sequence
        # and accessing the api is pretty slow. Takes on average 10 guesses.
        lo = 2
        mid = 0
        hi = self.wks.row_count-1
        while(lo < hi):
            mid = lo + (hi - lo + 1)//2
            if(self.wks.acell('A'+str(mid)).value != ''):
                lo = mid
            else:
                hi = mid-1
        # No users in the spreadsheet
        if self.wks.acell('A'+str(lo)).value == '':
            return self.wks.row_count
        return lo

if __name__ == '__main__':
    sst = SpreadSheetTracker()

