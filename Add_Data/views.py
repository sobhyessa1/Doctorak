from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime
from django.http import HttpResponse
from .models import Disease, PrescriptionImage, AnalysisImage
from django.contrib.auth.decorators import login_required

@login_required
def add_and_search_disease(request):
    def get_updated_context(disease_name=None):
        diseases_list = Disease.objects.filter(patient=request.user)
        context = {'diseases_list': diseases_list}
        
        if disease_name:
            diseases = diseases_list.filter(disease_name__icontains=disease_name)
            if diseases.exists():
                records_data = [
                    {
                        'id': disease.id,
                        'disease_name': disease.disease_name,
                        'treatment_start_date': disease.treatment_start_date,
                        'recovery_date': disease.recovery_date,
                        'analysis_images': disease.analysis_images.all(),
                        'prescription_images': disease.prescription_images.all(),
                        'modified_dates': disease.modified_dates.split(",") if disease.modified_dates else []
                    }
                    for disease in diseases
                ]
                context.update({'record_found': True, 'records': records_data})
            else:
                context.update({'error_message': "No matching diseases found"})
        
        return context

    if request.method == 'POST':
        if 'search' in request.POST:
            disease_name = request.POST.get('disease_name')
            context = get_updated_context(disease_name)
            return render(request, 'AddData/add_medical_record.html', context)

        elif 'add_images' in request.POST:
            disease_id = request.POST.get('disease_id')
            disease = get_object_or_404(Disease, id=disease_id, patient=request.user)
            analysis_images = request.FILES.getlist('analysis_images')
            prescription_images = request.FILES.getlist('prescription_images')
            new_recovery_date = request.POST.get('recovery_date')
            new_treatment_start_date = request.POST.get('treatment_start_date')

            for image in analysis_images:
                AnalysisImage.objects.create(disease=disease, image=image)

            for image in prescription_images:
                PrescriptionImage.objects.create(disease=disease, image=image)

            if disease.recovery_date:
                disease.modified_dates = (disease.modified_dates + f", end date was: {disease.recovery_date}") if disease.modified_dates else f"end date was: {disease.recovery_date}"
            
            if disease.treatment_start_date:
                disease.modified_dates = (disease.modified_dates + f", start date was: {disease.treatment_start_date}") if disease.modified_dates else f"start date was: {disease.treatment_start_date}"

            if new_recovery_date:
                disease.recovery_date = new_recovery_date
                disease.save()

            if new_treatment_start_date:
                disease.treatment_start_date = new_treatment_start_date
                disease.save()

            context = get_updated_context(disease.disease_name)
            return render(request, 'AddData/add_medical_record.html', context)

        elif 'delete_image' in request.POST:
            image_type = request.POST.get('image_type')
            image_id = request.POST.get('delete_image')


            if image_type == 'analysis':
                image = get_object_or_404(AnalysisImage, id=image_id, disease__patient=request.user)
            elif image_type == 'prescription':
                image = get_object_or_404(PrescriptionImage, id=image_id, disease__patient=request.user)
            else:
                print("Invalid image type encountered:", image_type)
                return HttpResponse("Invalid image type")

            disease = image.disease
            image.delete()

            context = get_updated_context(disease.disease_name)
            return render(request, 'AddData/add_medical_record.html', context)

        else:
            disease_name = request.POST.get('disease_name')
            treatment_start_date = request.POST.get('treatment_start_date')
            analysis_images = request.FILES.getlist('analysis_images')
            prescription_images = request.FILES.getlist('prescription_images')

            if all([disease_name, treatment_start_date]):
                treatment_start_date = datetime.strptime(treatment_start_date, '%Y-%m-%d').date()
                
                record = Disease.objects.create(
                    patient=request.user,
                    disease_name=disease_name,
                    treatment_start_date=treatment_start_date,
                )

                for image in analysis_images:
                    AnalysisImage.objects.create(disease=record, image=image)

                for image in prescription_images:
                    PrescriptionImage.objects.create(disease=record, image=image)

                context = get_updated_context()
                return render(request, 'AddData/add_medical_record.html', context)
            else:
                return HttpResponse('Please fill in all the required fields.')

    context = get_updated_context()
    return render(request, 'AddData/add_medical_record.html', context)
