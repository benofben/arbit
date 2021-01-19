import h2oai_client
from h2oai_client import Client

h2oai = Client(address='http://129.213.63.69:12345', username='ben', password='ben')

train = h2oai.create_dataset_sync('/train.csv')
test = h2oai.create_dataset_sync('/test.csv')

experiment = h2oai.start_experiment_sync(
    dataset_key = train.key,
    testset_key = test.key,

    accuracy = 10,
    time = 10,
    interpretability = 1,

    is_classification = True,
    target_col = 'LABEL',

    is_timeseries=True,
    time_col='DATE',
    num_gap_periods=1,
    num_prediction_periods=1
)

print("Final Model Score on Validation Data: " + str(round(experiment.valid_score, 3)))
print("Final Model Score on Test Data: " + str(round(experiment.test_score, 3)))
