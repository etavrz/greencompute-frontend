# Write some tests for the alpha module
from pytest import fixture

from sklearn.linear_model import LogisticRegression
from greencompute_frontend.alpha import load_data, train_model


@fixture
def data():
    return load_data()


def test_load_data(data):
    expected_train_shape = (120, 4)
    expected_test_shape = (30, 4)

    (X_train, y_train), (X_test, y_test) = data

    assert X_train.shape == expected_train_shape
    assert y_train.shape == (120,)
    assert X_test.shape == expected_test_shape
    assert y_test.shape == (30,)


def test_train_model(data):
    model = train_model(data[0])
    assert isinstance(model, LogisticRegression)
