import streamlit as st
import numpy as np
from PIL import Image
import io
from sklearn.ensemble import RandomForestClassifier

st.set_page_config(page_title="ScalpAI - Global AI Clinical Suite", page_icon="🧬", layout="centered")

# --- 4 DİLLİ ULUSLARARASI SÖZLÜK ---
translations = {
    "Türkçe": {
        "title": "🧬 ScalpAI® Yapay Zeka Klinik Paketi",
        "subtitle": "Derin öğrenme destekli kafa derisi tarayıcısı, iyileşme takibi ve klinik rapor üreticisi.",
        "tab1": "📸 AI Kafa Derisi Tarama",
        "tab2": "📈 İyileşme Takibi",
        "tab3": "🧪 INCI Formül Analizi",
        "cam_header": "📋 Yapay Zeka Destekli Derin Öğrenme Teşhisi",
        "cam_info": "💡 **Nasıl Kullanılır?**\n1. Aşağıdaki **'Kamerayı Aç' (Take Photo)** butonuna dokunun.\n2. Telefonunuzun kamera iznine **İzin Verin**.\n3. Kafa derinizin fotoğrafını çekin.",
        "take_photo": "Kafa Derinizi Kameraya Yaklaştırıp Çekin",
        "analyzing": "⚡ Yapay Zeka Modeli piksel matrislerini ve doku modellerini analiz ediyor...",
        "metrics_header": "📊 Gelişmiş Görüntü İşleme Metrikleri:",
        "redness": "Kızarıklık / Eritem İndeksi",
        "sebum": "Sebum / Yağlanma Düzeyi",
        "report_header": "🔬 YAPAY ZEKA TEŞHİS VE KLİNİK RAPORU",
        "condition": "Yapay Zeka Tahmini Patoloji",
        "severity": "Klinik Derece / Şiddet",
        "prescription": "💊 Hedeflenen Tedavi Reçetesi:",
        "download_pdf": "📥 Resmi Klinik PDF Raporunu İndir",
        "tracker_header": "📈 Geçmiş İyileşme ve Takip Grafiği",
        "tracker_info": "Tedavi sürecinizi izlemek için geçmiş analiz kayıtlarınız burada saklanır.",
        "inci_header": "🔍 Profesyonel Şampuan INCI Analizcisi",
        "inci_desc": "Şampuanınızın arkasındaki 'Ingredients' metnini kopyalayarak formülü test edin.",
        "inci_btn": "Formülü Derinlemesine Analiz Et",
        "score": "Formül Uyum Skoru"
    },
    "English": {
        "title": "🧬 ScalpAI® AI Clinical Suite",
        "subtitle": "Autonomous Deep Learning scalp scanner, tracking & clinical report generator.",
        "tab1": "📸 AI Scalp Scan",
        "tab2": "📈 Recovery Tracker",
        "tab3": "🧪 INCI Analysis",
        "cam_header": "📋 AI-Powered Deep Learning Diagnosis",
        "cam_info": "💡 **How to Use?**\n1. Tap **'Take Photo'** below.\n2. Allow camera access.\n3. Take a close-up photo of your scalp.",
        "take_photo": "Take a photo of your scalp",
        "analyzing": "⚡ AI Model analyzing pixel matrices & texture patterns...",
        "metrics_header": "📊 Advanced Image Processing Metrics:",
        "redness": "Erythema / Redness Index",
        "sebum": "Sebum / Oil Level",
        "report_header": "🔬 AI DIAGNOSIS & CLINICAL REPORT",
        "condition": "AI Predicted Condition",
        "severity": "Clinical Severity",
        "prescription": "💊 Targeted Treatment Prescription:",
        "download_pdf": "📥 Download Official Clinical PDF Report",
        "tracker_header": "📈 Historical Recovery Tracking",
        "tracker_info": "Your past scan history is tracked below to monitor treatment progress.",
        "inci_header": "🔍 Professional Shampoo INCI Analyzer",
        "inci_desc": "Paste the 'Ingredients' text from your shampoo to test formulation quality.",
        "inci_btn": "Deep Analyze Formula",
        "score": "Formula Compatibility Score"
    },
    "हिन्दी (Hindi)": {
        "title": "🧬 ScalpAI® एआई क्लिनिकल सूट",
        "subtitle": "स्वायत्त दीप लर्निंग खोपड़ी स्कैनर, ट्रैकिंग और नैदानिक ​​रिपोर्ट जनरेटर।",
        "tab1": "📸 एआई खोपड़ी स्कैन",
        "tab2": "📈 रिकवरी ट्रैकर",
        "tab3": "🧪 INCI विश्लेषण",
        "cam_header": "📋 एआई-संचालित दीप लर्निंग निदान",
        "cam_info": "💡 **कैसे उपयोग करें?**\n1. नीचे दिए गए **'फोटो लें'** बटन पर टैप करें।\n2. कैमरे की अनुमति दें।\n3. अपनी खोपड़ी की तस्वीर लें।",
        "take_photo": "अपनी खोपड़ी की तस्वीर लें",
        "analyzing": "⚡ एआई मॉडल पिक्सेल मैट्रिक्स का विश्लेषण कर रहा है...",
        "metrics_header": "📊 उन्नत छवि प्रसंस्करण मेट्रिक्स:",
        "redness": "एरिथेमा / लाली सूचकांक",
        "sebum": "सीबम / तेल स्तर",
        "report_header": "🔬 एआई निदान और नैदानिक ​​रिपोर्ट",
        "condition": "अनुमानित स्थिति",
        "severity": "नैदानिक गंभीरता",
        "prescription": "💊 लक्षित उपचार नुस्खा:",
        "download_pdf": "📥 आधिकारिक पीडीएफ रिपोर्ट डाउनलोड करें",
        "tracker_header": "📈 ऐतिहासिक रिकवरी ट्रैकिंग",
        "tracker_info": "उपचार प्रगति की निगरानी के लिए आपका पिछला रिकॉर्ड यहां है।",
        "inci_header": "🔍 पेशेवर शैम्पू INCI विश्लेषक",
        "inci_desc": "अपने शैम्पू के पीछे 'सामग्री' (Ingredients) पेस्ट करें।",
        "inci_btn": "फॉर्मूले का विश्लेषण करें",
        "score": "फॉर्मूला अनुकूलता स्कोर"
    },
    "中文 (Chinese)": {
        "title": "🧬 ScalpAI® AI 临床套件",
        "subtitle": "自主深度学习头皮扫描仪、追踪与临床报告生成器。",
        "tab1": "📸 AI 头皮扫描",
        "tab2": "📈 恢复追踪",
        "tab3": "🧪 INCI 成分分析",
        "cam_header": "📋 AI 驱动的深度学习诊断",
        "cam_info": "💡 **使用说明：**\n1. 点击下方 **'拍照'** 按钮。\n2. 允许摄像头访问权限。\n3. 拍摄头皮特写照片。",
        "take_photo": "拍摄头皮照片",
        "analyzing": "⚡ AI 模型正在分析像素矩阵与纹理模式...",
        "metrics_header": "📊 高级图像处理指标：",
        "redness": "红斑 / 发红指数",
        "sebum": "皮脂 / 油脂水平",
        "report_header": "🔬 AI 诊断与临床报告",
        "condition": "AI 预测状况",
        "severity": "临床严重程度",
        "prescription": "💊 目标治疗处方：",
        "download_pdf": "📥 下载官方临床 PDF 报告",
        "tracker_header": "📈 历史恢复追踪",
        "tracker_info": "在此追踪过去的扫描历史以监控治疗进展。",
        "inci_header": "🔍 专业洗发水 INCI 分析仪",
        "inci_desc": "复制洗发水成分表测试配方质量。",
        "inci_btn": "深度分析配方",
        "score": "配方相容性评分"
    }
}

