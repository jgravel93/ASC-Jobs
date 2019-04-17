from bs4 import BeautifulSoup
import re
import pandas as pd
import datetime
import urllib

page = urllib.request.urlopen("http://www.asc41.com/dir3/jobposts.htm").read()
soup=BeautifulSoup(page,'lxml')
tables=soup.findAll('table')
table=tables[6]
rows=table.findAll('tr')
rows=rows[1:]

posts={}
p=-1
for r in rows:
    if r.find(lambda tag:[a for a in tag.attrs.values() if a=="#CCCCCC"])!=None:
        p+=1
        posts[p]={'School':None,'School website':None,
                  'Number of positions':None,
                  'Position detail link':None,
                  'Post date':None,'Position':None,
                  'Specialization':None,
                  'Deadline':None}
        l=r.findAll('a')
        rn=0
        schpos=r.findAll('td')[0]
        schpos=schpos.text
        pat=re.compile('\((.*)\s*(Position[s]*)\)')
        pos=pat.search(schpos)
        npos=None
        sch=None
        if pos:
            npos=pos.groups()[0]
            sch=schpos.split(pos[0])[0]
            sch=" ".join(sch.split())
            
        posdetl=l[1].attrs['href']
        #print(posdetl)
        posts[p]['School website']=l[0].attrs['href']
        if posdetl.startswith("http")==False:
            posts[p]['Position detail link']="http://www.asc41.com/dir3/"+posdetl
        else:
            posts[p]['Position detail link']=posdetl
        posts[p]['School']=sch
        posts[p]['Number of positions']=npos
    else:
        cols=r.findAll('td')
        if cols[0].text.startswith('Post Date:'):
            posts[p]['Post date']=" ".join(cols[1].text.split())
        elif cols[0].text.startswith('Position:'):
            posts[p]['Position']=" ".join(cols[1].text.split())
        elif cols[0].text.startswith('Area of Specialization:'):
            posts[p]['Specialization']=" ".join(cols[1].text.split())
        elif cols[0].text.startswith('Deadline:'):
            posts[p]['Deadline']=" ".join(cols[1].text.split())
         
       
df=pd.DataFrame.from_dict(posts,orient='index')
ct=datetime.datetime.now()
date=ct.strftime("%Y%m%d")
df.to_csv('asc_jobs_%s.csv'%date)

        
    
