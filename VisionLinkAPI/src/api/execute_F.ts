const pool  = require('../dbconfig.js');

async function executeF(schema_name, function_name, params) {
    const client = await pool.connect();
    let result;
    try {
        const paramPlaceholders = params.map((_, index) => `$${index + 1}`).join(', ');
        const queryText = `SELECT * FROM ${schema_name}.${function_name}(${paramPlaceholders})`;
        result = await client.query(queryText, params);
    } catch (err) {
        console.log(err);
        return "Error executing function";
    } finally {
        client.release();
    }
    return result ? result.rows : null;
}

module.exports = executeF;
