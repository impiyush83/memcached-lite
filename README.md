# memcached-lite
The main task is to implement a server, that stores and retrieves data for different clients. For each key, there is a unique value that the server stores, using the set &lt;key> &lt;value> command, and retrieves it using a get &lt;key> command.


### Client Commands:


1. **SET** 

    ```  
    Bytes represent length of value
    
    set <key> <bytes>\r\n <value>\r\n

    Responses:
    
    STORED\r\n  - If successfully stored 
    NOT-STORED\r\n - If an error occurs while storing data
    ERROR\r\n - error
    ```
    
    
2. **GET** 

    ```  
    Bytes represent length of value
    
    get <key>\r\n

    Responses:
    
    VALUE key1 zzzzz END
    
    NOT-FOUND\r\n - If key is not found
    ```
