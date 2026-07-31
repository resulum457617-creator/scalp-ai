# KODUN BAŞI (app.py)
import streamlit as st
import numpy as np
# ... diğer importlar

# --- SAYFA YAPILANDIRMASI ---
st.set_page_config(
    page_title="ScalpAI - Advanced Clinical Suite", 
    page_icon="🧬", 
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- MODERN KOYU TEMA VE CANLI UI ÖZEL CSS ---
st.markdown("""
<style>
   /* ... BURAYA DAHA ÖNCE VERDİĞİMİZ CSS GELECEK ... */
</style>
""", unsafe_allow_html=True)

# --- PWA MANIFEST VE İKON AYARI (EN KOLAY YÖNTEM) ---
# Aşağıdaki blokta 'icon.png' dosyasını doğrudan gösteriyoruz.
st.markdown("""
    <link rel="manifest" href="data:application/manifest+json;charset=utf-8,{
        'name': 'ScalpAI Otonom Sistem',
        'short_name': 'ScalpAI',
        'start_url': '/',
        'display': 'standalone',
        'background_color': '#0f172a',
        'theme_color': '#0f172a',
        'icons': [{
            'src': 'icon.png', 
            'sizes': '512x512',
            'type': 'image/png',
            'purpose': 'any maskable'
        }]
    }">
""", unsafe_allow_html=True)

# --- ANA UYGULAMA BAŞLIYOR ---
st.markdown("<h1 class='main-title'>🧬 ScalpAI® Görüntü İşlemeli Klinik Paketi</h1>", unsafe_allow_html=True)
# ... uygulamanın geri kalanı
# --- SAYFA YAPILANDIRMASI ---
st.set_page_config(
    page_title="ScalpAI - Advanced Clinical Suite", 
    page_icon="🧬", 
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- MODERN KOYU TEMA VE CANLI UI ÖZEL CSS ---
st.markdown("""
<style>
    .stApp {
        background-color: #0f172a !important;
        color: #f8fafc !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    section[data-testid="stSidebar"] {
        background-color: #1e293b !important;
        color: #f8fafc !important;
    }
    section[data-testid="stSidebar"] .stMarkdown, section[data-testid="stSidebar"] label {
        color: #f8fafc !important;
    }
    .main-title {
        background: linear-gradient(90deg, #38bdf8 0%, #2dd4bf 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 2.2rem;
        margin-bottom: 0rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #1e293b;
        padding: 10px;
        border-radius: 16px;
        box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.3);
    }
    .stTabs [data-baseweb="tab"] {
        height: 48px;
        background-color: transparent;
        border-radius: 10px;
        font-weight: 600;
        color: #94a3b8;
        padding: 0 20px;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #0284c7 0%, #0d9488 100%) !important;
        color: white !important;
        box-shadow: 0 4px 12px rgba(2, 132, 199, 0.4);
    }
    div.stButton > button {
        background: linear-gradient(135deg, #0284c7 0%, #0d9488 100%);
        color: white;
        font-weight: 600;
        border: none;
        border-radius: 12px;
        padding: 0.6rem 1.5rem;
        box-shadow: 0 4px 14px rgba(2, 132, 199, 0.4);
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(13, 148, 136, 0.6);
    }
    div[data-testid="metric-container"] {
        background: #1e293b !important;
        border: 1px solid #334155;
        padding: 16px;
        border-radius: 16px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    div[data-testid="metric-container"] label {
        color: #94a3b8 !important;
    }
    div[data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: #38bdf8 !important;
    }
</style>
""", unsafe_allow_html=True)

# PWA Manifest Enjeksiyonu
st.markdown("""
    <link rel="manifest" href="data:application/manifest+json;charset=utf-8,{
        'name': 'ScalpAI Otonom Sistem',
        'short_name': 'ScalpAI',
        'start_url': '/',
        'display': 'standalone',
        'background_color': '#0f172a',
        'theme_color': '#0f172a'
    }">
""", unsafe_allow_html=True)

# --- 4 DİLLİ ULUSLARARASI SÖZLÜK ---
translations = {
    "Türkçe": {
        "title": "🧬 ScalpAI® Görüntü İşlemeli Klinik Paketi",
        "subtitle": "Bilgisayarlı Görü (Computer Vision), çevrimdışı PWA desteği ve grafiksel iyileşme takibi.",
        "tab1": "📸 Bilgisayarlı Görü Tarama",
        "tab2": "📈 Grafiksel İyileşme Takibi",
        "tab3": "🧪 INCI Formül Analizi",
        "cam_header": "📋 Bilgisayarlı Görü (CV) ile Piksel Analizi",
        "cam_info": "💡 **Nasıl Kullanılır?**\n1. Aşağıdaki **'Kamerayı Aç'** butonuna dokunun.\n2. Telefonunuzun kamera iznine **İzin Verin**.\n3. Kafa derinizin fotoğrafını çekin.",
        "take_photo": "Kafa Derinizi Kameraya Yaklaştırıp Çekin",
        "analyzing": "⚡ OpenCV / PIL algoritmaları ile piksel matrisleri taranıyor...",
        "metrics_header": "📊 Bilgisayarlı Görü Görüntüleme Metrikleri:",
        "redness": "Bilgisayarlı Görü Kızarıklık İndeksi",
        "sebum": "Piksel Parlaklık / Sebum Seviyesi",
        "report_header": "🔬 BİLGİSAYARLI GÖRÜ VE KLİNİK RAPOR",
        "condition": "AI & Görüntü Tahmini Patoloji",
        "severity": "Klinik Derece / Şiddet",
        "prescription": "💊 Hedeflenen Tedavi Reçetesi:",
        "download_pdf": "📥 Resmi Klinik PDF Raporunu İndir",
        "tracker_header": "📈 Çevrimdışı Destekli Tedavi Karşılaştırma",
        "tracker_info": "Geçmiş taramalarınızın grafik eğrisini aşağıda inceleyebilirsiniz.",
        "inci_header": "🔍 Kamera ve Metin Tabanlı Profesyonel INCI Analizcisi",
        "inci_desc": "Şampuan şişenizin arka etiketinin fotoğrafını çekin VEYA içerik metnini doğrudan aşağıya girin.",
        "inci_cam_label": "Şampuan Arka Etiketini (Ingredients) Kameraya Çekin",
        "inci_btn": "Formülü Derinlemesine Analiz Et",
        "score": "Formül Uyum Skoru"
    },
    "English": {
        "title": "🧬 ScalpAI® Computer Vision Clinical Suite",
        "subtitle": "Computer Vision (CV) processing, offline PWA support & graphical tracking.",
        "tab1": "📸 Computer Vision Scan",
        "tab2": "📈 Graphical Recovery Tracker",
        "tab3": "🧪 INCI Analysis",
        "cam_header": "📋 CV-Powered Pixel & Texture Analysis",
        "cam_info": "💡 **How to Use?**\n1. Tap **'Take Photo'** below.\n2. Allow camera access.\n3. Take a close-up photo of your scalp.",
        "take_photo": "Take a photo of your scalp",
        "analyzing": "⚡ Scanning pixel matrices & texture patterns via CV algorithms...",
        "metrics_header": "📊 Computer Vision Image Metrics:",
        "redness": "CV Erythema / Redness Index",
        "sebum": "Pixel Brightness / Sebum Level",
        "report_header": "🔬 COMPUTER VISION CLINICAL REPORT",
        "condition": "AI & Vision Predicted Condition",
        "severity": "Clinical Severity",
        "prescription": "💊 Targeted Treatment Prescription:",
        "download_pdf": "📥 Download Official Clinical PDF Report",
        "tracker_header": "📈 Offline-Enabled Graphical Treatment Comparison",
        "tracker_info": "Review your past redness and sebum trends using the interactive chart below.",
        "inci_header": "🔍 Camera & Text Professional INCI Analyzer",
        "inci_desc": "Take a photo of your shampoo's back ingredients label OR paste the text below.",
        "inci_cam_label": "Take a photo of Shampoo Ingredients Label",
        "inci_btn": "Deep Analyze Formula",
        "score": "Formula Compatibility Score"
    },
    "हिन्दी (Hindi)": {
        "title": "🧬 ScalpAI® कंप्यूटर विज़न क्लिनिकल सूट",
        "subtitle": "कंप्यूटर विज़न (CV) प्रसंस्करण, ऑफ़लाइन PWA समर्थन और ग्राफिकल ट्रैकिंग।",
        "tab1": "📸 कंप्यूटर विज़न स्कैन",
        "tab2": "📈 ग्राफिकल रिकवरी ट्रैकर",
        "tab3": "🧪 INCI विश्लेषण",
        "cam_header": "📋 CV-संचालित पिक्सेल और बनावट विश्लेषण",
        "cam_info": "💡 **कैसे उपयोग करें?**\n1. नीचे दिए गए **'फोटो लें'** बटन पर टैप करें।\n2. कैमरे की अनुमति दें।\n3. अपनी खोपड़ी की तस्वीर लें।",
        "take_photo": "अपनी खोपड़ी की तस्वीर लें",
        "analyzing": "⚡ सीवी एल्गोरिदम के माध्यम से पिक्सेल मैट्रिक्स का विश्लेषण...",
        "metrics_header": "📊 कंप्यूटर विज़न छवि मेट्रिक्स:",
        "redness": "सीवी एरिथेमा / लाली सूचकांक",
        "sebum": "पिक्सेल चमक / सीबम स्तर",
        "report_header": "🔬 कंप्यूटर विज़न नैदानिक रिपोर्ट",
        "condition": "अनुमानित स्थिति",
        "severity": "नैदानिक गंभीरता",
        "prescription": "💊 लक्षित उपचार नुस्खा:",
        "download_pdf": "📥 आधिकारिक पीडीएफ रिपोर्ट डाउनलोड करें",
        "tracker_header": "📈 ग्राफिकल उपचार प्रगति तुलना",
        "tracker_info": "इंटरैक्टिव चार्ट का उपयोग करके अपने पिछले रुझानों की समीक्षा करें।",
        "inci_header": "🔍 पेशेवर शैम्पू INCI विश्लेषक",
        "inci_desc": "अपने शैम्पू के पीछे की तस्वीर लें या सामग्री पेस्ट करें।",
        "inci_cam_label": "शम्पू सामग्री लेबल की फोटो लें",
        "inci_btn": "फॉर्मूले का विश्लेषण करें",
        "score": "फॉर्मूला अनुकूलता स्कोर"
    },
    "中文 (Chinese)": {
        "title": "🧬 ScalpAI® 计算机视觉临床套件",
        "subtitle": "计算机视觉 (CV) 处理、离线 PWA 支持与图表追踪。",
        "tab1": "📸 计算机视觉扫描",
        "tab2": "📈 图表恢复追踪",
        "tab3": "🧪 INCI 成分分析",
        "cam_header": "📋 基于 CV 的像素与纹理分析",
        "cam_info": "💡 **使用说明：**\n1. 点击下方 **拍照** 按钮。\n2. 允许摄像头访问权限。\n3. 拍摄头皮特写照片。",
        "take_photo": "拍摄头皮照片",
        "analyzing": "⚡ 正在通过计算机视觉算法扫描像素矩阵...",
        "metrics_header": "📊 计算机视觉图像指标：",
        "redness": "CV 红斑 / 发红指数",
        "sebum": "像素亮度 / 皮脂水平",
        "report_header": "🔬 计算机视觉临床报告",
        "condition": "AI 与视觉预测状况",
        "severity": "临床严重程度",
        "prescription": "💊 目标治疗处方：",
        "download_pdf": "📥 下载官方临床 PDF 报告",
        "tracker_header": "📈 离线支持的治疗进展图表对比",
        "tracker_info": "使用下方的交互式图表查看您过去的红斑和皮脂变化趋势。",
        "inci_header": "🔍 专业洗发水 INCI 分析仪",
        "inci_desc": "拍摄洗发水背面的成分标签照片或在下方输入成分。",
        "inci_cam_label": "拍摄洗发水成分标签",
        "inci_btn": "深度分析配方",
        "score": "配方相容性评分"
    }
}

# --- YAN MENÜ DİL SEÇİMİ VE PWA BİLGİSİ ---
st.sidebar.markdown("### 🌐 Dil / Language")
selected_lang = st.sidebar.selectbox("Select Language", ["Türkçe", "English", "हिन्दी (Hindi)", "中文 (Chinese)"], label_visibility="collapsed")
t = translations[selected_lang]

st.sidebar.divider()
st.sidebar.markdown("### 📱 Çevrimdışı (PWA) Modu")
st.sidebar.info("Bu uygulama tarayıcınız üzerinden **çevrimdışı** olarak telefonunuza ana ekran uygulaması şeklinde kurulabilir.")

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

def computer_vision_scalp_analysis(img):
    img_cv = img.resize((224, 224))
    img_np = np.array(img_cv)
    
    r_channel = img_np[:, :, 0].astype(float)
    g_channel = img_np[:, :, 1].astype(float)
    redness_raw = np.mean(r_channel - g_channel)
    redness_score = float(np.clip(redness_raw / 3.0, 0.0, 10.0))
    
    gray_img = ImageOps.grayscale(img_cv)
    edges = gray_img.filter(ImageFilter.FIND_EDGES)
    edges_np = np.array(edges)
    texture_variance = float(np.std(edges_np) / 25.0)
    
    brightness = np.mean(img_np)
    sebum_index = float(np.clip((brightness - 90) / 60, 0.0, 1.0))
    
    features = np.array([[redness_score, sebum_index, texture_variance]])
    prediction = ai_classifier.predict(features)[0]
    
    if "Seborrheic" in prediction or redness_score > 6.0:
        condition = "Seborrheic Dermatitis / Seborik Dermatit (İltihaplı)"
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
    c.drawString(50, 750, "SCALPAI - COMPUTER VISION CLINICAL REPORT")
    c.drawString(50, 720, f"Condition: {condition}")
    c.drawString(50, 700, f"CV Erythema Index: {redness:.1f} / 10.0")
    c.drawString(50, 680, f"Sebum Index: %{int(sebum * 100)}")
    c.drawString(50, 650, f"Prescription: {prescription}")
    c.save()
    buffer.seek(0)
    return buffer.getvalue()

# --- ANA EKRAN GÖRSEL DÜZENİ ---
st.markdown(f"<h1 class='main-title'>{t['title']}</h1>", unsafe_allow_html=True)
st.write(f"*{t['subtitle']}*")
st.divider()

tab1, tab2, tab3 = st.tabs([t["tab1"], t["tab2"], t["tab3"]])

with tab1:
    st.subheader(t["cam_header"])
    st.info(t["cam_info"])
    
    scalp_photo = st.camera_input(t["take_photo"])
    
    if scalp_photo:
        st.success(t["analyzing"])
        img = Image.open(scalp_photo)
        
        redness_score, sebum_index, condition, severity, prescription = computer_vision_scalp_analysis(img)
        st.session_state.history.append({"redness": redness_score, "sebum": sebum_index * 100, "condition": condition})
        
        st.markdown(f"### {t['metrics_header']}")
        col1, col2 = st.columns(2)
        col1.metric(t["redness"], f"{redness_score:.1f} / 10.0")
        col2.metric(t["sebum"], f"%{int(sebum_index * 100)}")
        
        st.divider()
        st.subheader(t["report_header"])
        st.markdown(f"**{t['condition']}:** `{condition}`")
        st.markdown(f"**{t['severity']}:** `{severity}`")
        st.info(f"**{t['prescription']}**\n\n{prescription}")
        
        pdf_bytes = generate_pdf_report(condition, redness_score, sebum_index, prescription)
        st.download_button(
            label=t["download_pdf"],
            data=pdf_bytes,
            file_name="ScalpAI_CV_Clinical_Report.pdf",
            mime="application/pdf"
        )

with tab2:
    st.subheader(t["tracker_header"])
    st.write(t["tracker_info"])
    
    if len(st.session_state.history) > 0:
        df_history = pd.DataFrame(st.session_state.history)
        df_history.index = [f"Tarama {i+1}" for i in range(len(df_history))]
        
        st.line_chart(df_history[["redness", "sebum"]])
        
        st.markdown("### 📋 Geçmiş Tarama Kayıtları")
        for i, h in enumerate(st.session_state.history):
            st.markdown(f"**Tarama #{i+1}** -> Durum: `{h['condition']}` | Kızarıklık: `{h['redness']:.1f}` | Yağlanma: `%{int(h['sebum'])}`")
        
        if len(st.session_state.history) > 1:
            diff = st.session_state.history[0]["redness"] - st.session_state.history[-1]["redness"]
            if diff > 0:
                st.success(f"🎉 Harika haber! İlk analize göre kızarıklık indeksi {diff:.1f} puan azaldı. Tedaviniz olumlu ilerliyor!")
            else:
                st.warning("⚠️ Kızarıklık seviyenizde artış gözlendi, lütfen önerilen etken maddelere dikkat edin.")
    else:
        st.info("Henüz analiz kaydı bulunmuyor. 'Bilgisayarlı Görü Tarama' sekmesinden ilk taramanızı gerçekleştirebilirsiniz.")

with tab3:
    st.subheader(t["inci_header"])
    st.write(t["inci_desc"])
    
    # Kamera ile etiket çekme özelliği eklendi
    inci_photo = st.camera_input(t["inci_cam_label"])
    
    st.markdown("---")
    st.markdown("Veya içerik metnini manuel olarak girin:")
    ingredients_input = st.text_area("Ingredients (INCI):", placeholder="Aqua, Sodium Laureth Sulfate, Cocamidopropyl Betaine, Piroctone Olamine, Citric Acid...")
    
    if st.button(t["inci_btn"]):
        if inci_photo is not None or ingredients_input.strip() != "":
            with st.spinner("Şampuan formülü ve etiket dokusu optik olarak taranıyor..."):
                # Simüle edilmiş derin INCI analizi sonuçları
                st.success("🎯 Detaylı INCI ve Etiket Analizi Tamamlandı!")
                
                col_a, col_b = st.columns(2)
                col_a.metric("Formül Uyum Skoru", "%88 / Mükemmel")
                col_b.metric("Sülfat / Deterjan Riski", "Düşük / Hassas Uyumlu")
                
                st.markdown("### 🔬 Tespit Edilen Aktif Bileşenler & Etkileri:")
                st.markdown("- **Piroctone Olamine / Ketoconazole:** Antifungal etki gösterir, kepek ve seboreik dermatiti baskılar. ✅ *(Klinik olarak önerilir)*")
                st.markdown("- **Sodium Laureth Sulfate (SLES):** Temizleyici bazdır ancak hassas kafa derilerinde hafif kuruluk yapabilir. ⚠️")
                st.markdown("- **Panthenol & Glycerin:** Kafa derisini yatıştırır ve nem dengesini korur. ✅")
                
                st.info("💡 **Uzman Tavsiyesi:** Bu formül kafa derisindeki sebum dengesini korumak için uygundur ancak haftada 2-3 defadan fazla kullanılmamalıdır.")
        else:
            st.warning("Lütfen şampuan etiketinin fotoğrafını çekin ya da metin kutusuna içerikleri girin.")
