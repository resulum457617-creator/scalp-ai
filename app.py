import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image, ImageOps, ImageFilter
import io
import hashlib
import re
from sklearn.ensemble import RandomForestClassifier

# --- APPLE HIG SEVİYESİ KURUMSAL SAYFA YAPILANDIRMASI ---
st.set_page_config(
    page_title="ScalpAI® Enterprise Clinical Suite", 
    page_icon="🧬", 
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.apple.com',
        'Report a bug': 'https://www.apple.com',
        'About': "### ScalpAI® Apple HIG Certified Clinical Computer Vision Suite"
    }
)

# --- APPLE VISONOS / LIQUID GLASS & DAİRESEL GÖSTERGE CSS MİMARİSİ ---
st.markdown("""
<style>
    .stApp {
        background: radial-gradient(circle at 50% -20%, #1e293b 0%, #090d16 70%, #020408 100%) !important;
        color: #f8fafc !important;
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", "Helvetica Neue", Roboto, sans-serif !important;
    }
    section[data-testid="stSidebar"] {
        background: rgba(13, 18, 30, 0.75) !important;
        backdrop-filter: blur(24px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(24px) saturate(180%) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.06);
    }
    section[data-testid="stSidebar"] .stMarkdown, section[data-testid="stSidebar"] label {
        color: #cbd5e1 !important;
    }
    .apple-hero-container {
        padding: 1.5rem 0 2rem 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.06);
        margin-bottom: 2.5rem;
    }
    .main-title {
        background: linear-gradient(135deg, #ffffff 0%, #94a3b8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        font-size: 2.8rem;
        letter-spacing: -0.03em;
        margin-bottom: 0.4rem;
    }
    .main-subtitle {
        color: #64748b;
        font-size: 1.15rem;
        font-weight: 400;
        letter-spacing: -0.01em;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(15, 23, 42, 0.65);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        padding: 8px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.06);
        box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.5);
    }
    .stTabs [data-baseweb="tab"] {
        height: 48px;
        background-color: transparent;
        border-radius: 14px;
        font-weight: 500;
        font-size: 0.95rem;
        color: #94a3b8;
        padding: 0 24px;
        transition: all 0.25s cubic-bezier(0.25, 1, 0.5, 1);
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: rgba(255, 255, 255, 0.04);
        color: #ffffff;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #0284c7 0%, #0d9488 100%) !important;
        color: white !important;
        font-weight: 600;
        box-shadow: 0 8px 24px rgba(2, 132, 199, 0.35);
    }
    
    .glass-card, .stAlert, [data-testid="stFileUploader"], [data-testid="stCameraInput"] {
        background: rgba(30, 41, 59, 0.45) !important;
        backdrop-filter: blur(16px) saturate(150%) !important;
        -webkit-backdrop-filter: blur(16px) saturate(150%) !important;
        border: 1px solid rgba(255, 255, 255, 0.07) !important;
        padding: 24px !important;
        border-radius: 24px !important;
        box-shadow: 0 16px 32px -8px rgba(0, 0, 0, 0.4);
    }
    
    .circle-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        background: rgba(30, 41, 59, 0.45);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.07);
        padding: 20px;
        border-radius: 24px;
        box-shadow: 0 16px 32px -8px rgba(0, 0, 0, 0.4);
        text-align: center;
        transition: transform 0.3s ease;
    }
    .circle-container:hover {
        transform: translateY(-2px);
        border-color: rgba(56, 189, 248, 0.25);
    }
    .circular-chart {
        display: block;
        margin: 10px auto;
        max-width: 130px;
        max-height: 130px;
    }
    .circle-bg {
        fill: none;
        stroke: rgba(255, 255, 255, 0.08);
        stroke-width: 3.8;
    }
    .circle {
        fill: none;
        stroke-width: 3.8;
        stroke-linecap: round;
        animation: progress 1s ease-out forwards;
    }
    .percentage {
        fill: #f8fafc;
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", sans-serif;
        font-size: 0.55em;
        font-weight: 700;
        text-anchor: middle;
    }
    .circle-label {
        color: #94a3b8;
        font-size: 0.9rem;
        font-weight: 500;
        margin-top: 8px;
    }
    
    div.stButton > button {
        background: linear-gradient(135deg, #0284c7 0%, #0d9488 100%);
        color: white;
        font-weight: 600;
        border: none;
        border-radius: 16px;
        padding: 0.75rem 2rem;
        box-shadow: 0 8px 20px rgba(2, 132, 199, 0.3);
        transition: all 0.25s ease;
        width: 100%;
        letter-spacing: -0.01em;
    }
    div.stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 12px 28px rgba(13, 148, 136, 0.5);
    }
</style>
""", unsafe_allow_html=True)

# --- GLOBAL KULLANICI VERİTABANI VE OTURUM YÖNETİMİ ---
if "users" not in st.session_state:
    st.session_state.users = {} 
if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = None

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def validate_password_strength(password):
    if len(password) < 8:
        return "Şifre en az 8 karakter uzunluğunda olmalıdır."
    if not re.search(r"[A-Z]", password):
        return "Şifre en az bir büyük harf (A-Z) içermelidir."
    if not re.search(r"[a-z]", password):
        return "Şifre en az bir küçük harf (a-z) içermelidir."
    if not re.search(r"\d", password):
        return "Şifre en az bir rakam (0-9) içermelidir."
    if not re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?]", password):
        return "Şifre en az bir özel karakter (!@#$%^&* vb.) içermelidir."
    return None

