def usuario(nome: str) -> str:
    return f"""SELECT usuarioid FROM t_usuario WHERE nome = '{nome}';"""


def nome_idade(nome: str, idade: int):
    return f"Nome: {nome}, Idade: {idade}"
