def usuario(nome: str) -> str:
    try:
        return f"""SELECT usuarioid FROM t_usuario WHERE nome = '{nome}';"""
    except:
        raise FileNotFoundError(f"Erro ao executar")


def nome_idade(nome: str, idade: int):
    return f"Nome: {nome}, Idade: {idade}"
