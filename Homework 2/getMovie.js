const ApiGatewayManagementApi = require('aws-sdk/clients/apigatewaymanagementapi');
const DynamoDB = require('aws-sdk/clients/dynamodb');

exports.handler = async function (event, context, callback) {
    const db = new DynamoDB.DocumentClient();
    let connectionId = event.requestContext.connectionId;
    let connection;

    var params = {
        TableName: 'SocketManager',
        Key: {
            ConnectionId: connectionId
        }
    }

    try {
        connection = await db.get(params).promise();
    } catch (e) {
        return { statusCode: 500, body: e.stack };
    }

    const api = new ApiGatewayManagementApi({
        endpoint: 'https://1hwbpyynnd.execute-api.eu-west-1.amazonaws.com/beta/@connections',
    });

    const body = JSON.parse(event.body)
    var parameters = {
        TableName: 'Movies',
        Key: {
            id: parseInt(body.message)
        }
    }

    try {
        const data1 = await db.get(parameters).promise()
        await api.postToConnection({ ConnectionId: connectionId, Data: JSON.stringify(data1.Item) }).promise();
    } catch (e) {
        return { statusCode: 500, body: e.stack };
    }

    console.log("Done")

    return { statusCode: 200, body: 'Event sent.' };
};
