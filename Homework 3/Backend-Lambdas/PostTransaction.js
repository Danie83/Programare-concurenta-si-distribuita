const DynamoDB = require('aws-sdk/clients/dynamodb');

exports.handler = async (event) => {
    const db = new DynamoDB.DocumentClient();
    
    const currentDate = new Date().toLocaleDateString('en-GB');
    
    var parameters = {
        TableName: 'Transactions',
        Item: {
            user_id: event.queryStringParameters.user_id,
            amount: event.queryStringParameters.amount,
            date: currentDate,
            type: event.queryStringParameters.type
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
