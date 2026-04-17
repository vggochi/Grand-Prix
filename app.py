import json
import numpy as np
from iris_recognition import capture_iris

ARQUIVO = "funcionarios.json"

try:
    with open(ARQUIVO, "r") as f:
        funcionarios = json.load(f)
except FileNotFoundError:
    funcionarios = {}

def salvar_dados():
    with open(ARQUIVO, "w") as f:
        json.dump(funcionarios, f)

def comparar_features(f1, f2):
    # Similaridade por correlação normalizada
    f1 = f1 / np.linalg.norm(f1)
    f2 = f2 / np.linalg.norm(f2)
    return float(np.dot(f1, f2))

def acessar():
    print("📸 Acesse colocando o olho na câmera...")
    iris_code, features = capture_iris()
    melhor_match = None
    melhor_similaridade = 0

    for nome, dados in funcionarios.items():
        similarity = comparar_features(features, np.array(dados["features"]))
        if similarity > melhor_similaridade:
            melhor_similaridade = similarity
            melhor_match = nome

    if melhor_match and melhor_similaridade > 0.8:
        dados = funcionarios[melhor_match]
        print(f"✅ Acesso permitido! Funcionário identificado: {melhor_match} "
              f"(código {dados['codigo']}, setor {dados['setor']}, nascimento {dados['nascimento']})")
    else:
        print("❌ Acesso negado! Nenhum funcionário correspondente encontrado.")

def cadastrar():
    nome = input("Digite o nome do funcionário: ")
    setor = input("Digite o setor: ")
    nascimento = input("Digite a data de nascimento (AAAA-MM-DD): ")

    print("📸 Capture o olho para cadastro...")
    iris_code, features = capture_iris()
    if iris_code:
        funcionarios[nome] = {
            "codigo": iris_code,
            "setor": setor,
            "nascimento": nascimento,
            "features": features.tolist()
        }
        salvar_dados()
        print(f"✅ Funcionário {nome} cadastrado com sucesso! Código: {iris_code}")
    else:
        print("Erro ao capturar olho.")

def excluir():
    nome = input("Digite o nome do funcionário a excluir: ")
    if nome in funcionarios:
        del funcionarios[nome]
        salvar_dados()
        print(f"🗑️ Funcionário {nome} excluído com sucesso!")
    else:
        print("Funcionário não encontrado.")

def listar():
    print("\n📋 Funcionários cadastrados:")
    for nome, dados in funcionarios.items():
        print(f"- {nome}: código {dados['codigo']}, setor {dados['setor']}, nascimento {dados['nascimento']}")

def menu():
    while True:
        print("\n=== Sistema de Reconhecimento de Íris ===")
        print("1 - Acessar (identificação automática)")
        print("2 - Cadastrar funcionário")
        print("3 - Excluir funcionário")
        print("4 - Listar funcionários")
        print("0 - Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            acessar()
        elif opcao == "2":
            cadastrar()
        elif opcao == "3":
            excluir()
        elif opcao == "4":
            listar()
        elif opcao == "0":
            print("Encerrando...")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    menu()