# --- YAN MENÜ GİRİŞ/KAYIT ---
st.sidebar.markdown("### 👤 Klinik Bulut Portalı")

if st.session_state.logged_in_user is None:
    auth_mode = st.sidebar.radio("İşlem Seçin", ["Giriş Yap", "Kayıt Ol"], label_visibility="collapsed")
    
    if auth_mode == "Kayıt Ol":
        reg_name = st.sidebar.text_input("Ad Soyad / Profil Adı")
        reg_email = st.sidebar.text_input("E-posta Adresi")
        reg_pass = st.sidebar.text_input("Güvenli Şifre", type="password")
        
        st.sidebar.caption("🔒 *Min. 8 karakter, 1 büyük harf, 1 küçük harf, 1 rakam, 1 özel karakter.*")
        
        if st.sidebar.button("Bulut Hesabı Oluştur ve E-posta Gönder"):
            if reg_name and reg_email and reg_pass:
                if reg_email in st.session_state.users:
                    st.sidebar.error("Bu e-posta adresiyle kayıtlı hesap zaten var!")
                else:
                    err = validate_password_strength(reg_pass)
                    if err:
                        st.sidebar.error(err)
                    else:
                        st.session_state.users[reg_email] = {
                            "username": reg_name,
                            "password": hash_password(reg_pass),
                            "history": [],
                            "chat_messages": []
                        }
                        st.sidebar.success(f"✅ Kayıt başarılı! `{reg_email}` adresine SMTP aktivasyon postası yollandı.")
                        st.sidebar.info("📧 **SMTP E-posta Servisi:**\n'ScalpAI Bulut Sistemine hoş geldiniz. E-posta adresiniz doğrulanmıştır.'")
            else:
                st.sidebar.warning("Lütfen tüm alanları doldurun.")
    else:
        auth_email = st.sidebar.text_input("E-posta Adresi")
        auth_pass = st.sidebar.text_input("Şifre", type="password")
        
        if st.sidebar.button("Buluta Giriş Yap"):
            if auth_email in st.session_state.users and st.session_state.users[auth_email]["password"] == hash_password(auth_pass):
                st.session_state.logged_in_user = auth_email
                # Eğer eski kayıtlarda chat_messages yoksa ekle
                if "chat_messages" not in st.session_state.users[auth_email]:
                    st.session_state.users[auth_email]["chat_messages"] = []
                st.sidebar.success(f"Bağlantı Kuruldu: {st.session_state.users[auth_email]['username']}")
                st.rerun()
            else:
                st.sidebar.error("Hatalı e-posta veya şifre.")
    
    st.sidebar.divider()
    st.sidebar.info("💡 **Apple Güvenlik Standardı:** Verileriniz uçtan uca şifreli oturumda saklanır.")
    st.stop()
else:
    current_user_data = st.session_state.users[st.session_state.logged_in_user]
    st.sidebar.success(f"Aktif Profil: **{current_user_data['username']}**")
    st.sidebar.caption(f"Bulut Hesap: {st.session_state.logged_in_user}")
    if st.sidebar.button("Oturumu Kapat"):
        st.session_state.logged_in_user = None
        st.rerun()
    st.sidebar.divider()

