from django.db import models

class CourtQuery(models.Model):
    case_type = models.CharField(max_length=50)
    case_number = models.CharField(max_length=50)
    filing_year = models.CharField(max_length=4)
    timestamp = models.DateTimeField(auto_now_add=True)
    raw_html = models.TextField()
    parsed_data = models.JSONField()

    def __str__(self):
        return f"{self.case_type} {self.case_number}/{self.filing_year}"

class CaseDetails(models.Model):
    query = models.ForeignKey(CourtQuery, on_delete=models.CASCADE, related_name='details')
    petitioner = models.CharField(max_length=255)
    respondent = models.CharField(max_length=255)
    filing_date = models.CharField(max_length=100, blank=True, null=True)
    next_hearing_date = models.CharField(max_length=100, blank=True, null=True)
    judgment_pdf_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"Details for {self.query}"

