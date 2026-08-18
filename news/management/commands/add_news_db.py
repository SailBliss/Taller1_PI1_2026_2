from django.core.management.base import BaseCommand
from news.models import News
from datetime import datetime
import csv


class Command(BaseCommand):
    help = "Load 5 news from Fake.csv"

    def handle(self, *args, **kwargs):
        csv_file_path = "news/management/commands/Fake.csv"

        created = 0

        with open(csv_file_path, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                if created == 5:
                    break

                try:
                    date_value = datetime.strptime(
                        row["date"].strip(),
                        "%B %d, %Y"
                    ).date()
                except ValueError:
                    continue

                News.objects.update_or_create(
                    headline=row["title"],
                    defaults={
                        "body": row["text"],
                        "date": date_value,
                    },
                )

                created += 1

        self.stdout.write(
            self.style.SUCCESS(f"Loaded {created} news")
        )