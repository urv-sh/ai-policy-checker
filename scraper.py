import requests
from  bs4 import BeautifulSoup

def scraper_policy(homepage_url, filename):
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"}
    response = requests.get(homepage_url, headers=headers)
   #  print(response.status_code)
   #  # print(len(response.text))
   #  print(response.text[:2000])
    # print("terms" in response.text.lower())
    soup = BeautifulSoup(response.text, "html.parser")
    print(soup.title.get_text())

    terms_url = None 

    for link in soup.find_all("a"): 
        link_text = link.get_text(strip=True)
        if link_text.lower() in ["terms of service", "terms", "terms of use", "steam subscriber agreement", "subscriber agreement", "terms & conditions" , "terms and conditions"]:  
            print(link.get("href"))
            terms_url = link.get("href")

    if terms_url is None:
       print(f"Could not find link for {homepage_url}")
       return 
    
    if terms_url.startswith('/'):
       terms_url = homepage_url.rstrip("/")+terms_url
    
    terms_response = requests.get(terms_url, headers=headers) 
    terms_soup = BeautifulSoup(terms_response.text, "html.parser") 
    print(terms_soup.title.get_text())

    page_text = terms_soup.get_text(separator="\n", strip=True)

    with open(filename, "w", encoding="utf-8") as f:
     f.write(page_text)

homepage_url = input("Please enter or paste your URL link: ")
filename = input("Enter file name: ")
scraper_policy(homepage_url, filename)
