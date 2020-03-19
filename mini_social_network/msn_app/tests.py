from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


def get_jwt_token(client, input_data):
    url = reverse('rest_login')
    response = client.post(url, input_data)
    data = response.data
    token = data.get('token')
    return token


class UserTests(APITestCase):
    fixtures = ['user.json', 'user_profile.json', 'post.json', 'like.json']

    def test_get_user(self):
        user_id = 1
        url = reverse('user-detail', args=[user_id])
        response = self.client.get(url)
        data = response.data
        with self.subTest('user data'):
            self.assertEqual(data.get('id'), 1)
            self.assertEqual(data.get('email'), 'some.guy@gmail.com')
            self.assertEqual(data.get('first_name'), 'Some')
            self.assertEqual(data.get('last_name'), 'Guy')
        with self.subTest('profile data'):
            profile = data.get('profile')
            self.assertIsNotNone(profile, "Profile can't be None")
            self.assertEqual(profile.get('date_of_birth'), '1991-01-01')
            self.assertEqual(profile.get('country'), 'Poland')
            self.assertEqual(profile.get('city'), 'Warsaw')
        with self.subTest('no password'):
            self.assertIsNone(data.get('password'),
                              'Password must be write only')
        with self.subTest('posts made by user'):
            posts = data.get('posts')
            self.assertIsNotNone(posts, "Posts can't be None")
            self.assertEqual(len(posts), 2)
            with self.subTest('post url'):
                post_url = posts[0]
                post_response = self.client.get(post_url)
                post_data = post_response.data
                self.assertEqual(post_data.get('id'), 1)
        with self.subTest('likes made by user'):
            likes = data.get('likes')
            self.assertIsNotNone(likes, "Likes can't be None")
            self.assertEqual(len(likes), 3)
            with self.subTest('like url'):
                like_url = likes[0]
                like_response = self.client.get(like_url)
                like_data = like_response.data
                self.assertEqual(like_data.get('id'), 1)

    def test_get_users(self):
        url = reverse('user-list')
        response = self.client.get(url)
        data = response.data
        results = data.get('results')
        self.assertIsNotNone(results, "Results can't be None")
        with self.subTest('number of users'):
            self.assertEqual(data.get('count'), 3)
            self.assertEqual(len(results), 3)
        with self.subTest('user url'):
            user_url = results[0].get('url')
            self.assertIsNotNone(user_url, "User URL can't be None")
            user_response = self.client.get(user_url)
            user_data = user_response.data
            self.assertEqual(user_data.get('id'), 1)

    def test_create_user(self):
        url = reverse('user-list')
        input_data = {'email': 'mr.example@gmail.com',
                      'first_name': 'Mr',
                      'last_name': 'Example',
                      'password': 'mrexamplepassword123',
                      'date_of_birth': '2001-02-02',
                      'country': 'USA',
                      'city': 'Texas City'}
        response = self.client.post(url, input_data)
        data = response.data
        with self.subTest('user data'):
            self.assertEqual(data.get('id'), 4)
            self.assertEqual(data.get('email'), 'mr.example@gmail.com')
        with self.subTest('no password'):
            self.assertIsNone(data.get('password'),
                              'Password must be write only')
        with self.subTest('number of users'):
            response = self.client.get(url)
            data = response.data
            self.assertEqual(data.get('count'), 4)
            self.assertEqual(len(data.get('results')), 4)

    def test_update_user(self):
        user_id = 1
        url = reverse('user-detail', args=[user_id])
        input_data = {'email': 'some.guy@gmail.com',
                      'password': 'pbkdf2_sha256$180000$0yKC2GpsMay7$Js64xQb26'
                                  'OdPFhrEsMEVJMhDQhIqXssphFlPPMUuNEU=',
                      'first_name': 'Some2',
                      'last_name': 'Guy2',
                      'date_of_birth': '1991-01-01',
                      'country': 'Germany',
                      'city': 'Berlin'}
        with self.subTest('no credentials'):
            response = self.client.put(url, input_data)

            self.assertEqual(response.status_code,
                             status.HTTP_401_UNAUTHORIZED)
            data = response.data
            detail = data.get('detail')
            self.assertEqual(detail,
                             'Authentication credentials were not provided.')
        with self.subTest('other user credentials'):
            other_person_credentials = {'email': 'this.girl@gmail.com',
                                        'password': '23bbn'}
            token = get_jwt_token(self.client, other_person_credentials)

            response = self.client.put(url, input_data,
                                       HTTP_AUTHORIZATION=f'JWT {token}')

            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
            data = response.data
            detail = data.get('detail')
            self.assertEqual(detail,
                             'You do not have permission to perform this '
                             'action.')
        with self.subTest('normal credentials'):
            person_credentials = {'email': 'some.guy@gmail.com',
                                  'password': 'aas1234'}
            token = get_jwt_token(self.client, person_credentials)

            response = self.client.put(url, input_data,
                                       HTTP_AUTHORIZATION=f'JWT {token}')

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            data = response.data
            self.assertEqual(data.get('first_name'), 'Some2')
            self.assertEqual(data.get('last_name'), 'Guy2')
            user_response = self.client.get(url)
            user_profile = user_response.data.get('profile')
            self.assertIsNotNone(user_profile, "Profile can't be None")
            self.assertEqual(user_profile.get('country'), 'Germany')
            self.assertEqual(user_profile.get('city'), 'Berlin')

    def test_partial_update_user(self):
        user_id = 1
        url = reverse('user-detail', args=[user_id])
        input_data = {'country': 'Germany',
                      'city': 'Berlin'}
        with self.subTest('no credentials'):
            response = self.client.patch(url, input_data)

            self.assertEqual(response.status_code,
                             status.HTTP_401_UNAUTHORIZED)
            data = response.data
            detail = data.get('detail')
            self.assertEqual(detail,
                             'Authentication credentials were not provided.')
        with self.subTest('other user credentials'):
            other_person_credentials = {'email': 'this.girl@gmail.com',
                                        'password': '23bbn'}
            token = get_jwt_token(self.client, other_person_credentials)

            response = self.client.patch(url, input_data,
                                         HTTP_AUTHORIZATION=f'JWT {token}')

            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
            data = response.data
            detail = data.get('detail')
            self.assertEqual(detail,
                             'You do not have permission to perform this '
                             'action.')
        with self.subTest('normal credentials'):
            person_credentials = {'email': 'some.guy@gmail.com',
                                  'password': 'aas1234'}
            token = get_jwt_token(self.client, person_credentials)

            response = self.client.patch(url, input_data,
                                         HTTP_AUTHORIZATION=f'JWT {token}')

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            data = response.data
            self.assertEqual(data.get('first_name'), 'Some')
            self.assertEqual(data.get('last_name'), 'Guy')
            user_response = self.client.get(url)
            user_profile = user_response.data.get('profile')
            self.assertIsNotNone(user_profile, "Profile can't be None")
            self.assertEqual(user_profile.get('country'), 'Germany')
            self.assertEqual(user_profile.get('city'), 'Berlin')

    def test_delete_user(self):
        user_id = 1
        url = reverse('user-detail', args=[user_id])
        with self.subTest('no credentials'):
            response = self.client.delete(url)
            self.assertEqual(response.status_code,
                             status.HTTP_401_UNAUTHORIZED)
            data = response.data
            detail = data.get('detail')
            self.assertEqual(detail,
                             'Authentication credentials were not provided.')
        with self.subTest('other user credentials'):
            other_person_credentials = {'email': 'this.girl@gmail.com',
                                        'password': '23bbn'}
            token = get_jwt_token(self.client, other_person_credentials)

            response = self.client.delete(url,
                                          HTTP_AUTHORIZATION=f'JWT {token}')

            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
            data = response.data
            detail = data.get('detail')
            self.assertEqual(detail,
                             'You do not have permission to perform this '
                             'action.')
        with self.subTest('normal credentials'):
            person_credentials = {'email': 'some.guy@gmail.com',
                                  'password': 'aas1234'}
            token = get_jwt_token(self.client, person_credentials)

            response = self.client.delete(url,
                                          HTTP_AUTHORIZATION=f'JWT {token}')

            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
            data = response.data
            self.assertIsNone(data, 'Data after deleting must be None')
            user_response = self.client.get(url)
            self.assertEqual(user_response.status_code,
                             status.HTTP_404_NOT_FOUND)
            data = user_response.data
            self.assertEqual(data.get('detail'), 'Not found.')

            users_url = reverse('user-list')
            response = self.client.get(users_url)
            data = response.data
            self.assertEqual(data.get('count'), 2)
            self.assertEqual(len(data.get('results')), 2)


