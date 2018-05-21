"""
polygonAction_tests.py - unit tests for geoAction/polygonAction service
"""
import os
import sys
import json
import unittest
from flask_testing import TestCase

topdir = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(topdir)

from geoAction import app


class FlaskPolygonActionTests(unittest.TestCase):
    """ polygonAction Test Case class """

    @classmethod
    def setUpClass(cls):
        """ setUpClass """

        pass

    @classmethod
    def tearDownClass(cls):
        """ tearDownClass """

        pass

    def setUp(self):
        """ setUp """

        # creates a test client
        self.app = app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True

    def tearDown(self):
        """ tearDown """
        pass

    def test_invalid_action(self):
        """ Test for invalid action """

        response = self.app.post(
            '/polygonAction/invalidAction',
            content_type='application/json'
        )
        assert response.status_code == 501

    def test_no_json(self):
        """ Test for no json in POST """
        response = self.app.post(
            '/polygonAction/intersection',
            content_type='application/json'
        )
        assert response.status_code == 400

    def test_invalid_json(self):
        """ Test for invalid json in POST """

        json = 'Not valid JSON data'
        response = self.app.post(
            '/polygonAction/intersection',
            content_type='application/json',
            data=json
        )
        assert response.status_code == 400

    def test_invalid_geojson(self):
        """ Test for invalid geojson in POST """

        response = self.app.post(
            '/polygonAction/intersection',
            content_type='application/json',
            data=self.get_json_data("fixtures/invalidGeo.json")
        )
        assert response.status_code == 400

    def test_invalid_polygon_pair(self):
        """ Test for invalid polygon pair in geojson """

        response = self.app.post(
            '/polygonAction/intersection',
            content_type='application/json',
            data=self.get_json_data("fixtures/validPolygon.json")
        )
        assert response.status_code == 400

    def test_invalid_polygon_pair_v2(self):
        """ Test for invalid polygon pair in geojson, other features """

        response = self.app.post(
            '/polygonAction/intersection',
            content_type='application/json',
            data=self.get_json_data("fixtures/validLinePolygon.json")
        )
        assert response.status_code == 400

    def test_valid_polygon_pair_intersection(self):
        """ Test for valid polygon pair intersection """

        response = self.app.post(
            '/polygonAction/intersection',
            content_type='application/json',
            data=self.get_json_data("fixtures/validPolygonPair.json")
        )
        geoJson = json.loads(response.data.decode('utf8'))
        assert response.status_code == 200
        assert geoJson['operation'] == 'intersection'

    def test_valid_polygon_pair_union(self):
        """ Test for valid polygon pair union """

        response = self.app.post(
            '/polygonAction/union',
            content_type='application/json',
            data=self.get_json_data("fixtures/validPolygonPair.json")
        )
        geoJson = json.loads(response.data.decode('utf8'))
        assert response.status_code == 200
        assert geoJson['operation'] == 'union'

    def test_valid_polygon_pair_no_intersection(self):
        """ Test for valid polygon pair, but no intersection """

        response = self.app.post(
            '/polygonAction/intersection',
            content_type='application/json',
            data=self.get_json_data(
                "fixtures/validPolygonPairNoIntersection.json"
            )
        )
        assert response.status_code == 204

    def test_valid_polygon_pair_no_union(self):
        """ Test for valid polygon pair, but no union """

        response = self.app.post(
            '/polygonAction/union',
            content_type='application/json',
            data=self.get_json_data(
                "fixtures/validPolygonPairNoIntersection.json"
            )
        )
        assert response.status_code == 204

    def get_json_data(self, filename):
        """ read json from file to string """

        return(json.dumps(json.load(open(filename, "r"))))


if __name__ == "__main__":
    unittest.main()
