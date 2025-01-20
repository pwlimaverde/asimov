"""Desafio da aula 09 - ChatBot financeiro"""

import json

from yfinance import Ticker  # type: ignore
from dotenv import find_dotenv, load_dotenv
from openai import OpenAI

_ = load_dotenv(find_dotenv())

client = OpenAI()

# %%


def retorna_cotacao_acao_historica(ticker: str, periodo: str = "1mo") -> str:
    """Função para retornar a cotação de um ativo financeiro em um determinado período"""
    ticker_obj = Ticker(f"{ticker}.SA")
    hist = ticker_obj.history(period=periodo)["Close"]
    hist.index = hist.index.strftime("%Y-%m-%d")
    hist = round(hist, 2)
    if len(hist) > 30:
        slice_size = int(len(hist) / 30)
        hist = hist.iloc[::-slice_size][::-1]
    return hist.to_json()


# %%

# %%
tools = [
    {
        "type": "function",
        "function": {
            "name": "retorna_cotacao_acao_historica",
            "description": "Obtém a cotação de um ativo financeiro em um determinado periodo",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticker": {
                        "type": "string",
                        "description": "Codigo ou ticker da empresa na bolsa brasileira."
                        " Ex: ABEV3 para ambev, PETR4 para petrobras.",
                    },
                    "periodo": {
                        "type": "string",
                        "description": "Abreviacao do periodo requerido. Ex: 1d, que"
                        " corresponde a 1 dia e 1mo, que corresponde a um mês",
                        "enum": [
                            "1d",
                            "5d",
                            "1mo",
                            "3mo",
                            "6mo",
                            "1y",
                            "2y",
                            "5y",
                            "10y",
                            "ytd",
                            "max",
                        ],
                    },
                },
                "required": ["ticker"],
            },
        },
    }
]

funcoes_disponiveis = {
    "retorna_cotacao_acao_historica": retorna_cotacao_acao_historica,
}

# %%


def gerar_resposta(
    messages,
    model="gpt-3.5-turbo-0125",
    max_tokens=200,
    temperature=0.5,
    tool=tools,
    tool_choice="auto",
):
    """Função para retornar a resposta vinda do chatGPT"""
    resposta = client.chat.completions.create(
        messages=messages,
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        tools=tool,
        tool_choice=tool_choice,
    )
    mensagem_resp = resposta.choices[0].message
    tool_calls = mensagem_resp.tool_calls

    if tool_calls:
        messages.append(mensagem_resp)
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = funcoes_disponiveis[function_name]
            function_args = json.loads(tool_call.function.arguments)
            function_response = function_to_call(**function_args)
            mensagens.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            )
        resposta = client.chat.completions.create(  # type: ignore
            model="gpt-3.5-turbo-0125",
            messages=messages,
        )

    print("Assistant: ", end="")
    print(resposta.choices[0].message.content)
    print()
    messages.append(resposta.choices[0].message.model_dump(exclude_none=True))
    return messages


# %%
if __name__ == "__main__":
    print("Bem vindo ao ChatBot de SYSPWL. Qual seu nome?")
    print('Digite a qualquer momento "sair", para sair do ChatBot.')
    nome: str = ""
    start: bool = False
    mensagens = []

    while True:
        nome = input("Digite seu nome aqui: ")
        if nome.lower() == "sair":
            print("Agradecemos seu contato. Até breve!")
            break
        if nome:
            print(f"Seu nome é {nome}, está correto?")
            confirmacao_nome = input("Digite S para confirmar!")
            if confirmacao_nome.lower() != "s":
                continue
            else:
                start = True
                break

    if start:
        print(f"Assistant: Olá {nome}, tudo bem? Em que posso ajudar?")
        while True:
            texto_user = input(f"{nome}: ")
            if texto_user.lower() != "sair":
                mensagens.append({"role": "user", "content": texto_user})
                mensagens = gerar_resposta(messages=mensagens)
            else:
                print("Agradecemos seu contato. Até breve!")
                break
