from django.shortcuts import render
import pandas as pd
from django.core.mail import EmailMessage
import csv
from django.contrib import messages
from io import StringIO
# Create your views here.

def index(request):
    if request.method == 'POST':
        allowed_extionsions = ['csv', 'xlsx']
        file = request.FILES['file']
        extension = file.name.split('.')[-1]

        if extension not in allowed_extionsions:
            messages.error(request, '.csv/.xlsx file extions only allowed')
            return render(request, 'index.html')

        if extension == 'csv':
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)

        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)
        csv_data = csv_buffer.getvalue()

        summary = df.groupby(['Cust State', 'DPD']).size().reset_index(name='counts')
        summary.sort_values(by='counts', ascending=False, inplace=True)

        csv_buffer = StringIO()
        summary.to_csv(csv_buffer, index=False)
        csv_summary = csv_buffer.getvalue()

        email = EmailMessage(
            "Python Assignment - Karanraj",
            "Thank you for the oppurtunity",
            "kara80499@gmail.com",
            ['tech@themedius.ai', 'hr@themedius.ai', 'kara80499@gmail.com'],
        )
        
        email.attach('data.csv', csv_data, 'text/csv')
        email.attach('summary.csv', csv_summary, 'text/csv')
        email.send(fail_silently=True)
        messages.success(request, 'Success summary sent to your email')

    return render(request, 'index.html')