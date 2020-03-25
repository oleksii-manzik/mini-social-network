# mini-social-network  
*Was made as test task for Junior Python Developer position*  
  
Small REST API which provide basic functionality for creating users and posts and likes by user.   
  
## Models description:  
* User - creating users by not registered users and manipulating own data by registered users;  
* Post - creating posts by users and manipulating post data bby user who created it;  
* Like - ability to like/dislike post by user.  
  
## Basic endpoints:  
* [Api root](#api-root)
* [Get users](#get-users)
* [Get user](#get-user)
* [Get posts](#get-posts)
* [Get post](#get-post)
* [Get likes](#get-likes)
* [Get like](#get-like)
* [Create user](#create-user)
* [Sign in](#sign-in)
* [Update user](#update-user)
* [Partial update user](#partial-update-user)
* [Delete user](#delete-user)
* [Create post](#create-post)
* [Update post](#update-post)
* [Delete post](#delete-post)
* [Make like/unlike](#make-like-unlike)

### Api root  
  
* **URL**: /api/  
* **Method**: GET  
* **Authorization**: Not needed  
* **Description**: Returns URLs to all available models
* **Request**: No body  
* **Response**:   
  * Status code: 200 OK  
  * Content: 
 ```json
		 {
			"users": "http://localhost:8000/api/users/",   
			"posts": "http://localhost:8000/api/posts/",   
			"likes": "http://localhost:8000/api/likes/"  
		 }
 ```

### Get users
  
* **URL**: /api/users/
* **Method**: GET  
* **Authorization**: Not needed  
* **Description**: Count is number of users. Next and previous are URLs to next and previous pages and they will be available if number of users is higher then 10. Results is the list of users
* **Request**: No body  
* **Response**:   
  * Status code: 200 OK  
  * Content: 
 ```json
		 {
			"count": 2,
			"next": null,
			"previous": null,
			"results": [
				{
					"url": "http://localhost:8000/api/users/1/",
					"id": 1,
					"date_joined": "2020-03-25T12:39:28.132702Z",
					"first_name": "Mr",
					"last_name": "Example",
					"email": "mr.example@gmail.com",
					"profile": {
						"date_of_birth": "2001-02-02",
						"country": "USA",
						"city": "Texas City"
					},
					"posts": [
						"http://localhost:8000/api/posts/1/",
						"http://localhost:8000/api/posts/2/"
					],
					"likes": [
						"http://localhost:8000/api/likes/1/"
					]
				},
				{
					"url": "http://localhost:8000/api/users/2/",
					"id": 2,
					"date_joined": "2020-03-25T12:50:54.241746Z",
					"first_name": "Mrs",
					"last_name": "Example",
					"email": "mrs.example@gmail.com",
					"profile": {
						"date_of_birth": "1995-03-03",
						"country": "UK",
						"city": "London"
					},
					"posts": [],
					"likes": [
						"http://localhost:8000/api/likes/2/",
						"http://localhost:8000/api/likes/3/",
						"http://localhost:8000/api/likes/4/",
						"http://localhost:8000/api/likes/5/"
					]
				}
			]
		}
 ```

### Get user
  
* **URL**: /api/users/\<id>/  
* **Method**: GET  
* **Authorization**: Not needed  
* **Description**: Returns user information and URLs to post created by this user and likes/unlikes which he/she made
* **Request**: No body  
* **Response**:   
  * Status code: 200 OK  
  * Content: 
 ```json
		 {
			"url": "http://localhost:8000/api/users/1/",
			"id": 1,
			"date_joined": "2020-03-25T12:39:28.132702Z",
			"first_name": "Mr",
			"last_name": "Example",
			"email": "mr.example@gmail.com",
			"profile": {
				"date_of_birth": "2001-02-02",
				"country": "USA",
				"city": "Texas City"
			},
			"posts": [
				"http://localhost:8000/api/posts/1/",
				"http://localhost:8000/api/posts/2/"
			],
			"likes": [
				"http://localhost:8000/api/likes/1/"
			]
		}
 ```
 
### Get posts
  
* **URL**: /api/posts/
* **Method**: GET  
* **Authorization**: Not needed  
* **Description**: Count is number of posts. Next and previous are URLs to next and previous pages and they will be available if number of posts is higher then 10. Results is the list of posts
* **Request**: No body  
* **Response**:   
  * Status code: 200 OK  
  * Content: 
 ```json
		 {
			"count": 2,
			"next": null,
			"previous": null,
			"results": [
				{
					"url": "http://localhost:8000/api/posts/1/",
					"id": 1,
					"created": "2020-03-25T12:56:19.344993Z",
					"owner": "http://localhost:8000/api/users/1/",
					"text": "My first post",
					"likes": [
						"http://localhost:8000/api/likes/1/",
						"http://localhost:8000/api/likes/2/"
					],
					"number_of_likes": 2
				},
				{
					"url": "http://localhost:8000/api/posts/2/",
					"id": 2,
					"created": "2020-03-25T12:56:27.516677Z",
					"owner": "http://localhost:8000/api/users/1/",
					"text": "Cool!",
					"likes": [
						"http://localhost:8000/api/likes/3/",
						"http://localhost:8000/api/likes/4/",
						"http://localhost:8000/api/likes/5/"
					],
					"number_of_likes": 1
				}
			]
		}
 ```

### Get post
  
* **URL**: /api/posts/\<id>/   
* **Method**: GET  
* **Authorization**: Not needed  
* **Description**: Returns post information and likes/unlikes of this post. Owner is the user whom token was used for authorization when post was created. Number of likes shows number of users who have liked this post (this number considers that user can unlike post)
* **Request**: No body  
* **Response**:   
  * Status code: 200 OK  
  * Content: 
 ```json
		 {
			"url": "http://localhost:8000/api/posts/1/",
			"id": 1,
			"created": "2020-03-25T12:56:19.344993Z",
			"owner": "http://localhost:8000/api/users/1/",
			"text": "My first post",
			"likes": [
				"http://localhost:8000/api/likes/1/",
				"http://localhost:8000/api/likes/2/"
			],
			"number_of_likes": 2
		}
 ```

### Get likes
  
* **URL**: /api/likes/
* **Method**: GET  
* **Authorization**: Not needed  
* **Description**: Count is number of likes/unlikes. Next and previous are URLs to next and previous pages and they will be available if number of likes/unlikes is higher then 10. Results is the list of likes/unlikes
* **Request**: No body  
* **Response**:   
  * Status code: 200 OK  
  * Content: 
 ```json
		 {
			"count": 5,
			"next": null,
			"previous": null,
			"results": [
				{
					"url": "http://localhost:8000/api/likes/1/",
					"id": 1,
					"post": "http://localhost:8000/api/posts/1/",
					"owner": "http://localhost:8000/api/users/1/",
					"created": "2020-03-25T12:57:52.004696Z",
					"is_liked": true
				},
				{
					"url": "http://localhost:8000/api/likes/2/",
					"id": 2,
					"post": "http://localhost:8000/api/posts/1/",
					"owner": "http://localhost:8000/api/users/2/",
					"created": "2020-03-25T12:58:22.103267Z",
					"is_liked": true
				},
				{
					"url": "http://localhost:8000/api/likes/3/",
					"id": 3,
					"post": "http://localhost:8000/api/posts/2/",
					"owner": "http://localhost:8000/api/users/2/",
					"created": "2020-03-25T12:58:27.164883Z",
					"is_liked": true
				},
				{
					"url": "http://localhost:8000/api/likes/4/",
					"id": 4,
					"post": "http://localhost:8000/api/posts/2/",
					"owner": "http://localhost:8000/api/users/2/",
					"created": "2020-03-25T12:58:32.150749Z",
					"is_liked": false
				},
				{
					"url": "http://localhost:8000/api/likes/5/",
					"id": 5,
					"post": "http://localhost:8000/api/posts/2/",
					"owner": "http://localhost:8000/api/users/2/",
					"created": "2020-03-25T12:58:33.239545Z",
					"is_liked": true
				}
			]
		}
 ```

### Get like
  
* **URL**: /api/likes/\<id>/
* **Method**: GET  
* **Authorization**: Not needed  
* **Description**: Returns like/unlike information. Post is post which was liked/unliked and owner is the user who has made like/unlike. If "is_liked" is true it is like, otherwise unlike
* **Request**: No body  
* **Response**:   
  * Status code: 200 OK  
  * Content: 
 ```json
		 {
			"url": "http://localhost:8000/api/likes/1/",
			"id": 1,
			"post": "http://localhost:8000/api/posts/1/",
			"owner": "http://localhost:8000/api/users/1/",
			"created": "2020-03-25T12:57:52.004696Z",
			"is_liked": true
		}
 ```

### Create user

* **URL**: /api/users/
* **Method**: POST 
* **Authorization**: Not needed  
* **Description**: When creating a user no authorization is needed. All fields in request example is required
* **Request**: 
```json
{
	"email": "mr.example@gmail.com",
	"first_name": "Mr",
	"last_name": "Example",
	"password": "mrexamplepassword123",
	"date_of_birth": "2001-02-02",
	"country": "USA",
	"city": "Texas City"
}
```
* **Response**:   
  * Status code: 201 Created  
  * Content: 
 ```json
		 {
			"url": "http://localhost:8000/api/users/1/",
			"id": 1,
			"date_joined": "2020-03-25T12:39:28.132702Z",
			"first_name": "Mr",
			"last_name": "Example",
			"email": "mr.example@gmail.com"
		}
 ```
 
 ### Sign in

* **URL**: /api/auth/login/
* **Method**: POST 
* **Authorization**: Not needed  
* **Description**: Returns JWT token for specific user. This token is expired after 5 minutes
* **Request**: 
```json
{
	"email": "mr.example@gmail.com", 
	"password": "mrexamplepassword123"
}
```
* **Response**:   
  * Status code: 200 OK 
  * Content: 
 ```json
		 {
			"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjozLCJ1c2VybmFtZSI6Im1yLmV4YW1wbGVAZ21haWwuY29tIiwiZXhwIjoxNTg1MTYzMDM2LCJlbWFpbCI6Im1yLmV4YW1wbGVAZ21haWwuY29tIn0.bcw7Gu_Gr7Wyq9__bz8Ng-ABBlU2-iir435tP8m-Lho",
			"user": {
				"pk": 1,
				"username": null,
				"email": "mr.example@gmail.com",
				"first_name": "Mr",
				"last_name": "Example"
			}
		}
 ```
 * **Token expired response**:
  ```json
 {
	"detail": "Signature has expired."
}
```

### Update user
 
* **URL**: /api/users/\<id>/
* **Method**: PUT
* **Authorization**: JWT
* **Description**: You need to send all fields to make complete update. Also user can update only his/her own information 
* **Request**: 
```json
{
	"email": "mr.example@gmail.com",
	"first_name": "Mr",
	"last_name": "Example",
	"password": "mrexamplepassword123",
	"date_of_birth": "2001-02-02",
	"country": "USA",
	"city": "New York"
}
```
* **Response**:   
  * Status code: 200 OK  
  * Content: 
 ```json
		 {
			"url": "http://localhost:8000/api/users/1/",
			"id": 1,
			"date_joined": "2020-03-25T12:39:28.132702Z",
			"first_name": "Mr",
			"last_name": "Example",
			"email": "mr.example@gmail.com"
		}
 ```
 
### Partial update user
 
* **URL**: /api/users/\<id>/
* **Method**: PATCH
* **Authorization**: JWT
* **Description**: You need to send fields which you want to update. Also user can update only his/her own information 
* **Request**: 
```json
{
	"city": "New York"
}
```
* **Response**:   
  * Status code: 200 OK  
  * Content: 
 ```json
		 {
			"url": "http://localhost:8000/api/users/1/",
			"id": 1,
			"date_joined": "2020-03-25T12:39:28.132702Z",
			"first_name": "Mr",
			"last_name": "Example",
			"email": "mr.example@gmail.com"
		}
 ```
 ### Delete user
 
* **URL**: /api/users/\<id>/
* **Method**: Delete
* **Authorization**: JWT
* **Description**: User can only delete himself/herself
* **Request**: No body
* **Response**:   
  * Status code: 204 No Content 
  
 ### Create post

* **URL**: /api/posts/
* **Method**: POST 
* **Authorization**: JWT
* **Description**: Post is created by the user which JWT token is using
* **Request**: 
```json
{
	"text": "Cool!"
}
```
* **Response**:   
  * Status code: 201 Created  
  * Content: 
 ```json
		 {
			"url": "http://localhost:8000/api/posts/3/",
			"id": 3,
			"created": "2020-03-25T19:22:47.334668Z",
			"owner": "http://localhost:8000/api/users/3/",
			"text": "Cool!",
			"likes": [],
			"number_of_likes": 0
		}
 ```
 
 ### Update post
 
* **URL**: /api/posts/\<id>/
* **Method**: PUT
* **Authorization**: JWT
* **Description**: User can update only posts which he/she has created 
* **Request**: 
```json
{
	"text": "New text"
}
```
* **Response**:   
  * Status code: 200 OK  
  * Content: 
 ```json
		 {
			"url": "http://localhost:8000/api/posts/3/",
			"id": 3,
			"created": "2020-03-25T19:22:47.334668Z",
			"owner": "http://localhost:8000/api/users/3/",
			"text": "New text",
			"likes": [],
			"number_of_likes": 0
		}
 ```
 
 ### Delete post
 
* **URL**: /api/posts/\<id>/
* **Method**: Delete
* **Authorization**: JWT
* **Description**: User can only delete posts he/she has created
* **Request**: No body
* **Response**:   
  * Status code: 204 No Content 

### Make like-unlike

* **URL**: /api/likes/
* **Method**: POST 
* **Authorization**: JWT 
* **Description**: You only need to specify which post you want to like/unlike. If post was liked by this user the last time it will be unliked. Otherwise it will be liked
* **Request**: 
```json
{
	"post_id": 1
}
```
* **Response**:   
  * Status code: 201 Created  
  * Content: 
 ```json
		 {
		"url": "http://localhost:8000/api/likes/6/",
		"id": 6,
		"post": "http://localhost:8000/api/posts/1/",
		"owner": "http://localhost:8000/api/users/3/",
		"created": "2020-03-25T19:31:40.801571Z",
		"is_liked": true
		}
 ```
 

