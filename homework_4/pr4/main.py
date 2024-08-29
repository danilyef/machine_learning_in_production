import re
import string
import pandas as pd
from sklearn.metrics import accuracy_score, log_loss
from sklearn.model_selection import cross_val_predict
from sklearn.linear_model import LogisticRegression
from sentence_transformers import SentenceTransformer

from cleanlab import Datalab

import warnings
warnings.filterwarnings("ignore")

# Read parquet data into pandas DataFrame
df = pd.read_parquet('synthetic_reviews.parquet')

raw_texts, labels = df["Email"].values, df["Category"].values
num_classes = len(set(labels))


transformer = SentenceTransformer('distiluse-base-multilingual-cased-v2')
text_embeddings = transformer.encode(raw_texts)

model = LogisticRegression(max_iter=400)
pred_probs = cross_val_predict(model, text_embeddings, labels, method="predict_proba")

data_dict = {"texts": raw_texts, "labels": labels}
lab = Datalab(data_dict, label_name="labels",verbosity = 0)
lab.find_issues(pred_probs=pred_probs, features=text_embeddings)


label_issues = lab.get_issues("label")
label_issues_idx = label_issues[label_issues["is_label_issue"] == True].index.to_numpy()
print(df.iloc[label_issues_idx])

outlier_issues = lab.get_issues("outlier")
outlier_issues_idx = outlier_issues[outlier_issues["is_outlier_issue"] == True].index.to_numpy()
print(df.iloc[outlier_issues_idx])



duplicate_issues = lab.get_issues("near_duplicate")
duplicate_issues_idx = duplicate_issues[duplicate_issues["is_near_duplicate_issue"] == True].index.to_numpy()
duplicate_issues_idx_2 = duplicate_issues[duplicate_issues["is_near_duplicate_issue"] == True].near_duplicate_sets.to_numpy()

duplicate_issues_idx_2 = [item for sublist in duplicate_issues_idx_2 for item in sublist]

duplicates_df = pd.concat([df.loc[duplicate_issues_idx].reset_index(drop=True), 
                           df.loc[duplicate_issues_idx_2].reset_index(drop=True)], axis=1)
duplicates_df.columns = ['Original_Email', 'Original_Category', 'Duplicate_Email', 'Duplicate_Category']
print(duplicates_df)