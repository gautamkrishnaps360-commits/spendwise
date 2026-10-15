from google import genai

api_key="AQ.Ab8RN6IBNoDTXM_p0yYk1aar5ul6o5W8UyY1eZF8sLnboXQPbQ"

#step1:authenticate

client=genai.Client(api_key=api_key)


promt="what is ai agent in simple words"

response=client.models.generate_content(

    model="gemini-3.8-flash",

    contents=promt


)

print(response.text)