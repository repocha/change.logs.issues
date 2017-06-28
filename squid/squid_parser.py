import sys
sys.path.append('..')
from base_parser import BaseParser

class SquidParser(BaseParser):
  def parse(self, chalog):
    """Parse squid change logs
    """
    totalv = 0
    with open(chalog) as f:
      startflag = False
      prevline = ''
      version = ''
      for line in f:
        lline = line.lower().strip()
        if len(lline) == 0:
          continue
        if lline.startswith('changes to squid-'):
          #Start of a version
          lline = lline.replace('changes to squid-', '')
          version = lline[:lline.find(' ')]
          totalv += 1 
          print version
        elif lline.startswith('-'):
          #Handle the previous one
          if len(prevline) > 0:
            cha = {}
            cha['version'] = version
            cha['changes'] = prevline
            self.cmts.append(cha)
            prevline = line
          else:
            prevline += ' ' + line
        else:
          prevline += ' ' + line
      #the last one
      cha = {}
      cha['version'] = version
      cha['changes'] = prevline
      self.cmts.append(cha)   
      print len(self.cmts)
      print totalv
    
squidp = SquidParser()
squidp.parse('ChangeLog-3.4.txt')
squidp.printN()
