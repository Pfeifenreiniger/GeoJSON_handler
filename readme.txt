Vers. 0.1 (2023-02-17)
______________

A class to handle GeoJSON files.

Python dictionaries can be casted into the correct GeoJSON formatting and finally be exported,
or you can import GeoJSON files as python dictionaries.

______________

**Python dictionary to GeoJSON file:**
example:

	from geojson import GeoJSON
	
	geo_json = GeoJSON()
	
	sample_dict = {
	    "type": "Point",
	    "coordinates": [[102.0, 0.5]],
	    "properties" : {
	        "name": "someWhere",
	        "city": "exampleVille"
	    }
	}
	
	output_path = "C:/Users/<USERNAME>/<FOLDER1>/<FOLDER2>/"
	file_name = "test"
	
	geo_json.export_as_geojson(data=sample_dict,
				feature_collection=False,
				properties_names=["name", "city"],
				output_file_path=output_path,
				output_file_name=file_name)

**GeoJSON file to Python dictionary**
example:

	from geojson import GeoJSON
	
	sample_json = "C:/Users/<USERNAME>/<FOLDER>/<FILE>.json"
	
	geo_json = GeoJSON()
	
	dictionary = geo_json.input_geojson_to_dict(sample_json)


______________

Attributes such as data, feature_collection, properties_names, input_file_path, output_file_path, and output_file_name can be
passed as arguments either during instancing object or in the method signature.

