import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify

app = Flask(__name__)

def scrape_cases():
    url = "https://main.sci.gov.in/judgments"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    table = soup.find("table", {"id": "example"})
    cases = []
    if table:
        for row in table.find_all("tr")[1:]:
            cols = row.find_all("td")
            if len(cols) >= 6:
                cases.append({
                    "diary_no": cols[0].get_text(strip=True),
                    "case_no": cols[1].get_text(strip=True),
                    "petitioner": cols[2].get_text(strip=True),
                    "respondent": cols[3].get_text(strip=True),
                    "judgment_date": cols[4].get_text(strip=True),
                    "pdf_link": cols[5].a["href"] if cols[5].a else None,
                })
    return cases

@app.route("/cases", methods=["GET"])
def get_cases():
    return jsonify(scrape_cases())

if __name__ == "__main__":
    app.run(debug=True)
