import os
from fpdf import FPDF

# Create data directory
os.makedirs("data", exist_ok=True)

# Generate 14 Markdown/Text files
kb_content = [
    ("data/faq_login.md", "# Login FAQ\n\nQ: How do I reset my password?\nA: Go to the login page and click 'Forgot Password'. You will receive an email with a reset link. If you do not receive the email, check your spam folder or contact support."),
    ("data/api_rate_limits.txt", "API Rate Limits Documentation\n\nOur API has a strict rate limit to ensure fair usage.\nFree Tier: 100 requests per minute.\nPro Tier: 1000 requests per minute.\nEnterprise Tier: Custom limits.\n\nWhen a rate limit is exceeded, the API returns a 429 Too Many Requests status code. Please implement exponential backoff in your application to handle this."),
    ("data/billing_policy.md", "# Billing Policy\n\nSubscriptions are billed on a monthly or annual basis. You can cancel at any time, but we do not offer refunds for partial months. If your credit card fails, we will retry 3 times over 7 days before suspending the account."),
    ("data/troubleshooting_sso.md", "# SSO Troubleshooting Guide\n\nIf Single Sign-On (SSO) is failing:\n1. Ensure your IdP configuration has the correct Reply URL.\n2. Verify the SAML certificate has not expired.\n3. Check that the user's email domain matches the approved list.\n4. Review the audit logs in the admin dashboard for detailed SAML assertion errors."),
    ("data/downtime_sla.txt", "Service Level Agreement (SLA) & Uptime\n\nWe guarantee 99.9% uptime for Pro and Enterprise customers. In the event of downtime exceeding this SLA in a given month, customers are eligible for service credits proportional to the downtime. Please contact billing support to claim your credits. Note: Scheduled maintenance does not count towards downtime."),
    ("data/webhook_setup.md", "# Setting Up Webhooks\n\nTo receive real-time events:\n1. Go to Developer Settings > Webhooks.\n2. Click 'Add Endpoint'.\n3. Enter your HTTPS URL.\n4. Select the events you wish to subscribe to.\n5. Save. Ensure your endpoint responds with a 2xx status code within 3 seconds, or the delivery will be marked as failed and retried."),
    ("data/data_retention.md", "# Data Retention Policy\n\nAccount data is retained for as long as your account is active. Upon account deletion, all customer data is permanently removed within 30 days. Backup logs are retained for 90 days for compliance purposes. If you need a data export, please use the 'Export Data' tool before deleting your account."),
    ("data/mobile_app_crash.md", "# Mobile App Crashing Issues\n\nIf the mobile app is crashing on launch:\n1. Ensure you are on the latest version of iOS or Android.\n2. Clear the app cache in your device settings.\n3. Uninstall and reinstall the app.\nIf the issue persists, please send us the crash logs from your device."),
    ("data/upgrade_plan.txt", "How to Upgrade Your Plan\n\nTo upgrade from Free to Pro:\n1. Navigate to Account Settings > Billing.\n2. Click 'Upgrade Plan'.\n3. Select 'Pro' and choose Monthly or Annual billing.\n4. Enter your payment details.\nThe new features will be available immediately upon successful payment."),
    ("data/security_compliance.md", "# Security and Compliance\n\nOur platform is SOC 2 Type II compliant and fully GDPR compliant. Data in transit is encrypted using TLS 1.2+, and data at rest is encrypted using AES-256. For access to our full SOC 2 report, please contact our compliance team under NDA."),
    ("data/api_authentication.md", "# API Authentication\n\nAuthenticate API requests using Bearer tokens. Include the token in the Authorization header: `Authorization: Bearer YOUR_API_KEY`.\nAPI keys can be generated in the Developer Dashboard. Never share or commit your API keys. If a key is compromised, revoke it immediately and generate a new one."),
    ("data/integration_salesforce.md", "# Salesforce Integration Guide\n\nConnect our platform to Salesforce to sync contacts and leads automatically.\n1. Go to Integrations > Salesforce.\n2. Click 'Connect'.\n3. Log in to your Salesforce account and authorize the application.\n4. Map the desired fields between the platforms.\n5. Enable the sync toggle. Synchronization runs every 15 minutes."),
    ("data/account_suspension.txt", "Account Suspension Policy\n\nAccounts may be suspended for violations of our Terms of Service, including but not limited to: sending spam, hosting malicious content, or excessive abuse of our API. If you believe your account was suspended in error, please reply to the suspension email to appeal."),
    ("data/performance_tuning.md", "# Performance Tuning and Best Practices\n\nTo maximize performance:\n- Use pagination for all API list requests (e.g., limit=50, offset=0).\n- Only request the fields you need using the `fields` query parameter.\n- Cache static responses on your end to reduce API calls.\n- Use the bulk API endpoints when creating or updating multiple records simultaneously.")
]

for filepath, content in kb_content:
    with open(filepath, "w") as f:
        f.write(content)

# Generate 1 PDF file
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Enterprise Support Guide', 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

pdf = PDF()
pdf.add_page()
pdf.set_font('Arial', '', 12)
pdf_content = """
Enterprise Support & Escalation Procedures

Welcome to Enterprise Support.
As an enterprise customer, you have access to 24/7 priority support and a dedicated Technical Account Manager (TAM).

Support Tiers:
Tier 1: General inquiries, how-to questions, basic troubleshooting.
Tier 2: Advanced technical issues, API debugging, integrations.
Tier 3: Critical bugs, system outages, architecture reviews.

Response Time SLAs:
- Critical (System Down): 1 hour
- High (Significant Impact): 4 hours
- Normal (General Questions): 12 hours

Escalation Matrix:
If your issue is not resolved within the SLA, you can escalate it directly to your TAM or to the Director of Support via the contact details provided in your onboarding packet.

Custom Feature Requests:
Enterprise customers can request custom features. These requests are reviewed by our Product Management team quarterly.
"""
for line in pdf_content.split('\n'):
    if line.strip() == "":
        pdf.ln(10)
    else:
        pdf.cell(200, 10, txt=line.strip()[:80], new_x="LMARGIN", new_y="NEXT")

pdf.output('data/enterprise_support_guide.pdf')

print("Successfully generated knowledge base files.")
