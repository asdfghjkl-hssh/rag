import time
from rag import RagService
import streamlit as st
import config_data as config
st.title("智能客服")
#使用分隔符
st.divider()
if "message_history" not in st.session_state:
    st.session_state["message_history"] = [{"role": "assistant", "content": "你好，有什么可以帮助你的吗？"}]

if "rag" not in st.session_state:
    st.session_state.rag = RagService()

for message in st.session_state.message_history:
    st.chat_message(message["role"]).write(message["content"])
#在最下面创建输入框
prompt = st.chat_input("请输入问题：")
if prompt:
    st.chat_message("user").write(prompt)
    st.session_state.message_history.append({"role": "user", "content": prompt})
    ai_list=[]



    #转圈1秒
    with st.spinner("思考中..."):
        res_stream=st.session_state.rag.chain.stream({"input": prompt},config.session_config)
        #定义函数抓包来获取stream流中的数据
        # 使用yield
        def catch_stream(stream, catch_list):
            for chunk in stream:
                catch_list.append(chunk)
                yield chunk


        st.chat_message("assistant").write_stream(catch_stream(res_stream,ai_list))
        st.session_state.message_history.append({"role": "assistant", "content": "".join(ai_list)})
