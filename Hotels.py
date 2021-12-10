import mysql.connector
import json

hoteldata = []


database = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="Scrapping"
)


def locdata(city):


  mycursor = database.cursor()

  sql = ("SELECT * FROM datatable WHERE location  ="+f"'{city}'")

  mycursor.execute(sql)

  myresult = mycursor.fetchall()

  for x in myresult:
    data = {
      "Title": x[0],
      "Location": x[1],
      "Sleeps": x[2],
      "Bedrooms": x[3],
      "Bathrooms": x[4],
      "Price": x[5],
      "Pictures": {
        "Picture_1": x[6],
        "Picture_2": x[7],
        "Picture_3": x[8],
      },

    }
    hoteldata.append(data)


  data_library = json.dumps(hoteldata, indent = 4)
  print(data_library)
  return data_library