from flask import Flask, render_template
from flask import request
import requests
import os
from anthropic import Anthropic
import json
import csv
from datetime import datetime

app = Flask(__name__)

api_key = os.environ.get("ANTHROPIC_API_KEY")

client = Anthropic(api_key=api_key)

@app.route("/"  , methods=["GET","POST"])
def home():
    print(os.getcwd())
    parsed_data = {}   
    scenario = ""
    selected_site = "" 
    site_names = set()
    for filename in os.listdir("Policies/"):
        if filename.endswith("2"):
            stripped_name = filename[:-1].strip()
            site_names.add(stripped_name)
        elif filename.endswith(".txt"):
            stripped_nametxt = filename[:-4]
            site_names.add(stripped_nametxt)
        else:
            nochangesite = filename
            site_names.add(nochangesite)


    if request.method == "POST":
        # print(request.form)
        selected_site = request.form["Websites"]
        scenario = request.form["Scenario"]
        print(selected_site)
        print(scenario)
        base_path = "Policies/" + selected_site
        second_path = "Policies/" + selected_site + " 2"
        print(os.path.exists(second_path))

        if os.path.exists(base_path + ".txt") == True:
            base_path = "Policies/" + selected_site + ".txt"
        else:
            base_path =  "Policies/" + selected_site
        
        if os.path.exists(second_path) == True:
            with open(base_path , 'r', encoding='utf-8') as file1 , open(second_path, 'r', encoding='utf-8') as file2:
                policy1 = file1.read()
                policy2 = file2.read()
                complete_policy = policy1+policy2
                print(len(complete_policy))
                
        else:
            with open(base_path, 'r', encoding='utf-8') as file1:
                policy1 = file1.read()
                complete_policy= policy1
                print(len(complete_policy))

        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1024,
            messages=[{"role": "user", "content": f"Here is a website's policy: {complete_policy} and the user scenario {scenario} Before classifying, carefully review the ENTIRE policy text provided, not just the beginning. Specifically search the full document for any clauses related to: copying, reproduction, distribution, scraping, automated data collection, commercial use, machine learning or AI training, and content restrictions — these clauses may appear anywhere in the document, including near the end. If the policy contains multiple documents combined together, check all of them equally. If you find any clause that restricts, prohibits, or requires permission for the user's described scenario, your classification MUST reflect that restriction, even if other parts of the policy contain general, permissive, or promotional language (such as descriptions of features or personalization). Restriction and prohibition clauses take priority over general service descriptions.Respond ONLY with valid JSON in this exact format, nothing else before or after: 'classification': '...', 'quote': '...', 'explanation': '...'. The classification value must be exactly one of: Allowed, Restricted, Permission Required, Unclear. If the scenario is not a real, describable use case, then respond with 'classification': 'Invalid Scenario'. For the quote field, include not only the most relevant line but also the one line immediately before it and the one line immediately after it from the source text, so the quote has full surrounding context. Join these lines together separated by ' | ' so they are clearly distinguishable as separate lines, not a single sentence."}])
        #print(message.content[0].text)
        ptext = message.content[0].text
        ptext = ptext.replace("```json", "").replace("```", "")
        ptext = ptext.strip()

        try:
            parsed_data = json.loads(ptext)
            form_url = "https://docs.google.com/forms/d/e/1FAIpQLScZf-v_vKz4NkHcgRedYEFgf7WMApnsQdsL0zuHZ4ZECBzgOg/formResponse"
            form_data = {
                    "entry.891702206": selected_site,
                    "entry.1943224188": scenario,
                    "entry.1949090489": parsed_data["classification"],
                    "entry.1107915020": parsed_data["quote"],
                    "entry.202762862": parsed_data["explanation"]
            }

            try:
                response = requests.post(form_url , data = form_data)
                print("Form submit status:", response.status_code)
            except Exception as e:
                print("Error:", e)

        except json.JSONDecodeError:
            parsed_data = {"classification": "Parsing Error", "quote": "", "explanation": "Could not parse the model's response."}

    # print(site_names)
    return render_template("checker.html" , sites=site_names, result = parsed_data , site_choose = selected_site , user_scenario = scenario)
             
if __name__ == "__main__":
    app.run(debug=True)


