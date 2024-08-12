from django.shortcuts import render, redirect, HttpResponse
import pandas as pd
from django import forms
from .models import UploadedFile
from django.conf import settings  # Import settings


class UploadFileForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ["file"]


def index(request):
    return render(request, "home.html")


def success(request):
    # Retrieve the latest uploaded file
    latest_file = UploadedFile.objects.latest("uploaded_at")

    # Read the file as a DataFrame (handling both CSV and Excel formats)
    file_path = latest_file.file.path
    if file_path.endswith(".csv"):
        data = pd.read_csv(file_path, encoding="ISO-8859-1", on_bad_lines="skip")
    elif file_path.endswith(".xlsx"):
        data = pd.read_excel(file_path)
    else:
        return HttpResponse("Unsupported file format.", status=400)

    # Handle empty files
    if data.empty:
        return HttpResponse("The uploaded file is empty.", status=400)

    # Group the data by 'Cust State' and 'Cust Pin' and aggregate the DPD values
    grouped_data = data.groupby(["Cust State", "Cust Pin"])["DPD"].sum().reset_index()

    # Rename columns to avoid spaces in the template
    grouped_data.rename(
        columns={"Cust State": "CustState", "Cust Pin": "CustPin"}, inplace=True
    )

    # Convert the grouped data to a list of dictionaries for easy use in the template
    grouped_data_list = grouped_data.to_dict(orient="records")

    return render(request, "success.html", {"grouped_data": grouped_data_list})


def upload_file(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("success")  # Redirect to a success page
    else:
        form = UploadFileForm()
    return render(request, "upload.html", {"form": form})


def about(request):
    return HttpResponse("Welcome to csv Project About page")
