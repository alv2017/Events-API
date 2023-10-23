## Event API Documentation 

### 1. Authentication

#### 1.1 User Login [+]
```
Method: POST
URL: /api/v1/auth/login/
Authentication required: No

Request Body Template:
{
    "username": "some_name",
    "password": "some_password"
}

In case of success the response contains access and refresh tokens.

Successful Response Status Code: 200
```

#### 1.2 Refresh token (Access Token Renewal) [+]
```
Method: POST
URL: /api/v1/auth/login/refresh/
Authentication required: No

Request Body Template:
{
    "refresh": "refresh_token_goes_here",
}

In case of success the response body contains access token.

Successful Response Status Code: 200
```

#### 1.3 Verify Token [+]
```
Method: POST
URL: /api/v1/auth/verify/
Authentication required: Yes
Authentication type: Access Token

Request Body Template:
{
    "token": "token_to_verify",
}

In case of valid token the response body is empty.

Successful Response Status Code: 200
```

### 2. User Personal Account

#### 2.1 Create User Account [+]
```
Method: POST
URL: /api/v1/user/account/
Authentication required: No

Request Body Template:
{
    "username": "your_username",
    "first_name": "your_first_name",
    "last_name": "your_last_name",
    "email": "your_email",
    "password": "account_password"
}

In case of success the response body will contain newly created user details.
Fields: username, first_name, last_name, email, last_login

Successful Response Status Code: 201
```

#### 2.2 Show Logged-in User Account Details [+]
```
Method: GET
URL: /api/v1/user/account/me/
Authentication required: Yes
Authentication type: Access Token

In case of success the response body will contain details of the account owner.
Fields: username, first_name, last_name, email, last_login

Successful Response Status Code: 200
```

#### 2.3 Update Logged-in User Account Details [+]
```
Method: PATCH
URL: /api/v1/user/account/me/
Authentication required: Yes
Authentication type: Access Token

Request body must contain the account details you want to update.

Successful Response Status Code: 200
```

### 3. User Management (for Admin Users only)

#### 3.1 Get List of Users [+]
```
Method: GET
URL: /api/v1/user/manage/
Authentication required: Yes
Authentication type: Access Token
Comment: Only Admin users can access this endpoint

In case of success the response body will contain a list of users.

Successful Response Status Code: 200
```

#### 3.2 Create User [+]
```
Method: POST
URL: /api/v1/user/manage/
Authentication required: Yes
Authentication type: Access Token
Comment: Only Admin users can access this endpoint

Request Body Template:
{
    "username": "user_username",
    "first_name": "user_first_name",
    "last_name": "user_last_name",
    "email": "user_email",
    "password": "user_password"
}

In case of success the response body will contain newly created user details.
Fields: username, first_name, last_name, email, is_active, is_staff, is_superuser, last_login, date_joined

Successful Response Status Code: 201
```

#### 3.3 Retrieve User Details [+]
```
Method: GET
URL: /api/v1/user/manage/<int:pk>/
Authentication required: Yes
Authentication type: Access Token
Comment: Only Admin users can access this endpoint

In case of success the response body will contain the details of the user with the specified id.

Successful Response Status Code: 200
```

#### 3.4 Update User Details [+]
```
Method: PUT
URL: /api/v1/user/manage/<int:pk>/
Authentication required: Yes
Authentication type: Access Token
Comment: Only Admin users can access this endpoint

Request body must contain the user account details which you want to update.

Response body will contain all user details with the updates applied.

Successful Response Status Code: 200
```

#### 3.5 Delete User [+]
```
Method: DELETE
URL: /api/v1/user/manage/<int:pk>/
Authentication required: Yes
Authentication type: Access Token
Comment: Only Admin users can access this endpoint

Successful Response Status Code: 204
```

### 4. Event Management

#### 4.1 Create Event [+]
```
Method: POST
URL: /api/v1/event/events/
Authentication required: Yes
Authentication type: Access Token

Request Body Template:
{
    "name": "event_name",
    "description": "event description",
    "start": "YYYY-MM-DD HH:m:s",
    "end": "YYYY-MM-DD HH:m:s",
    "is_published": true
}

In case of success the response body will contain newly created event details.
Fields: id, name, description, start(time), end(time), is_published, created_on, updated_on

Successful Response Status Code: 201
```

#### 4.2 List Events (Published Only) [+]
```
Method: GET
URL: /api/v1/event/events/
Authentication required: Yes
Authentication type: Access Token

In case of success the response body will contain a list of all published events.

Successful Response Status Code: 200
```

The endpoint support the query parameter *t*. For example, the endpoint below will return future events only:
```
/api/v1/event/events/?t=future
```

**Available Options**
- t=today: returns today's events, this includes published events only;
- t=past: returns past events, this includes published events only;
- t=future: returns future events, this includes published events only;
- t=all: returns all the events, published and unpublished.

#### 4.3 Event Details [+]
```
Method: GET
URL: /api/v1/event/events/<int:pk>/
Authentication required: Yes
Authentication type: Access Token

In case of success the response body will contain the details of the event with the specified id.

Successful Response Status Code: 200
```

#### 4.4 Update Event [+]
```
Method: PUT or PATCH
URL: /api/v1/event/events/<int:pk>/
Authentication required: Yes
Authentication type: Access Token
Comment: Only a creator of the event will be able to make updates

Request body must contain the details of event that need an update.

Response body will contain the event details with the updates applied.

Successful Response Status Code: 200
```

#### 4.5 Delete Event [+]
```
Method: DELETE
URL: /api/v1/event/events/<int:pk>/
Authentication required: Yes
Authentication type: Access Token
Comment: Only a creator of the event will be able to make updates

Successful Response Status Code: 204
```

#### 4.6 List Logged-in User Created Events (List all events created by me)
```
Method: GET
URL: /api/v1/event/me/events/
Authentication required: Yes
Authentication type: Access Token

In case of success the response body will contain a list of events created by the logged-in user.

Successful Response Status Code: 200
```

#### 4.7 Registrations for Events of the Logged-in User (Show all my registrations)
```
Method: GET
URL: /api/v1/event/me/registrations/<int:event_id>/
Authentication required: Yes
Authentication type: Access Token

In case of success the response body will contain a list of events the logged-in user registered for.

Successful Response Status Code: 200
```

#### 4.8 Register for an Event (Register me for event)
```
Method: POST
URL: /api/v1/event/me/registrations/<int:event_id>/
Authentication required: Yes
Authentication type: Access Token

Request body is empty.

In case of success the response body will contain a message saying that you are registered for the event.

Successful Response Status Code: 201
```

#### 4.9 Cancel Registration for an Event
```
Method: DELETE
URL: /api/v1/event/me/registrations/<int:event_id>/
Authentication required: Yes
Authentication type: Access Token

In case of success the response body will contain a message saying that your registration is cancelled.

Successful Response Status Code: 204
```