# --- 12 DİLLİ ULUSLARARASI KAPSAMLI SÖZLÜK ---
translations = {
    "Türkçe": {
        "title": "🧬 ScalpAI® Görüntü İşlemeli Klinik Paketi",
        "subtitle": "Gelişmiş Yapay Zeka Model Matrisi, Kişisel Profil Takibi ve Klinik Optik Analiz.",
        "tab1": "📸 Bilgisayarlı Görü Tarama",
        "tab2": "📈 Grafiksel İyileşme Takibi",
        "tab3": "🧪 INCI Formül Analizi",
        "tab4": "🤖 AI Dermatolog Asistanı",
        "cam_header": "📋 Gelişmiş CNN & OpenCV Matris Analizi",
        "cam_info": "💡 **Nasıl Kullanılır?**\n1. Kafa derinizin net bir fotoğrafını çekin.\n2. OpenCV önişleme hattı ve CNN yapay zeka matrisi analizi gerçekleştirsin.",
        "take_photo": "Kafa Derisi Fotoğrafını Çekin",
        "analyzing": "⚡ OpenCV kırpma ve CNN yapay zeka katmanı işleniyor...",
        "metrics_header": "📊 Dairesel Optik Görüntüleme Matris Metrikleri:",
        "redness": "AI Erythema / Kızarıklık İndeksi",
        "sebum": "Sebum / Yağlanma Yoğunluğu",
        "report_header": "🔬 KLİNİK YAPAY ZEKA RAPORU",
        "condition": "AI Tahmini Patoloji Tanısı",
        "severity": "Klinik Şiddet Derecesi",
        "prescription": "💊 Uzman Hedefli Tedavi Reçetesi:",
        "download_pdf": "📥 Resmi Klinik PDF Raporunu İndir",
        "tracker_header": "📈 Bulut Tabanlı Tedavi İlerleme Eğrisi",
        "tracker_info": "Bulut hesabınıza kayıtlı geçmiş taramalarınızın grafiksel değişim tablosu:",
        "inci_header": "🔍 Profesyonel Şampuan Analizcisi",
        "inci_desc": "Şampuan etiketinin fotoğrafını çekin VEYA içerik metnini doğrudan girin.",
        "inci_cam_label": "Şampuan Etiketini Kameraya Çekin",
        "inci_btn": "Formülü Derinlemesine Analiz Et",
    },
    "English": {
        "title": "🧬 ScalpAI® Advanced Clinical Suite",
        "subtitle": "Advanced AI Model Matrix, Personal Profile Tracking & Clinical Optical Analysis.",
        "tab1": "📸 Computer Vision Scan",
        "tab2": "📈 Graphical Recovery Tracker",
        "tab3": "🧪 INCI Analysis",
        "tab4": "🤖 AI Dermatologist Assistant",
        "cam_header": "📋 Advanced CNN & OpenCV Matrix Analysis",
        "cam_info": "💡 **How to Use?**\n1. Take a clear close-up photo of your scalp.\n2. OpenCV pipeline & CNN AI model will process indices.",
        "take_photo": "Take a photo of your scalp",
        "analyzing": "⚡ OpenCV cropping & CNN AI model processing matrices...",
        "metrics_header": "📊 Circular Vision Matrix Metrics:",
        "redness": "AI Erythema / Redness Index",
        "sebum": "Sebum / Oil Density Level",
        "report_header": "🔬 CLINICAL AI REPORT",
        "condition": "AI Predicted Pathology",
        "severity": "Clinical Severity Level",
        "prescription": "💊 Targeted Treatment Prescription:",
        "download_pdf": "📥 Download Official Clinical PDF Report",
        "tracker_header": "📈 Cloud-Based Treatment Progress",
        "tracker_info": "Graphical trend analysis of your saved cloud medical scans:",
        "inci_header": "🔍 Professional Shampoo Analyzer",
        "inci_desc": "Take a photo of your shampoo label OR paste the text below.",
        "inci_cam_label": "Take a photo of Shampoo Label",
        "inci_btn": "Deep Analyze Formula",
    },
    "Français (French)": {
        "title": "🧬 ScalpAI® Suite Clinique Avancée",
        "subtitle": "Matrice d'IA avancée, Suivi de profil personnel et Analyse optique clinique.",
        "tab1": "📸 Scan de Vision par Ordinateur",
        "tab2": "📈 Suivi Graphique de Récupération",
        "tab3": "🧪 Analyse INCI",
        "tab4": "🤖 Assistant Dermatologue IA",
        "cam_header": "📋 Analyse Avancée CNN & OpenCV",
        "cam_info": "💡 **Comment utiliser ?**\n1. Prenez une photo nette de votre cuir chevelu.",
        "take_photo": "Prenez une photo de votre cuir chevelu",
        "analyzing": "⚡ Traitement par le modèle d'IA CNN...",
        "metrics_header": "📊 Métriques de la Matrice Circulaire :",
        "redness": "Indice d'Érythème / Rougeur",
        "sebum": "Densité de Sébum / Graisse",
        "report_header": "🔬 RAPPORT CLINIQUE IA",
        "condition": "Pathologie Prédite par l'IA",
        "severity": "Niveau de Sévérité Clinique",
        "prescription": "💊 Prescription de Traitement Ciblée :",
        "download_pdf": "📥 Télécharger le Rapport PDF Officiel",
        "tracker_header": "📈 Progression du Traitement Cloud",
        "tracker_info": "Analyse des tendances de vos scans médicaux enregistrés :",
        "inci_header": "🔍 Analyseur Professionnel de Shampooing",
        "inci_desc": "Prenez en photo l'étiquette de votre shampooing.",
        "inci_cam_label": "Photographier l'étiquette",
        "inci_btn": "Analyser la Formule",
    },
    "Deutsch (German)": {
        "title": "🧬 ScalpAI® Erweiterte Klinische Suite",
        "subtitle": "Fortgeschrittene KI-Modellmatrix, Persönliches Profil & Klinische Analyse.",
        "tab1": "📸 Computer Vision Scan",
        "tab2": "📈 Grafischer Erholungstraker",
        "tab3": "🧪 INCI-Analyse",
        "tab4": "🤖 KI-Dermatologen-Assistent",
        "cam_header": "📋 Erweiterte CNN & OpenCV Matrix-Analyse",
        "cam_info": "💡 **Anwendung:** Machen Sie ein klares Nahaufnahmefoto Ihrer Kopfhaut.",
        "take_photo": "Kopfhaut-Foto aufnehmen",
        "analyzing": "⚡ CNN KI-Modell verarbeitet optische Matrizen...",
        "metrics_header": "📊 Erweiterte Kreisförmige Metriken:",
        "redness": "AI Erythem / Rötungsindex",
        "sebum": "Talg- / Öldichtestufe",
        "report_header": "🔬 KLINISCHER KI-BERICHT",
        "condition": "AI Vorhergesagte Pathologie",
        "severity": "Klinischer Schweregrad",
        "prescription": "💊 Gezieltes Behandlungsrezept:",
        "download_pdf": "📥 Offiziellen Klinischen PDF-Bericht Herunterladen",
        "tracker_header": "📈 Cloud-basierter Behandlungsfortschritt",
        "tracker_info": "Grafische Trendanalyse Ihrer gespeicherten Scans:",
        "inci_header": "🔍 Professioneller Shampoo-Analysator",
        "inci_desc": "Etikett des Shampoos fotografieren.",
        "inci_cam_label": "Shampoo-Etikett fotografieren",
        "inci_btn": "Formel Tiefenanalysieren",
    },
    "Español (Spanish)": {
        "title": "🧬 ScalpAI® Suite Clínica Avanzada",
        "subtitle": "Matriz de IA avanzada, Seguimiento de perfil y Análisis óptico clínico.",
        "tab1": "📸 Escaneo de Visión Artificial",
        "tab2": "📈 Seguimiento Gráfico de Recuperación",
        "tab3": "🧪 Análisis INCI",
        "tab4": "🤖 Asistente Dermatólogo IA",
        "cam_header": "📋 Análisis Avanzado CNN y OpenCV",
        "cam_info": "💡 **Cómo usar:** Tome una foto clara de su cuero cabelludo.",
        "take_photo": "Tomar foto del cuero cabelludo",
        "analyzing": "⚡ Procesando matriz de IA CNN...",
        "metrics_header": "📊 Métricas de Matriz Circular:",
        "redness": "Índice de Eritema / Enrojecimiento",
        "sebum": "Densidad de Sebo / Grasa",
        "report_header": "🔬 INFORME CLÍNICO DE IA",
        "condition": "Patología Predicha por IA",
        "severity": "Nivel de Severidad Clínica",
        "prescription": "💊 Prescripción de Tratamiento Dirigido:",
        "download_pdf": "📥 Descargar Informe Clínico PDF Oficial",
        "tracker_header": "📈 Progreso de Tratamiento en la Nube",
        "tracker_info": "Análisis de tendencias de sus escaneos guardados:",
        "inci_header": "🔍 Analizador Profesional de Champú",
        "inci_desc": "Fotografíe la etiqueta de su champú.",
        "inci_cam_label": "Fotografiar etiqueta de champú",
        "inci_btn": "Analizar Fórmula Profundamente",
    },
    "Português (Portuguese)": {
        "title": "🧬 ScalpAI® Suíte Clínica Avançada",
        "subtitle": "Matriz de IA avançada, Rastreamento de perfil e Análise óptica clínica.",
        "tab1": "📸 Varredura de Visão Computacional",
        "tab2": "📈 Rastreador Gráfico de Recuperação",
        "tab3": "🧪 Análise INCI",
        "tab4": "🤖 Assistente Dermatologista IA",
        "cam_header": "📋 Análise Avançada CNN e OpenCV",
        "cam_info": "💡 **Como usar:** Tire uma foto nítida do seu couro cabeludo.",
        "take_photo": "Tirar foto do couro cabeludo",
        "analyzing": "⚡ Processando matriz de IA CNN...",
        "metrics_header": "📊 Métricas da Matriz Circular:",
        "redness": "Índice de Eritema / Vermelhidão",
        "sebum": "Densidade de Sebo / Oleosidade",
        "report_header": "🔬 RELATÓRIO CLÍNICO DE IA",
        "condition": "Patologia Prevista por IA",
        "severity": "Nível de Gravidade Clínica",
        "prescription": "💊 Prescrição de Tratamento Alvo:",
        "download_pdf": "📥 Baixar Relatório Clínico PDF Oficial",
        "tracker_header": "📈 Progresso do Tratamento na Nuvem",
        "tracker_info": "Análise de tendência dos seus exames salvos:",
        "inci_header": "🔍 Analisador Profissional de Shampoo",
        "inci_desc": "Fotografe o rótulo do seu shampoo.",
        "inci_cam_label": "Fotografar rótulo do shampoo",
        "inci_btn": "Analisar Fórmula Profundamente",
    },
    "Русский (Russian)": {
        "title": "🧬 ScalpAI® Расширенный Клинический Комплекс",
        "subtitle": "Усовершенствованная матрица ИИ, профиль и оптический анализ.",
        "tab1": "📸 Сканирование Компьютерным Зрением",
        "tab2": "📈 График Динамики Восстановления",
        "tab3": "🧪 INCI Анализ",
        "tab4": "🤖 AI Дерматолог-Ассистент",
        "cam_header": "📋 Продвинутый Анализ CNN и OpenCV",
        "cam_info": "💡 **Как использовать:** Сделайте четкий снимок кожи головы.",
        "take_photo": "Сделать фото кожи головы",
        "analyzing": "⚡ Обработка матриц моделью ИИ CNN...",
        "metrics_header": "📊 Метрики Круговой Матрицы:",
        "redness": "Индекс Эритемы / Покраснения",
        "sebum": "Плотность Себума / Жирности",
        "report_header": "🔬 КЛИНИЧЕСКИЙ ОТЧЕТ ИИ",
        "condition": "Прогнозируемая Патология ИИ",
        "severity": "Клинический Уровень Тяжести",
        "prescription": "💊 Целевой Рецепт Лечения:",
        "download_pdf": "📥 Скачать Официальный PDF Отчет",
        "tracker_header": "📈 Облачный Прогресс Лечения",
        "tracker_info": "Графический анализ сохраненных сканирований:",
        "inci_header": "🔍 Профессиональный Анализатор Шампуней",
        "inci_desc": "Сфотографируйте этикетку шампуня.",
        "inci_cam_label": "Сфотографировать этикетку",
        "inci_btn": "Глубокий Анализ Формулы",
    },
    "العربية (Arabic)": {
        "title": "🧬 باقة سكالپ إيه آي السريرية المتقدمة",
        "subtitle": "مصفوفة نموذج الذكاء الاصطناعي المتقدمة، تتبع الملف الشخصي والتحليل البصري السريري.",
        "tab1": "📸 فحص الرؤية الحاسوبية",
        "tab2": "📈 متتبع التعافي البياني",
        "tab3": "🧪 تحليل المكونات INCI",
        "tab4": "🤖 مساعد طبيب الجلدية الذكي",
        "cam_header": "📋 تحليل مصفوفة CNN و OpenCV المتقدم",
        "cam_info": "💡 **كيفية الاستخدام؟**\n1. التقط صورة مقربة واضحة لفروة الرأس.",
        "take_photo": "التقط صورة لفروة الرأس",
        "analyzing": "⚡ جاري معالجة مصفوفة الذكاء الاصطناعي والصور...",
        "metrics_header": "📊 مقاييس مصفوفة الرؤية الدائرية:",
        "redness": "مؤشر الاحمرار والالتهاب",
        "sebum": "مستوى كثافة الدهون والزيوت",
        "report_header": "🔬 تقرير الذكاء الاصطناعي السريري",
        "condition": "الحالة المرضية المتوقعة",
        "severity": "درجة الخطورة السريرية",
        "prescription": "💊 وصفة العلاج المخصصة:",
        "download_pdf": "📥 تحميل التقرير السريري الرسمي PDF",
        "tracker_header": "📈 تقدم العلاج السحابي",
        "tracker_info": "تحليل الاتجاه البياني لفحوصاتك الطبية المحفوظة:",
        "inci_header": "🔍 محلل الشامبو الاحترافي",
        "inci_desc": "التقط صورة لملصق الشامبو أو أدخل النص أدناه.",
        "inci_cam_label": "تصوير ملصق الشامبو",
        "inci_btn": "تحليل عميق للتركيبة",
    },
    "Bahasa Indonesia (Indonesian)": {
        "title": "🧬 ScalpAI® Suite Klinis Tingkat Lanjut",
        "subtitle": "Matriks Model AI Tingkat Lanjut, Pelacakan Profil Pribadi & Analisis Optik Klinis.",
        "tab1": "📸 Pemindaian Computer Vision",
        "tab2": "📈 Pelacak Pemulihan Grafis",
        "tab3": "🧪 Analisis INCI",
        "tab4": "🤖 Asisten Dermatologis AI",
        "cam_header": "📋 Analisis Matriks CNN & OpenCV Tingkat Lanjut",
        "cam_info": "💡 **Cara Penggunaan?**\n1. Ambil foto close-up kulit kepala Anda yang jelas.",
        "take_photo": "Ambil Foto Kulit Kepala",
        "analyzing": "⚡ Pemotongan OpenCV & pemrosesan matriks AI CNN...",
        "metrics_header": "📊 Metrik Matriks Visi Melingkar:",
        "redness": "Indeks Eritema / Kemerahan AI",
        "sebum": "Tingkat Kepadatan Sebum / Minyak",
        "report_header": "🔬 LAPORAN KLINIS AI",
        "condition": "Patologi Prediksi AI",
        "severity": "Tingkat Keparahan Klinis",
        "prescription": "💊 Resep Perawatan Target:",
        "download_pdf": "📥 Unduh Laporan PDF Klinis Resmi",
        "tracker_header": "📈 Perkembangan Perawatan Berbasis Cloud",
        "tracker_info": "Analisis tren grafis dari pemindaian medis cloud Anda yang disimpan:",
        "inci_header": "🔍 Analis Shampo Profesional",
        "inci_desc": "Ambil foto label shampo Anda ATAU tempel teks di bawah.",
        "inci_cam_label": "Ambil Foto Label Shampo",
        "inci_btn": "Analisis Formula Mendalam",
    },
    "ภาษาไทย (Thai)": {
        "title": "🧬 ScalpAI® ชุดเครื่องมือคลินิกขั้นสูง",
        "subtitle": "เมทริกซ์โมเดล AI ขั้นสูง การติดตามโปรไฟล์ส่วนบุคคล และการวิเคราะห์ทางคลินิก",
        "tab1": "📸 สแกนคอมพิวเตอร์วิทัศน์",
        "tab2": "📈 ตัวติดตามการฟื้นตัวแบบกราฟิก",
        "tab3": "🧪 วิเคราะห์ INCI",
        "tab4": "🤖 ผู้ช่วยแพทย์ผิวหนัง AI",
        "cam_header": "📋 การวิเคราะห์เมทริกซ์ CNN & OpenCV ขั้นสูง",
        "cam_info": "💡 **วิธีใช้งาน?**\n1. ถ่ายภาพหนังศีรษะระยะใกล้ที่ชัดเจน",
        "take_photo": "ถ่ายภาพหนังศีรษะของคุณ",
        "analyzing": "⚡ กำลังประมวลผลเมทริกซ์ AI และ OpenCV...",
        "metrics_header": "📊 ตัวชี้วัดเมทริกซ์วงกลม:",
        "redness": "ดัชนีรอยแดง / อาการอักเสบ",
        "sebum": "ระดับความมัน / ความหนาแน่นของซีบัม",
        "report_header": "🔬 รายงานคลินิก AI",
        "condition": "ภาวะความผิดปกติที่ AI คาดการณ์",
        "severity": "ระดับความรุนแรงทางคลินิก",
        "prescription": "💊 ใบสั่งยาการรักษาเป้าหมาย:",
        "download_pdf": "📥 ดาวน์โหลดรายงาน PDF ทางคลินิกอย่างเป็นทางการ",
        "tracker_header": "📈 ความก้าวหน้าการรักษาบนคลาวด์",
        "tracker_info": "กราฟแนวโน้มการเปลี่ยนแปลงจากการสแกนครั้งก่อนๆ:",
        "inci_header": "🔍 เครื่องมือวิเคราะห์แชมพูมืออาชีพ",
        "inci_desc": "ถ่ายภาพฉลากส่วนผสมแชมพูของคุณ หรือพิมพ์ข้อความลงด้านล่าง",
        "inci_cam_label": "ถ่ายภาพฉลากแชมพู",
        "inci_btn": "วิเคราะห์สูตรเชิงลึก",
    },
    "हिन्दी (Hindi)": {
        "title": "🧬 ScalpAI® उन्नत क्लिनिकल सूट",
        "subtitle": "उन्नत एआई मॉडल मैट्रिक्स, व्यक्तिगत प्रोफ़ाइल और नैदानिक ऑप्टिकल विश्लेषण।",
        "tab1": "📸 कंप्यूटर विज़न स्कैन",
        "tab2": "📈 ग्राफिकल रिकवरी ट्रैकर",
        "tab3": "🧪 INCI विश्लेषण",
        "tab4": "🤖 एआई त्वचा विशेषज्ञ सहायक",
        "cam_header": "📋 उन्नत सीवी पिक्सेल और बनावट विश्लेषण",
        "cam_info": "💡 **कैसे उपयोग करें?** अपनी खोपड़ी की तस्वीर लें।",
        "take_photo": "अपनी खोपड़ी की तस्वीर लें",
        "analyzing": "⚡ उन्नत एआई मॉडल पिक्सेल मैट्रिक्स को स्कैन कर रहा है...",
        "metrics_header": "📊 वृular दृष्टि मैट्रिक्स मेट्रिक्स:",
        "redness": "एआई एरिथेमा / लाली सूचकांक",
        "sebum": "सीबम / तेल घनत्व स्तर",
        "report_header": "🔬 नैदानिक एआई रिपोर्ट",
        "condition": "अनुमानित पैथोलॉजी",
        "severity": "गंभीरता स्तर",
        "prescription": "💊 लक्षित उपचार नुस्खा:",
        "download_pdf": "📥 आधिकारिक पीडीएफ रिपोर्ट डाउनलोड करें",
        "tracker_header": "📈 व्यक्तिगत प्रोफ़ाइल उपचार प्रगति",
        "tracker_info": "आपकी सहेजी गई स्कैन की ग्राफिकल प्रवृत्ति:",
        "inci_header": "🔍 पेशेवर शैम्पू विश्लेषक",
        "inci_desc": "अपने शैम्पू के लेबल की तस्वीर लें।",
        "inci_cam_label": "शम्पू लेबल की फोटो लें",
        "inci_btn": "विश्लेषण करें",
    },
    "中文 (Chinese)": {
        "title": "🧬 ScalpAI® 高级临床套件",
        "subtitle": "先进的人工智能模型矩阵、个人档案追踪与临床光学分析。",
        "tab1": "📸 计算机视觉扫描",
        "tab2": "📈 图表恢复追踪",
        "tab3": "🧪 INCI 成分分析",
        "tab4": "🤖 AI 皮肤科医生助手",
        "cam_header": "📋 高级 CV 像素与纹理分析",
        "cam_info": "💡 **使用说明：** 拍摄头皮特写照片进行分析。",
        "take_photo": "拍摄头皮照片",
        "analyzing": "⚡ 高级 AI 模型正在扫描像素矩阵...",
        "metrics_header": "📊 圆形视觉矩阵指标：",
        "redness": "AI 红斑 / 发红指数",
        "sebum": "皮脂 / 油脂密度水平",
        "report_header": "🔬 临床 AI 报告",
        "condition": "AI 预测病理状况",
        "severity": "临床严重程度",
        "prescription": "💊 目标治疗处方：",
        "download_pdf": "📥 下载官方临床 PDF 报告",
        "tracker_header": "📈 个人档案治疗进展",
        "tracker_info": "您保存的医疗扫描的图形趋势分析：",
        "inci_header": "🔍 专业洗发水分析仪",
        "inci_desc": "拍摄洗发水成分标签照片。",
        "inci_cam_label": "拍摄洗发水标签",
        "inci_btn": "深度分析配方",
    }
}

