import os
import re
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


def gen_variant(prompt, model="dall-e-2"):
    card = Image.new("RGBA", (512, 512), (255, 255, 255))
    img = Image.open("./img/me.png").convert("RGBA")
    x, y = img.size
    card.paste(img, (0, 0, x, y), img)
    card.save("./img/me-2.png", format="png")
    response = openai.images.edit(
        model=model,
        image=open("./img/me-2.png", "rb"),
        mask=open("./img/me-2.png", "rb"),
        prompt=prompt,
        n=1,
        size="1024x1024"
    )
    
    for img in response.data:
        image_url = img.url
        print(image_url)
        show_images_from_openai_response(image_url)


# gen_image("A simple gold necklace with a 5 cm circular pendant of the trxee of life in a given person wearing it")
gen_image("A real person wearing a gold necklace with a pendant of a small simple infinity symbol")
# gen_image("A woman wearing in her finger a simple plate ring with a little rose gold paw")
# gen_image("Uma pulseira de prata de berloques da Taylor Swift sendo um do album 1989, um do album reputation, um do album speak now, um do album folklore, um do album lover, um do album midnight")

