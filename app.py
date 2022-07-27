import pandas as pd
from flask import Flask, request, render_template
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import LabelEncoder
from sklearn.naive_bayes import MultinomialNB

app = Flask(__name__)

ds = pd.read_csv('DATALENGKAP.csv', usecols= ['JK','STATUS','MENIKAH','UMUR','IPK ','SK'])


x = ds.iloc[:,:-1].values 
y = ds.iloc[:,-1].values 


encoder = LabelEncoder()

x[:,0] = encoder.fit_transform(x[:,0]) 
x[:,1] = encoder.fit_transform(x[:,1]) 
x[:,2] = encoder.fit_transform(x[:,2])
x[:,3] = encoder.fit_transform(x[:,3])
x[:,4] = encoder.fit_transform(x[:,4])
y = encoder.fit_transform(y) 

model = MultinomialNB()

# train model
model.fit(x, y)

@app.route('/')
def index():
    return render_template('index.html', predicted="?", JK = "?", STATUS = "?", MENIKAH = "?", UMUR = "?", IPK= "?",)


@app.route('/prediction', methods=['POST'])
def prediction():
    
    JK = int(request.form['JK'])
    STATUS = int(request.form['STATUS'])
    MENIKAH = int(request.form['MENIKAH'])
    UMUR = int(request.form['UMUR'])
    IPK = float(request.form['IPK'])
    
    
    predicted = model.predict([[JK, STATUS, MENIKAH, UMUR, IPK]])
    
    
    if JK == 0:
        JK = "Pria"
    else:
        JK = "Wanita"
    
    
    if STATUS == 0:
        STATUS = "Bekerja"
    else:
        STATUS = "Mahasiswa"
    if MENIKAH == 0:
        MENIKAH = "Belum"
    else:
        MENIKAH = "Sudah"
    if IPK >= 3 :  
        predicted = "TEPAT WAKTU"
    else:
        predicted = "TERLAMBAT"
    

    return render_template('index.html', Hasil = predicted, JK = JK, STATUS = STATUS, UMUR = UMUR ,IPK = IPK, MENIKAH = MENIKAH)


if __name__ == '__main__':
    app.run(debug=True)