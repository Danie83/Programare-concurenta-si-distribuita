const ApiGatewayManagementApi = require('aws-sdk/clients/apigatewaymanagementapi');
const DynamoDB = require('aws-sdk/clients/dynamodb');

exports.handler = async (event) => {
    const db = new DynamoDB.DocumentClient();
    
    var parameters = {
        TableName: 'Balances',
        Key: {
            user_id: event.queryStringParameters.user_id
        },
        UpdateExpression: 'set balance = :newBalance',
        ExpressionAttributeValues: {
            ':newBalance': parseFloat(event.queryStringParameters.balance)
        },
        ReturnValues: 'ALL_NEW'
    }
    
    try 
    {
        const result = await db.update(parameters).promise();
        const items = result.Attributes;
        return {
            statusCode: 200,
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(items)
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
