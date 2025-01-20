# %%
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

# %%
client = OpenAI()

# %%


def gerar_resposta(mensagens, model="gpt-4-turbo-2024-04-09", max_tokens=200, temperature=0.5, stream=False):
    resposta = client.chat.completions.create(
        messages=mensagens,
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        stream=stream
    )
    if stream:
        resposta_completa = ''
        print(f'Assistant: ', end='')
        for token in resposta:
            texto = token.choices[0].delta.content
            if texto:
                resposta_completa += texto
                print(texto, end='')
        print()
        mensagens.append({'role': 'assistant', 'content': resposta_completa})
    else:
        print(f'Assistant: ', end='')
        print(resposta.choices[0].message.content)
        print()
        mensagens.append(
            resposta.choices[0].message.model_dump(exclude_none=True))
    return mensagens


if __name__ == '__main__':
    # %%
    print('Bem vindo ao ChatBot de SYSPWL. Qual seu nome?')
    print(f'Digite a qualquer momento "sair", para sair do ChatBot.')
    nome = ''
    iniciar_chat = False
    mensagens = []

    while True:
        nome = input('Digite seu nome aqui: ')
        if nome.lower() == 'sair':
            print('Agradecemos seu contato. Até breve!')
            break
        if nome:
            print(f'Seu nome é {nome}, está correto?')
            confirmacao_nome = input('Digite S para confirmar!')
            if confirmacao_nome.lower() != 's':
                continue
            else:
                iniciar_chat = True
                break

    if iniciar_chat:
        print(f'Assistant: Olá {nome}, tudo bem? Em que posso ajudar?')
        while True:
            texto_user = input(f'{nome}: ')
            if texto_user.lower() != 'sair':
                mensagens.append({
                    'role': 'user',
                    'content': texto_user
                })
                mensagens = gerar_resposta(mensagens, stream=True)
            else:
                print('Agradecemos seu contato. Até breve!')
                break
