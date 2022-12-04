# Prediksi Kebakaran 
##### by Hendrik Tanaka
  
  
Berikut ini adalah Tugas Akhir dari subject "ML Process" pada Sekolah Data Pacmann.

### Latar Belakang
Membuat model untuk memprediksi terjadinya kebakaran, berdasarkan beberapa variabel. Kasus ini dapat dikategorikan sebagai Supervised Learning - Binnary Classification.

### Project architecture
Berikut ini adalah diagram project secara keseluruhan :  

![alt text](https://github.com/hendrikt1479/ml_project_final/blob/master/images/project.png?raw=true)

Project ini dapat di bagi menjadi 5 bagian besar, yaitu :
1. Data Preparation & EDA
2. Data Preprocessing
3. Feature Engineering
4. Data Modelling, Evaluation & Hyperparameter Tunning
5. Deployment

#### Data Preparation & EDA
![alt text](https://github.com/hendrikt1479/ml_project_final/blob/master/images/dataprep.png?raw=true)

#### Data Preprocessing
![alt text](https://github.com/hendrikt1479/ml_project_final/blob/master/images/datapreprop.png?raw=true)

#### Feature Engineering
![alt text](https://github.com/hendrikt1479/ml_project_final/blob/master/images/feateng.png?raw=true)

#### Data Modelling, Evaluation & Hyperparameter Tunning
![alt text](https://github.com/hendrikt1479/ml_project_final/blob/master/images/model.png?raw=true)

#### Deployment
![alt text](https://github.com/hendrikt1479/ml_project_final/blob/master/images/deploy.png?raw=true)

### Format Message
#### Prediksi via API
Berikut ini adalah kode yang digunakan dalam file "api.py" dalam function untuk menerima data yang dikirimkan dari frontend kemudian di masukkan kedalam pickle model, untuk menghasilkan y_pred.
```bash
@app.post("/predict/")
def predict(data: api_data):    
    # Convert data api to dataframe
    data = pd.DataFrame(data).set_index(0).T.reset_index(drop = True)  # type: ignore
    data.columns = config["predictors"]

    # Predict data
    y_pred = model_data.predict(data)

    return str(y_pred)
```

#### Response via API
Berikut ini adalah kode dalam file "streamlit.py" dalam function untuk mengirimkan data yang di convert dalam bentuk JSON ke api backend, untuk kemudian dikembalikan lagi dalam bentuk JSON juga dan kemudian menampilkan hasilnya.
```bash
       # Create loading animation while predicting
        with st.spinner("Mengirim data ke server ..."):
            result = requests.post('http://localhost:8080/predict/', json = raw_data).json()
       
        if result == '[1]':
            st.error("#### Prediksi akan terjadi kebakaran :fire:")
        else :
            st.success("#### Prediksi tidak terjadi kebakaran :sunglasses:")
```

## Cara menjalankan Layanan Machine Learning di local komputer