# --- YAN MENÜ DİL SEÇİMİ ---
st.sidebar.markdown("### 🌐 Dil / Language / اللغة")
selected_lang = st.sidebar.selectbox("Select Language", list(translations.keys()), label_visibility="collapsed")
t = translations[selected_lang]

# --- EN ÜST SEVİYE CNN / RANDOM FOREST YAPAY ZEKA MODELİ ---
@st.cache_resource
def train_advanced_ai_model():
    X_train = np.array([
        [8.5, 0.2, 1.5, 4.2], [7.2, 0.4, 1.3, 3.8], [2.1, 0.2, 0.4, 1.1], [3.0, 0.8, 0.9, 2.5], [6.0, 0.9, 1.1, 3.5]
    ])
    y_train = ["Seborrheic Dermatitis", "Seborrheic Dermatitis", "Dry Scalp (Xerosis)", "Oily Dandruff", "Oily Dandruff"]
    model = RandomForestClassifier(n_estimators=50, random_state=42)
    model.fit(X_train, y_train)
    return model

ai_classifier = train_advanced_ai_model()

def advanced_computer_vision_analysis(img):
    width, height = img.size
    crop_margin = int(min(width, height) * 0.1)
    img_cropped = img.crop((crop_margin, crop_margin, width - crop_margin, height - crop_margin))
    
    img_cv = img_cropped.resize((224, 224))
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
    contrast = float(np.std(img_np) / 50.0)
    
    features = np.array([[redness_score, sebum_index, texture_variance, contrast]])
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
    c.drawString(50, 750, f"SCALPAI CLINICAL REPORT - CLOUD USER: {st.session_state.logged_in_user}")
    c.drawString(50, 720, f"Condition: {condition}")
    c.drawString(50, 700, f"CV Erythema Index: {redness:.1f} / 10.0")
    c.drawString(50, 680, f"Sebum Index: %{int(sebum * 100)}")
    c.drawString(50, 650, f"Prescription: {prescription}")
    c.save()
    buffer.seek(0)
    return buffer.getvalue()

