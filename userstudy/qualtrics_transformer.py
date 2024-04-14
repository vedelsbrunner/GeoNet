import pandas as pd

def transform(input_file, output_file):
    df = pd.read_csv(input_file)
    df.drop(1, inplace=True)
    df.drop(0, inplace=True)
    df = df.loc[:, ~df.columns.str.contains('_First Click|_Last Click|_Click Count')]

    metadata_col_count = 17
    cols_to_exclude_at_end = 2
    total_cols = df.shape[1]
    task_cols_count = total_cols - metadata_col_count - cols_to_exclude_at_end

    tasks_df = pd.DataFrame()

    techniques_count = 4
    questions_per_technique = 4
    tasks_per_question = 8
    columns_per_task = 2  # Each task has a 'Page Submit (Time)' and 'Answer'

    # Define Latin square mapping of techniques to group IDs
    technique_sequences = {
        1: ['Stacked', 'Grid', 'Circular', 'Sunflower'],
        2: ['Sunflower', 'Stacked', 'Grid', 'Circular'],
        3: ['Circular', 'Sunflower', 'Stacked', 'Grid'],
        4: ['Grid', 'Circular', 'Sunflower', 'Stacked']
    }

    # Iterate over questions and tasks within the range of task-related columns
    for index, row in df.iterrows():
        group_id = row.get('GroupID', None)  # Extract GroupID from row
        technique_order = technique_sequences.get(int(group_id), ['?']*techniques_count)  # Default to '?' if GroupID is invalid

        for t_idx, technique in enumerate(technique_order):
            for q in range(questions_per_technique):
                base_index = metadata_col_count + (t_idx * questions_per_technique + q) * tasks_per_question * columns_per_task
                for t in range(tasks_per_question):
                    index_offset = t * columns_per_task
                    task_data = {
                        'ParticipantID': row.get('ResponseId', '?'),
                        'GroupID': group_id,
                        'Group': row.get('Group', '?'),
                        'Technique': technique,
                        'Question': f"Q{q + 1}",
                        'Task': t + 1,
                        'Training': t < 2,  # First two tasks are training tasks
                        'Answer': row[base_index + index_offset + 1],  # The answer column
                        'Time': row[base_index + index_offset]  # The time column
                    }
                    tasks_df = tasks_df._append(task_data, ignore_index=True)

    tasks_df.to_csv(output_file, index=False)
    print(f"Output saved to {output_file}")

def main():
    input_filename = 'test_input.csv'
    output_filename = 'output_transformed.csv'
    transform(input_filename, output_filename)

if __name__ == '__main__':
    main()
