# pydelighted


This is pydelighted, a python package to import your data from the delighted API

--> How to write the config file :

    schema_prefix: schema_name
    endpoints:
        endpoint_name:
            table: 'table_name'
            date_fields:
                - 'created_at'
                - 'updated_at' 
