#insta check: 
if 'term' in link_text.lower():
    print(repr(link.text)),link.get('href')

# steam check
for link in soup.find_all("a"):
    link_text = link.get_text(strip=True)
    if "ssa" in link_text.lower() or "subscriber" in link_text.lower() or "terms" in link_text.lower():
        print(repr(link_text), link.get("href"))

# pinterest 
   all_links = soup.find_all("a")
    print(f"Total links found: {len(all_links)}") 
    for link in all_links:
     print(repr(link.get_text(strip=True)))


#to test

try:
    element = driver.find_element(By.PARTIAL_LINK_TEXT , "Terms")
    print("Found!")
except NoSuchElementException:
    print("not found")