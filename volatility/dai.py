import h2oai_client
from h2oai_client import Client

h2oai = Client(address='http://129.213.63.69:12345', username='ben', password='ben')

train = h2oai.create_dataset_sync('/train.csv')
validate = h2oai.create_dataset_sync('/validate.csv')
test = h2oai.create_dataset_sync('/test.csv')

experiment = h2oai.start_experiment_sync(
    dataset_key = train.key,
    testset_key = test.key,
    validset_key = validate.key,
    
    target_col = 'LABEL',
    is_classification = True,

    accuracy = 10,
    time = 10,
    interpretability = 1,

    scorer = "AUC",
    seed = 1234,

    is_timeseries=True,
    time_col='DATE',
    num_gap_periods=2,
    num_prediction_periods=2
)

print("Final Model Score on Validation Data: " + str(round(experiment.valid_score, 3)))
print("Final Model Score on Test Data: " + str(round(experiment.test_score, 3)))
