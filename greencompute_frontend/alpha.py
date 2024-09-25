from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import pandas as pd


def load_data() -> (
    tuple[tuple[pd.DataFrame, pd.DataFrame], tuple[pd.DataFrame, pd.DataFrame]]
):
    df = datasets.load_iris(as_frame=True)
    X = df.data
    y = df.target

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    return (X_train, y_train), (X_test, y_test)


def train_model(data: tuple[pd.DataFrame, pd.DataFrame]):
    lr = LogisticRegression()
    lr.fit(data[0], data[1])
    return lr