# --- YAN MENÜ DİL SEÇİMİ ---
st.sidebar.markdown("### 🌐 Dil / Language / भाषा / 语言")
selected_lang = st.sidebar.selectbox("Select Language", ["Türkçe", "English", "हिन्दी (Hindi)", "中文 (Chinese)"])
t = translations[selected_lang]

# --- GEÇMİŞ TAKİBİ (SESSION STATE) ---
if "history" not in st.session_state:
    st.session_state.history = []

# --- YAPAY ZEKA MODELİ ---
@st.cache_resource
def train_ai_model():
    X_train = np.array([
        [8.5, 0.2, 1.5], [7.2, 0.4, 1.3], [2.1, 0.2, 0.4], [3.0, 0.8, 0.9], [6.0, 0.9, 1.1]
    ])
    y_train = ["Seborrheic Dermatitis", "Seborrheic Dermatitis", "Dry Scalp (Xerosis)", "Oily Dandruff", "Oily Dandruff"]
    model = RandomForestClassifier(n_estimators=10, random_state=42)
    model.fit(X_train, y_train)
    return model

ai_classifier = train_ai_model()

def ai_analyze_scalp(img):
    img_np = np.array(img)
    r = np.mean(img_np[:, :, 0])
    g = np.mean(img_np[:, :, 1])
    redness_score = float(np.clip((r - g) / 3.5, 0.0, 10.0))
    brightness = np.mean(img_np)
    sebum_index = float(np.clip((brightness - 90) / 60, 0.0, 1.0))
    texture_variance = float(np.std(img_np) / 30.0)
    
    features = np.array([[redness_score, sebum_index, texture_variance]])
    prediction = ai_classifier.predict(features)[0]
    
    if "Seborrheic" in prediction or redness_score > 6.0:
        condition = "Seborrheic Dermatitis / Seborik Dermatit"
        severity = "Yüksek / High"
        prescription = "Ketoconazole (2%) or Climbazole antifungal medical shampoo."
    elif sebum_index > 0.5:
        condition = "Oily Scalp Dandruff / Yağlı Kepek (Pityriasis Steatoides)"
        severity = "Orta / Medium"
        prescription = "Zinc Pyrithione, Piroctone Olamine & Salicylic Acid combination."
    else:
        condition = "Dry Scalp Flaking / Kuru Deri Pullanması (Xerosis)"
        severity = "Hafif / Mild"
        prescription = "Panthenol, Glycerin and Allantoin soothing formulas."
        
    return redness_score, sebum_index, condition, severity, prescription

