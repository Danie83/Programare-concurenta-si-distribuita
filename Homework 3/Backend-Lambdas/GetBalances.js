const ApiGatewayManagementApi = require('aws-sdk/clients/apigatewaymanagementapi');
const DynamoDB = require('aws-sdk/clients/dynamodb');

exports.handler = async (event) => {
    const db = new DynamoDB.DocumentClient();
    
    var parameters = {
        TableName: 'Balances'
    }
    
    try 
    {
        const result = await db.scan(parameters).promise();
        const items = result.Items;
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
