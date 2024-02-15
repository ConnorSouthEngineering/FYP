"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const app = express();
app.use(cors({
    origin: ['http://localhost:4200', 'http://localhost:8080'],
}));
const deploymentRoutes = require('./api/routes/deployments');
const targetRoutes = require('./api/routes/targets');
const reportRoutes = require('./api/routes/reports');
const mapRoutes = require('./api/routes/maps');
const taskRoutes = require('./api/routes/tasks');
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());
app.use('/reports', reportRoutes);
app.use('/targets', targetRoutes);
app.use('/deployments', deploymentRoutes);
app.use('/maps', mapRoutes);
app.use('/tasks', taskRoutes);
app.use((req, res, next) => {
    const error = new Error('Not Found');
    error.status = 404;
    next(error);
});
module.exports = app;
//# sourceMappingURL=app.js.map