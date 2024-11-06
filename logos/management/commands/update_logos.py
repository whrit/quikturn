from django.core.management.base import BaseCommand
from django.conf import settings
from logos.models import Company
from logos.scraper_connector import LogoScraperConnector
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Updates company logos using the logo scraper service'

    def add_arguments(self, parser):
        parser.add_argument(
            '--company',
            type=str,
            help='Update logo for a specific company domain'
        )
        parser.add_argument(
            '--scraper-url',
            type=str,
            default='http://localhost:5000',
            help='Base URL of the logo scraper service'
        )

    def handle(self, *args, **options):
        scraper = LogoScraperConnector(options['scraper_url'])
        
        if options['company']:
            # Update specific company
            success = scraper.update_company_logo(options['company'])
            if success:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully updated logo for {options["company"]}')
                )
            else:
                self.stdout.write(
                    self.style.ERROR(f'Failed to update logo for {options["company"]}')
                )
        else:
            # Update all companies
            companies = Company.objects.all()
            for company in companies:
                try:
                    success = scraper.update_company_logo(company.website)
                    if success:
                        self.stdout.write(
                            self.style.SUCCESS(f'Successfully updated logo for {company.website}')
                        )
                    else:
                        self.stdout.write(
                            self.style.WARNING(f'Failed to update logo for {company.website}')
                        )
                except Exception as e:
                    logger.error(f'Error updating logo for {company.website}: {str(e)}')