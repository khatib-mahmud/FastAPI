import os
from dotenv import load_dotenv
from flask.views import MethodView
import google.cloud.dialogflow_v2 as dialogflow
from google.protobuf import field_mask_pb2
from pathlib import Path
from flask import request, jsonify

dir_path = str(Path(__file__).parent.parent.parent)
cred_path = dir_path + '/config/ava-existing-customer-v2.json'
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = cred_path
load_dotenv(dir_path + "/.env")
project_id = os.getenv('project_id')

global_intent_list = []
is_parent = "NO"
is_child = "NO"
replypreproces = ""


class ManageIntents(MethodView):

    def get_intent_data(self, intent):
        tokenize_intent_id = intent.name.split('/')[-1]
        child_intent_id = tokenize_intent_id[len(tokenize_intent_id) - 1]
        tokenize_intent_parent_followup = intent.parent_followup_intent_name.split('/')
        parent_intent_id = tokenize_intent_parent_followup[len(tokenize_intent_parent_followup) - 1]

        input_context_list = []
        if intent.input_context_names is not None:
            for input_context_name in intent.input_context_names:
                input_context_list.append(input_context_name)

        output_context_list = []
        if intent.output_contexts is not None:
            for output_context in intent.output_contexts:
                output_context_list.append(output_context.name)

        training_phrases_list = []
        entity_list = []
        # intent.TrainingPhrase.Part(text=text, entity_type=entity_type, alias=alias)
        for training_phrase_parts in intent.training_phrases:
            train_phrase = ''
            for training_phrase in training_phrase_parts.parts:

                train_phrase = train_phrase + str(training_phrase.text)
                entity_type = str(training_phrase.entity_type)
                if len(entity_type) > 3:
                    *first, last = train_phrase.split()
                    entity_list.append({'name': last,
                                        'entity': entity_type,
                                        'value': str(training_phrase.alias)})

            training_phrases_list.append({'text': train_phrase,
                                          'entity': entity_list})

        reply_messages_list = []
        for reply_message in intent.messages:
            reply_message_unicode = str(reply_message.text).encode('raw_unicode_escape').decode('unicode_escape').encode('latin1').decode()
            reply_messages_list.append(reply_message_unicode)

        json_dict = dict(id=tokenize_intent_id, name=intent.display_name,
                         parent_followup_intent=tokenize_intent_parent_followup[
                             len(tokenize_intent_parent_followup) - 1],
                         input_context=input_context_list, output_context=output_context_list,
                         is_parent=is_parent,
                         action=intent.action,
                         training_message=training_phrases_list, reply_message=reply_messages_list)
        return json_dict

    def get_intent_by_id(self, intent_id):
        intents_client = dialogflow.IntentsClient()
        intent_name = intents_client.intent_path(project_id, intent_id)
        intent = intents_client.get_intent(request={"name": intent_name, "intent_view": 'INTENT_VIEW_FULL'})
        return self.get_intent_data(intent)

    def get_children(self, intent_id):
        try:
            children_intents = []
            for dict_item in global_intent_list:

                if intent_id in dict_item.get("parent_followup_intent"):
                    child_id = dict_item.get("id")
                    children_intents.append(self.get_intent_by_id(child_id))
                else:
                    continue

        except Exception as e:
            print(e)
            return str(e)

        return children_intents

    def get(self, intent_id=None, get_child=None):

        try:

            print("ManageIntents get method api is called")

            global global_intent_list
            global is_parent
            if get_child is not None:
                return jsonify(self.get_children(intent_id))

            # retry: Union[google.api_core.retry.Retry,
            # timeout: Optional[float] = None
            i = 0
            if intent_id is None and len(global_intent_list) <= 0:
                intents_client = dialogflow.IntentsClient()
                parent = dialogflow.AgentsClient.agent_path(project_id)
                intents = intents_client.list_intents(request={"parent": parent, "intent_view": 'INTENT_VIEW_FULL'})

                for intent in intents:
                    print(i)
                    i = i + 1
                    intent_info = self.get_intent_data(intent)

                    global_intent_list.append(intent_info)

                json_response = jsonify(global_intent_list)
                return json_response

                # return "success"
            elif intent_id is None and len(global_intent_list) > 0:
                json_response = jsonify(global_intent_list)
                return json_response
            else:
                intents_client = dialogflow.IntentsClient()
                intent_name = intents_client.intent_path(project_id, intent_id)
                intent = intents_client.get_intent(request={"name": intent_name, "intent_view": 'INTENT_VIEW_FULL'})
                # response_dictionary = self.get_intent_data(intent)

                return jsonify(self.get_intent_data(intent))

        except Exception as e:
            print(e)
            return str(e)

    def post(self):

        try:
            print("create(POST) intent api is called")
            global global_intent_list
            intent_info = request.get_json(force=True)
            intent_display_name = intent_info['intent_display_name']
            training_phrases_parts = intent_info['training_phrases_parts']
            intent_message_texts = intent_info['intent_message_texts']
            # entity_type = intent_info['entity_type']
            try:
                parent_intent_id = intent_info['parent_intent_id']
                print('parent_intent_id', parent_intent_id)
                parent_intent = "projects/project-id-" + project_id + "/agent/intents/" + parent_intent_id
            except Exception as e:
                parent_intent_id = None
                print(e)

            intents_client = dialogflow.IntentsClient()
            parent = dialogflow.AgentsClient.agent_path(project_id)
            training_phrases = []
            for training_phrases_part in training_phrases_parts:
                part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)  # +
                                                             # ) + dialogflow.Intent.TrainingPhrase.Part(text='apples',
                                                             #                                           entity_type='@fruit',
                                                             #                                           alias='fruit')
                training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
                training_phrases.append(training_phrase)

            text = dialogflow.Intent.Message.Text(text=intent_message_texts)
            message = dialogflow.Intent.Message(text=text)

            if parent_intent_id is not None:
                intent = dialogflow.Intent(
                    display_name=intent_display_name,
                    training_phrases=training_phrases,
                    messages=[message],
                    parent_followup_intent_name=parent_intent
                )

            else:
                intent = dialogflow.Intent(
                    display_name=intent_display_name,
                    training_phrases=training_phrases,
                    messages=[message]
                )

            response = intents_client.create_intent(
                request={"parent": parent, "intent": intent}
            )

            intent_id = response.name.split('/')[-1].strip()
            created_intent = self.get_intent_by_id(intent_id)
            global_intent_list.append(created_intent)
            return {"code": 1, "message": "intent created successfully"}
        except Exception as e:
            print(e)
            return {"code": 0, "message": "intent creation failed! Error is: " + str(e)}

    def put(self):

        try:
            print("update(PUT) intent api is called")
            global global_intent_list
            parent = dialogflow.AgentsClient.agent_path(project_id)
            intent_info = request.get_json(force=True)
            intent_id = intent_info['intent_id']
            intent_display_name = intent_info['intent_display_name']
            training_phrases_parts = intent_info['training_phrases_parts']
            intent_message_texts = intent_info['intent_message_texts']
            intents_client = dialogflow.IntentsClient()

            intent_name = intents_client.intent_path(project_id, intent_id)
            intent = intents_client.get_intent(request={"name": intent_name, "intent_view": 'INTENT_VIEW_FULL'})

            intent.display_name = intent_display_name

            training_phrases = []
            for training_phrases_part in training_phrases_parts:
                part = dialogflow.types.Intent.TrainingPhrase.Part(
                    text=training_phrases_part)
                training_phrase = dialogflow.types.Intent.TrainingPhrase(parts=[part])
                training_phrases.append(training_phrase)
            intent.training_phrases.clear()
            intent.training_phrases.extend(training_phrases)
            text = dialogflow.Intent.Message.Text(text=intent_message_texts)
            message = dialogflow.Intent.Message(text=text)
            intent.messages.clear()
            intent.messages.extend([message])

            update_mask = field_mask_pb2.FieldMask(
                paths=["display_name", "training_phrases", "messages", " root_followup_intent_name"])
            response = intents_client.update_intent(intent=intent, update_mask=update_mask)
            # response = intents_client.update_intent(intent=intent)
            updated_intent = self.get_intent_by_id(intent_id)
            for i, intent in enumerate(global_intent_list):
                if intent["id"] == intent_id:
                    global_intent_list.pop(i)
                    global_intent_list.insert(i, updated_intent)
                    break

            return {"code": 1, "message": "intent updated successfully"}
        except Exception as e:
            print(e)
            return {"code": 0, "message": "intent update failed! Error is: " + str(e)}

    def delete(self, intent_id):

        try:
            print("delete intent api is called")
            global global_intent_list
            intents_client = dialogflow.IntentsClient()
            intent_path = intents_client.intent_path(project_id, intent_id)
            for i, intent in enumerate(global_intent_list):
                if intent["id"] == intent_id:
                    global_intent_list.pop(i)
                    break
            intents_client.delete_intent(request={"name": intent_path})

            return {"code": 1, "message": "intent deleted successfully"}
        except Exception as e:
            return {"code": 0, "message": "intent deletion failed! Error is: " + str(e)}


if __name__ == "__main__":
    dir_path = ManageIntents().get()
    print(dir_path)
    pass
