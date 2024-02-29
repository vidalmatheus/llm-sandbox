import base64
import os
import re
import openai

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
import requests
from PIL import Image
from io import BytesIO


def get_response_to_prompt(prompt):
    completion = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ])
    return completion.choices[0].message.content

get_response_to_prompt("Hey, how's it going?")

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

def show_images_from_openai_response(image_url):
    # Download the image
    response = requests.get(image_url)

    if response.status_code == 200:
        # Read the image data
        image_data = BytesIO(response.content)

        # Open the image using PIL
        image = Image.open(image_data)

        # Display the image
        image.show()

        # Extract filename pattern "img-BdAsWGPtwIrVVIS9CUzeEM05.png"
        filename_match = re.search(r'img-[A-Za-z0-9]+\.png', image_url)
        if filename_match:
            filename = f"./img/{filename_match.group()}"
        else:
            filename = "./img/downloaded_image.png"

        # Save the image in the current directory with the extracted filename
        save_path = os.path.join(os.getcwd(), filename)
        image.save(save_path)
        print(f"Image saved as {save_path}")
    else:
        print(f"Failed to download image. Status code: {response.status_code}")


def gen_image(prompt, model="dall-e-3"):
    response = openai.images.generate(
        model=model,
        prompt=prompt,
        size="1024x1024",
        quality="hd",
        n=1,
    )

    for img in response.data:
        image_url = img.url
        print(image_url)
        show_images_from_openai_response(image_url)


def gen_variant(model="dall-e-2"):
    byte_stream: BytesIO = open("./img/img-azpe0gilVzNd2MqhC952QpWT.png", 'rb')
    byte_array = byte_stream.read()
    response = openai.images.create_variation(
        image=byte_array,
        n=1,
        model=model,
        size="1024x1024"
    )
    
    for img in response.data:
        image_url = img.url
        print(image_url)
        print("---------------------------------------")
        show_images_from_openai_response(image_url)


def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')


def gen_description(image_path):
    base64_image = encode_image(image_path)
    headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {openai.api_key}"
    }

    payload = {
    "model": "gpt-4-vision-preview",
    "messages": [
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": "You're a great describer of jewelry. You describe them with very much details when they are in the image."
            },
            {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/png;base64,{base64_image}"
            }
            }
        ]
        }
    ],
    "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    description = response.json()["choices"][0]["message"]["content"]
    print(description)
    print("---------------------------------------")
    return description


IMG_TO_DESCRIPTION = {
    "./img/img-azpe0gilVzNd2MqhC952QpWT.png":
    """
    The image showcases a close-up of an elegant pendant necklace worn by a person. The pendant is a circular disc, crafted with a high degree of detail. Central to its design is a beautifully etched tree of life symbol, meticulously rendered to depict the intricate branches and roots which fill the entirety of the pendant's surface. The tree's canopy and roots are interconnected, forming a continuous and harmonious design within the circular boundary.

    The pendant possesses a metal with a warm, golden hue, suggesting it may be gold or gold-plated, and it hangs gracefully from a delicate gold chain. The chain itself features small, regularly spaced links that catch the light with a subtle gleam. The pendant nestles against the individual's collarbone, its placement indicative of both comfort and style.

    The person wearing the necklace has a smooth, unblemished complexion, and we can see the faintest hint of garments draped around the shoulders—a soft, silky fabric in a neutral, cream color that compliments the warm tones of the jewelry. A portion of the person's hair appears to be softly styled and is of a light, natural tone that does not compete with the prominence of the necklace.
    """
}

def my_gen_variant(image_path, prompt):
    if image_path in IMG_TO_DESCRIPTION.keys():
        description = IMG_TO_DESCRIPTION[image_path]
    else:
        description = gen_description(image_path)
        IMG_TO_DESCRIPTION[image_path] = description
    new_description = f"First prompt: {description}\nNew details: \n{prompt}. \n\nGenerate exact the image with the first prompt, but considering the new details passed."
    print(new_description)
    print("---------------------------------------")
    gen_image(new_description)

# gen_variant()
gen_image("A simple gold necklace with a 5 cm circular pendant of the trxee of life in a given person wearing it")
# gen_image("A woman wearing in her finger a simple plate ring with a little rose gold paw")
# gen_image("Uma pulseira de prata de berloques da Taylor Swift sendo um do album 1989, um do album reputation, um do album speak now, um do album folklore, um do album lover, um do album midnight")
# gen_description("./img/img-azpe0gilVzNd2MqhC952QpWT.png")
# my_gen_variant("./img/img-azpe0gilVzNd2MqhC952QpWT.png", "silver")

