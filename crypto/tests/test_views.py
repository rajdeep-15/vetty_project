import unittest
from unittest.mock import patch
from django.core.cache import cache
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status


class CoinViewsTestCase(TestCase):
    """Test cases for CoinListView, CoinCategoryView, and CoinDataView"""

    def setUp(self):
        """Set up test client and test data."""
        self.client = Client()
        self.coin_list_url = reverse("coins-list")
        self.coin_category_url = reverse("coins-by-category")
        self.coin_data_url = reverse("coins-market-data")

        self.mock_coin_list = [
            {"id": "bitcoin", "symbol": "btc", "name": "Bitcoin"},
            {"id": "ethereum", "symbol": "eth", "name": "Ethereum"},
        ]

        self.mock_coin_category = [
            {"id": "defi", "name": "DeFi"},
            {"id": "nft", "name": "NFT"},
        ]

        self.mock_coin_data = [
            {"id": "bitcoin", "current_price": 45000, "market_cap": 850000000},
            {"id": "ethereum", "current_price": 3000, "market_cap": 350000000},
        ]

    def tearDown(self):
        """Clear the cache after each test."""
        cache.clear()

    @patch("crypto.views.CoinListView.get_data_from_gecko")
    def test_coin_list_view_success(self, mock_get_data):
        """Test successful retrieval of coin list with caching."""
        mock_get_data.return_value = self.mock_coin_list

        response = self.client.get(self.coin_list_url, {"page_size": 2, "page_number": 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.json())  
        self.assertEqual(len(response.json()["results"]), 2)

    @patch("crypto.views.CoinListView.get_data_from_gecko")
    def test_coin_list_view_failure(self, mock_get_data):
        """Test when the external API fails to return data."""
        mock_get_data.return_value = None

        response = self.client.get(self.coin_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"error": "Could not fetch any data from the provider."})

    @patch("crypto.views.CoinCategoryView.get_data_from_gecko")
    def test_coin_category_view_success(self, mock_get_data):
        """Test successful retrieval of coin categories with caching."""
        mock_get_data.return_value = self.mock_coin_category

        response = self.client.get(self.coin_category_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.json())  
        self.assertEqual(len(response.json()["results"]), 2)

    @patch("crypto.views.CoinCategoryView.get_data_from_gecko")
    def test_coin_category_view_failure(self, mock_get_data):
        """Test when the external API fails to return category data."""
        mock_get_data.return_value = None

        response = self.client.get(self.coin_category_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"error": "Could not fetch any data from the provider."})

    @patch("crypto.views.CoinDataView.get_data_from_gecko")
    def test_coin_data_view_with_ids(self, mock_get_data):
        """Test successful retrieval of coin data by IDs."""
        mock_get_data.return_value = self.mock_coin_data

        response = self.client.get(self.coin_data_url, {"ids": "bitcoin,ethereum"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)

    @patch("crypto.views.CoinDataView.get_data_from_gecko")
    def test_coin_data_view_with_category(self, mock_get_data):
        """Test successful retrieval of coin data by category."""
        mock_get_data.return_value = self.mock_coin_data

        response = self.client.get(self.coin_data_url, {"category": "defi"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)

    @patch("crypto.views.CoinDataView.get_data_from_gecko")
    def test_coin_data_view_failure(self, mock_get_data):
        """Test when the external API fails to return coin market data."""
        mock_get_data.return_value = None

        response = self.client.get(self.coin_data_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"error": "Could not fetch any data from the provider."})


if __name__ == "__main__":
    unittest.main()
