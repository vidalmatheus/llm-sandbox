import os
import openai
from openai import OpenAI

client = OpenAI()

response = client.audio.speech.create(
    model="tts-1",
    voice="alloy",
    input="""
		Oláaaaa, meu caro! Eaí, como vai seu dia?
		Espero que bem em. Então... eu estava pensando naquela
		contraproposta que nos pediu e tenho uma ótima notícia.
		Vimos que é possível ser ainda 20% mais barato!!!
	"""
)

response.stream_to_file("output.mp3")
