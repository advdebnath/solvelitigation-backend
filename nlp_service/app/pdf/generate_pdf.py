import os
from datetime import datetime

from jinja2 import Template
from weasyprint import HTML


def generate_judgment_pdf(judgment, user, output_path):

    template_path = os.path.join(os.path.dirname(__file__), "judgment_template.html")

    with open(template_path, "r", encoding="utf-8") as f:
        template_html = f.read()

    template = Template(template_html)

    rendered_html = template.render(
        logo_path="/var/www/solvelitigation/frontend/public/solve_logo.png",
        court_name=judgment.get("court", ""),
        judgment_number=judgment.get("judgmentNumber", ""),
        year=judgment.get("year", ""),
        judgment_content=judgment.get("htmlContent", ""),
        user_name=user.get("name", "User"),
        timestamp=datetime.now().strftime("%d %b %Y, %H:%M IST"),
    )

    HTML(string=rendered_html).write_pdf(output_path)
