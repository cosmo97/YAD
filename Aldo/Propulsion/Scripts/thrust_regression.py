import regression_methods

THRUST_DATASET_CSV = "Aldo/Propulsion/Datasets/Motors/thrust_dataset.csv"


def main():
    input_columns_ = ["motor width (mm)", "motor height (mm)", "Kv (rms/V)",
                      "propeller diameter (in)", "propeller pitch (in)", "battery (V)"]
    output_columns_ = ["Thrust (kgf)"]
    x_, y_ = regression_methods.extract_data_from_csv(
        THRUST_DATASET_CSV, input_columns_, output_columns_)
    x_train_, x_test_, y_train_, y_test_ = regression_methods.preprocess_data(
        x_, y_)
    ridge_model_ = regression_methods.fit_ridge_model_to_data(
        x_train_, y_train_)
    MSE_ridge_, MAE_ridge_, y_test_, y_test_hat_ = regression_methods.test_model(
        ridge_model_, x_test_, y_test_)


if __name__ == "__main__":
    main()
