def normalize_column_names(df, column_name_mapping):
    return df.rename(columns=column_name_mapping)


marieboucher_mapping = {
    'Name1': 'source',
    'Name2': 'target',
    'Place1': 'source_location',
    'Place2': 'target_location'
}
