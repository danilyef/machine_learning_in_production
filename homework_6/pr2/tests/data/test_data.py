import pytest
import pandas as pd
import great_expectations as ge
import warnings

warnings.filterwarnings("ignore")

@pytest.fixture
def dataset():
    df = pd.read_parquet("homework_6/pr2/data/data.parquet")

    return ge.dataset.PandasDataset(df)

def test_column_count_and_names(dataset):
    assert dataset.expect_table_column_count_to_equal(2)["success"]
    assert dataset.expect_table_columns_to_match_ordered_list(["text", "label"])["success"]

def test_column_types(dataset):
    assert dataset.expect_column_values_to_be_of_type("text", "str")["success"]
    assert dataset.expect_column_values_to_be_of_type("label", "str")["success"]

def test_label_values(dataset):
    assert dataset.expect_column_values_to_be_in_set("label", ["Positive", "Negative"])["success"]

def test_text_length(dataset):
    assert dataset.expect_column_value_lengths_to_be_between("text", min_value=1, max_value=10000)["success"]

def test_non_empty_text(dataset):
    assert dataset.expect_column_values_to_not_be_null("text")["success"]

def test_label_distribution(dataset):
    label_counts = dataset["label"].value_counts(normalize=True)
    assert 0.2 <= label_counts["Positive"] <= 0.8, "Label distribution is too imbalanced"
    assert 0.2 <= label_counts["Negative"] <= 0.8, "Label distribution is too imbalanced"

def test_unique_texts(dataset):
    assert dataset.expect_column_values_to_be_unique("text")["success"]
