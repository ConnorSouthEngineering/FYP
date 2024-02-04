const express = require('express');
const bodyParser = require('body-parser');
const app = express();

const deploymentRoutes = require('./api/routes/deployments');
const targetRoutes = require('./api/routes/targets');
const reportRoutes = require('./api/routes/reports');

app.use(bodyParser.urlencoded({extended: false}));
app.use(bodyParser.json());

/* app.use((req, res, next) => {
    res.header("access-control-allow-origin", "*");
    res.header(
        "access-control-allow-headers",
        "Origin, X-Requested-With, Content-Type, Accept, Authorization"
    );
    if (req.method === 'OPTIONS') {
        res.header('access-control-allow-methods', 'POST, PUT, PATCH, DELETE');
        return res.status(200).json({});
    }
}); */

app.use('/reports', reportRoutes);
app.use('/targets', targetRoutes);
app.use('/deployments', deploymentRoutes);

app.use((req, res, next) => {
    const error = new Error('Not Found');
    error.status = 404;
    next(error);
});
module.exports = app;