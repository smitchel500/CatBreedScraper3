import requests
from bs4 import BeautifulSoup
from app.model import db, Kitty, User

# get the "soup" to parse
cat_html = requests.get("https://en.wikipedia.org/wiki/List_of_cat_breeds").text
soup = BeautifulSoup(cat_html, "html.parser")

# discard the first row of the table, which contains the column headers
heading = soup.select("#firstHeading")[0].text
# grab the remaining table rows
rows = soup.select("table.wikitable tr")[1:]

# for each row, grab the data, create a Kitty object and add it to the database session
for row in rows:
    # grab the breed name from the first column
    breed_name = row.select("th")[0].text.strip()
    # grab the data from the remaining columns in the row
    td = row.select("td")
    country = td[0].text
    origin = td[1].text
    body = td[2].text.strip()
    coat = td[3].text
    pattern = td[4].text
    images = td[5].select("img")
    if images:
        image_url = images[0].attrs["src"]
    # add the data to the session
    db.session.add(Kitty(
        name=breed_name,
        country=country,
        origin=origin,
        body=body,
        coat=coat,
        pattern=pattern,
        image_url=image_url,
    ))

# add a user to the database session
db.session.add(User(username="Ben", email="ben.johnson@umbc.edu"))
# create the database
db.create_all()
# write the session to the database
db.session.commit()
