from google import genai

client = genai.Client(api_key="AIzaSyAO45PdsYOuOZliIY93FP7YC0vj5UJiZBU")

with open("dummy_transcript.txt", "r") as f:
    transcript = f.read()

prompt = f"""
Extract this information from the transcript:
- executive_summary
- key_points
- action_items (description, owner, due_date)

Transcript:
{transcript}
"""

response = client.models.generate_content(
    model="models/gemini-2.0-flash",
    contents=[prompt],
)

print(response.text)
