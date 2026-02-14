import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Direct PDF link from Delhi High Court
url = "https://lobis.nic.in/ddir/dhc/SAN/judgement/12-10-2023/SAN12102023CRLMM23102023_123816.pdf"
filename = "real_judgment.pdf"

print("Downloading Delhi High Court judgment...")
try:
    response = requests.get(url, verify=False, timeout=60)
    
    # Check if it's actually a PDF
    if response.content[:4] == b'%PDF':
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"✅ Downloaded valid PDF: {filename}")
        print(f"   Size: {len(response.content)} bytes")
    else:
        print("❌ Not a PDF file")
        print("First 100 characters:", response.content[:100])
except Exception as e:
    print(f"❌ Error: {e}")