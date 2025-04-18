from django.http import HttpRequest
from django.shortcuts import render


def qr_view(request: HttpRequest, amount: int, message: str):
    context = {
        'amount': amount,
        'message': message,
    }
    return render(request, 'pages/qr-code.html', context)
