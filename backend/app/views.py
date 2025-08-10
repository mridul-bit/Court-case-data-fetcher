import asyncio
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
import os

from . import scraper
from .models import CourtQuery, CaseDetails

# Define your mock values here (must match frontend defaults)
MOCK_CASE_TYPE = "W.P.(C)"
MOCK_CASE_NUMBER = "1234"
MOCK_FILING_YEAR = "2023"

@api_view(['GET', 'POST'])
def fetch_case(request):
    # GET: return form meta and captcha from scraper as usual
    if request.method == "GET":
        try:
            form_data = asyncio.run(scraper.fetch_case_form_data())
            return Response({
                "status": "success",
                "case_types": form_data.get("case_types", []),
                "years": form_data.get("years", []),
                "captcha": form_data.get("captcha")
            }, status=200)
        except Exception as e:
            return Response({"status": "error", "message": f"Failed to load form data: {str(e)}"}, status=500)

    # POST: handle mock or real submission
    if request.method == "POST":
        payload = request.data
        case_type = payload.get("case_type")
        case_number = payload.get("case_number")
        filing_year = payload.get("filing_year")
        captcha_text = payload.get("captcha_text")

        if not all([case_type, case_number, filing_year, captcha_text]):
            return Response({"status": "error", "message": "Missing required fields."}, status=400)

        # If all inputs match mock, serve mock response
        if (case_type == MOCK_CASE_TYPE and
            case_number == MOCK_CASE_NUMBER and
            filing_year == MOCK_FILING_YEAR):

            # Read mockresult.html from disk
            mock_path = os.path.join(settings.BASE_DIR, 'mockresult.html')
            try:
                with open(mock_path, 'r', encoding='utf-8') as f:
                    mock_html = f.read()
            except Exception as e:
                return Response({"status": "error", "message": f"Failed to load mock result: {str(e)}"}, status=500)

            # Return mock HTML as raw_html field inside data
            return Response({
                "status": "success",
                "data": {
                    "raw_html": mock_html
                }
            }, status=200)

        # Else real submission: just return raw_html from scraper, no parsing
        try:
            res = asyncio.run(scraper.fetch_case_details(case_type, case_number, filing_year, captcha_text))
        except Exception as e:
            return Response({"status": "error", "message": f"Scraper exception: {str(e)}"}, status=500)

        raw_html = res.get("raw_html", "")

        # Store query + raw_html only, parsed_data empty
        q = CourtQuery.objects.create(
            case_type=case_type,
            case_number=case_number,
            filing_year=filing_year,
            raw_html=raw_html,
            parsed_data={}
        )

        return Response({
            "status": "success",
            "data": {
                "raw_html": raw_html
            }
        }, status=200)

