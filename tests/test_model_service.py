import pytest
from src.model_config import FEATURE_COLUMNS
from src.model_service import load_model, predict_energy


def get_valid_feature_values():
    return {
        "T1": 20.0,
        "RH_1": 40.0,
        "T2": 19.5,
        "RH_2": 42.0,
        "T_out": 8.0,
        "RH_out": 75.0,
        "hour": 14,
        "day_of_week": 2,
        "is_weekend": 0,
    }


def test_model_can_be_loaded():
    model = load_model()

    assert model is not None
    assert hasattr(model, "predict")


def test_expected_features_are_defined():
    assert FEATURE_COLUMNS == [
        "T1",
        "RH_1",
        "T2",
        "RH_2",
        "T_out",
        "RH_out",
        "hour",
        "day_of_week",
        "is_weekend",
    ]


def test_model_can_make_prediction():
    model = load_model()

    feature_values = get_valid_feature_values()

    prediction = predict_energy(
        model,
        feature_values,
    )

    assert isinstance(prediction, float)


    import pytest


def test_prediction_fails_when_feature_is_missing():
    model = load_model()

    feature_values = get_valid_feature_values()
    feature_values.pop("T_out")

    with pytest.raises(
        ValueError,
        match="Missing required features",
    ):
        predict_energy(
            model,
            feature_values,
        )