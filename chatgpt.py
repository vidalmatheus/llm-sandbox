import os
import openai
import requests
from PIL import Image
from io import BytesIO

openai.api_key = os.getenv("OPENAI_API_KEY")

def get_response_to_prompt(prompt):
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}])
    return completion.choices[0].message.content


def get_sentiment_from(text):
    resp = get_response_to_prompt(
        f"""
            Classify the text below, delimited by three dashes (-), as having either a 'positive' or 'negative' sentiment.

        ---
            {text}
        ---
        """
    )
    print(f"{resp}: {text}")


# get_sentiment_from("I'm very tired of this")
# get_sentiment_from("Enough of this")
# get_sentiment_from("I luv u")
# get_sentiment_from("I'm pretty excited about it")

def show_images_from_openai_response(image_resp):
    for img in image_resp["data"]:
        img_url = img["url"]
        response = requests.get(img_url)
        image_data = BytesIO(response.content)
        image = Image.open(image_data)
        image.show()

def gen_image(prompt):
    image_resp = openai.Image.create(prompt=prompt, n=2, size="512x512")
    show_images_from_openai_response(image_resp)

gen_image("A happy person jumping off the christ the redeemer in Rio de Janeiro")
