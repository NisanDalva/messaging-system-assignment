Here is a list of endpoints the system supports:  

**Register**
----
Register a new user.

* **Method + URL**

   **```POST```** ```/user/register```

* **Data Params**

    ***Required***  
    **```name```** = ```"[string]"```  **```email```** = ```"[string]"```  **```password```** = ```"[string]"```

* **Success Response**

    **Code:** 200  **Content:**
    ```json
    {
        "email": "[string]",
        "id": "[integer]",
        "name": "[string]",
        "password": "[encrypted password]"
    }
    ```

* **Error Response**

    **Code:** 400 Bad Request  
    if a given body is not a ```json```, missed at least one data param or entered an email that already exists.

* **Sample Call**

    ```json
    {
        "email": "user@email.com",
        "name": "user",
        "password": "123"
    }
    ```


**Login**
----
Login an existing user.

* **Method + URL**

   **```GET```** ```/user/login/<email>/<password>```

* **URL Params**

    ***Required***  
    **```email```** = ```"[string]"```  **```password```** = ```"[string]"```

* **Success Response**

    **Code:** 200  **Content:**
    ```json
    {
        "email": "[string]",
        "id": "[integer]",
        "name": "[string]",
        "password": "[encrypted password]"
    }
    ```

* **Error Response**

    **Code:** 404 Not Found  
    if a given email doesn't found in the data base or if typed a incorrect password.

* **Sample Call**

    **```POST```** ```/user/login/user1@email.com/123```


**Logout**
----
Logout an existing user.

* **Method + URL**

   **```GET```** ```/user/logout```

* **Success Response**

    **Code:** 200  **Content:**
    ```json
    {
        "message": "logout successfully",
        "status": 200
    }
    ```

* **Sample Call**

    **```GET```** ```/user/logout```


**Send message**
----
Send a message between user.  
**NOTE:** In order to this functionality will work, you must be login first.

* **Method + URL**

   **```POST```** ```/message/send```

* **Data Params**

    ***Required***  
    **```subject```** = ```"[string]"```  **```message```** = ```"[string]"```  **```receiver```** = ```[user.id]```

* **Success Response**

    **Code:** 200  **Content:**
    ```json
    {
        "creation_date": "[datetime]",
        "did_read": false,
        "id": "[message.id]",
        "message": "[message]",
        "receiver": "[the user.id to whom the message was sent]",
        "sender": "[the user.id who sends the message]",
        "subject": "[the subject]"
    }
    ```

* **Error Response**

    **Code:** 400 Bad Request  
    if a given body is not a ```json``` or missed at least one data param.

* **Sample Call**

    ```json
    {
        "subject": "example subject",
        "message": "some message",
        "receiver": 3
    }
    ```


**Get all Messages**
----
Get all messages that **sent** to the logged in user only, and mark each message returned as read.  
**NOTE:** In order to this functionality will work, you must be login first.

* **Method + URL**

   **```PUT```** ```/message/all```

* **Success Response**

    **Code:** 200  **Content:**
    ```json
    [
        {
            "creation_date": "[datetime]",
            "did_read": false,
            "id": "[message.id]",
            "message": "[message]",
            "receiver": "[the user.id to whom the message was sent]",
            "sender": "[the user.id who sends the message]",
            "subject": "[the subject]"
        },
        {
            "creation_date": "[datetime]",
            "did_read": false,
            "id": "[message.id]",
            "message": "[message]",
            "receiver": "[the user.id to whom the message was sent]",
            "sender": "[the user.id who sends the message]",
            "subject": "[the subject]"
        },
        .
        .
        .
    ]
    ```

* **Sample Call**

    **```PUT```** ```/message/all```


**Get all Unread Messages**
----
Get all unread messages that **sent** to the logged in user only, and mark each message returned as read.  
**NOTE:** In order to this functionality will work, you must be login first.

* **Method + URL**

   **```PUT```** ```/message/all/unread```

* **Success Response**

    **Code:** 200  **Content:**
    ```json
    [
        {
            "creation_date": "[datetime]",
            "did_read": false,
            "id": "[message.id]",
            "message": "[message]",
            "receiver": "[the user.id to whom the message was sent]",
            "sender": "[the user.id who sends the message]",
            "subject": "[the subject]"
        },
        {
            "creation_date": "[datetime]",
            "did_read": false,
            "id": "[message.id]",
            "message": "[message]",
            "receiver": "[the user.id to whom the message was sent]",
            "sender": "[the user.id who sends the message]",
            "subject": "[the subject]"
        },
        .
        .
        .
    ]
    ```

* **Sample Call**

    **```PUT```** ```/message/all/unread```


**Read One Message**
----
Read only one unread message that **sent** to the logged in user only, and mark each message returned as read (I chose to pick up the latest one).  
**NOTE:** In order to this functionality will work, you must be login first.

* **Method + URL**

   **```PUT```** ```/message/latest```

* **Success Response**

    **Code:** 200  **Content:**
    ```json
    {
        "creation_date": "[datetime]",
        "did_read": false,
        "id": "[message.id]",
        "message": "[message]",
        "receiver": "[the user.id to whom the message was sent]",
        "sender": "[the user.id who sends the message]",
        "subject": "[the subject]"
    }
    ```

* **Sample Call**

    **```PUT```** ```/message/latest```


**Delete Message**
----
Delete a message by id as an owner or as receiver.
**NOTE:** In order to this functionality will work, you must be login first.

* **Method + URL**

   **```DELETE```** ```/message/delete/<id>```

* **Data Params**

    ***Required***  
    **```id```** = ```[message.id]```

* **Error Response**

    **Code:** 500  **Content:**
    ```json
    {
        "message": "unable to delete the message",
        "status": 500
    }
    ```

* **Sample Call**

    **```DELETE```** ```/message/delete/2```