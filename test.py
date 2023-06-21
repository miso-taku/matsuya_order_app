from chatgpt_text_gen import ChatGPT

chat_gpt = ChatGPT()
additional_text = "牛めしと豚汁"
print(chat_gpt.generate_from_file('prompt.txt', additional_text))