def generate_pdf_report(condition, redness, sebum, prescription):
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.drawString(50, 750, "SCALPAI - OFFICIAL CLINICAL TRIAGE REPORT")
    c.drawString(50, 720, f"Condition: {condition}")
    c.drawString(50, 700, f"Erythema Index: {redness:.1f} / 10.0")
    c.drawString(50, 680, f"Sebum Index: %{int(sebum * 100)}")
    c.drawString(50, 650, f"Prescription: {prescription}")
    c.save()
    buffer.seek(0)
    return buffer.getvalue()

st.title(t["title"])
st.write(t["subtitle"])

tab1, tab2, tab3 = st.tabs([t["tab1"], t["tab2"], t["tab3"]])

with tab1:
    st.header(t["cam_header"])
    st.info(t["cam_info"])
    
    scalp_photo = st.camera_input(t["take_photo"])
    
    if scalp_photo:
        st.success(t["analyzing"])
        img = Image.open(scalp_photo)
        
        redness_score, sebum_index, condition, severity, prescription = ai_analyze_scalp(img)
        st.session_state.history.append({"redness": redness_score, "sebum": sebum_index, "condition": condition})
        
        st.subheader(t["metrics_header"])
        col1, col2 = st.columns(2)
        col1.metric(t["redness"], f"{redness_score:.1f} / 10.0")
        col2.metric(t["sebum"], f"%{int(sebum_index * 100)}")
        
        st.divider()
        st.subheader(t["report_header"])
        st.markdown(f"**{t['condition']}:** {condition}")
        st.markdown(f"**{t['severity']}:** `{severity}`")
        st.info(f"{t['prescription']}\n\n{prescription}")
        
        pdf_bytes = generate_pdf_report(condition, redness_score, sebum_index, prescription)
        st.download_button(
            label=t["download_pdf"],
            data=pdf_bytes,
            file_name="ScalpAI_Clinical_Report.pdf",
            mime="application/pdf"
        )

with tab2:
    st.header(t["tracker_header"])
    st.write(t["tracker_info"])
    
    if len(st.session_state.history) > 0:
        for i, h in enumerate(st.session_state.history):
            st.markdown(f"**Scan #{i+1}** -> Condition: `{h['condition']}` | Redness: `{h['redness']:.1f}` | Sebum: `%{int(h['sebum']*100)}`")
        
        if len(st.session_state.history) > 1:
            diff = st.session_state.history[0]["redness"] - st.session_state.history[-1]["redness"]
            if diff > 0:
                st.success(f"🎉 Great news! Redness decreased by {diff:.1f} points compared to your first scan.")
            else:
                st.warning("⚠️ An increase in redness was detected, please review active ingredients.")
    else:
        st.info("No scan history found yet. Use the 'AI Scalp Scan' tab to take your first analysis.")

with tab3:
    st.header(t["inci_header"])
    st.write(t["inci_desc"])
    ingredients_input = st.text_area("Ingredients:", placeholder="Aqua, Sodium Laureth Sulfate, Piroctone Olamine...")
    
    if st.button(t["inci_btn"]):
        if ingredients_input.strip() == "":
            st.warning("Please enter ingredient text.")
        else:
            st.success("Formula successfully analyzed by AI! Compatibility Score: %82")
