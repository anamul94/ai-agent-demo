import streamlit as st
from main import cyber_security_agent

st.set_page_config(page_title="CyberGuard Scanner", layout="wide", page_icon="🛡️")

# Header
st.title("🛡️ CyberGuard Scanner")

st.markdown(
    "An advanced cybersecurity analysis platform that performs comprehensive domain and URL security assessments. "
    "CyberGuard Scanner analyzes threat intelligence, DNS security, SSL certificates, reputation databases, "
    "and detects phishing, malware, typosquatting, and other cyber threats with actionable security recommendations."
)

# Main input area
default_query = (
    "Perform a comprehensive security analysis of arcgen.in, including threat assessment, "
    "similar domains analysis, DNS security evaluation, SSL certificate validation, "
    "reputation scoring, and detailed risk assessment with actionable recommendations."
)

# Use example query if selected, otherwise use default
query_value = st.session_state.get('query_to_use', default_query)

query = st.text_area(
    "🔍 Security Analysis Request",
    value=query_value,
    height=120,
    key="main_query"
)

# Clear the session state after using it
if 'query_to_use' in st.session_state:
    del st.session_state.query_to_use

# Scan button
if st.button("🛡️ Start Security Scan", type="primary"):
    with st.spinner("🔍 Analyzing domain security..."):
        try:
            # Execute security scan
            security_report = cyber_security_agent.run(query)

            # Display results
            st.subheader("📋 Security Analysis Report")
            st.markdown(security_report.content)

        except Exception as e:
            st.error(f"❌ Security scan failed: {str(e)}")
            st.error("Please check your internet connection and ensure the domain/URL is accessible.")

# Sidebar with helpful information
with st.sidebar:
    st.header("🎯 How to Use CyberGuard Scanner")
    st.markdown("""
    ### Include in your security request:
    - **Domain or URL** to analyze
    - **Analysis type** (basic, comprehensive, threat hunting)
    - **Specific concerns** (phishing, malware, spoofing)
    - **Analysis depth** (DNS, SSL, reputation, infrastructure)
    - **Brand protection** needs
    - **Incident response** requirements
    """)
    
    st.header("📝 Example Security Requests")
    
    # Pre-defined examples
    example1 = "Analyze suspicious domain 'paypaI-security.com' for phishing indicators, brand spoofing, and credential harvesting threats with detailed risk assessment."
    
    example2 = "Perform comprehensive security analysis of 'free-downloads-software.tk' including malware hosting detection, infrastructure assessment, and bulletproof hosting indicators."
    
    example3 = "Investigate 'amazon-prize-winner.org' for scam indicators, typosquatting analysis, similar domains detection, and brand abuse assessment."
    
    example4 = "Emergency security analysis of potentially compromised domain 'company-internal-portal.net' with incident response guidance and containment measures."
    
    # Example buttons
    if st.button("🎣 Phishing Analysis", help="Analyze potential phishing domain"):
        st.session_state.example_query = example1
        
    if st.button("🦠 Malware Detection", help="Scan for malware hosting"):
        st.session_state.example_query = example2
        
    if st.button("🏷️ Brand Protection", help="Check for brand spoofing"):
        st.session_state.example_query = example3
        
    if st.button("🚨 Incident Response", help="Emergency security analysis"):
        st.session_state.example_query = example4

    # Load example into text area if selected
    if 'example_query' in st.session_state:
        st.text_area("Selected Example:", value=st.session_state.example_query, height=100, disabled=True)
        if st.button("📋 Use This Example"):
            st.session_state.query_to_use = st.session_state.example_query
            st.rerun()
    
    st.markdown("---")
    
    # Quick scan options
    st.header("⚡ Quick Scan Options")
    domain_input = st.text_input("Enter Domain/URL:", placeholder="example.com")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔍 Quick Scan"):
            if domain_input:
                quick_query = f"Perform a quick security analysis of {domain_input} with basic threat assessment and risk scoring."
                with st.spinner("Running quick scan..."):
                    try:
                        result = cyber_security_agent.run(quick_query)
                        st.success("✅ Quick scan completed!")
                        with st.expander("📊 Quick Scan Results"):
                            st.markdown(result.content)
                    except Exception as e:
                        st.error(f"Quick scan failed: {str(e)}")
            else:
                st.warning("Please enter a domain or URL")
    
    with col2:
        if st.button("🎯 Deep Scan"):
            if domain_input:
                deep_query = f"Perform comprehensive deep security analysis of {domain_input} including DNS security, SSL analysis, reputation check, similar domains, infrastructure assessment, and detailed threat intelligence with actionable recommendations."
                with st.spinner("Running deep scan..."):
                    try:
                        result = cyber_security_agent.run(deep_query)
                        st.success("✅ Deep scan completed!")
                        with st.expander("🔬 Deep Scan Results"):
                            st.markdown(result.content)
                    except Exception as e:
                        st.error(f"Deep scan failed: {str(e)}")
            else:
                st.warning("Please enter a domain or URL")
    
    st.markdown("---")
    
    # Threat categories
    st.header("🚨 Threat Categories")
    st.markdown("""
    **CyberGuard Scanner detects:**
    - 🎣 **Phishing** - Credential harvesting sites
    - 🦠 **Malware** - Malicious software hosting
    - 🏷️ **Brand Spoofing** - Trademark infringement
    - 📧 **Spam** - Unwanted email sources
    - 🔒 **SSL Issues** - Certificate problems
    - 🌐 **DNS Anomalies** - Suspicious configurations
    - 🏗️ **Infrastructure** - Bulletproof hosting
    - 🎭 **Typosquatting** - Domain name abuse
    """)
    
    st.markdown("---")
    
    # Disclaimer
    st.caption("**Security Disclaimer:** This tool provides cybersecurity analysis based on threat intelligence and security best practices. Results should be verified through additional security tools and professional assessment. Not responsible for false positives or missed threats.")
    
    st.caption("**Privacy Notice:** Domain queries may be logged for security research purposes. Do not submit sensitive or confidential domains.")