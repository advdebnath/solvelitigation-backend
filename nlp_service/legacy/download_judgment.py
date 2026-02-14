import requests
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Try multiple sources
sources = [
    {
        'url': 'https://main.sci.gov.in/supremecourt/2019/28173/28173_2019_2_1501_22070_Judgement_25-Jul-2019.pdf',
        'name': 'Supreme Court'
    },
    {
        'url': 'https://indiankanoon.org/doc/37581810/',
        'name': 'Indian Kanoon (HTML)'
    }
]

filename = "real_judgment.pdf"

for source in sources:
    try:
        print(f"Trying {source['name']}...")
        response = requests.get(source['url'], stream=True, verify=False, timeout=30)
        
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"✅ Downloaded: {filename}")
            break
    except Exception as e:
        print(f"❌ Failed: {e}")
        continue
else:
    print("\n❌ All sources failed. Manual download needed:")
    print("1. Go to: https://indiankanoon.org")
    print("2. Search any case")
    print("3. Download the PDF")
    print("4. Save as 'real_judgment.pdf' in this folder")