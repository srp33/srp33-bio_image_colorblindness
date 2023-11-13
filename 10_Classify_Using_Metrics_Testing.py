import sklearn as sk
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np

out_file_path = "Testing_Results_Metrics.tsv"

training_df = pd.read_csv("Image_Metrics_Classification_Data.tsv", delimiter="\t")
testing_df = pd.read_csv("Image_Metrics_Classification_Data_Testing.tsv", delimiter="\t")

training_df = training_df.drop("image_file_path", axis=1)
testing_df = testing_df.drop("image_file_path", axis=1)
training_df = training_df.drop("deut_image_file_path", axis=1)
testing_df = testing_df.drop("deut_image_file_path", axis=1)

training_y = training_df["Class"].values
training_X = training_df.drop("Class", axis=1)
testing_y = testing_df["Class"].values
testing_X = testing_df.drop("Class", axis=1)

columns_to_scale = ["max_ratio", "num_high_ratios", "proportion_high_ratio_pixels", "mean_delta", "euclidean_distance_metric"]
pipeline = ColumnTransformer([("scaler", StandardScaler(), columns_to_scale)])
training_X = pipeline.fit_transform(training_X)
testing_X = pipeline.transform(testing_X)

model = LogisticRegression(solver='liblinear', class_weight="balanced", random_state=0)
model.fit(training_X, training_y)
predictions = model.predict_proba(testing_X)
auroc = roc_auc_score(testing_y, predictions[:,1])

with open(out_file_path, "w") as out_file:
    out_file.write(f"auroc\n{auroc}")