import sys
sys.path.append('..')
from base_parser import BaseParser

class HTTPDParser(BaseParser):
  def parse(self, chalog):
    """Parse httpd change logs
    """
    totalv = 0
    with open(chalog) as f:
      prevline = ''
      version = ''
      for line in f:
        lline = line.lower().strip()
        if len(lline) == 0:
          continue
        if lline.find('-*- coding: utf-8 -*-') != -1:
          continue
        if lline.startswith('changes with apache'):
          #start of a version
          lline = lline.replace('changes with apache', '')
          version = lline.strip()
          totalv += 1 
          print version
        elif lline.startswith('*)'):
          if len(prevline) > 0:
            #handle the previous one
            cha = {}
            cha['version'] = version
            cha['changes'] = prevline
            self.cmts.append(cha)
            prevline = line
          else:
            prevline += line
        else:
          prevline += ' ' + line
      #the last one
      cha = {}
      cha['version'] = version
      cha['changes'] = prevline
      self.cmts.append(cha)   
      print len(self.cmts)
      print totalv

httpdp = HTTPDParser()
httpdp.parse('CHANGES_ALL')
httpdp.printN()

