import os
from dotenv import load_dotenv
from flask.views import MethodView
import google.cloud.dialogflow_v2 as dialogflow
from pathlib import Path
from flask import request, jsonify

dir_path = str(Path(__file__).parent.parent.parent)
cred_path = dir_path + '/config/ava-existing-customer-v2.json'
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = cred_path
load_dotenv(dir_path + "/.env")
project_id = os.getenv('project_id')
global_entity_list = []


class ManageEntities(MethodView):

    def get_entity_data(self, entity_type):
        tokenize_entity_uuid = entity_type.name.split('/')[-1]
        kind = entity_type.kind

        entities_list = []

        for entity in entity_type.entities:
            synonyms_list = []
            for synonym in entity.synonyms:
                synonyms_list.append(synonym)
            entities_list.append({"value": entity.value, "synonyms": synonyms_list})

        json_dict = dict(uiid=tokenize_entity_uuid, kind=kind,
                         display_name=entity_type.display_name, entities_list=entities_list)
        return json_dict

    def get(self, entity_uuid=None):
        try:
            print("Manage Entities get method api is called")
            global global_entity_list
            entity_type_client = dialogflow.EntityTypesClient()
            parent = dialogflow.AgentsClient.agent_path(project_id)

            entity_types = entity_type_client.list_entity_types(parent=parent)
            entity_type_to_find = None
            entity_type_to_find_uuid = entity_uuid

            i = 0
            if entity_uuid is None and len(global_entity_list) <= 0:
                for entity_type in entity_types:
                    i += 1
                    entity_info = self.get_entity_data(entity_type)
                    global_entity_list.append(entity_info)
                return jsonify(global_entity_list)

            elif entity_uuid is None and len(global_entity_list) > 0:
                return jsonify(global_entity_list)

            else:

                print("simple", entity_uuid)
                if len(global_entity_list) <= 0:
                    for entity_type in entity_types:
                        entity_info = self.get_entity_data(entity_type)
                        global_entity_list.append(entity_info)
                for entity_info in global_entity_list:
                    if entity_type_to_find_uuid == entity_info["uiid"]:
                        return jsonify(entity_info)
                return jsonify({"error_code": 1, "message": "entity does not exists"})
        except Exception as e:
            print(e)
            return str(e)

    def post(self):
        try:
            global global_entity_list
            entity_info = request.get_json(force=True)
            entity_display_name = entity_info['display_name']
            entities_list = entity_info['entities_list']

            entity_list = []
            for entity in entities_list:
                value = entity["value"]
                print(value)
                synonyms = []
                synonym_list = entity["synonyms"]
                print(synonym_list)
                for synonym in synonym_list:
                    synonyms.append(synonym)
                entity_to_add = dialogflow.types.EntityType.Entity(value=value, synonyms=synonyms)
                entity_list.append(entity_to_add)

            entity_types_client = dialogflow.EntityTypesClient()
            parent = dialogflow.AgentsClient.agent_path(project_id)
            entity_type = dialogflow.types.EntityType(display_name=entity_display_name, kind=1, entities=entity_list)
            response = entity_types_client.create_entity_type(parent=parent, entity_type=entity_type)
            global_entity_list.append(self.get_entity_data(response))
            print('Entity type created: \n{}'.format(response))
            return jsonify({"error_code": 0, "message": "entity is created successfully"})
        except Exception as e:
            print(e)
            return jsonify({"error_code": 1, "message": str(e)})

    def put(self):
        try:
            global global_entity_list
            entity_info = request.get_json(force=True)
            entity_uiid = entity_info['uiid']
            entity_display_name = entity_info['display_name']
            entities_list = entity_info['entities_list']

            entity_list = []
            for entity in entities_list:
                value = entity["value"]
                # print(value)
                synonyms = []
                synonym_list = entity["synonyms"]
                # print(synonym_list)
                for synonym in synonym_list:
                    synonyms.append(synonym)
                entity_to_add = dialogflow.types.EntityType.Entity(value=value, synonyms=synonyms)
                entity_list.append(entity_to_add)

            entity_types_client = dialogflow.EntityTypesClient()
            parent = dialogflow.AgentsClient.agent_path(project_id)

            name = "projects/" + project_id + "/agent/entityTypes/" + entity_uiid
            entity_type = dialogflow.types.EntityType(name=name, display_name=entity_display_name, kind=1,
                                                      entities=entity_list)
            response = entity_types_client.update_entity_type(entity_type=entity_type)

            updated_entity_uuid = response.name.split('/')[-1]

            for i, entity in enumerate(global_entity_list):
                if entity["uiid"] == updated_entity_uuid:
                    global_entity_list.pop(i)
                    global_entity_list.insert(i, self.get_entity_data(response))
                    break
            print('Entity type updated: \n{}'.format(response))
            return jsonify({"error_code": 0, "message": "entity is updated successfully"})
        except Exception as e:
            print(e)
            return jsonify({"error_code": 1, "message": str(e)})

    def delete(self, entity_uuid=None):
        try:
            global global_entity_list
            entity_types_client = dialogflow.EntityTypesClient()
            name = "projects/" + project_id + "/agent/entityTypes/" + entity_uuid
            response = entity_types_client.delete_entity_type(name=name)
            for i, entity in enumerate(global_entity_list):
                if entity["uiid"] == entity_uuid:
                    global_entity_list.pop(i)
                    break
            print('Entity type deleted: \n{}'.format(response))
            return jsonify({"error_code": 0, "message": "entity is deleted successfully"})
        except Exception as e:
            print(e)
            return jsonify({"error_code": 1, "message": str(e)})
