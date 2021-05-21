from django.shortcuts import render, get_object_or_404, redirect
from .models import Device
from .forms import DeviceForm

def device_index_view(request):
    queryset = Device.objects.all()
    context = {
        'object_list': queryset
    }
    return render(request, "device/index.html", context)

def device_show_view(request, id=id):
    obj = get_object_or_404(Device, id=id)
    context = {
        'object': obj
    }
    return render(request, "device/show.html", context)

def device_create_view(request):
    form = DeviceForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = DeviceForm()
        return redirect('/devices')
    context = {
        'form': form
    }
    return render(request, "device/create.html", context)

def device_update_view(request, id=id):
    obj = get_object_or_404(Device, id=id)
    form = DeviceForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
    context = {
        'form': form
    }
    return render(request, "device/create.html", context)

def device_delete_view(request, id):
    obj = get_object_or_404(Device, id=id)
    if request.method == "POST":
        obj.delete()
        return redirect('../../')
    context = {
        "object": obj
    }
    return render(request, "device/delete.html", context)