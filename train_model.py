import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

# Load Dataset
def load_data():
    return pd.read_csv("data/house_prices.csv")

# Preprocess Dataset
def preprocess_data(df):

    df = df.copy()

    yes_no_columns = [
        "mainroad",
        "guestroom",
        "basement",
        "hotwaterheating",
        "airconditioning",
        "prefarea"
    ]

    for col in yes_no_columns:
        df[col] = df[col].map({
            "yes": 1,
            "no": 0
        })

    df = pd.get_dummies(
        df,
        columns=["furnishingstatus"],
        drop_first=True,
        dtype=int
    )

    return df

# Train Model
def train_model(X_train, y_train):

    model = LinearRegression()

    model.fit(X_train, y_train)

    return model

# Evaluate Model
def evaluate_model(model, X_test, y_test):

    predictions = model.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)

    mse = mean_squared_error(y_test, predictions)

    rmse = mse ** 0.5

    r2 = r2_score(y_test, predictions)

    print("\n========== MODEL PERFORMANCE ==========")
    print(f"MAE       : {mae:,.2f}")
    print(f"RMSE      : {rmse:,.2f}")
    print(f"R² Score  : {r2:.4f}")

    print("\nFirst 10 Predictions:")
    print(predictions[:10])

    return predictions

# Save Model
def save_model(model, feature_names):

    joblib.dump(
        model,
        "model/house_price_model.pkl"
    )

    joblib.dump(
        feature_names,
        "model/model_features.pkl"
    )

    print("\n✅ Model saved successfully!")
    print("✅ Feature names saved successfully!")

# Main
def main():

    df = load_data()
    df = preprocess_data(df)

    X = df.drop("price", axis=1)
    y = df["price"]

    print("\n========== DATASET ==========")
    print(f"Features Shape : {X.shape}")
    print(f"Target Shape   : {y.shape}")

    # Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42
    )

    print("\n========== TRAIN / TEST ==========")
    print(f"Training Set : {X_train.shape}")
    print(f"Testing Set  : {X_test.shape}")

    # Train Model
    model = train_model(
        X_train,
        y_train
    )
    print("\n✅ Linear Regression Model Trained Successfully!")

    # Evaluate
    evaluate_model(
        model,
        X_test,
        y_test
    )

    # Save Model
    save_model(
        model,
        X.columns.tolist()
    )

if __name__ == "__main__":
    main()