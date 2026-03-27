from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings

import config_data as config

class VectorStoreService(object):
    def __init__(self,embedding):
        self.embedding=embedding
        self.vector_store=Chroma(
            collection_name=config.collection_name,
            embedding_function=self.embedding,
            persist_directory=config.persist_directory,
        )
    #get_检索器
    def get_retriever(self):
        return self.vector_store.as_retriever(search_kwargs={"k": config.similarity_threshold})

if __name__ == '__main__':
    res=service=VectorStoreService(DashScopeEmbeddings()).get_retriever()
    resu=res.invoke("体重180斤，尺码推荐")
    print(resu)

