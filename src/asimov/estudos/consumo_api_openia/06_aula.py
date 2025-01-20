# %%
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

# %%
client = OpenAI()

# %%


def gerar_chat(mensagens, model="gpt-4-turbo-2024-04-09", max_tokens=200, temperature=0.5, stream=False):
    resposta = client.chat.completions.create(
        messages=mensagens,
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        stream=stream
    )
    if stream:
        resposta_completa = ''
        for token in resposta:
            texto = token.choices[0].delta.content
            if texto:
                resposta_completa += texto
                print(texto, end='')
        mensagens.append({'role': 'assistant', 'content': resposta_completa})
    else:
        print(resposta.choices[0].message.content)
        mensagens.append(
            resposta.choices[0].message.model_dump(exclude_none=True))
    return mensagens


# %%
mensagens = [{
    'role': 'user',
    'content': 'Crie uma pequena historia sobre uma viagem a marte com no máximo 100 palavras'
}]

mensagens = gerar_chat(mensagens, stream=True)
