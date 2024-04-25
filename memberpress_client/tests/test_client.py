from unittest import TestCase
from unittest.mock import patch

from django.core.cache import cache

from memberpress_client.client import MemberpressAPIClient


class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data

    def raise_for_status(self):
        pass


class TestClient(TestCase):

    def setUp(self):
        cache.clear()

    @patch("memberpress_client.client.requests.patch", return_value=MockResponse({"foo": "bar"}, 200))
    @patch("memberpress_client.client.requests.post", return_value=MockResponse({"foo": "bar"}, 200))
    @patch("memberpress_client.client.requests.get", return_value=MockResponse({"foo": "bar"}, 200))
    def test_response_caching(self, mock_get, mock_post, mock_patch):
        client = MemberpressAPIClient()
        assert mock_get.call_count == 0
        # first call should make a request
        client.get("test")
        assert mock_get.call_count == 1
        # second call should retrieve from cache
        client.get("test")
        assert mock_get.call_count == 1
        # first call with params should make a request
        client.get("test", params={"param_1": "value_1"})
        assert mock_get.call_count == 2
        # second call with params should retrieve from cache
        client.get("test", params={"param_1": "value_1"})
        assert mock_get.call_count == 2
        # first call with multiple params should make a request
        client.get("test", params={"param_1": "value_1", "param_2": "value_2"})
        assert mock_get.call_count == 3
        # second call with params out of order should still retrieve from cache
        client.get("test", params={"param_2": "value_2", "param_1": "value_1"})
        assert mock_get.call_count == 3
        # third call with same params but different values should make a request
        client.get("test", params={"param_1": "value_1", "param_2": "value_3"})
        assert mock_get.call_count == 4
        # call again with same params but caching disabled should make a request
        client.get("test", params={"param_1": "value_1", "param_2": "value_3"}, enable_caching=False)
        assert mock_get.call_count == 5
        client.post("test-post", {"input": "post data"})
        mock_post.assert_called_with(
            client.get_url("test-post"),
            data={"input": "post data"},
            headers=client.headers
        )
        client.patch("test-patch", {"input": "patch data"})
        mock_patch.assert_called_with(
            client.get_url("test-patch"),
            json={"input": "patch data"},
            headers=client.headers
        )
