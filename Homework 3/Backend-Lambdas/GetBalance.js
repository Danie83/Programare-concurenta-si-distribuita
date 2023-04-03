const ApiGatewayManagementApi = require('aws-sdk/clients/apigatewaymanagementapi');
const DynamoDB = require('aws-sdk/clients/dynamodb');

exports.handler = async (event) => {
    const db = new DynamoDB.DocumentClient();
    
    var parameters = {
        TableName: 'Balances',
        Key: {
            user_id: event.queryStringParameters.user_id
        }
    }
    
    try 
    {
        const result = await db.get(parameters).promise();
        if (!result.Item) {
            return {
                statusCode: 404,
                body: JSON.stringify('User not found'),
            };
        }
        return {
            statusCode: 200,
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(result.Item)
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