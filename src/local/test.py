def usuario(nome: str) -> str:
    return f"""SELECT usuarioid FROM t_usuario WHERE nome = '{nome}';"""
