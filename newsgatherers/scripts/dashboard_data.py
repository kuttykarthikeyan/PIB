# import pandas as pd
# import json

# def get_state_negative_counts(csv_file_path):
#     df = pd.read_csv(csv_file_path)

#     negative_articles = df[df['SENTIMENT_ANALYSIS_RESULT'] == 'NEGATIVE']

#     state_negative_counts = negative_articles['State'].value_counts()

#     state_negative_counts_dict = state_negative_counts.to_dict()

#     json_result = {
#         "state_negative_counts": state_negative_counts_dict
#     }

#     json_result_str = json.dumps(json_result, indent=2)

#     return json_result_str

# csv_file_path = "final_data1.csv"
# result = get_state_negative_counts(csv_file_path)
# print(result)