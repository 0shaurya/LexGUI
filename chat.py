import llama_cpp
from openai import OpenAI
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

class Chat:
	def __init__(self):
		self.type_of_model = 0 # 0 for local, 1 for openai, 2 for mistral
		self.model = None
		self.openai_api_key = None
		self.mistral_api_key = None
		self.context = [{"role": "system", "content": "You are a highly intelligent assistant."}]
		self.is_generating = False

	def query(self):
		# iterate through the stream of events and print it
		if self.type_of_model == 0 and self.model != None:
			try:
				for dictionary in self.model.create_chat_completion(self.context, stream = True):
						if 'content' in dictionary['choices'][0]['delta'] and self.is_generating:
							yield dictionary['choices'][0]['delta']['content']
						if not self.is_generating:
							break
			except:
				print('Error running local model!')
		elif self.type_of_model == 1 and self.openai_api_key != None:
			client = OpenAI(api_key=self.openai_api_key)
			try:
				for chunk in client.chat.completions.create(model = 'gpt-3.5-turbo', messages = self.context, stream = True):
					if chunk.choices[0].delta.content is not None and self.is_generating:
						yield chunk.choices[0].delta.content
					if not self.is_generating:
						break
			except:
				print('Error using OpenAI API! Maybe check to see if your API key is valid?')
		elif self.type_of_model == 2 and self.mistral_api_key != None:
			client = MistralClient(api_key=self.mistral_api_key)
			try:
				context = [ChatMessage(role=dictionary['role'], content=dictionary['content']) for dictionary in self.context] # Using Mistral's ChatMessage function
				for chunk in client.chat_stream(model = 'mistral-small', messages = context):
					print(chunk)
					if chunk.choices[0].delta.content and self.is_generating:
						yield chunk.choices[0].delta.content
					if not self.is_generating:
						break
			except:
				print('Error using Mistral API! Maybe check to see if your API key is valid?')


	def add_to_context(self, role, content):
		self.context.append({
			"role": role,
			"content": content
			})

	def get_context(self):
		return self.context