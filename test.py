
from openai import OpenAI
import os


with open("./OPEN_AI_API.txt", "r") as file:
    os.environ["OPENAI_API_KEY"] = file.read().strip()  


# def get_embedding(text):

#     response = client.embeddings.create(input=[text], model="text-embedding-3-small").data[0].embedding

#     embedding = response.data.embedding
#     print(response)
#     # print(embedding)
#     len(response) 

#     return response


def get_openai_embeddings(texts):
        embeddings = []
        for text in texts:
            response = client.embeddings.create(
                model="text-embedding-3-small",
                input=text
            ).data[0].embedding
            # embeddings.append(response["data"][0]["embedding"])
            embedding = response
            embeddings.append(embedding)
        return embeddings



# Example usage

text_to_embed = "This is a sentence to be embedded."

embedding = get_openai_embeddings(text_to_embed) 

print(embedding) 
