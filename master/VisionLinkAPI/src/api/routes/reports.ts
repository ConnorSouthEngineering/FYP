const express = require('express');
const router = express.Router();
const executeSP = require('../execute_SP.js');
const executeF= require('../execute_F.js');

router.get('/',(req,res,next)=>{
    const _item_limit = parseInt(req.query.itemLimit, 10) || 10; 
    const _current_page = parseInt(req.query.currentPage, 10) || 1;
    const params = [_item_limit,_current_page];
    executeF("vision_data","get_latest_reports", params)
    .then(result => {
        res.status(200).json(result);
    })
    .catch(err => {
        res.status(500).json({error: err});
    });
})

router.get('/:_report_id',(req,res,next)=>{
    const _report_id = req.params._report_id;
    const params = [_report_id];
    executeF("vision_data","get_report", params)
    .then(result => {
        res.status(200).json(result);
    })
    .catch(err => {
        res.status(500).json({error: err});
    });
})

router.get('/:_report_id/classes',(req,res,next)=>{
    const _report_id = req.params._report_id;
    const params = [_report_id];
    executeF("vision_data","get_report_classes", params)
    .then(result => {
        res.status(200).json(result);
    })
    .catch(err => {
        res.status(500).json({error: err});
    });
})

router.get('/:_report_id/graph',(req,res,next)=>{
    const _report_id = req.params._report_id;
    const params = [_report_id];
    executeF("vision_data","get_graph_id", params)
    .then(result => {
        res.status(200).json(result);
    })
    .catch(err => {
        res.status(500).json({error: err});
    });
})

router.get('/:_report_id/data', (req, res, next) => {
    const _start_date = req.query._start_date;
    const _end_date = req.query._end_date;
    const _class_ids = req.query._class_ids;
    const _deployment_id = req.query._deployment_id;
    const _metric_value = req.query._metric_value || null; 


    const params = [_start_date, _end_date, _class_ids, _deployment_id, _metric_value];

    executeF("vision_data", "get_report_data", params)
        .then(result => {
            res.status(200).json(result);
        })
        .catch(err => {
            res.status(500).json({ error: err });
        });
});


module.exports = router;