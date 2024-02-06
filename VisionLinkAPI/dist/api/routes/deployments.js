"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const express = require('express');
const router = express.Router();
const executeSP = require('../execute_SP.js');
const executeF = require('../execute_F.js');
router.get('/', (req, res, next) => {
    res.status(200).json({
        message: "Handling requests for /deployments"
    });
});
router.get('/SP', (req, res, next) => {
    const sp_name = "test_sp";
    const sc_name = "vision_data";
    const params = [];
    executeSP(sc_name, sp_name, params)
        .then(result => {
        res.status(200).json(result);
    })
        .catch(err => {
        res.status(500).json({ error: err });
    });
});
router.get('/F', (req, res, next) => {
    const f_name = "test_f";
    const sc_name = "vision_data";
    const params = [];
    executeF(sc_name, f_name, params)
        .then(result => {
        res.status(200).json(result);
    })
        .catch(err => {
        res.status(500).json({ error: err });
    });
});
router.get('/:deploymentID', (req, res, next) => {
    const id = req.params.deploymentID;
    const message = "Handling requests for deployment " + id + " number";
    res.status(200).json({
        message: message
    });
});
router.post('/', (req, res, next) => {
    const deployment = {
        deployment_id: req.body.deployment_id,
        deployment_name: req.body.deployment_name,
        target_id: req.body.target_id,
        status_value: req.body.status_value,
        model_id: req.body.model_id,
        creation_date: req.body.creation_date,
        start_date: req.body.start_date,
        expiry_date: req.body.expiry_date
    };
    console.log(deployment.expiry_date);
    res.status(200).json({
        message: deployment.expiry_date
    });
});
module.exports = router;
//# sourceMappingURL=deployments.js.map