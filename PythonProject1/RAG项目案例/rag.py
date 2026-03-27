from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_models import ChatTongyi
from langchain_core.runnables import RunnablePassthrough, RunnableWithMessageHistory, RunnableLambda
from file_history_store import get_history
from vector_stores import VectorStoreService
import config_data as config
from langchain_core.prompts import MessagesPlaceholder


def print_examples(prompt):
    print("=" * 10)
    print(prompt.to_string())
    print("=" * 10)
    return prompt
class RagService(object):
    def __init__(self):
        self.vector_service = VectorStoreService(
            embedding=DashScopeEmbeddings()
        )

        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", "以我提供的已知参考资料为主，"
                "简洁和专业的回答用户问题。参考资料:{context}。"),
                ("system","用户的对话历史如下："),
                MessagesPlaceholder(variable_name="history"),
                ("user", "请回答用户提问: {input}")
            ]
        )

        self.chat_model = ChatTongyi(model="qwen-max")

        self.chain = self.__get_chain()

    def __get_chain(self):
        def hanshu(docs:list[Document]):
            if not docs:
                return "无相关参考文档"
            str1=""
            for doc in docs:
                str1+=doc.page_content
            return str1




        """获取最终的执行链"""
        retriever=self.vector_service.get_retriever()
        #chain中使用runnablepassthrough
        def format_for_retriever(value)->str:
            return value["input"]
        def format_for_prompt_template(value):
            new_valu={}
            new_valu["input"]=value["input"]["input"]
            new_valu["context"]=value["context"]
            new_valu["history"]=value["input"]["history"]
            return new_valu
        chain=(
            {
                "input":RunnablePassthrough(),
                "context":RunnableLambda(format_for_retriever)|retriever|hanshu
            }|RunnableLambda(format_for_prompt_template)|self.prompt_template|print_examples|self.chat_model|StrOutputParser()
        )
        #RunnableWithMessageHistory
        conversation_chain=RunnableWithMessageHistory(
            chain,
            get_history,
            input_messages_key="input",
            history_messages_key="history"
        )
        return conversation_chain
if __name__ == '__main__':
    # 自定义session_id（区分不同用户/会话，比如 user_001、user_002）
    session_config = {"configurable": {"session_id": "user_002"}}
    resx=RagService().chain.invoke({"input":"春天穿什么颜色的衣服"},config=session_config)
    print(resx)
