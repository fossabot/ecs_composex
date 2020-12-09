﻿#  -*- coding: utf-8 -*-
#   ECS ComposeX <https://github.com/lambda-my-aws/ecs_composex>
#   Copyright (C) 2020  John Mille <john@lambda-my-aws.io>
#  #
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#  #
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#  #
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Module to import CFN Resources defined by their properties
"""

from inspect import isfunction
from troposphere import AWSProperty

from ecs_composex.common import keypresent, keyisset


def handle_list(properties, property_class):
    """
    Function to handle list properties

    :param property_class:
    :param properties:
    :return:
    """
    rendered_properties = []
    for property_definition in properties:
        if not isinstance(property_definition, (str, int, float, bool)):
            record = import_record_properties(property_definition, property_class)
            rendered_properties.append(property_class(**record))
        else:
            rendered_properties.append(property_definition)
    return rendered_properties


def import_non_functions(props, prop_name, top_class, properties, set_to_novalue):
    """
    Function to set property for flat object or recursive to sub properties

    :param dict props:
    :param str prop_name:
    :param top_class:
    :param dict properties:
    :param bool set_to_novalue:
    """
    if isinstance(properties[prop_name], (str, int, float, tuple)) or top_class.props[
        prop_name
    ][0] in (str, int, float):
        if top_class.props[prop_name][0] in (str, int, float):
            props[prop_name] = top_class.props[prop_name][0](properties[prop_name])
        else:
            props[prop_name] = properties[prop_name]
    elif isinstance(properties[prop_name], dict):
        try:
            if issubclass(top_class.props[prop_name][0], AWSProperty):
                sub_props = import_record_properties(
                    properties[prop_name],
                    top_class.props[prop_name][0],
                    set_to_novalue,
                    ignore_missing_required=False,
                )
                props[prop_name] = top_class.props[prop_name][0](**sub_props)
            else:
                props[prop_name] = properties[prop_name]
        except TypeError:
            props[prop_name] = properties[prop_name]


def import_record_properties(
    properties, top_class, set_to_novalue=False, ignore_missing_required=True
):
    """
    Generic function importing the RecordSet properties.
    If the property was not defined, it is either left empty or set to AWS::NoValue
    For inner recursive, we enforce check on required properties.

    :param dict properties:
    :param top_class: The class we are going to import properties for
    :param bool set_to_novalue: Instead of skipping the property, actively set to AWS::NoValue
    :param bool ignore_missing_required: Whether or not raise an error when missing an essential key.
    :return:  The properties for the RecordSet
    :rtype: dict
    """
    props = {}
    for prop_name in top_class.props:
        if not keypresent(prop_name, properties) and not top_class.props[prop_name][1]:
            continue
        elif (
            not keypresent(prop_name, properties)
            and top_class.props[prop_name][1]
            and not ignore_missing_required
        ):
            raise KeyError(
                f"Property {prop_name} is required for the definition of {top_class}"
            )
        elif keyisset(prop_name, properties) and isinstance(
            top_class.props[prop_name][0], list
        ):
            props[prop_name] = handle_list(
                properties[prop_name], top_class.props[prop_name][0][0]
            )
        elif keypresent(prop_name, properties) and isfunction(
            top_class.props[prop_name][0]
        ):
            props[prop_name] = properties[prop_name]
        elif keypresent(prop_name, properties) and not isfunction(
            properties[prop_name]
        ):
            import_non_functions(
                props, prop_name, top_class, properties, set_to_novalue
            )
        elif keypresent(prop_name, properties):
            props[prop_name] = properties[prop_name]
    return props
