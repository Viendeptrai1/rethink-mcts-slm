from datetime import datetime

class Solution:
    def valid_date(self, date):
        if not date:
            return False
        
        try:
            month, day, year = map(int, date.split('-'))
        except ValueError:
            return False
        
        if month < 1 or month > 12:
            return False
        
        if day < 1:
            return False
        
        if month == 2:
            if day > 29:
                return False
        elif month in [4, 6, 9, 11]:
            if day > 30:
                return False
        else:
            if day > 31:
                return False
        
        try:
            datetime(year, month, day)
        except ValueError:
            return False
        
        return True