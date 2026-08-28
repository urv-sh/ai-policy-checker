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
            messages=[{"role": "user", "content": f"Here is a website's policy: {policy_text} \n\nRespond ONLY with valid JSON in this exact format, nothing else before or after: 'classification': ''...', 'quote': ''...', 'explanation': ''...'. The classification value must be exactly one of: Allowed, Restricted, Permission Required, Unclear. If the scenario is not real, describable use case, then respond with 'classification': ''Invalid Scenario'. For the quote field, include not only the most relevant line but also the one line immediately before it and the one line immediately after it from the source text, so the quote has full surrounding context. Join these lines together separated by ' | ' so they are clearly distinguishable as separate lines, not a single sentence."}])
        w.write(filename + "\n")
        w.write(message.content[0].text + "\n\n")

