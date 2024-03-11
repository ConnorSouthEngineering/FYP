const express = require('express');
const router = express.Router();
const executeSP = require('../execute_SP.js');
const executeF= require('../execute_F.js');

router.post('/connect',async(req,res,next)=>{
    console.log(req.body)
    const _node_key_value = req.body.node_key_value;
    const _node_id = req.body.node_id || null;
    const _node_name = req.body.node_name || null;
    let _creation_date;
    let _node_address;
    if (req.body.creation_date) {
        try {
            let tempDate = new Date(req.body.creation_date);
            if (!isNaN(tempDate.getTime())) { 
                _creation_date = tempDate.toISOString();
            } else {
                _creation_date = null; 
            }
        } catch (error) {
            _creation_date = null; 
        }
    } else {
        _creation_date = null; 
    }
    if(!_node_id){
        _node_address = req.ip;
    }
    else{
        _node_address = null;
    }

    const params = [_node_key_value,_node_id,_node_name,_node_address,_creation_date];
    const result = await executeF("vision_data","create_connection", params)
    const map_result = result[0].create_connection.map
    switch(map_result){
        case "new":
            res.status(200).json({status:"Connected",node_id: result[0].create_connection.node_id});
            break;
        case "existing":
            res.status(200).json({status:"Connected",node_id: result[0].create_connection.node_id});
            break;
        case "different":
            res.status(500).json({error: "Key is already assigned to a different node"});
            break;
        case "missing":
            res.status(500).json({error: "Key is invalid"});
            break;
        default:
            res.status(500).json({error: "Unknown error"});
            break;
    }
})

router.get('/',(req,res,next)=>{
    const _item_limit = parseInt(req.query.itemLimit, 10) || 10; 
    const _current_page = parseInt(req.query.currentPage, 10) || 1;
    const params = [_item_limit,_current_page];
    executeF("vision_data","get_latest_nodes", params)
    .then(result => {
        res.status(200).json(result);
    })
    .catch(err => {
        res.status(500).json({error: err});
    });
})

router.get('/key/:key_id',(req,res,next)=>{
    const _key_id = req.params.key_id
    const params = [_key_id];
    executeF("vision_data","get_key", params)
    .then(result => {
        res.status(200).json(result);
    })
    .catch(err => {
        res.status(500).json({error: err});
    });
})

router.post('/key/generate',(req,res,next)=>{
    const _creation_date = new Date().toISOString();
    const params = [_creation_date];
    executeF("vision_data","insert_node_key", params)
    .then(result => {
        res.status(200).json(result);
    })
    .catch(err => {
        res.status(500).json({error: err});
    });
})

module.exports = router;