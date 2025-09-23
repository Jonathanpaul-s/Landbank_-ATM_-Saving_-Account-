import joblib

encoder = joblib.load("label_encoder.pkl")
print("Disease classes in encoder:", encoder.classes_)