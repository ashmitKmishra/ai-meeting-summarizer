from google import genai

client = genai.Client(api_key="AIzaSyAO45PdsYOuOZliIY93FP7YC0vj5UJiZBU")

for model in client.models.list():
    print(model.name)
