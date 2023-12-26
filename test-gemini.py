"""Test for talking with Google Gemini API."""

import pathlib
import textwrap
import json
import google.generativeai as genai


genai.configure(api_key="AIzaSyCC72Bzb3vvgCwvVwvS8i6hYsyaEyaaQ_Q")

# def to_markdown(text):
#   text = text.replace('•', '  *')
#   return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))


# model = genai.GenerativeModel('gemini-pro')
model = genai.GenerativeModel("gemini-pro-vision")

responses = model.generate_content(
    [video1, """Analyze the video from a radiologist perspective. Also, provide a detailed summary as to possible abnormalities with explanation and suggestions if found"""],
    generation_config={
        "max_output_tokens": 2048,
        "temperature": 0.4,
        "top_p": 1,
        "top_k": 32
    },
    )
  
print(responses)

response = model.generate_content('Is reality real?') # input
print(response.prompt_feedback)
print(response.text)