"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const express = require('express');
const router = express.Router();
const executeSP = require('../execute_SP.js');
const executeF = require('../execute_F.js');
const axios = require('axios');
router.post('/', async (req, res, next) => {
    const _model_name = req.body.model_name;
    const _creation_date = req.body.creation_date;
    const _status_value = req.body.status_value;
    const _train = req.body.train;
    const _test = req.body.test;
    const _verification = req.body.verification;
    const _classes = req.body.classes;
    const _sources = req.body.sources;
    const params = [_model_name, _creation_date, _status_value, _train, _test, _verification, _classes, _sources];
    try {
        const task_id = await executeF("vision_data", "insert_model_task", params);
        const initialisation_data = {
            "task_id": task_id
        };
        /*         const model_creation_url = "http://localhost:8080/api/model";
                await axios.post(model_creation_url, initialisation_data, {
                    headers: {
                        'Content-Type': 'application/json',
                    }
                });
                res.status(200).json({
                    task_id: task_id
                });   */
    }
    catch (err) {
        console.error('Error:', err);
        res.status(500).json({ error: err.toString() });
    }
});
router.get('/:_task_id', (req, res, next) => {
    const _task_id = req.params._task_id;
    const params = [_task_id];
    executeF("vision_data", "get_task", params)
        .then(result => {
        res.status(200).json(result);
    })
        .catch(err => {
        res.status(500).json({ error: err });
    });
});
router.get('/:_task_id/classes', (req, res, next) => {
    const _task_id = req.params._task_id;
    const params = [_task_id];
    executeF("vision_data", "get_task_classes", params)
        .then(result => {
        res.status(200).json(result);
    })
        .catch(err => {
        res.status(500).json({ error: err });
    });
});
router.get('/:_task_id/sources', (req, res, next) => {
    const _task_id = req.params._task_id;
    const params = [_task_id];
    executeF("vision_data", "get_task_sources", params)
        .then(result => {
        res.status(200).json(result);
    })
        .catch(err => {
        res.status(500).json({ error: err });
    });
});
module.exports = router;
//# sourceMappingURL=tasks.js.map