class PostTests(APITestCase):
    fixtures = ['user.json', 'user_profile.json', 'post.json', 'like.json']

    def test_get_post(self):
        post_id = 1
        url = reverse('post-detail', args=[post_id])
        response = self.client.get(url)
        data = response.data
        with self.subTest('post data'):
            self.assertEqual(data.get('id'), 1)
            self.assertEqual(data.get('text'),
                             'Hello World! It is my first post. \nSome Guy')
            self.assertEqual(data.get('number_of_likes'), 1)
        with self.subTest('likes of post'):
            likes = data.get('likes')
            self.assertIsNotNone(likes, "Likes can't be None")
            self.assertEqual(len(likes), 1)
            with self.subTest('like url'):
                like_url = likes[0]
                like_response = self.client.get(like_url)
                like_data = like_response.data
                self.assertEqual(like_data.get('id'), 3)

    def test_get_posts(self):
        url = reverse('post-list')
        response = self.client.get(url)
        data = response.data
        results = data.get('results')
        self.assertIsNotNone(results, "Results can't be None")
        with self.subTest('number of posts'):
            self.assertEqual(data.get('count'), 5)
            self.assertEqual(len(results), 5)
        with self.subTest('post url'):
            post_url = results[0].get('url')
            self.assertIsNotNone(post_url, "Post URL can't be None")
            post_response = self.client.get(post_url)
            post_data = post_response.data
            self.assertEqual(post_data.get('id'), 1)

    def test_create_post(self):
        url = reverse('post-list')
        input_data = {'text': 'Test post'}
        person_credentials = {'email': 'some.guy@gmail.com',
                              'password': 'aas1234'}
        token = get_jwt_token(self.client, person_credentials)
        response = self.client.post(url, input_data,
                                    HTTP_AUTHORIZATION=f'JWT {token}')
        data = response.data
        with self.subTest('post data'):
            self.assertEqual(data.get('id'), 6)
            self.assertEqual(data.get('text'), 'Test post')
        with self.subTest('post owner'):
            owner_url = data.get('owner')
            self.assertIsNotNone(owner_url, "Owner URL can't be None")
            owner_response = self.client.get(owner_url)
            owner_data = owner_response.data
            self.assertEqual(owner_data.get('email'), 'some.guy@gmail.com')
        with self.subTest('number of posts'):
            response = self.client.get(url)
            data = response.data
            self.assertEqual(data.get('count'), 6)
            self.assertEqual(len(data.get('results')), 6)

    def test_update_post(self):
        post_id = 1
        url = reverse('post-detail', args=[post_id])
        input_data = {'text': 'New text'}
        with self.subTest('no credentials'):
            response = self.client.put(url, input_data)

            self.assertEqual(response.status_code,
                             status.HTTP_401_UNAUTHORIZED)
            data = response.data
            detail = data.get('detail')
            self.assertEqual(detail,
                             'Authentication credentials were not provided.')
        with self.subTest('other user credentials'):
            other_person_credentials = {'email': 'this.girl@gmail.com',
                                        'password': '23bbn'}
            token = get_jwt_token(self.client, other_person_credentials)

            response = self.client.put(url, input_data,
                                       HTTP_AUTHORIZATION=f'JWT {token}')

            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
            data = response.data
            detail = data.get('detail')
            self.assertEqual(detail,
                             'You do not have permission to perform this '
                             'action.')
        with self.subTest('normal credentials'):
            person_credentials = {'email': 'some.guy@gmail.com',
                                  'password': 'aas1234'}
            token = get_jwt_token(self.client, person_credentials)

            response = self.client.put(url, input_data,
                                       HTTP_AUTHORIZATION=f'JWT {token}')

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            data = response.data
            self.assertEqual(data.get('text'), 'New text')

    def test_partial_update(self):
        post_id = 1
        url = reverse('post-detail', args=[post_id])
        response = self.client.patch(url)
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)
        data = response.data
        self.assertEqual(data.get('detail'),
                         'Method "PATCH" not allowed.')

    def test_delete_post(self):
        post_id = 1
        url = reverse('post-detail', args=[post_id])
        with self.subTest('no credentials'):
            response = self.client.delete(url)
            self.assertEqual(response.status_code,
                             status.HTTP_401_UNAUTHORIZED)
            data = response.data
            detail = data.get('detail')
            self.assertEqual(detail,
                             'Authentication credentials were not provided.')
        with self.subTest('other user credentials'):
            other_person_credentials = {'email': 'this.girl@gmail.com',
                                        'password': '23bbn'}
            token = get_jwt_token(self.client, other_person_credentials)

            response = self.client.delete(url,
                                          HTTP_AUTHORIZATION=f'JWT {token}')

            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
            data = response.data
            detail = data.get('detail')
            self.assertEqual(detail,
                             'You do not have permission to perform this '
                             'action.')
        with self.subTest('normal credentials'):
            person_credentials = {'email': 'some.guy@gmail.com',
                                  'password': 'aas1234'}
            token = get_jwt_token(self.client, person_credentials)

            response = self.client.delete(url,
                                          HTTP_AUTHORIZATION=f'JWT {token}')

            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
            data = response.data
            self.assertIsNone(data, 'Data after deleting must be None')
            user_response = self.client.get(url)
            self.assertEqual(user_response.status_code,
                             status.HTTP_404_NOT_FOUND)
            data = user_response.data
            self.assertEqual(data.get('detail'), 'Not found.')

            posts_url = reverse('post-list')
            response = self.client.get(posts_url)
            data = response.data
            self.assertEqual(data.get('count'), 4)
            self.assertEqual(len(data.get('results')), 4)


