from django.shortcuts import render

from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny

import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView

from .models import EquipmentDataset
from .serializers import EquipmentDatasetSerializer

import os
from django.conf import settings
from django.http import FileResponse, Http404
from rest_framework.permissions import IsAuthenticated

from .pdf_utils import generate_pdf_report
from django.http import FileResponse

class CSVUploadAPIView(APIView):

    def post(self, request):
        file = request.FILES.get('file')

        if not file:
            return Response(
                {"error": "No file uploaded"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Read CSV using Pandas
        try:
            df = pd.read_csv(file)
        except Exception:
            return Response(
                {"error": "Invalid CSV file"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Basic validation
        required_columns = {
            "Equipment Name",
            "Type",
            "Flowrate",
            "Pressure",
            "Temperature"
        }

        if not required_columns.issubset(df.columns):
            return Response(
                {"error": "CSV missing required columns"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if df.empty:
            return Response(
                {"error": "CSV has no data rows"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Numbers must be numbers: a text value would crash the averages,
        # and a column with no values at all has no average to report.
        for column in ["Flowrate", "Pressure", "Temperature"]:
            raw = df[column]
            values = pd.to_numeric(raw, errors="coerce")
            bad = raw[values.isna() & raw.notna()]
            if not bad.empty:
                return Response(
                    {"error": f"{column} must be a number; found {bad.iloc[0]!r} "
                              f"in row {bad.index[0] + 2}"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if values.isna().all():
                return Response(
                    {"error": f"{column} has no values"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            df[column] = values

        # Analytics
        summary = {
            "total_equipment": len(df),
            "average_flowrate": float(df["Flowrate"].mean()),
            "average_pressure": float(df["Pressure"].mean()),
            "average_temperature": float(df["Temperature"].mean()),
            "equipment_type_distribution": df["Type"].value_counts().to_dict()
        }

        # Save to DB
        dataset = EquipmentDataset.objects.create(
            csv_file=file,
            summary=summary
        )

        # Keep only last 5 records
        datasets = EquipmentDataset.objects.order_by('-uploaded_at')
        if datasets.count() > 5:
            for old_dataset in datasets[5:]:
                old_dataset.csv_file.delete()
                old_dataset.delete()

        serializer = EquipmentDatasetSerializer(dataset)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class DatasetListAPIView(ListAPIView):
    queryset = EquipmentDataset.objects.order_by('-uploaded_at')[:5]
    serializer_class = EquipmentDatasetSerializer

class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if not user:
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_400_BAD_REQUEST
            )

        token, _ = Token.objects.get_or_create(user=user)

        return Response({"token": token.key})

class DatasetPDFAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            dataset = EquipmentDataset.objects.get(pk=pk)
        except EquipmentDataset.DoesNotExist:
            raise Http404

        pdf_name = generate_pdf_report(dataset)
        file_path = os.path.join(settings.MEDIA_ROOT, pdf_name)

        if not os.path.exists(file_path):
            raise Http404

        response = FileResponse(
            open(file_path, "rb"),
            content_type="application/pdf",
        )
        response["Content-Disposition"] = f'attachment; filename="{pdf_name}"'
        return response