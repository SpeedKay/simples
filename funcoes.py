import os
import sys
from tabulate import tabulate
ARQUIVO_DADOS = "itens.txt"

def main():
    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            cadastrar_item()
        elif opcao == "2":
            alterar_item()
        elif opcao == "3":
            excluir_item()
        elif opcao == "4":
            relatorio()
        elif opcao == "5":
            print("\n PESQUISA PARCIAL")
            print("1 - Por nome")
            print("2 - Por tipo")
            escolha = input("Escolha uma opção: ").strip()
            if escolha == "1":
                pesquisa_nome()
            elif escolha == "2":
                pesquisa_tipo()
            else:
                print("Opção inválida.")
                pausar()
        elif opcao == "6":
            print("Encerrando o sistema...")
            break
        else:
            print("Opção inválida. Tente novamente.")

def pausar():
    escolha = input("\nPressione ENTER para voltar ao menu ou digite 'sair' para encerrar: ").strip().lower()
    if escolha == "sair":
        print("Encerrando o sistema...")
        sys.exit()
    else:
        limpar_tela()

def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")

def carregar_dados():
    if not os.path.exists(ARQUIVO_DADOS):
        return []
    with open(ARQUIVO_DADOS, "r", encoding="utf-8") as file:
        linhas = file.readlines()
    dados = []
    for linha in linhas:
        partes = linha.strip().split(";")
        if len(partes) == 5:
            dados.append({
                "codItem": partes[0],
                "nomeItem": partes[1],
                "tipoItem": partes[2],
                "valorItem": float(partes[3]),
                "quantidade": int(partes[4])
            })
    return dados

def cadastrar_item():    
    dados = carregar_dados()
    print("\n Cadastro de Novo Item Mágico")
    while True:
        codItem = input("Código do Item (apenas números): ").strip()
        if not codItem:
            print("O código não pode estar vazio.")
        elif not codItem.isdigit():
            print("O código deve conter apenas números.")
        elif any(item['codItem'] == codItem for item in dados):
            print("Já existe um item com esse código.")
        else:
            break
    while True:
        nomeItem = input("Nome do Item (apenas letras e espaços): ").strip()
        if not nomeItem:
            print("O nome não pode estar vazio.")
        elif not all(c.isalpha() or c.isspace() for c in nomeItem):
            print("O nome deve conter apenas letras e espaços.")
        else:
            break
    tipos_validos = {
        "1": "Poção",
        "2": "Arma",
        "3": "Artefato"
    }
    print("\nSelecione o tipo do item:")
    for chave, valor in tipos_validos.items():
        print(f"{chave} - {valor}")
    escolha = input("Digite o número correspondente ao tipo: ").strip()
    if escolha not in tipos_validos:
        print("Tipo inválido. Item não cadastrado.")
        return
    tipoItem = tipos_validos[escolha]
    try:
        valorItem = float(input("Valor em moedas de ouro: "))
        quantidade = int(input("Quantidade em estoque: "))
    except ValueError:
        print("Valor ou quantidade inválidos. Tente novamente.")
        return
    novo_item = {
        "codItem": codItem,
        "nomeItem": nomeItem,
        "tipoItem": tipoItem,
        "valorItem": valorItem,
        "quantidade": quantidade
    }
    dados.append(novo_item)
    salvar_dados(dados)
    print("Item cadastrado com sucesso!")
    pausar()

def salvar_dados(dados):
        with open(ARQUIVO_DADOS, "w", encoding="utf-8") as file:
            for item in dados:
                linha = f"{item['codItem']};{item['nomeItem']};{item['tipoItem']};{item['valorItem']};{item['quantidade']}\n"
                file.write(linha)
                
def exibir_menu():
    print("\n╔══════════════════════════════════════════════╗")
    print("║        LOJA DE POÇÕES E ITENS MÁGICOS        ║")
    print("╠══════════════════════════════════════════════╣")
    print("║ (1) Inclusão                                 ║")
    print("║ (2) Alteração                                ║")
    print("║ (3) Exclusão                                 ║")
    print("║ (4) Relatório Geral                          ║")
    print("║ (5) Pesquisa Parcial                         ║")
    print("║ (6) Saída                                    ║")
    print("╚══════════════════════════════════════════════╝")

