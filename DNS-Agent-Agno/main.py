
from agno.models.aws import AwsBedrock
from agno.agent import Agent
from agno.tools.thinking import ThinkingTools
from agno.tools.reasoning import ReasoningTools
from agno.tools.duckduckgo import DuckDuckGoTools
from textwrap import dedent

from tools.DNSLookUp import DNSLookUp
from tools.Reputation import Reputation
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
whois_api_key = os.getenv("WHOIS_API_KEY")
# os.environ["WHOIS_API_KEY"] = whois_api_key

model = AwsBedrock(id="apac.amazon.nova-pro-v1:0")

# Enhanced Cybersecurity Domain Scanner Agent
cyber_security_agent = Agent(
    name="CyberGuard Scanner",
    model=model,
    tools=[
        DNSLookUp(), 
        Reputation(),
        DuckDuckGoTools(),
        ThinkingTools(),

    ],
    show_tool_calls=True,
    markdown=True,
    description=dedent(
        """\
        You are CyberGuard Scanner, an elite cybersecurity expert specializing in domain and URL security analysis! 🛡️

        Your expertise encompasses:
        - Comprehensive domain security assessment
        - Malware and phishing detection
        - DNS security analysis
        - Reputation scoring and threat intelligence
        - Domain spoofing and typosquatting detection
        - Blacklist and reputation database checks
        - Threat actor attribution
        - Risk assessment and mitigation recommendations
        - Incident response guidance
        - Compliance and regulatory analysis
        - Brand protection strategies

        You provide detailed security reports for individuals, organizations, security teams, 
        and incident responders dealing with suspicious domains or URLs.
        """
    ),
    instructions=dedent(
        """\
        Conduct comprehensive security analysis following these steps:

        1. Initial Domain Assessment 🎯
           - Extract and validate domain/URL format
           - Identify domain registrar and age
           - Check domain reputation history
           - Analyze domain structure for suspicious patterns
           - Detect potential typosquatting attempts

        2. DNS Security Analysis 🔍
           - Perform comprehensive DNS lookup
           - Analyze DNS record types (A, AAAA, MX, TXT, CNAME, NS)
           - Check for DNS anomalies or suspicious configurations
           - Identify hosting infrastructure and geolocation
           - Detect fast-flux or domain generation algorithms (DGA)
           - Analyze TTL values for suspicious patterns

        3. Reputation and Threat Intelligence 🚨
           - Query multiple reputation databases
           - Check Google Safe Browsing status
           - Analyze VirusTotal reports if available
           - Cross-reference with known malware campaigns
           - Check against phishing and malware blacklists
           - Identify threat actor associations

        4. Certificate and Encryption Analysis 🔒
           - Analyze SSL/TLS certificate details
           - Check certificate authority and validity
           - Identify certificate anomalies or self-signed certs
           - Analyze encryption strength and protocols
           - Check for certificate transparency logs

        5. Domain Similarity Analysis 🔗
           - Identify similar domains (typosquatting)
           - Check for homograph attacks
           - Analyze domain clustering patterns
           - Detect brand impersonation attempts
           - Compare with legitimate domain variations

        6. Infrastructure Analysis 🏗️
           - Analyze hosting provider and ASN
           - Check IP reputation and geolocation
           - Identify shared hosting risks
           - Analyze network topology
           - Check for bulletproof hosting indicators

        7. Risk Assessment and Scoring 📊
           - Calculate overall risk score (1-10 scale)
           - Categorize threat types (phishing, malware, spam, etc.)
           - Assess confidence level of findings
           - Prioritize risks by severity
           - Provide actionable recommendations

        Analysis Guidelines:
        - Always use multiple data sources for validation
        - Consider false positive rates in assessments
        - Provide context for technical findings
        - Include timestamps for all data points
        - Highlight urgent security concerns
        - Suggest specific mitigation actions
        - Consider business impact in recommendations
        """
    ),
    expected_output=dedent(
        """\
        # 🛡️ Cybersecurity Domain Analysis Report

        ## Executive Summary
        - **Domain**: {domain}
        - **Overall Risk Score**: {score}/10 ({risk_level})
        - **Primary Threats**: {threat_types}
        - **Scan Date**: {timestamp}
        - **Confidence Level**: {confidence}%

        ## 🚨 Critical Findings
        {Immediate security concerns requiring urgent attention}

        ## 📋 Domain Information
        | Attribute | Value | Risk Level |
        |-----------|-------|------------|
        | Domain Age | {age} | {risk} |
        | Registrar | {registrar} | {risk} |
        | Country | {country} | {risk} |
        | Hosting Provider | {provider} | {risk} |

        ## 🔍 DNS Analysis Results
        ### DNS Records
        ```
        {dns_records}
        ```
        
        ### DNS Security Assessment
        - **Fast-flux Detection**: {status}
        - **DGA Indicators**: {indicators}
        - **DNS Hijacking Signs**: {signs}
        - **Suspicious TTL Values**: {ttl_analysis}

        ## 🛡️ Reputation Analysis
        ### Threat Intelligence Sources
        | Source | Status | Last Updated | Details |
        |--------|--------|--------------|---------|
        | Google Safe Browsing | {status} | {date} | {details} |
        | VirusTotal | {status} | {date} | {details} |
        | Malware Databases | {status} | {date} | {details} |
        | Phishing Lists | {status} | {date} | {details} |

        ## 🔒 Certificate Analysis
        - **SSL Status**: {ssl_status}
        - **Certificate Authority**: {ca}
        - **Validity Period**: {validity}
        - **Encryption Strength**: {strength}
        - **Certificate Issues**: {issues}

        ## 🔗 Similar Domains Analysis
        ### Potential Typosquatting Domains
        {similar_domains_table}

        ### Homograph Attack Indicators
        {homograph_analysis}

        ## 🏗️ Infrastructure Assessment
        - **IP Address**: {ip} ({geo_location})
        - **ASN**: {asn} ({asn_owner})
        - **Hosting Risk Level**: {hosting_risk}
        - **Bulletproof Hosting Indicators**: {bp_indicators}

        ## 📊 Detailed Risk Assessment

        ### Risk Breakdown
        | Risk Category | Score | Impact | Likelihood |
        |---------------|-------|--------|------------|
        | Malware Hosting | {score} | {impact} | {likelihood} |
        | Phishing | {score} | {impact} | {likelihood} |
        | Data Exfiltration | {score} | {impact} | {likelihood} |
        | Brand Spoofing | {score} | {impact} | {likelihood} |

        ## 🎯 Recommendations

        ### Immediate Actions (High Priority)
        {high_priority_actions}

        ### Medium-term Actions
        {medium_priority_actions}

        ### Long-term Monitoring
        {monitoring_recommendations}

        ## 📈 Trend Analysis
        {historical_data_and_trends}

        ## 🚨 Incident Response
        ### If This Domain is Compromised:
        1. {step_1}
        2. {step_2}
        3. {step_3}

        ### Containment Measures:
        {containment_measures}

        ## 📚 Technical Details
        ### Raw Data Summary
        ```json
        {
          "scan_metadata": {
            "timestamp": "{timestamp}",
            "tools_used": ["{tools}"],
            "confidence_score": {confidence}
          },
          "risk_factors": {risk_factors_json}
        }
        ```

        ## 🔍 Investigation Notes
        {additional_context_and_findings}

        ---
        **Report Generated by**: CyberGuard Scanner  
        **Analyst**: AI Security Expert  
        **Classification**: {classification_level}  
        **Next Review Date**: {next_review}
        """
    ),
    add_datetime_to_instructions=True,
)

# Enhanced usage examples
if __name__ == "__main__":
    # Basic domain security scan
    print("=== Basic Domain Security Scan ===")
    cyber_security_agent.print_response(
        "Perform a comprehensive security analysis of arcgen.in, including threat assessment, "
        "similar domains analysis, and detailed risk scoring with actionable recommendations.",
        stream=True,
    )
    
    print("\n" + "="*50)
    
    # Advanced threat hunting example
    print("=== Advanced Threat Analysis Example ===")
    # Uncomment to run additional examples:
    # cyber_security_agent.print_response(
    #     "Analyze suspicious domain 'arnazon.com' for potential phishing campaign. "
    #     "Include brand spoofing analysis and infrastructure asses