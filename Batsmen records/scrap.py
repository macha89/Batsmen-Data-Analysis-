import requests
import lxml.html as lh
import pandas as pd
#imprting modules


left_url = 'http://stats.espncricinfo.com/ci/engine/stats/index.html?class=2;orderby=start;page='
right_url = ';template=results;type=batting;view=innings'
j = 0
#loading the url of espncric info from where I extracted the data
pages = []


for pageno in range(1,1827):                                                            #going through all the pages to extract the record
    url= left_url + str(pageno) + right_url                                             #merging page no to url
    page = requests.get(url)
    doc = lh.fromstring(page.content)                                                   #Store the contents of the website under doc
    tr_elements = doc.xpath('//*[@id="ciHomeContentlhs"]/div[3]/table[3]/tbody')        #Parse data that are stored between <tr>..</tr> of HTML

    #Create empty list
    col = []
    #For each row, store each first element
    for t in tr_elements[0]:
        name=t.text_content()
        col.append(name)

    row = []
    for i in col:
        j += 1
        r = i.split("\n")
        r = [i for i in r if i is not ' ']
        r = [i for i in r if i.strip() is not '']
        r = [r[0],r[1],r[10]]                                   #EXTRACTING THE NAME, RUNS IN EACH INNINGS AND DATE FROM THE RECORDS
        row.append((j,r))


    Dict={title:column for (title,column) in row}               #CONVERTING LIST INTO DATAFRAME
    df=pd.DataFrame(Dict)
    df = df.transpose()
    pages.append(df)
    df.head()

final = pd.concat(pages)  #concatinating all the data frames to a single data frame
final.to_csv('data.csv', sep='\t')  #saving the dataframe to csv
