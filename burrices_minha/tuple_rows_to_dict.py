def tuple_rows_to_dict(list_of_tuples, columns):
    """
    Recebe uma lista de tuplas, cujas são linhas selecionadas de uma tabela, e converte em um dicionário no formato: coluna: valor. Devolvendo uma lista de dicionários.

    Args:
        list_of_tuples (_type_): _description_

    Returns:
        _type_: _description_
    """
    n_cols = len(columns)
    list_ = []
    for tuple_ in list_of_tuples: 
        current_dict = {}
        for i in range(n_cols):
            current_dict[columns[i]] = tuple_[i]
        list_.append(current_dict)
    return list_

list_of_tuples = [("id_1", "col1_1", "col2_1"), ("id_2", "col1_2", "col2_2")]
columns=["id", "col1", "col2"]
print(tuple_rows_to_dict(list_of_tuples, columns))