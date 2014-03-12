create table users (
    username string primary key,
    first_name string,
    last_name string,
    email string,
    openid string
) clustered into 5 shards with (number_of_replicas='0-all')
