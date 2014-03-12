create table users (
    id string primary key,
    username string,
    first_name string,
    last_name string,
    email string,
    openid string
) clustered into 5 shards with (number_of_replicas='0-all')
