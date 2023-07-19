"""
Used to create a DynamoDB table when it does not exist - i.e. when using dynamodb-local.
"""
from periodic_lambda_app.dependencies import make_dynamodb_client

TABLE_NAME = "Todos"


def setup_table():
    client = make_dynamodb_client()
    response = client.create_table(
        AttributeDefinitions=[
            {
                'AttributeName': 'id',
                'AttributeType': 'S',
            },
        ],
        KeySchema=[
            {
                'AttributeName': 'id',
                'KeyType': 'HASH',
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5,
        },
        TableName=TABLE_NAME,
    )
    print(response)


if __name__ == "__main__":
    setup_table()
