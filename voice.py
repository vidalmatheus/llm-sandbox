import os
import openai
from openai import OpenAI

openai.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()

response = client.audio.speech.create(
    model="tts-1",
    voice="alloy",
    input="""
		Oláaaaa, meu caro! Fala tu, como vai?
		Acabei de receber uma ligação sua daqui e
		queria entender o que realmente procura, tudo bem para você?"
	"""
)

response.stream_to_file("output.mp3")
