const ApiGatewayManagementApi = require('aws-sdk/clients/apigatewaymanagementapi');
const DynamoDB = require('aws-sdk/clients/dynamodb');

exports.handler = async (event) => {
    const db = new DynamoDB.DocumentClient();
    
    var parameters = {
        TableName: 'Balances',
        Item: {
            user_id: event.queryStringParameters.user_id,
            balance: 0
        }
    }
    
    try 
    {
        await db.put(parameters).promise();
        return {
            statusCode: 200,
            body: JSON.stringify('New item added successfully')
        }
    } 
    catch (e) 
    {
        console.log(e);
        return {
            statusCode: 500,
            body: 'Internal Server Error'
        }
    }
};
