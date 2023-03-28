from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from .models import FileModel
from django.core.files.base import ContentFile
from .recursivley_summarizer import summarizer
import base64

def gpt3(request):
    # template = loader.get_template('index.html')
    # return HttpResponse(template.render())
    return render(request, 'index.html')

def upload_file(request):
    print('wertyuio')
    folder='gpt3/media/' 
    # file = request.FILES.get("file")
    file = request.FILES['file']
    fs = FileSystemStorage(location=folder) #defaults to   MEDIA_ROOT  
    filename = fs.save(file.name, file)
    file_url = fs.url(filename)
    print(file_url)
    # fss = FileSystemStorage()
    # filename = fss.save(file.name, file)
    # url = fss.url(filename)
    print(filename)
    result = summarizer(file_url)
    print("++++++++++++++++++++++++++++", result)
    # context={result:result}
    # return render(request, 'index.html', context=context)
    # data = ContentFile(base64.b64decode(file), name=file) 
    # FileModel.objects.create(doc=data)
    # print(data)
    return JsonResponse({"link": result})
    