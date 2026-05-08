import streamlit as st
import json
import time
import os
import sys
from pathlib import Path

# --- NEW: PATH FIX FOR CLOUD DEPLOYMENT ---
# This adds the 'src' directory to the system path so modules are found
current_dir = Path(__file__).parent.parent
sys.path.append(str(current_dir))

# --- CLOUD SECURITY GATE ---
if "GOOGLE_API_KEY" in st.secrets:
    os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]
if "SERPER_API_KEY" in st.secrets:
    os.environ["SERPER_API_KEY"] = st.secrets["SERPER_API_KEY"]

from datetime import datetime
# Change this import to be relative or ensure the path fix above is active
from my_research_agent.crew import MyResearchAgent


# --- 2026 AERO-MODERN CONFIG ---
st.set_page_config(
    page_title="Venture Intel 2026",
    page_icon="⚡",
    layout="wide"
)

# --- TRENDY GLASSMORPHIC CSS (2026 AESTHETIC) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=JetBrains+Mono:wght@400;500&display=swap');
    
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    code { font-family: 'JetBrains+Mono', monospace; }

    /* Dark Mode Glassmorphism Theme */
    .main { background: radial-gradient(circle at top left, #0d1117, #010409); color: #e6edf3; }
    
    .agent-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }

    .stButton>button {
        background: linear-gradient(90deg, #007cf0, #00dfd8);
        border: none;
        border-radius: 12px;
        color: white;
        font-weight: 600;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
        height: 3.5rem;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(0, 124, 240, 0.3);
        color: white;
    }

    /* Agent Status Tags */
    .agent-tag {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        margin-bottom: 10px;
    }
    
    .tag-scout { background: rgba(0, 223, 216, 0.2); color: #00dfd8; border: 1px solid #00dfd8; }
    .tag-arch { background: rgba(191, 0, 255, 0.2); color: #bf00ff; border: 1px solid #bf00ff; }
    .tag-audit { background: rgba(255, 124, 0, 0.2); color: #ff7c00; border: 1px solid #ff7c00; }
    
    h1 { background: -webkit-linear-gradient(#fff, #888); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.title("⚡ VENTURE INTELLIGENCE SUITE")
st.markdown("##### <span style='color:#888'>SYSTEM STATUS: READY // MULTI-AGENT CORE ACTIVE</span>", unsafe_allow_html=True)
st.divider()

# --- INPUT SECTION ---
with st.container():
    col_input, col_btn = st.columns([3, 1])
    with col_input:
        product_concept = st.text_input(
            "Target Venture/Solution Concept", 
            placeholder="e.g., AI Voice Agents for HR in 2026"
        )
    with col_btn:
        st.write("##") # Buffer for alignment
        run_button = st.button("RUN DEEP ANALYSIS")

# --- BACKEND ARCHITECTURE PREVIEW ---
st.markdown("### 🛠️ MULTI-AGENT ARCHITECTURE")
a1, a2, a3 = st.columns(3)
with a1:
    st.markdown('<div class="agent-card"><span class="agent-tag tag-scout">Agent 1: Data Scout</span><br><b>Task:</b> Identifying market competitors and technical benchmarks.</div>', unsafe_allow_html=True)
with a2:
    st.markdown('<div class="agent-card"><span class="agent-tag tag-arch">Agent 2: Architect</span><br><b>Task:</b> Modeling TAM/SAM/SOM and financial unit economics.</div>', unsafe_allow_html=True)
with a3:
    st.markdown('<div class="agent-card"><span class="agent-tag tag-audit">Agent 3: Auditor</span><br><b>Task:</b> Validating risk factors and final investment thesis.</div>', unsafe_allow_html=True)

# --- EXECUTION PIPELINE ---
if run_button:
    if not product_concept:
        st.error("Missing Venture Concept. Please enter a topic.")
    else:
        # Modern Status Pipeline (2026 Style)
        with st.status("🛠️ **EXECUTING MULTI-AGENT PIPELINE...**", expanded=True) as status:
            try:
                # 1. Initialize Scout Phase
                st.write("🕵️ **AGENT 1: DATA SCOUT** - Scouring global search indexes...")
                time.sleep(1.5) # Narrative delay for UI effect
                
                inputs = {
                    'product_concept': product_concept, 
                    'current_year': str(datetime.now().year)
                }
                
                # Kickoff CrewAI Backend
                result = MyResearchAgent().crew().kickoff(inputs=inputs)
                data = result.pydantic
                
                # 2. Architect Phase
                st.write("📐 **AGENT 2: FINANCIAL ARCHITECT** - Processing raw signals into economic models...")
                time.sleep(1.5)
                
                # 3. Auditor Phase
                st.write("⚖️ **AGENT 3: STRATEGIC AUDITOR** - Stress-testing findings against market risks...")
                time.sleep(1.5)
                
                status.update(label="🚀 **DUE DILIGENCE VERIFIED**", state="complete", expanded=False)
                
                # --- RESULTS DISPLAY ---
                st.divider()
                st.header("I. Strategic Overview")
                st.success(f"**Investment Thesis:** {data.investment_thesis}")
                
                # Market Metrics
                m1, m2, m3 = st.columns(3)
                m1.metric("TAM", data.market_sizing.tam)
                m2.metric("SAM", data.market_sizing.sam)
                m3.metric("SOM (Y1)", data.market_sizing.som)
                
                st.divider()

                # --- COMPETITOR MATRIX (Safe-Access Fix for 'name' error) ---
                st.header("II. Competitor Landscape")
                comp_cols = st.columns(len(data.top_competitors))
                
                for idx, comp in enumerate(data.top_competitors):
                    # Fixed access: handle both dictionaries and Pydantic objects safely
                    c_name = getattr(comp, 'name', comp.get('name', 'Unknown'))
                    c_val = getattr(comp, 'value_proposition', comp.get('value_proposition', 'N/A'))
                    c_weak = getattr(comp, 'weakness', comp.get('weakness', 'N/A'))
                    
                    with comp_cols[idx]:
                        st.markdown(f"""
                        <div class="agent-card">
                            <h4 style="color:#00dfd8">📍 {c_name}</h4>
                            <p style="font-size:0.9rem"><b>Value Prop:</b> {c_val}</p>
                            <p style="font-size:0.9rem; color:#ff4b4b"><b>Vulnerability:</b> {c_weak}</p>
                        </div>
                        """, unsafe_allow_html=True)
                
                # --- RISK AUDIT & MEMO ---
                st.header("III. Risk Audit & Mitigation")
                for r in data.strategic_risks:
                    with st.expander(f"⚠️ {r.risk_factor} (Impact: {r.impact})"):
                        st.write(f"**Mitigation Strategy:** {r.mitigation_strategy}")

                st.divider()
                memo_md = f"# VC MEMO: {product_concept.upper()}\n\n{data.investment_thesis}"
                st.download_button("📥 DOWNLOAD VENTURE MEMO (.md)", memo_md, file_name=f"memo_{product_concept.replace(' ', '_')}.md")

            except Exception as e:
                status.update(label="❌ **PIPELINE FAILURE**", state="error")
                st.error(f"Execution Error: {str(e)}")