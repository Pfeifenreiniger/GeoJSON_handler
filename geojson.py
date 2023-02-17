
import json
import os
import time

class GeoJSON:
    """class to im- and export GeoJSON file(s)"""

    """---------CONSTRUCTOR---------"""
    def __init__(self,
                 data=None,
                 feature_collection:bool=None,
                 properties_names=None,
                 input_file_path:str=None,
                 output_file_path:str=None,
                 output_file_name:str=None):
        """data param can be a list or tuple with GeoJSON like formatted dictionaries or a single such dictionary itself."""

        self.__json_geometry_types = ["Point", "LineString", "Polygon", "MultiPoint", "MultiLineString", "MultiPolygon"]

        if data != None:
            self.set_data(data)

        if feature_collection != None:
            self.set_feature_collection(feature_collection)

        if properties_names != None:
            self.set_properties_names(properties_names)

        if input_file_path != None:
            self.set_input_file_path(input_file_path)

        if output_file_path != None:
            self.set_output_file_path(output_file_path)
        if output_file_name != None:
            self.set_output_file_name(output_file_name)

    """---------METHODS---------"""

    def __check_dictionary_formatting(self, dic:dict) -> bool:

        def check_feature(dic:dict) -> bool:

            if dic.get("geometry", False):
                if isinstance(dic["geometry"], dict):
                    if dic["geometry"].get("type", False):
                        if dic["geometry"]["type"] in self.__json_geometry_types:
                            if dic["geometry"].get("coordinates", False):
                                if isinstance(dic["geometry"]["coordinates"], list):
                                    coords = dic["geometry"]["coordinates"]
                                    if len(coords) == 2:
                                        if not type(coords[0]) == float and not type(coords[1]) == float:
                                            return False
                                    else:
                                        return False
                                    if dic.get("properties", False):
                                        if isinstance(dic["properties"], dict):
                                            for key, value in dic["properties"].items():
                                                if isinstance(key, str):
                                                    while isinstance(value, dict):
                                                        to_check = [value.items()]
                                                        for k_v_pair in to_check:
                                                            for k, v in k_v_pair:
                                                                if isinstance(k, str):
                                                                    if isinstance(v, dict):
                                                                        value = v
                                                                        to_check.append(value.items())
                                                                    else:
                                                                        value = None
                                                                else:
                                                                    return False
                                                    return True # feature is correctly formatted
                                                else:
                                                    return False
                                        else:
                                            return False
                                    else:
                                        return False
                                else:
                                    return False
                            else:
                                return False
                        else:
                            return False
                    else:
                        return False
                else:
                    return False
            else:
                return False

        def check_dictionary(dic:dict) -> bool:

            if dic.get("type", False):
                if dic["type"] == "Feature":
                    if check_feature(dic):
                        return True
                    else:
                        return False
                elif dic["type"] == "FeatureCollection":
                    if dic.get("features", False):
                        if isinstance(dic["features"], list):
                            for feature in dic["features"]:
                                if isinstance(feature, dict):
                                    if check_feature(feature):
                                        return True
                                    else:
                                        return False
                                else:
                                    return False
                        else:
                            return False
                    else:
                        return False
                else:
                    return False
            else:
                return False

        if check_dictionary(dic):
            # dictionary correctly formatted as GeoJSON
            return True
        else:
            # not correctly formatted
            return False


    def __check_data_for_export(self):

        if isinstance(self._data, list) or isinstance(self._data, tuple): # handling of list/tuple of dictionaries
            for dic in self._data:

                if self.__check_dictionary_formatting(dic):
                    formatted_dict = dic
                else:
                    formatted_dict = self.__format_as_geojson(dic)
                self.__save_geojson_file(formatted_data=formatted_dict)
                time.sleep(0.5)

        else: # handling of single dictionary
            formatted_dict = self.__format_as_geojson(self._data)
            self.__save_geojson_file(formatted_data=formatted_dict)

    def __format_as_geojson(self, dic) -> dict:

        def check_dictionary_for_values(dic):
            for key, value in dic.items():

                while isinstance(value, dict):
                    to_check = [value.items()]
                    for k_v_pair in to_check:
                        for k, v in k_v_pair:
                            if isinstance(v, dict):
                                value = v
                                to_check.append(value.items())
                            else:
                                value = v
                                get_values(k, value)


                get_values(key, value)

        def get_values(key, value):
            # geometry type
            if value in self.__json_geometry_types:
                self.__geometry_type = value
            elif key in self.__json_geometry_types:
                self.__geometry_type = key

            # coordinates
            is_coords = None
            if isinstance(value, list):
                if len(value) > 0:
                    for elem in value:
                        if is_coords != None and not is_coords:
                            break
                        if isinstance(elem, list):
                            if len(elem) == 2:
                                if isinstance(elem[0], float) and isinstance(elem[1], float):
                                    is_coords = True
                                else:
                                    is_coords = False
                                    break
                            else:
                                is_coords = False
                        else:
                            is_coords = False
                else:
                    is_coords = False
            else:
                is_coords = False
            if is_coords:
                self.__coordinates = value

            # properties
            if key in self.__properties.keys():
                self.__properties[key] = value

        self.__geometry_type = None
        self.__coordinates = None
        self.__properties = {}

        if hasattr(self, '_property_name'):
            self.__properties[self._property_name] = None
        elif hasattr(self, '_properties_names'):
            for prop in self._properties_names:
                self.__properties[prop] = None

        if self._feature_collection:
            geojson = {
                        "type": "FeatureCollection",
                        "features": []
                        }

            for key, value in dic.items():
                check_dictionary_for_values({key : value})
                if self.__geometry_type != None and self.__coordinates != None:
                    geojson["features"].append({
                        "type": "Feature",
                        "geometry": {
                            "type": self.__geometry_type,
                            "coordinates": self.__coordinates
                        },
                        "properties": self.__properties
                    })
                else:
                    raise Exception("Cound not convert dictionary into GeoJSON format. Not all necessary information are included.")

        else:
            geojson = {
                        "type": "Feature",
                        "geometry": {},
                        "properties": {}
                        }

            check_dictionary_for_values(dic)
            if self.__geometry_type != None and self.__coordinates != None:
                geojson["geometry"]["type"] = self.__geometry_type
                geojson["geometry"]["coordinates"] = self.__coordinates
                geojson["properties"] = self.__properties
            else:
                raise Exception("Cound not convert dictionary into GeoJSON format. Not all necessary information are included.")

        return geojson


    def __save_geojson_file(self, formatted_data):

        # checks if attributes of file path and name are set
        if hasattr(self, '_output_file_path') and hasattr(self, '_output_file_name'):

            # if necessary, adjusts file name by adding a number at its end
            present_files = os.listdir(self._output_file_path)
            counter = 0
            for file in present_files:
                if file.endswith(".json"):
                    file = file[:file.index(".json")]
                    if file[-1].isnumeric():
                        file = file[:-2]
                    if self._output_file_name[:self._output_file_name.index(".json")] == file:
                        counter += 1

            if counter > 0:
                output_file_name = self._output_file_name[:self._output_file_name.index(".json")] + f"_{counter}" + ".json"
            else:
                output_file_name = self._output_file_name

            # save the data as file
            with open(self._output_file_path + "/" + output_file_name, "w") as file:
                json.dump(formatted_data, file)

        else:
            raise Exception("Attribute 'output_file_path' or 'output_file_name' is missing. Set values.")

    def input_geojson_to_dict(self, input_file_path=None) -> dict:
        """Returns a Python dictionary from a GeoJSON file"""
        if hasattr(self, '_import_file_path') or input_file_path != None:
            if input_file_path != None:
                self.set_input_file_path(input_file_path)
            with open(self._input_file_path, "r") as file:
                temp_content = file.read()
                dic = json.loads(temp_content)
            if not self.__check_dictionary_formatting(dic):
                raise Exception("JSON file is not formatted as GeoJSON.")
            else:
                return dic
        else:
            raise Exception("Attribute 'import_file_path' not set.")

    def export_as_geojson(self,
                          data=None,
                          feature_collection:bool=None,
                          properties_names=None,
                          output_file_path:str=None,
                          output_file_name:str=None):
        """Exports a python dictionary as a GeoJSON file.
        Needs data to handle with, specification if data is a collection of features, the names of the including properties
        and finally the output file path and file name where the file will be saved."""
        if data != None:
            self.set_data(data)
        if feature_collection!= None:
            self.set_feature_collection(feature_collection)
        if properties_names != None:
            self.set_properties_names(properties_names)
        if output_file_path != None:
            self.set_output_file_path(output_file_path)
        if output_file_name != None:
            self.set_output_file_name(output_file_name)

        if hasattr(self, '_data') and hasattr(self, '_feature_collection')\
                and (hasattr(self, 'properties_names') or hasattr(self, '_property_name'))\
                and hasattr(self, '_output_file_path') and hasattr(self, '_output_file_name'):
            self.__check_data_for_export()
        else:
            raise Exception("Necessary attributes like data, feature_collection, etc are missing. Please add to object or pass as argument.")

    """---------GETTERS AND SETTERS---------"""
    def get_data(self):
        return self._data

    def set_data(self, data):
        """data can only be set if iterable object list/tuple or a single dictionary"""
        if isinstance(data, list) or isinstance(data, tuple):
            if len(data) < 1:
                raise Exception("Iterable object is empty.")

            for ele in data:
                if not isinstance(ele, dict):
                    raise Exception(f"Iterable object (list or tuple) data does not contain dictionary data type data. Got {type(ele)} instead.")
            self._data = data

        elif isinstance(data, dict):
            self._data = data
        else:
            raise Exception(f"Passed data is not supported. Expected a list/tuple with dictionaries or a single dictionary; got {type(data)} instead.")

    def is_feature_collection(self) -> bool:
        return self._feature_collection

    def set_feature_collection(self, feature_collection:bool):
        if isinstance(feature_collection, bool):
            self._feature_collection = feature_collection
        else:
            raise Exception(f"For feature_collection expected bool, got {type(feature_collection)} instead.")


    def get_properties_names(self):
        if hasattr(self, '_property_name'):
            return self._property_name
        elif hasattr(self, '_properties_names'):
            return self._properties_names
        else:
            raise Exception("No property related attribute found")

    def set_properties_names(self, properties_names):
        if isinstance(properties_names, str): # a single property name
            self._property_name = properties_names

        elif isinstance(properties_names, list) or isinstance(properties_names, tuple): # multiple property names

            for prop in properties_names:
                if not isinstance(prop, str):
                    raise Exception(f"Expected list/tuple of strings as data type for property names, got {type(prop)} element inside instead.")

            self._properties_names = properties_names
        else:
            raise Exception(f"No supported data type. Expected list/tuple with strings or single string, got {type(properties_names)} instead.")

    def del_properties_names(self):

        if not hasattr(self, '_property_name') and not hasattr(self, '_properties_names'):
            raise Exception("No attribute present to delete")

        if hasattr(self, '_property_name'):
            del self._property_name
        if hasattr(self, '_properties_names'):
            del self._properties_names

    def get_input_file_path(self) -> str:
        return self._input_file_path

    def set_input_file_path(self, input_file_path:str):
        if isinstance(input_file_path, str):
            if input_file_path.endswith(".json"):
                self._input_file_path = input_file_path
            else:
                raise Exception("File path should lead to a .json file (file-extension must be part of the path).")
        else:
            raise Exception(f"Parameter input_file_path needs a string argument; got {type(input_file_path)} instead.")

    def get_output_file_path(self) -> str:
        return self._output_file_path

    def set_output_file_path(self, output_file_path:str):
        if isinstance(output_file_path, str):
            self._output_file_path = output_file_path
        else:
            raise Exception(f"Parameter output_file_path needs a string argument; got {type(output_file_path)} instead.")

    def get_output_file_name(self) -> str:
        return self._output_file_name

    def set_output_file_name(self, output_file_name:str):
        if isinstance(output_file_name, str):
            self._output_file_name = output_file_name if output_file_name.endswith(".json") else output_file_name + ".json"
        else:
            raise Exception(f"Parameter output_file_name needs a string argument; got {type(output_file_name)} instead.")

    ## ATTRIBUTES AS PROPERTY ATTRIBUTES ##
    data = property(get_data, set_data)
    features_collection = property(is_feature_collection, set_feature_collection)
    properties_names = property(get_properties_names, set_properties_names, del_properties_names)
    input_file_path = property(get_input_file_path, set_input_file_path)
    output_file_path = property(get_output_file_path, set_output_file_path)
    output_file_name = property(get_output_file_name, set_output_file_name)

