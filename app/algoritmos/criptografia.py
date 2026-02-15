"""
Arquivo para criptografia
"""

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

ph = PasswordHasher()

def gerar_hash(senha_plana):
    # O Argon2 gera o salt automaticamente e o embuti no hash final
    hash_gerado = ph.hash(senha_plana)
    return hash_gerado

"""
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

# 1. Inicializamos o Hasher
# O argon2-cffi já vem com parâmetros seguros por padrão.
ph = PasswordHasher()

def cadastrar_usuario(senha_plana):
    # O Argon2 gera o salt automaticamente e o embuti no hash final
    hash_gerado = ph.hash(senha_plana)
    return hash_gerado

def verificar_login(hash_do_banco, senha_digitada):
    try:
        # A função verify extrai os parâmetros e o salt do hash e compara
        ph.verify(hash_do_banco, senha_digitada)
        print("✅ Login realizado com sucesso!")
        return True
    except VerifyMismatchError:
        print("❌ Senha incorreta.")
        return False

# --- Testando o fluxo ---
print("Digite sua senha: ")
senha_do_usuario = input(str())


# Simulando salvamento no banco de dados
hash_para_salvar = cadastrar_usuario(senha_do_usuario)
print(f"Hash que será guardado no DB: {hash_para_salvar}\n")

# Simulando tentativa de login
print("Tentativa 1 (Senha correta):")
verificar_login(hash_para_salvar, senha_do_usuario)

print("\nTentativa 2 (Senha errada):")
verificar_login(hash_para_salvar, "senha_errada")
"""