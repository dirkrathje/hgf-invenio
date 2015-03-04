# -*- coding: utf-8 -*-
##
## This file is part of Invenio.
## Copyright (C) 2011, HGF
##
## CDS Invenio is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation; either version 2 of the
## License, or (at your option) any later version.
##
## CDS Invenio is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with CDS Invenio; if not, write to the Free Software Foundation, Inc.,
## 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

"""
BibFormat element for conference information from 1112_
@author: arwagner
"""
__revision__ = "$Id$"

# Variable naming conventions: we use Uppercase for function names:
# pylint: disable=C0103

from invenio.bibformat_engine import BibFormatObject
import re
import time

def format_element(bfo, tag='1112_', alttag='29510a', separator='<br/>',
                  sep=', ',format='no'):
   # FIXME XFEL is to specific. Refactor
   """
   @param tag: from where to read conference information defaults to 1112_
   @param alttag: if this tag exists additional information is displayed from
                  there. It is assumed to hold the literal dispay that should
                  be rendered.  (Defaults to 29510a and stems from data
                  migration procedures @HGF)
   @param sep: separator for subfields
   @param format: no for standard date format, yes for XFEL date format
   """

   confinfos  = bfo.fields(tag)
   altinfos   = bfo.fields(alttag)
   result     = []
   univ       = bfo.field('502__c')
   talkdate   = bfo.field('245__f')


   for a in altinfos:
       result.append('<span class="altconfinfo">' + a + "</span>")

   # address block start
   startblock  = '<span itemprop="location" itemscope itemtype="http://schema.org/Place">'
   startblock += '<span itemprop="address" itemscope itemtype="http://schema.org/PostalAddress">'

   for c in confinfos:
       line = []
       if 'a' in c:
           line.append('<span itemprop="name">' + c['a'] + '</span>') # Name
       if 'g' in c:
           line.append('<span itemprop="alternateName">' + c['g'] + '</span>') # Acronym

       # open the location span
       if ('c' in c) or ('w' in c) or (univ != ''):
           # Do not append to the array as we will then get useless
           # separator chars (,)
           if len(line) > 0:
               line[len(line)-1] += startblock

       if 'c' in c: # City
           if len(line) == 0:
               line.append(startblock + '<span itemprop="addressLocality">' + c['c'] + '</span>')
           else:
               line.append('<span itemprop="addressLocality">' + c['c'] + '</span>')
       elif univ != '':
           if len(line) == 0:
               line.append(startblock + '<span itemprop="addressLocality">' + univ + '</span>')
           else:
               line.append('<span itemprop="addressLocality">' + univ + '</span>')
       if 'w' in c: # Country
           if len(line) == 0:
               line.append(startblock + '<span itemprop="addressCountry">' + c['w'] + '</span>')
           else:
               line.append('<span itemprop="addressCountry">' + c['w'] + '</span>')

       # close the location span
       if ('c' in c) or ('w' in c) or (univ != ''):
           line[len(line)-1] += '</span>'

       if 'd' in c:
           d = re.compile(r'[0-9][0-9]:[0-9][0-9]:[0-9][0-9]')
           date = d.sub('', c['d']) # strip of time codes
           if format=='yes':
               try:
                   date = change_time_format(date)
               except:
                   date = date
           if date != '':
               line.append(date)
       else:
          line.append(talkdate)
       result.append('<span itemscope itemtype="http://schema.org/Event" class="subconfinfo">' + sep.join(line) + '</span></span>')

   return separator.join(result)

def change_time_format(date):
   if "/" in date:
       datenew = prepare_date_format(date)
       starttime = time.strptime(datenew[0],"%m %d %Y")
       endtime = time.strptime(datenew[1],"%m %d %Y")
   else:
       datenew = prepare_date_format(date)
       starttime = time.strptime(datenew[0],"%Y %m %d")
       endtime = time.strptime(datenew[1],"%Y %m %d")
   newdate = time.strftime("%-d %B %Y",starttime) + " - " + time.strftime("%-d %B %Y",endtime)
   return newdate

def prepare_date_format(date):
   datenew = str(date).split(' - ')
   datenew[0] = datenew[0].replace("/","").replace("-","")
   datenew[1] = datenew[1].replace("/","").replace("-","")
   return datenew

def escape_values(bfo):
   """
   Called by BibFormat in order to check if output of this element
   should be escaped.
   """
   return 0

def test_format(recID):
   """
   only for testing of format
   """
   bfo = BibFormatObject(recID)
   print format_element(bfo)

if __name__ == '__main__':
   # test_format(recID = 127174)
   # test_format(recID = 62493)
   # test_format(recID = 128409)
   # test_format(recID = 168169)
    test_format(recID = 91169)
