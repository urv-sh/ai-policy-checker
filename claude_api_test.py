from anthropic import Anthropic
import os

with open ("api_key.txt", 'r') as f:
    api_key = f.read().strip()

client = Anthropic(api_key=api_key)

# with open("C:/Users/Urvashi/Desktop/ai-policy-checker/Policies/spotify2", "r", encoding="utf-8") as f:
#     policy_text = f.read()

with open('all_sites_policies.txt', 'w',  encoding='utf-8') as w:
    for filename in os.listdir("C:/Users/Urvashi/Desktop/ai-policy-checker/Policies/"):
        full_path = "C:/Users/Urvashi/Desktop/ai-policy-checker/Policies/"+filename
        with open(full_path, 'r' , encoding='utf-8') as f:
            policy_text = f.read()
        message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
                        messages=[{"role": "user", "content": f"Here is a website's policy: {policy_text} Before classifying, carefully review the ENTIRE policy text provided, not just the beginning. Specifically search the full document for any clauses related to: copying, reproduction, distribution, scraping, automated data collection, commercial use, machine learning or AI training, and content restrictions — these clauses may appear anywhere in the document, including near the end. If the policy contains multiple documents combined together, check all of them equally. If you find any clause that restricts, prohibits, or requires permission for the user's described scenario, your classification MUST reflect that restriction, even if other parts of the policy contain general, permissive, or promotional language (such as descriptions of features or personalization). Restriction and prohibition clauses take priority over general service descriptions. Before classifying, also check whether the user's scenario actually relates to the website whose policy was provided. If the scenario clearly names or describes a different organisation, platform, or content source than the one this policy belongs to, respond with 'classification': 'Invalid Scenario', and explain in the explanation field that the scenario does not appear to match the selected site.     Respond ONLY with valid JSON in this exact format, nothing else before or after: 'classification': '...', 'explanation': '...', 'quote': '...'. The classification value must be exactly one of: Allowed, Restricted, Permission Required, Unclear. If the scenario is not a real, describable use case, then respond with 'classification': 'Invalid Scenario'. For the quote field, return only the single line from the source text that is most directly and specifically relevant to the user's described scenario — not a general, supporting, or adjacent clause. Do not include surrounding lines or context. The quote must be consistent with and reference the same clause you identify in your explanation. Verify that this line specifically addresses the core action in the scenario (for example, AI training, scraping, or commercial use), rather than a related but less specific clause such as monetisation or account-sharing restrictions."}])  

        w.write(filename + "\n")
        w.write(message.content[0].text + "\n\n")

