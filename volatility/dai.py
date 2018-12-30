import h2oai_client
from h2oai_client import Client

h2oai = Client(address='http://129.213.63.69:12345', username='ben', password='ben')

train_path = '/output.csv'
train = h2oai.create_dataset_sync(train_path)

exp_preview = h2oai.get_experiment_preview_sync(
    dataset_key=train.key,
    validset_key='',
    classification=True,
    dropped_cols = [],
    target_col='LABEL',
    enable_gpus=True,
    accuracy=10,
    time=10,
    interpretability=1,
    config_overrides=None,
    is_time_series=True
)

print(exp_preview)

experiment = h2oai.start_experiment_sync(
    is_time_series=True,
    dataset_key = train.key,
    testset_key = train.key,
    target_col = 'LABEL',
    is_classification = True,
    accuracy = 10,
    time = 10,
    interpretability = 1,
    scorer = "AUC",
    seed = 1234
)

print("Final Model Score on Validation Data: " + str(round(experiment.valid_score, 3)))
print("Final Model Score on Test Data: " + str(round(experiment.test_score, 3)))
