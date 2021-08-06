from django.http import HttpResponse
from .models import Categories, Note, Banners
from django.db.models import Max

def homeAdd(request):
    id = request.POST['id']
    source = request.POST['slug']

    note = Note.objects.get(pk=id)
    
    if(source == 'main'):
        Note.objects.all().update(main_note=False)
        note.main_note=True
    elif(source == 'lasts'):
        note.last_notes = True
    else:
        note.top = True
    note.save()
    return HttpResponse(status=200)

def homeRemove(request=None,id=False,source=False):
    if(not (id and source)):
        id = request.POST['id']
        source = request.POST['slug']
    
    Note.removeItem(id=id,source=source)
   
    return HttpResponse(status=200)


def homeReorder(request):
    note_id = request.POST['id']
    source = request.POST['slug']
    direc = request.POST['dir']

    note = Note.objects.get(pk=note_id)

    if(source == 'lasts'):
        current = note.top_order
        if(direc=='1'):
            target = Note.objects.filter(last_notes=True).get(top_order=current+1)
        else:
            target = Note.objects.filter(last_notes=True).get(top_order=current-1)
        note.top_order = target.top_order
        target.top_order = current
    else:
        current = note.category_order
        
        if(direc=='1'):
            target = Note.objects.filter(category__slug=source).get(category_order=current+1)
        else:
            target = Note.objects.filter(category__slug=source).get(category_order=current-1)
        note.category_order = target.category_order
        target.category_order = current
    note.save()
    target.save()
    return HttpResponse(status=200)

def menuReorder(request):
    cat_id = request.POST['id']
    source = request.POST['slug']
    direc = request.POST['dir']

    category = Categories.objects.get(pk=cat_id)
    
    current = category.order
    if(direc=='1'):
        target = Categories.objects.filter(target=source).get(order=current-1)
    else:
        target = Categories.objects.filter(target=source).get(order=current+1)
    category.order = target.order
    target.order = current
    category.save()
    target.save()
    return HttpResponse(status=200)
    
def firstOrder(request):
    order =1
    for cat in Categories.objects.filter(target="M").order_by('order'):
        cat.order = order
        cat.save()
        order+=1
    
    order =1
    for cat in Categories.objects.filter(target="S").order_by('order'):
        cat.order = order   
        cat.save()
        order+=1
    return HttpResponse(status=200)

def reorder(request):
    lasts = Note.objects.filter(last_notes=True).order_by('-top_order')
    total = len(lasts)
    for note in lasts:
        note.top_order = total
        total -= 1
        note.save()
    return HttpResponse(status=200)


def depureBanners(request):
    to_delete = Banners.objects.filter(visible=False)
    to_delete.delete()
    return HttpResponse(status=200)