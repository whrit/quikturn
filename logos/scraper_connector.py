import logging
from django.conf import settings
from .models import Company, Logo
import requests
from urllib.parse import urljoin
import tempfile
from django.core.files import File

logger = logging.getLogger(__name__)

class LogoScraperConnector:
    def __init__(self, scraper_base_url):
        self.scraper_base_url = scraper_base_url.rstrip('/')

    def update_company_logo(self, company_domain):
        """
        Connect to the logo scraper service and update the company's logo
        """
        try:
            # Call the scraper service
            response = requests.get(
                urljoin(self.scraper_base_url, '/scrape'),
                params={'domain': company_domain},
                timeout=30
            )
            response.raise_for_status()
            data = response.json()

            if not data.get('success'):
                logger.error(f"Failed to scrape logo for {company_domain}: {data.get('error')}")
                return False

            # Get or create company
            company, created = Company.objects.get_or_create(
                website=company_domain,
                defaults={'name': data.get('company_name', company_domain)}
            )

            # Download the logo
            logo_url = data.get('logo_url')
            if not logo_url:
                logger.error(f"No logo URL found for {company_domain}")
                return False

            logo_response = requests.get(logo_url, stream=True)
            logo_response.raise_for_status()

            # Save the logo to a temporary file
            with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                for chunk in logo_response.iter_content(chunk_size=4096):
                    tmp_file.write(chunk)
                tmp_file.seek(0)

                # Create the logo object
                logo = Logo.objects.create(
                    company=company,
                    is_primary=True,  # Make this the primary logo
                    source_url=logo_url
                )
                logo.image.save(
                    f"{company.name.lower().replace(' ', '_')}_logo.png",
                    File(tmp_file),
                    save=True
                )

            return True

        except requests.RequestException as e:
            logger.error(f"Error connecting to scraper service: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error updating logo: {str(e)}")
            return False