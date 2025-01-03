import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# قراءة البيانات
data = pd.read_csv('C:\\Users\\sobhy essa\\OneDrive\\Desktop\\OP\\Graduate_Project\\Aianalysis\\diabetes.csv')

# عرض رؤوس الأعمدة لمعرفة الأسماء الصحيحة
print(data.columns)

# بعد معرفة الأسماء الصحيحة، استخدمها بدلاً من 'feature1', 'feature2', 'feature3'
# استخدام الأعمدة المتاحة في البيانات
X = data[['Pregnancies', 'HbA1C', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age', 'FBS', 'PPBS', 'RBS', 'OGTT']]
y = data['Outcome']

# تقسيم البيانات إلى مجموعات التدريب والاختبار
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# تدريب النموذج
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# حفظ النموذج
joblib.dump(model, 'C:\\Users\\sobhy essa\\OneDrive\\Desktop\\OP\\Graduate_Project\\Aianalysis\\model.pkl')