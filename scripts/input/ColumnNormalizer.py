def normalize_column_names(df, column_name_mapping):
    return df.rename(columns=column_name_mapping)


marieboucher_mapping = {
    'Name1': 'source',
    'Name2': 'target',
    'Place1': 'source_location',
    'Place2': 'target_location'
}

smith_mapping = {
    'Sender': 'source',
    'Courrier': 'target',
    'Sender Location': 'source_location',
    'Courrier Location': 'target_location'
}

jucs_mapping = {
    'Aut'
}

archeology_mapping = {
    'FROM': 'source',
    'TO': 'target',
    'SOURCE_LOCATION': 'source_location',
    'TARGET_LOCATION': 'target_location'
}

russia_mapping = {

}