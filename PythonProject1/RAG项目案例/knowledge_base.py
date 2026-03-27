import os
import config_data as config
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from datetime import datetime

def check_md5(md5_str:str):
    if not os.path.exists(config.md5_path):
        open(config.md5_path, "w", encoding="utf-8").close()
        return False
    else:
        for line in open(config.md5_path, "r", encoding="utf-8").readlines():
            line = line.strip()
            if md5_str in line:
                return True
        return  False

def save_md5(md5_str:str):
    with open(config.md5_path, "a", encoding="utf-8") as f:
        f.write(md5_str + "\n")


def get_string_md5(input_str:str,encoding="utf-8"):
    import hashlib

    str_bytes=input_str.encode(encoding=encoding)
    #创建md5对象
    md5_obj=hashlib.md5()
    md5_obj.update(str_bytes)
    return md5_obj.hexdigest()


class KnowledgeBaseService(object):
    def __init__(self):
        os.makedirs(config.persist_directory, exist_ok=True)
        self.chroma= Chroma(
            collection_name=config.collection_name,
            embedding_function=DashScopeEmbeddings(),
            persist_directory=config.persist_directory,
        )
        self.spliter=RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,
            chunk_overlap=config.chunk_overlap,
            separators=config.spliter_separators,
            length_function=len,
        )
    def upload_by_str(self,data:str,filename):
        md5_str=get_string_md5(data)
        if check_md5(md5_str):
            return "不能重复上传"
        if len(data)>config.max_split_char_number:
            text_list=self.spliter.split_text(data)
        else:
            text_list=[data]
        metadata={
            "filename": filename,
            "upload_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            #操作员
            "operator": "admin",
        }
        self.chroma.add_texts(
            text_list,
            metadatas=[metadata for _ in text_list]
        )
        save_md5(md5_str)
        return "上传成功"


if __name__ == '__main__':
    #测试上面的三个函数
    # r1=get_string_md5("周杰伦")
    # r2=get_string_md5("周杰伦")
    # r3=get_string_md5("周杰伦2")
    # print(r1)
    # print(r2)
    # print(r3)
    # save_md5("d41d8cd98f00b204e9800998ecf8427e")
    # print(check_md5("周杰伦"))
    service=KnowledgeBaseService()
    r=service.upload_by_str("小张", "test")
    print(r)