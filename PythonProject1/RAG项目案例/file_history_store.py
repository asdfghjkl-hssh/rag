import os,json
from typing import Sequence
from langchain_core.messages import message_to_dict, messages_from_dict, BaseMessage
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_community.chat_models import ChatTongyi
from langchain_core.runnables import RunnableLambda
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory





def get_history(session_id):
    return FileChatMessageHistory(session_id,"./chat_history")
class FileChatMessageHistory(BaseChatMessageHistory):
    def __init__(self,session_id,file_path):
        self.session_id=session_id
        self.file_path=file_path
        self.file_result_path=os.path.join(self.file_path,self.session_id)
        #判断文件是否存在，使用makedirs创建文件
        os.makedirs(os.path.dirname(self.file_result_path),exist_ok=True)
    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        all_messages=list(self.messages)
        all_messages.extend(messages)
        new_messages=[]
        #通过message_to_dict将message转换为dict
        for message in all_messages:
            d=message_to_dict(message)
            new_messages.append(d)
        #将数据写入文件中
        with open(self.file_result_path,"w",encoding="utf-8") as f:
            json.dump(new_messages,f,ensure_ascii=False)
    @property
    def messages(self)->list[BaseMessage]:
        try:
            with open(self.file_result_path,"r",encoding="utf-8") as f:
                data=json.load(f)
                return messages_from_dict(data)
        except FileNotFoundError:
            return []
    def clear(self) -> None:
        with open(self.file_result_path,"w",encoding="utf-8") as f:
            json.dump([],f)