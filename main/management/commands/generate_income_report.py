# management/commands/generate_income_report.py
from django.core.management.base import BaseCommand
from main.models import TotalIncomeReport
from main.models import CartOrder  # Import your Order model
from datetime import date  # Import the date class from the datetime module
from django.db.models import Sum

class Command(BaseCommand):
    help = 'Generate total income report for paid orders'

    def handle(self, *args, **kwargs):
        # Calculate total income for paid orders for a specific date (e.g., today)
        # Replace 'order_dt' with the actual date field in your CartOrder model
        total_income = CartOrder.objects.filter(paid_status=True, order_dt__date=date.today()).aggregate(Sum('total_amt'))['total_amt__sum'] or 0.0

        # Create or update TotalIncomeReport instance for today's date
        income_report, created = TotalIncomeReport.objects.get_or_create(
            date=date.today(),
            defaults={'total_income': total_income}
        )

        if not created:
            # If the instance already exists, update the total_income field
            income_report.total_income = total_income
            income_report.save()

        self.stdout.write(self.style.SUCCESS('Total income report generated successfully'))