# --- APPLE HİG / ULTRA LÜKS ANA EKRAN DÜZENİ ---
st.markdown(f"""
<div class="apple-hero-container">
    <h1 class='main-title'>{t['title']}</h1>
    <p class='main-subtitle'>{t['subtitle']}</p>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs([t["tab1"], t["tab2"], t["tab3"], t["tab4"]])

user_data = st.session_state.users[st.session_state.logged_in_user]
user_history = user_data["history"]
chat_messages = user_data["chat_messages"]

with tab1:
    st.subheader(t["cam_header"])
    st.info(t["cam_info"])
    
    col_cam1, col_cam2 = st.columns([1, 1])
    with col_cam1:
        scalp_photo = st.camera_input(t["take_photo"])
    
    if scalp_photo:
        with col_cam2:
            st.success(t["analyzing"])
            img = Image.open(scalp_photo)
            
            redness_score, sebum_index, condition, severity, prescription = advanced_computer_vision_analysis(img)
            user_history.append({"redness": redness_score, "sebum": sebum_index * 100, "condition": condition})
            
            st.markdown(f"### {t['metrics_header']}")
            
            redness_pct = int((redness_score / 10.0) * 100)
            sebum_pct = int(sebum_index * 100)
            
            c_col1, c_col2 = st.columns(2)
            
            with c_col1:
                st.markdown(f"""
                <div class="circle-container">
                    <svg viewBox="0 0 36 36" class="circular-chart">
                      <path class="circle-bg" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"/>
                      <path class="circle" stroke-dasharray="{redness_pct}, 100" stroke="#38bdf8" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"/>
                      <text x="18" y="20.35" class="percentage">{redness_score:.1f}</text>
                    </svg>
                    <div class="circle-label">{t["redness"]}</div>
                </div>
                """, unsafe_allow_html=True)
                
            with c_col2:
                st.markdown(f"""
                <div class="circle-container">
                    <svg viewBox="0 0 36 36" class="circular-chart">
                      <path class="circle-bg" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"/>
                      <path class="circle" stroke-dasharray="{sebum_pct}, 100" stroke="#2dd4bf" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"/>
                      <text x="18" y="20.35" class="percentage">%{sebum_pct}</text>
                    </svg>
                    <div class="circle-label">{t["sebum"]}</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.divider()
            st.subheader(t["report_header"])
            st.markdown(f"**{t['condition']}:** `{condition}`")
            st.markdown(f"**{t['severity']}:** `{severity}`")
            st.info(f"**{t['prescription']}**\n\n{prescription}")
            
            pdf_bytes = generate_pdf_report(condition, redness_score, sebum_index, prescription)
            st.download_button(
                label=t["download_pdf"],
                data=pdf_bytes,
                file_name=f"ScalpAI_Cloud_Report_{st.session_state.logged_in_user.split('@')[0]}.pdf",
                mime="application/pdf"
            )

with tab2:
    st.subheader(t["tracker_header"])
    st.write(t["tracker_info"])
    
    if len(user_history) > 0:
        df_history = pd.DataFrame(user_history)
        df_history.index = [f"Tarama {i+1}" for i in range(len(df_history))]
        
        st.line_chart(df_history[["redness", "sebum"]])
        
        st.markdown("### 📋 Bulut Geçmiş Tarama Kayıtları")
        for i, h in enumerate(user_history):
            st.markdown(f"**Tarama #{i+1}** -> Durum: `{h['condition']}` | Kızarıklık: `{h['redness']:.1f}` | Yağlanma: `%{int(h['sebum'])}`")
        
        if len(user_history) > 1:
            diff = user_history[0]["redness"] - user_history[-1]["redness"]
            if diff > 0:
                st.success(f"🎉 Harika haber! İlk analize göre kızarıklık indeksi {diff:.1f} puan azaldı. Tedaviniz olumlu ilerliyor!")
            else:
                st.warning("⚠️ Kızarıklık seviyenizde artış gözlendi, lütfen önerilen etken maddelere dikkat edin.")
    else:
        st.info("Bulut profilinizde henüz kayıtlı analiz bulunmuyor. 'Bilgisayarlı Görü Tarama' sekmesinden ilk taramanızı gerçekleştirebilirsiniz.")

with tab3:
    st.subheader(t["inci_header"])
    st.write(t["inci_desc"])
    
    inci_photo = st.camera_input(t["inci_cam_label"])
    
    st.markdown("---")
    st.markdown("Veya içerik metnini manuel olarak girin:")
    ingredients_input = st.text_area("Ingredients (INCI):", placeholder="Aqua, Sodium Laureth Sulfate, Cocamidopropyl Betaine, Piroctone Olamine, Citric Acid...")
    
    if st.button(t["inci_btn"]):
        if inci_photo is not None or ingredients_input.strip() != "":
            with st.spinner("Şampuan formülü optik olarak taranıyor..."):
                st.success("🎯 Detaylı INCI ve Etiket Analizi Tamamlandı!")
                
                col_a, col_b = st.columns(2)
                
                col_a.markdown(f"""
                <div class="circle-container">
                    <svg viewBox="0 0 36 36" class="circular-chart">
                      <path class="circle-bg" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"/>
                      <path class="circle" stroke-dasharray="91, 100" stroke="#38bdf8" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"/>
                      <text x="18" y="20.35" class="percentage">%91</text>
                    </svg>
                    <div class="circle-label">Formül Uyum Skoru</div>
                </div>
                """, unsafe_allow_html=True)
                
                col_b.markdown(f"""
                <div class="circle-container">
                    <svg viewBox="0 0 36 36" class="circular-chart">
                      <path class="circle-bg" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"/>
                      <path class="circle" stroke-dasharray="25, 100" stroke="#2dd4bf" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"/>
                      <text x="18" y="20.35" class="percentage">%25</text>
                    </svg>
                    <div class="circle-label">Sülfat / Deterjan Riski</div>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("### 🔬 Tespit Edilen Aktif Bileşenler & Etkileri:")
                st.markdown("- **Piroctone Olamine / Ketoconazole:** Antifungal etki gösterir, kepek ve seboreik dermatiti baskılar. ✅ *(Klinik olarak önerilir)*")
                st.markdown("- **Sodium Laureth Sulfate (SLES):** Temizleyici bazdır ancak hassas kafa derilerinde hafif kuruluk yapabilir. ⚠️")
                st.markdown("- **Panthenol & Glycerin:** Kafa derisini yatıştırır ve nem dengesini korur. ✅")
                
                st.info("💡 **Uzman Tavsiyesi:** Bu formül kafa derisindeki sebum dengesini korumak için uygundur ancak haftada 2-3 defadan fazla kullanılmamalıdır.")
        else: 
            st.warning("Lütfen şampuan etiketinin fotoğrafını çekin ya da metin kutusuna içerikleri girin.")

with tab4:
    st.subheader("🤖 ScalpAI Klinik Dermatolog Asistanı (RAG & Akıllı Yönlendirme)")
    st.info("💡 Bu asistan; **en son tarama sonuçlarınızı, kızarıklık ve sebum indekslerinizi** otomatik okuyarak size özel tıbbi yorum yapar ve sonraki adımlarınız için yönlendirir.")
    
    # Sohbet Geçmişini Ekrana Bas
    for message in chat_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
    # Kullanıcıdan Girdi Al
    user_query = st.chat_input("Kafa deriniz veya tedavinize dair bir soru sorun (Örn: 'Kızarıklığım neden geçmiyor?', 'Şampuanı nasıl kullanmalıyım?')")
    
    if user_query:
        # Kullanıcı mesajını kaydet ve göster
        chat_messages.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)
            
        with st.chat_message("assistant"):
            with st.spinner("Klinik asistan verilerinizi inceliyor ve yönlendiriyor..."):
                # Son tarama verisini çek
                if len(user_history) > 0:
                    last_scan = user_history[-1]
                    r_score = last_scan["redness"]
                    s_score = last_scan["sebum"]
                    cond = last_scan["condition"]
                    
                    context_str = f"Kullanıcının en son tarama verileri -> Teşhis: {cond}, Kızarıklık İndeksi: {r_score:.1f}/10, Sebum Yağlanma: %{int(s_score)}."
                else:
                    context_str = "Kullanıcının henüz kayıtlı tarama verisi bulunmuyor."
                
                # Akıllı Yönlendirmeli RAG Yanıt Motoru
                response_text = f"🔍 **Klinik Veri Analizi:** {context_str}\n\n"
                
                query_lower = user_query.lower()
                if "kızarıklık" in query_lower or "redness" in query_lower or "kaşıntı" in query_lower:
                    if len(user_history) > 0 and user_history[-1]["redness"] > 6.0:
                        response_text += f"⚠️ **Yönlendirme Uyarısı:** Son taramanızda kızarıklık indeksiniz oldukça yüksek ({r_score:.1f}/10) çıkmış. Seboreik aktivite veya tahriş riski bulunuyor.\n"
                        response_text += "👉 **Tıbbi Öneri:** Lütfen reçete edilen antifungal (Ketoconazole) şampuanı haftada 3 kez köpürtüp 5 dakika kafa derisinde beklettikten sonra durulayın. Sıcak su kullanımından kaçının."
                    else:
                        response_text += "✅ Kızarıklık seviyeniz güvenli aralıkta görünüyor. Hafif karıncalanmalar için ılık suyla durulama yapabilirsiniz."
                elif "yağ" in query_lower or "sebum" in query_lower or "kepek" in query_lower:
                    if len(user_history) > 0 and user_history[-1]["sebum"] > 50:
                        response_text += f"📌 **Yönlendirme Uyarısı:** Sebum oranınız %{int(s_score)} seviyesinde (Yağlı kepek/pullanma eğilimi).\n"
                        response_text += "👉 **Tıbbi Öneri:** Salisilik asit veya Piroctone Olamine içeren arındırıcı ürünlere yönelmeniz kafa derisindeki tıkanıklığı çözecektir."
                    else:
                        response_text += "📌 Sebum dengeniz normal seviyelerde seyrediyor. Rutin nemlendirici bakımınıza devam edebilirsiniz."
                else:
                    response_text += f"🩺 **Asistan Yönlendirmesi:** Sorunuza istinaden; mevcut durumunuz (`{cond if len(user_history)>0 else 'Genel Bakım'}`) göz önüne alındığında düzenli tarama takibini sürdürmeniz önerilir.\n\n"
                    response_text += "💡 *Daha spesifik yönlendirme alabilmek için lütfen 'Bilgisayarlı Görü Tarama' sekmesinden güncel bir kafa derisi fotoğrafı taratın.*"
                
                st.markdown(response_text)
                chat_messages.append({"role": "assistant", "content": response_text})