def alterar_item():
    dados = carregar_dados()
    print("\nAlteração de Item")
    cod = input("Digite o código do item a ser alterado: ").strip()
    item = next((i for i in dados if i["codItem"] == cod), None)
    if not item:
        print("Item não encontrado.")
        return
    print(f"\nItem atual:")
    print(f"Nome: {item['nomeItem']}")
    print(f"Tipo: {item['tipoItem']}")
    print(f"Valor: {item['valorItem']}")
    print(f"Quantidade: {item['quantidade']}")
    novo_nome = input("Novo nome (deixe vazio para manter): ").strip()
    if novo_nome:
        if all(c.isalpha() or c.isspace() for c in novo_nome):
            item["nomeItem"] = novo_nome
        else:
            print("Nome inválido. Mantendo o nome antigo.")
    print("\nSelecione o novo tipo (ou pressione ENTER para manter atual):")
    tipos_validos = {
        "1": "Poção",
        "2": "Arma",
        "3": "Artefato"
    }
    for chave, valor in tipos_validos.items():
        print(f"{chave} - {valor}")
    while True:
        nova_escolha = input("Digite o número do novo tipo ou ENTER para manter: ").strip()
        if not nova_escolha:
            break
        elif nova_escolha in tipos_validos:
            item["tipoItem"] = tipos_validos[nova_escolha]
            break
        else:
            print("Tipo inválido. Digite 1, 2, 3 ou pressione ENTER para manter.")
    try:
        novo_valor = input("Novo valor (ENTER para manter): ").strip()
        if novo_valor:
            item["valorItem"] = float(novo_valor)
        nova_qtd = input("Nova quantidade (ENTER para manter): ").strip()
        if nova_qtd:
            item["quantidade"] = int(nova_qtd)
    except ValueError:
        print("Entrada inválida em valor ou quantidade. Mantendo os dados antigos.")
    salvar_dados(dados)
    print("Item alterado com sucesso!")
    pausar()
    
def excluir_item():
    dados = carregar_dados()
    print("\nExclusão de Item Mágico")

    cod = input("Digite o código do item a ser removido: ").strip()
    item = next((i for i in dados if i["codItem"] == cod), None)

    if not item:
        print("Item não encontrado.")
        pausar()
        return

    print("\nItem encontrado:")
    print(f"Nome: {item['nomeItem']}")
    print(f"Tipo: {item['tipoItem']}")
    print(f"Valor: {item['valorItem']}")
    print(f"Quantidade: {item['quantidade']}")

    confirmar = input("Tem certeza que deseja excluir este item? (s/n): ").strip().lower()
    if confirmar == "s":
        dados.remove(item)
        salvar_dados(dados)
        print("Item removido com sucesso.")
    else:
        print("Exclusão cancelada.")

    pausar()

def relatorio():
    dados = carregar_dados()
    if not dados:
        print("Nenhum item cadastrado")
        pausar()
        return
    dados = sorted(carregar_dados(), key=lambda x: int(x["codItem"]))
    tabela = []
    for item in dados:
        tabela.append([
            item["codItem"],
            item["nomeItem"],
            item["tipoItem"],
            f"{item['valorItem']:.2f} 🪙",
            item["quantidade"]
        ])
    print("\n RELATÓRIO GERAL DE ITENS")
    print(tabulate(
        tabela,
        headers=["Código", "Nome", "Tipo", "Valor", "Qtd"],
        tablefmt="rounded_grid",
        stralign="center",
        numalign="center"
    ))
    pausar()

def pesquisa_nome():
    dados = carregar_dados()
    termo = input("\n Digite parte do nome do item a buscar: ").strip().lower()
    if not termo:
        print(" Entrada vazia. Pesquisa cancelada.")
        pausar()
        return
    resultados = []
    for item in dados:
        if termo in item["nomeItem"].lower():
            resultados.append([
                item["codItem"],
                item["nomeItem"],
                item["tipoItem"],
                f"{item['valorItem']:.2f} 🪙",
                item["quantidade"]
            ])
    if resultados:
        resultados_ord = sorted(resultados, key=lambda x: int(x[0]))
        print(f"\n Resultados da pesquisa por: \"{termo}\"")
        print(tabulate(
            resultados_ord,
            headers=["Código", "Nome", "Tipo", "Valor", "Qtd"],
            tablefmt="rounded_grid",
            stralign="center",
            numalign="center"
        ))
    else:
        print(" Nenhum item encontrado com esse termo.")
    pausar()

def pesquisa_tipo():
    dados = carregar_dados()
    tipos_validos = {
        "1": "Poção",
        "2": "Arma",
        "3": "Artefato"
    }

    print("\n Escolha o tipo de item para pesquisar:")
    for chave, valor in tipos_validos.items():
        print(f"{chave} - {valor}")

    escolha = input("Digite o número correspondente ao tipo: ").strip()

    if escolha not in tipos_validos:
        print(" Tipo inválido.")
        pausar()
        return

    tipo_escolhido = tipos_validos[escolha]

    resultados = []
    for item in dados:
        if item["tipoItem"] == tipo_escolhido:
            resultados.append([
                item["codItem"],
                item["nomeItem"],
                item["tipoItem"],
                f"{item['valorItem']:.2f} 🪙",
                item["quantidade"]
            ])

    if resultados:
        resultados_ord = sorted(resultados, key=lambda x: int(x[0]))
        print(f"\n Itens do tipo: {tipo_escolhido}")
        print(tabulate(
            resultados_ord,
            headers=["Código", "Nome", "Tipo", "Valor", "Qtd"],
            tablefmt="rounded_grid",
            stralign="center",
            numalign="center"
        ))
    else:
        print(f" Nenhum item do tipo {tipo_escolhido} foi encontrado.")

    pausar()
