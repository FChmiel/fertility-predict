import os
with open(os.path.join('Procfile'), "w") as file1:
    toFile = 'web: sh setup.sh && streamlit run fertility-predict.py'
    file1.write(toFile)