def current_timestamp(dia: int) -> str:
    return f"""SELECT CURRENT_TIMESTAMP {dia} FROM RDB$DATABASE;"""
