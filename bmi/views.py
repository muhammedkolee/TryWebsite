from django.shortcuts import render, redirect

# Create your views here.

def bmi(request):
    if request.method == 'POST':
        height = float(request.POST['height'])
        weight = float(request.POST['weight'])
        bmi = weight / (height/100)**2
        bmi = round(bmi, 2)

        request.session['height'] = height
        request.session['weight'] = weight
        request.session['bmi'] = bmi
        return redirect('result')
    else:
        return render(request, 'bmi/bmi.html')
    
def result(request):
    bmi = request.session.get('bmi', None)
    height = request.session.get('height', None)
    weight = request.session.get('weight', None)

    return render(request, 'bmi/result.html', {'bmi': bmi, 'height': height, 'weight': weight})