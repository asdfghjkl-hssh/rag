md5_path="./md5.txt"
collection_name="rag"
persist_directory="./chroma_db"
chunk_size=100
chunk_overlap=10
spliter_separators=["\n", "。", "？", "！", "；", "，"]
max_split_char_number=1000
#相似度检索的阈值
similarity_threshold=1
session_config = {"configurable": {"session_id": "user_002"}}

