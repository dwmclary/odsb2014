
import requests
from bs4 import BeautifulSoup
import cx_Oracle
import datetime


base_year = 2004
years = 10
base_url = "http://www.oie.int/animal-health-in-the-world/update-on-avian-influenza/"
report = requests.get(base_url+str(base_year))

searchable_report = BeautifulSoup(report.text)
flu_table = searchable_report.table

row_tags = flu_table.find_all("tr")[1:]

def make_db_row(r):
    #newer reports have an extra year column
    if len(r) > 4:
        r.pop(2)
        
    r[-1]=r[-1].findChild()
    #try to get the report url
    url = None
    try:
        url = r[-1]['href']
    except:
        pass
    row_text = map(lambda x: x.text.encode('ascii', 'ignore'), r)+[url]
    try:
        row_text[2] = datetime.datetime.strptime(row_text[2], "%d/%m/%y").date()
    except Exception as e:
        print r, e
    return tuple(row_text)

data_to_insert = map(lambda x: make_db_row(x.find_all("td")), row_tags)
for i in range(1,years+1):
    print base_year+i
    report = requests.get(base_url+str(base_year+i))
    searchable_report = BeautifulSoup(report.text)
    flu_table = searchable_report.table
    row_tags = flu_table.find_all("tr")[1:]
    data_to_insert += map(lambda x: make_db_row(x.find_all("td")), row_tags)
create_table = """CREATE TABLE PATHOGENIC_FLU (
                    INCIDENT_LOCATION VARCHAR2(100),
                    INCIDENT_TYPE VARCHAR2(50),
                    INCIDENT_DATE DATE,
                    INCIDENT_REPORT VARCHAR2(100),
                    REPORT_LINK VARCHAR2(200)
                    )
                    """
db = cx_Oracle.connect("fludb", "flushot", "localhost:1521/orcl")
cursor = db.cursor()
cursor.execute(create_table)


cursor.prepare("""INSERT INTO PATHOGENIC_FLU
                (INCIDENT_LOCATION,INCIDENT_TYPE,INCIDENT_DATE, INCIDENT_REPORT, REPORT_LINK)
                VALUES
                (:1, :2, :3, :4, :5)
                """)
cursor.executemany(None, data_to_insert)
db.commit()



