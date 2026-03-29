import streamlit as st
import google.generativeai as genai

# 1. 網頁基本設定
st.set_page_config(page_title="專屬產業知識網", page_icon="🧠", layout="centered")
st.title("🧠 深度產業知識網 (Beta)")
st.write("結合技術洞察與財務預測的專屬 AI 顧問。")

# 2. 側邊欄：設定 API Key 與系統提示詞 (這裡可以設定為只有管理員能看到)
with st.sidebar:
    st.header("⚙️ 系統設定")
    api_key = st.text_input("輸入 Gemini API Key", type="password")
    st.markdown("---")
    st.write("💡 **管理員操作區**：在這裡貼上最新的產業報告、法說會紀錄或技術文章。")
    
    # 這裡就是你的「知識庫」核心
    knowledge_base = st.text_area(
        "輸入知識庫內容", 
        height=300, 
        placeholder="例如：貼上最新的 CoWoS 產能預估、CPO 規格競爭分析，或是本土法人與外資的最新報告摘要..."
    )

# 3. 主畫面：使用者提問區
st.subheader("💬 向知識庫提問")
user_question = st.text_input("你想了解什麼？", placeholder="例如：根據資料，這項技術突破對設備廠的毛利影響為何？")

# 4. 執行 AI 分析
if st.button("🚀 生成深度分析"):
    if not api_key:
        st.error("請先在左側輸入 Gemini API Key！")
    elif not knowledge_base:
        st.error("知識庫目前是空的，請管理員先輸入背景資料！")
    elif not user_question:
        st.warning("請輸入你的問題！")
    else:
        try:
            # 設定 Gemini API
            genai.configure(api_key=api_key)
            # 使用 Gemini 1.5 Flash 或 Pro 模型
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # 設計精準的 Prompt，強制 AI 只能根據你提供的資料回答
            prompt = f"""
            你是一位頂尖的產業分析師，同時精通半導體技術與財務估值。
            請「嚴格」根據以下提供的【知識庫內容】來回答使用者的【問題】。
            如果知識庫內容中沒有提到相關資訊，請誠實回答「目前知識庫缺乏此數據」，不要自己編造。
            
            【知識庫內容】：
            {knowledge_base}
            
            【問題】：
            {user_question}
            
            請用專業、客觀且條理分明的語氣回答：
            """
            
            with st.spinner("AI 正在交叉比對技術與財務資料..."):
                response = model.generate_content(prompt)
                
            st.success("✅ 分析完成！")
            st.markdown("### 📊 系統回覆：")
            st.write(response.text)
            
        except Exception as e:
            st.error(f"發生錯誤：{e}")