class LikeTests(APITestCase):
    fixtures = ['user.json', 'user_profile.json', 'post.json', 'like.json']

    def test_get_like(self):
        like_id = 1
        url = reverse('like-detail', args=[like_id])
        response = self.client.get(url)
        data = response.data
        with self.subTest('like data'):
            self.assertEqual(data.get('id'), 1)
            self.assertEqual(data.get('is_liked'), True)
        with self.subTest('post data'):
            post_url = data.get('post')
            self.assertIsNotNone(post_url, "Post URL can't be None")
            post_response = self.client.get(post_url)
            post_data = post_response.data
            self.assertEqual(post_data.get('id'), 3)
        with self.subTest('owner data'):
            owner_url = data.get('owner')
            self.assertIsNotNone(owner_url, "Owner URL can't be None")
            owner_response = self.client.get(owner_url)
            owner_data = owner_response.data
            self.assertEqual(owner_data.get('id'), 1)

    def test_get_likes(self):
        url = reverse('like-list')
        response = self.client.get(url)
        data = response.data
        results = data.get('results')
        self.assertIsNotNone(results, "Results can't be None")
        with self.subTest('number of likes'):
            self.assertEqual(data.get('count'), 4)
            self.assertEqual(len(results), 4)
        with self.subTest('like url'):
            like_url = results[0].get('url')
            self.assertIsNotNone(like_url, "Like URL can't be None")
            like_response = self.client.get(like_url)
            like_data = like_response.data
            self.assertEqual(like_data.get('id'), 1)

    def test_create_like(self):
        url = reverse('like-list')
        input_data = {'post_id': 1}
        person_credentials = {'email': 'just.kid@gmail.com',
                              'password': '0o0o0o0'}
        token = get_jwt_token(self.client, person_credentials)
        response = self.client.post(url, input_data,
                                    HTTP_AUTHORIZATION=f'JWT {token}')
        data = response.data
        with self.subTest('like data'):
            self.assertEqual(data.get('id'), 5)
            self.assertEqual(data.get('is_liked'), False)
        with self.subTest('second like'):
            response_2 = self.client.post(url, input_data,
                                          HTTP_AUTHORIZATION=f'JWT {token}')
            data_2 = response_2.data
            self.assertEqual(data_2.get('id'), 6)
            self.assertEqual(data_2.get('is_liked'), True)
            # check number of likes
            post_url = data_2.get('post')
            self.assertIsNotNone(post_url, "Post URL can't be None")
            post_response = self.client.get(post_url)
            post_data = post_response.data
            self.assertEqual(post_data.get('number_of_likes'), 1)
        with self.subTest('post owner'):
            owner_url = data.get('owner')
            self.assertIsNotNone(owner_url, "Owner URL can't be None")
            owner_response = self.client.get(owner_url)
            owner_data = owner_response.data
            self.assertEqual(owner_data.get('email'), 'just.kid@gmail.com')

    def test_update_like(self):
        like_id = 1
        url = reverse('like-detail', args=[like_id])
        response = self.client.put(url)
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)
        data = response.data
        self.assertEqual(data.get('detail'),
                         'Method "PUT" not allowed.')

    def test_partial_update_like(self):
        like_id = 1
        url = reverse('like-detail', args=[like_id])
        response = self.client.patch(url)
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)
        data = response.data
        self.assertEqual(data.get('detail'),
                         'Method "PATCH" not allowed.')

    def test_delete_like(self):
        like_id = 1
        url = reverse('like-detail', args=[like_id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)
        data = response.data
        self.assertEqual(data.get('detail'),
                         'Method "DELETE" not allowed.')
