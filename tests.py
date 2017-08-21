import unittest
from unittest import mock
import requests

import api


github_followers = [
	{
		"login": "jezdez",
		"id": 1610,
		"avatar_url": "https://avatars0.githubusercontent.com/u/1610?v=4",
		"gravatar_id": "",
		"url": "https://api.github.com/users/jezdez",
		"html_url": "https://github.com/jezdez",
		"followers_url": "https://api.github.com/users/jezdez/followers",
		"following_url": "https://api.github.com/users/jezdez/following{/other_user}",
		"gists_url": "https://api.github.com/users/jezdez/gists{/gist_id}",
		"starred_url": "https://api.github.com/users/jezdez/starred{/owner}{/repo}",
		"subscriptions_url": "https://api.github.com/users/jezdez/subscriptions",
		"organizations_url": "https://api.github.com/users/jezdez/orgs",
		"repos_url": "https://api.github.com/users/jezdez/repos",
		"events_url": "https://api.github.com/users/jezdez/events{/privacy}",
		"received_events_url": "https://api.github.com/users/jezdez/received_events",
		"type": "User",
		"site_admin": False
	},
	{
		"login": "pagenoare",
		"id": 1623,
		"avatar_url": "https://avatars2.githubusercontent.com/u/1623?v=4",
		"gravatar_id": "",
		"url": "https://api.github.com/users/pagenoare",
		"html_url": "https://github.com/pagenoare",
		"followers_url": "https://api.github.com/users/pagenoare/followers",
		"following_url": "https://api.github.com/users/pagenoare/following{/other_user}",
		"gists_url": "https://api.github.com/users/pagenoare/gists{/gist_id}",
		"starred_url": "https://api.github.com/users/pagenoare/starred{/owner}{/repo}",
		"subscriptions_url": "https://api.github.com/users/pagenoare/subscriptions",
		"organizations_url": "https://api.github.com/users/pagenoare/orgs",
		"repos_url": "https://api.github.com/users/pagenoare/repos",
		"events_url": "https://api.github.com/users/pagenoare/events{/privacy}",
		"received_events_url": "https://api.github.com/users/pagenoare/received_events",
		"type": "User",
		"site_admin": False
	}
]

github_user_jezdez = {
	"login": "jezdez",
	"id": 1610,
	"avatar_url": "https://avatars0.githubusercontent.com/u/1610?v=4",
	"gravatar_id": "",
	"url": "https://api.github.com/users/jezdez",
	"html_url": "https://github.com/jezdez",
	"followers_url": "https://api.github.com/users/jezdez/followers",
	"following_url": "https://api.github.com/users/jezdez/following{/other_user}",
	"gists_url": "https://api.github.com/users/jezdez/gists{/gist_id}",
	"starred_url": "https://api.github.com/users/jezdez/starred{/owner}{/repo}",
	"subscriptions_url": "https://api.github.com/users/jezdez/subscriptions",
	"organizations_url": "https://api.github.com/users/jezdez/orgs",
	"repos_url": "https://api.github.com/users/jezdez/repos",
	"events_url": "https://api.github.com/users/jezdez/events{/privacy}",
	"received_events_url": "https://api.github.com/users/jezdez/received_events",
	"type": "User",
	"site_admin": False,
	"name": "Jannis Leidel",
	"company": "Mozilla",
	"blog": "https://twitter.com/jezdez",
	"location": None,
	"email": None,
	"hireable": None,
	"bio": "@mozilla software developer. @python & @django member, @jazzband roadie, @pypa alum. Writer of apps, opener of sources, handler of data",
	"public_repos": 50,
	"public_gists": 71,
	"followers": 1643,
	"following": 110,
	"created_at": "2008-02-28T16:00:34Z",
	"updated_at": "2017-08-17T09:50:24Z"
}

github_user_pagenoare = {
	"login": "pagenoare",
	"id": 1623,
	"avatar_url": "https://avatars2.githubusercontent.com/u/1623?v=4",
	"gravatar_id": "",
	"url": "https://api.github.com/users/pagenoare",
	"html_url": "https://github.com/pagenoare",
	"followers_url": "https://api.github.com/users/pagenoare/followers",
	"following_url": "https://api.github.com/users/pagenoare/following{/other_user}",
	"gists_url": "https://api.github.com/users/pagenoare/gists{/gist_id}",
	"starred_url": "https://api.github.com/users/pagenoare/starred{/owner}{/repo}",
	"subscriptions_url": "https://api.github.com/users/pagenoare/subscriptions",
	"organizations_url": "https://api.github.com/users/pagenoare/orgs",
	"repos_url": "https://api.github.com/users/pagenoare/repos",
	"events_url": "https://api.github.com/users/pagenoare/events{/privacy}",
	"received_events_url": "https://api.github.com/users/pagenoare/received_events",
	"type": "User",
	"site_admin": False,
	"name": "Kacper Krupa",
	"company": None,
	"blog": "http://pagenoare.net",
	"location": "Wrocław, Poland",
	"email": None,
	"hireable": None,
	"bio": None,
	"public_repos": 20,
	"public_gists": 33,
	"followers": 35,
	"following": 62,
	"created_at": "2008-02-28T17:24:46Z",
	"updated_at": "2017-08-14T19:08:58Z"
}


def mocked_requests_get(*args, **kwargs):
    if args[0] == 'https://api.github.com/users/jezdez':
        mock_response = mock.Mock()
        mock_response.json.return_value = github_user_jezdez
        return mock_response

    elif args[0] == 'https://api.github.com/users/pagenoare':
        mock_response = mock.Mock()
        mock_response.json.return_value = github_user_pagenoare
        return mock_response

    elif args[0] == 'https://api.github.com/users/mitsuhiko/followers':
        mock_response = mock.Mock()
        mock_response.json.return_value = github_followers
        return mock_response


class APITestCase(unittest.TestCase):

    def setUp(self):
        self.app = api.app

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_get_github_user(self, mock_get):
        with self.app.test_request_context():
            user = api.get_github_user('pagenoare')
            self.assertDictEqual(user, {'name': 'Kacper Krupa',
                                        'email': None,
                                        'location': 'Wrocław, Poland',
                                        'repos': 20})

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_get_github_followers(self, mock_get):
        with self.app.test_request_context():
            followers = api.get_github_followers('mitsuhiko')['data']
            self.assertIn({'name': 'Kacper Krupa', 'email': None,
                           'location': 'Wrocław, Poland', 'repos': 20}, followers)
            self.assertIn({'name': 'Jannis Leidel', 'email': None,
                           'location': None, 'repos': 50}, followers)


if __name__ == "__main__":
    unittest.main()
