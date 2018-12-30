import h2oai_client
from h2oai_client import Client

h2oai = Client(address='http://129.213.63.69:12345', username='ben', password='ben')

train_path = '/output.csv'
train = h2oai.create_dataset_sync(train_path)

preview = h2oai.get_experiment_preview_sync(
    dataset_key=train.key,
    validset_key='',
    dropped_cols=[],
    classification=True,
    target_col='LABEL',
    enable_gpus=True,
    accuracy=10,
    time=10,
    interpretability=1,
    is_time_series=True,
    config_overrides='num_folds=1\n'
)

print(preview)

experiment = h2oai.start_experiment_sync(
    dataset_key = train.key,
    target_col = 'LABEL',
    is_classification = True,

    accuracy = 10,
    time = 10,
    interpretability = 1,

    scorer = "AUC",
    seed = 1234,

    is_time_series=True,
    num_folds=1,
    num_gap_periods=1,
    num_prediction_periods=1,
    overlap = 0.000000
)

print("Final Model Score on Validation Data: " + str(round(experiment.valid_score, 3)))
print("Final Model Score on Test Data: " + str(round(experiment.test_score, 3)))
