from django.core.management.base import BaseCommand
from ...models import InventorizationList

class Command(BaseCommand):
    help = 'Generates reports for InventorizationList objects that are COMPLETED and do not have a PDF or Excel file.'

    def handle(self, *args, **kwargs):

        lists_to_generate = InventorizationList.objects.filter(
            status='COMPLETED',  
            pdf_report__isnull=True,  
            excel_report__isnull=True  
        )

        if lists_to_generate.exists():
            self.stdout.write(f'Found {lists_to_generate.count()} items without reports. Generating reports...')
            for item in lists_to_generate:
                try:
                    item.generate_report()
                    self.stdout.write(f'Successfully generated report for InventorizationList with ID: {item.id}')
                except Exception as e:
                    self.stderr.write(f'Error generating report for InventorizationList with ID: {item.id}: {str(e)}')
        else:
            self.stdout.write('No InventorizationList items found without reports and with status COMPLETED.')
