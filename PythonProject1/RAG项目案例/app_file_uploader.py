import time

import streamlit as st
from botocore.compat import file_type
from knowledge_base import KnowledgeBaseService

st.title("知识库更新服务")
# 上传文件
upload_file=st.file_uploader(
    "上传文件",
    type=["txt", "pdf", "docx"],
    accept_multiple_files=False,
)

if "service" not in st.session_state:
    st.session_state["service"]=KnowledgeBaseService()
if upload_file is not None:
    file_name=upload_file.name
    file_type=upload_file.type
    file_size=upload_file.size/1024
    st.write(f"文件的名字为：{file_name}")
    st.write(f"文件的类型为：{file_type}")
    st.write(f"文件的大小为：{file_size:.2f}KB")
    text=upload_file.getvalue().decode("utf-8")
    st.write(text)
    # st.session_state["counter"]+=1
    with st.spinner("上传中..."):
        time.sleep(3)
        result = st.session_state["service"].upload_by_str(text, file_name)
        st.write(result)


# print(f'上传文件的次数为：{st.session_state["counter"]}')