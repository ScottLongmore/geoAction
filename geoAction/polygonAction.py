# -*- coding: utf-8 -*-
"""
Provides geoJSON transformation services

Services
--------
polygon_action - creates geoJSON intersection or union polygon from geoJSON polygon pair

"""

__author__ = 'Scott Longmore'
__version__ = '0.1dev1'
__maintainer__ = 'Scott Longmore'
__email__ = 'scott.longmore@gmail.com'

from geoAction import app

# System Modules
from flask import Flask, request, jsonify, make_response
import json
import geojson
from shapely.geometry import Polygon
from shapely.geometry import mapping
import traceback

@app.route('/polygonAction/<action>', methods=['POST'])
def polygon_action(action):
    """
    Preforms transformation on geoJSON polygon geometry objects

    Parameters
    ----------
    action : 'intersection' or 'union'
    geoJson : FeatureCollection containing two polygon features

    Returns
    -------
    geoJson : 'intersection' or 'union' feature with request attribute,
               json object with error attribute on exception
    """

    # Determine if valid geojson action
    actions = ['intersection', 'union']
    if action not in actions:
        return(not_implemented("{} action not supported".format(action)))

    # Validate geoJson polygon pair within features
    try:
        geoJson = __validate_geojson_request()
    except Exception, e:
        # traceback.print_exc()
        return(bad_request("geoJSON validation problem: {}".format(e)))

    # Convert geoJSON polygon pair to shapely polygon pair
    try:
        poly0 = Polygon(geojson.utils.coords(geoJson['features'][0]))
        poly1 = Polygon(geojson.utils.coords(geoJson['features'][1]))
    except Exception, e:
        # traceback.print_exc()
        return(internal_server("Problem extracting polygons: {}".format(e)))

    # Perform action on polygon pair
    polyAction=None
    try:
        if action == 'intersection':
            polyAction = poly0.intersection(poly1)
        else:
            polyAction = poly0.union(poly1)

    except Exception, e:
        # traceback.print_exc()
        return(
            internal_server(
                "Problem processing geoJSON action: {}".format(e)
            )
        )

    # Convert shapely polygon action to geoJSON, with request action attribute
    try:
        geoJson = geojson.Feature(geometry=mapping(polyAction))
        if geoJson['geometry']['type'] is 'Polygon':
             geoJson["operation"] = action
             return jsonify(geoJson)
        else:
             return(
                 make_response("no intersection or union between polygons",204)
             )
  
    except Exception, e:
        # traceback.print_exc()
        return(
            internal_server(
                "Problem converting shape polygon to geoJSON".format(e)
            )
        )


def __validate_geojson_request():
    """
    Validates POST request with geoJSON feature colleciton with
    two polygon features

    Parameters
    ----------
    request : global Flask request object

    Returns
    -------
    geoJson : validated geoJSON feature collection with two polygon features,
              raises exceptions on error
    """

    data = None
    if request.is_json:
        data = request.get_json()
    else:
        raise ValueError('Not valid JSON')

    geoJson = geojson.loads(json.dumps(data))
    if geoJson.is_valid:
        if len(geoJson["features"]) == 2:
            if all(
                d['geometry']['type'] == "Polygon" for d in geoJson["features"]
            ):
                return(geoJson)
            else:
                raise ValueError('One or more features is not a polygon')
        else:
            raise ValueError('Exactly two geoJson features not found')
    else:
        raise ValueError('Not valid GeoJSON')


@app.errorhandler(400)
def bad_request(error):
    """
    Bad Request (400) error handler routine

    Parameters
    ----------
    error : error message

    Returns
    -------
    response : response object with JSON error attribute

    """
    message = "Bad Request: {}\n".format(error)
    return make_response(jsonify({'error': message}), 400)


@app.errorhandler(500)
def internal_server(error):
    """
    Internal Server Error (500) error handler routine

    Parameters
    ----------
    error : error message

    Returns
    -------
    response : response object with JSON error attribute

    """
    message = "Internal Server Error: {}\n".format(error)
    return make_response(jsonify({'error': message}), 500)


@app.errorhandler(501)
def not_implemented(error):
    """
    Not Implemented Error (501) error handler routine

    Parameters
    ----------
    error : error message

    Returns
    -------
    response : response object with JSON error attribute

    """
    message = "Not Implemented: {}\n".format(error)
    return make_response(jsonify({'error': message}), 501)


if __name__ == '__main__':
    app.run(debug=True, port=5000)  # Run app in debug mode on port 5000
