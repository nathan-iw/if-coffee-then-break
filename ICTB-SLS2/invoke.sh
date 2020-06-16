sls invoke -f drinksDynamoImport -d '{ "Records": [ { "s3": { "object": { "key": "transactions/20200611133022.csv" } } } ] }'
sls invoke local -f drinksDynamoImport -d '{ "Records": [ { "s3": { "object": { "key": "transactions/20200611133022.csv" } } } ] }'
# sls logs -f drinksDynamoImport -tail