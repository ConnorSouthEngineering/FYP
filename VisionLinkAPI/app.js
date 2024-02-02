const express = require('express');
const bodyParser = require('body-parser');
const app = express();

const deploymentRoutes = require('./api/routes/deployments');
const targetRoutes = require('./api/routes/targets');
const reportRoutes = require('./api/routes/reports');

app.use(bodyParser.urlencoded({extended: false}));
app.use(bodyParser.json());

app.use('/reports', reportRoutes);
app.use('/targets', targetRoutes);
app.use('/deployments', deploymentRoutes);

app.use((req, res, next) => {
    const error = new Error('Not Found');
    error.status = 404;
    next(error);
});
module.exports = app;