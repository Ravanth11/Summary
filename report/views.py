from django.shortcuts import render
from django.http import HttpResponse
from .forms import UploadFileForm

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file_path = handle_uploaded_file(request.FILES['file'])
            summary = generate_summary_report(file_path)
            return render(request, 'summary.html', {'summary': summary})
    else:
        form = UploadFileForm()
    return render(request, 'home.html', {'form': form})

def handle_uploaded_file(f):
    upload_dir = os.path.join(os.path.dirname(__file__), 'uploads')
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, f.name)
    
    with open(file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    
    return file_path


import os
import pandas as pd

def generate_summary_report(file_path):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(file_path, names=['Date', 'ACCNO', 'Cust State', 'Cust Pin', 'DPD'], header=0, encoding='latin1')
    
    # Group by 'Cust State' and 'DPD', and calculate the count
    summary = df.groupby(['Cust State', 'DPD']).size().reset_index(name='Count')
    
    # Create an HTML table string
    html_table = summary.to_html(index=False, classes='table table-bordered', header=True, border=1)
    
    return html_table
