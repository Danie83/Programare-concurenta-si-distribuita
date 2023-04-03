const ApiGatewayManagementApi = require('aws-sdk/clients/apigatewaymanagementapi');
const DynamoDB = require('aws-sdk/clients/dynamodb');

exports.handler = async (event) => {
    const db = new DynamoDB.DocumentClient();
    
    var parameters = {
        TableName: 'Transactions',
        KeyConditionExpression: 'user_id = :user_id',
        ExpressionAttributeValues: {
            ':user_id' : event.queryStringParameters.user_id
        }
    }
    
    try 
    {
        const result = await db.query(parameters).promise();
        if (!result.Items) {
            return {
                statusCode: 404,
                body: JSON.stringify('There are no transactions made for this user'),
            };
        }
        return {
            statusCode: 200,
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(result.Items)
        }
    } 
    catch (e) 
    {
        console.log(e);
        return {
            statusCode: 500,
            headers: {'Content-Type': 'text/plain'},
            body: 'Internal Server Error'
        }
    }
};