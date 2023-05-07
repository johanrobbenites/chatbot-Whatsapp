import openai
# Indica el API Key
openai.api_key = "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"
# Uso de ChapGPT en Python
model_engine = "text-davinci-003"
prompt = "cual es el mejor banco del peru"
completion = openai.Completion.create(engine=model_engine,
                                    prompt=prompt,
                                    max_tokens=1024,
                                    n=1,
                                    stop=None,
                                    temperature=0.7)
respuesta_completa=""
for choice in completion.choices:
    respuesta_completa=respuesta_completa+choice.text
    print(f"Response: %s" % choice.text)
