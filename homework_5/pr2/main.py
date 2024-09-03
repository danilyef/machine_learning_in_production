import numpy as np
import pandas as pd
from scipy.io.arff import loadarff 
import wandb
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score



def main():
    # Dataset taken from: https://www.openml.org/search?type=data&status=active&id=1597
    raw_data = loadarff('/Users/daniil.yefimov/Desktop/Github/machine_learning_in_production/homework_5/pr2/phpKo8OWT.arff')
    df_data = pd.DataFrame(raw_data[0])

    df_data.drop(columns = ['Time', 'Amount'], inplace=True)
    df_data.rename(columns = {'Class': 'target'}, inplace=True)
    df_data['target'] = df_data['target'].apply(lambda x: 1 if x == b'1' else 0)

    # Split the data
    X = df_data.drop('target', axis=1)
    y = df_data['target']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # hyperparameters dict
    hyperparameter_space = {
        'n_estimators': {'values': [50, 150, 300]},
        'max_depth': {'values': [5, 15, 30]},
    }

    # Initialize wandb sweep
    sweep_config = {
        'method': 'random',
        'metric': {'name': 'f1_score', 'goal': 'maximize'},
        'parameters': hyperparameter_space
    }

    sweep_id = wandb.sweep(sweep_config, project="credit_card_fraud_detection")

    # Train function
    def train():
        with wandb.init() as run:
            config = wandb.config

            rf = RandomForestClassifier(n_estimators=config.n_estimators,
                                        max_depth=config.max_depth,
                                        random_state=42)
            rf.fit(X_train, y_train)
            
            y_pred = rf.predict(X_test)
            f1 = f1_score(y_test, y_pred)
            
            wandb.log({"f1_score": f1})

    # Run the sweep
    wandb.agent(sweep_id, function=train, count=9)

if __name__ == "__main__":
    main()
