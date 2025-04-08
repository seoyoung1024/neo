const https = require('http');

const data = JSON.stringify({ todo : 'Buy the milk' });

const options = {
    hostname: '192.168.1.21',
    port: 8000,
    path: '/hello',
    method: 'GET',
};

const req = https.request(options, res => {
    console.log(`statusCode: ${res.statusCode}`);
    res.on('data', (d) => {
        process.stdout.write(d);
    })
})

req.on('error', (error) => {
    console.error(error);
})

req.write(data);
req.end();