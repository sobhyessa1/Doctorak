import os
import cv2
import pytesseract

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
os.environ['TESSDATA_PREFIX'] = r'C:\Program Files\Tesseract-OCR\tessdata'

def preprocess_image(image_path):
    if not os.path.exists(image_path):
        print(f"The file does not exist at path: {image_path}")
        return None
    
    image = cv2.imread(image_path)
    
    if image is None:
        print(f"Unable to load image at path: {image_path}")
        return None
    
    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply bilateral filter to reduce noise
    filtered_image = cv2.bilateralFilter(gray_image, 11, 17, 17)
    
    # Apply thresholding to clarify text
    _, threshold_image = cv2.threshold(filtered_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    return threshold_image

def image_to_text(image):
    text = pytesseract.image_to_string(image, lang='eng')
    return text.strip()

def preprocess_text(text):
    # Remove unnecessary characters and convert text to lowercase
    return ''.join(e for e in text if e.isalnum() or e.isspace()).lower()

def extract_glucose_values(text):
    test_values = {'fbs': None, 'ppbs': None, 'rbg': None, 'hba1c': None}
    
    for line in text.split('\n'):
        if 'fasting' in line.lower() or 'fbs' in line.lower():
            parts = line.split()
            for part in parts:
                try:
                    value = float(part)
                    test_values['fbs'] = value
                    break
                except ValueError:
                    continue
        elif 'postprandial' in line.lower() or 'ppbs' in line.lower():
            parts = line.split()
            for part in parts:
                try:
                    value = float(part)
                    test_values['ppbs'] = value
                    break
                except ValueError:
                    continue
        elif 'random' in line.lower() or 'rbg' in line.lower():
            parts = line.split()
            for part in parts:
                try:
                    value = float(part)
                    test_values['rbg'] = value
                    break
                except ValueError:
                    continue
        elif 'hba1c' in line.lower() or 'a1c' in line.lower():
            parts = line.split()
            for part in parts:
                try:
                    value = float(part.strip('%'))
                    test_values['hba1c'] = value
                    break
                except ValueError:
                    continue
    return test_values

def determine_severity_level(test_values):
    guidelines = ""
    diagnosis = "You are not diabetic."
    
    if test_values['hba1c'] is not None:
        HbA1c_value = test_values['hba1c']
        if HbA1c_value < 5.5:
            severity_level = 50
            guidelines = "Eat a balanced diet focusing on whole grains, lean proteins, and vegetables. Avoid sugary snacks and drinks."
        elif 5.5 <= HbA1c_value < 6.8:
            severity_level = 60
            guidelines = "Increase intake of fiber-rich foods such as vegetables, legumes, and whole grains. Reduce intake of high-carbohydrate foods."
        elif 6.8 <= HbA1c_value < 7.6:
            severity_level = 70
            guidelines = "Focus on a diet rich in non-starchy vegetables and lean proteins. Avoid processed foods and sugary drinks."
        else:
            severity_level = 80
            guidelines = "Adopt a low-carbohydrate diet with fiber-rich foods. Exercise regularly and avoid any form of sugar."
        diagnosis = "You are diabetic." if severity_level > 50 else "You are not diabetic."
    elif test_values['fbs'] is not None:
        FBS_value = test_values['fbs']
        if FBS_value < 100:
            severity_level = 50
            guidelines = "Maintain a healthy diet with regular meals. Avoid sugary snacks and drinks."
        elif 100 <= FBS_value < 126:
            severity_level = 60
            guidelines = "Include more whole grains and fiber in your diet. Monitor carbohydrate intake."
        else:
            severity_level = 70
            guidelines = "Focus on low-carbohydrate, high-fiber foods. Exercise regularly and avoid sugary foods."
        diagnosis = "You are diabetic." if severity_level > 50 else "You are not diabetic."
    elif test_values['ppbs'] is not None:
        PPBS_value = test_values['ppbs']
        if PPBS_value < 140:
            severity_level = 50
            guidelines = "Maintain balanced meals with controlled portions. Avoid overeating and sugary drinks."
        elif 140 <= PPBS_value < 200:
            severity_level = 60
            guidelines = "Reduce intake of refined carbohydrates. Include more vegetables and lean proteins in your diet."
        else:
            severity_level = 70
            guidelines = "Adopt a low-carbohydrate diet and increase physical activity. Avoid high-sugar foods and drinks."
        diagnosis = "You are diabetic." if severity_level > 50 else "You are not diabetic."
    elif test_values['rbg'] is not None:
        RBG_value = test_values['rbg']
        if RBG_value < 140:
            severity_level = 50 
            guidelines = "Maintain regular eating habits with balanced meals. Avoid sugary snacks and drinks."
        elif 140 <= RBG_value < 200:
            severity_level = 60
            guidelines = "Focus on a balanced diet with whole grains and vegetables. Monitor and reduce carbohydrate intake."
        else:
            severity_level = 70
            guidelines = "Adopt a low-carbohydrate diet focusing on non-starchy vegetables. Increase physical activity and avoid sugary foods."
        diagnosis = "You are diabetic." if severity_level > 50 else "You are not diabetic."
    else:
        severity_level = 50
        guidelines = "Maintain a healthy diet with regular meals. Avoid sugary snacks and drinks."

    return severity_level, guidelines, diagnosis

def determine_test_type(test_values):
    if test_values['hba1c'] is not None:
        return "HbA1c"
    elif test_values['fbs'] is not None:
        return "Fasting Blood Sugar"
    elif test_values['ppbs'] is not None:
        return "2-Hour Postprandial"
    elif test_values['rbg'] is not None:
        return "Random Blood Sugar"
    else:
        return "Unknown Test Type"
