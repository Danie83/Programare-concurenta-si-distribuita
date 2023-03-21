const ApiGatewayManagementApi = require('aws-sdk/clients/apigatewaymanagementapi');
const DynamoDB = require('aws-sdk/clients/dynamodb');

exports.handler = async function (event, context, callback) {
    const db = new DynamoDB.DocumentClient();
    let connections;

    try {
        connections = await db.scan({ TableName: 'SocketManager', ProjectionExpression: 'Id' }).promise();
    } catch (e) {
        return { statusCode: 500, body: e.stack };
    }

    const api = new ApiGatewayManagementApi({
        endpoint: 'https://1hwbpyynnd.execute-api.eu-west-1.amazonaws.com/beta/@connections',
    });

    var parameters = {
        TableName: 'Movies'
    }
    const data = await db.scan(parameters).promise()

    const postCalls = connections.Items.map(async ({ Id }) => {
        await api.postToConnection({ ConnectionId: Id, Data: JSON.stringify(data.Items) }).promise();
    });

    try {
        await Promise.all(postCalls);
    } catch (e) {
        return { statusCode: 500, body: e.stack };
    }

    return { statusCode: 200, body: 'Event sent.' };
};