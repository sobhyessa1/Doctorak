from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from . import ocr_ai
import joblib

# Load the trained model at startup
model = joblib.load('C:\\Users\\sobhy essa\\OneDrive\\Desktop\\OP\\Graduate_Project\\Aianalysis\\model.pkl')

def upload(request):
    if request.method == 'POST' and request.FILES['image']:
        image = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(image.name, image)
        uploaded_file_url = fs.url(filename)
        image_path = fs.path(filename)
        
        # Preprocess the image
        preprocessed_image = ocr_ai.preprocess_image(image_path)
        if preprocessed_image is not None:
            # Extract text from the image
            text = ocr_ai.image_to_text(preprocessed_image)
            if text:
                # Debug: Print the raw text extracted
                print("Extracted Text:", text)
                
                # Preprocess and extract relevant info
                preprocessed_text = ocr_ai.preprocess_text(text)
                test_values = ocr_ai.extract_glucose_values(preprocessed_text)
                if any(test_values.values()):
                    # Determine test type, severity level, and diagnosis
                    severity_level, guidelines, diagnosis = ocr_ai.determine_severity_level(test_values)
                    test_type = ocr_ai.determine_test_type(test_values)
                    
                    # Prepare context for the template
                    context = {
                        'uploaded_file_url': uploaded_file_url,
                        'test_type': test_type,
                        'test_values': test_values,
                        'severity_level': severity_level,
                        'guidelines': guidelines,
                        'diagnosis': diagnosis
                    }
                    return render(request, 'AI/upload.html', context)
                else:
                    print("No relevant information found in the text.")
                    return HttpResponse("No relevant information found in the text.")
            else:
                print("Unable to extract text from the image.")
                return HttpResponse("Unable to extract text from the image.")
        else:
            print("Unable to load or process the image.")
            return HttpResponse("Unable to load or process the image.")
    
    return render(request, 'AI/upload.html')
