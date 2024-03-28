import requests

base_url = "http://172.17.0.2:4000/iris" #changed to docker ip address

def upload_dataset(file_path):
    url = f"{base_url}/dataset"
    with open(file_path, 'rb') as file:
        files = {'train': file}
        response = requests.post(url, files=files)
    return response.text

def create_model(dataset_id):
    url = f"{base_url}/model"
    data = {'dataset': dataset_id}
    response = requests.post(url, data=data)
    return response.text

def retrain_model(model_id, dataset_id):
    url = f"{base_url}/model/{model_id}"
    data = {'dataset': dataset_id}
    response = requests.put(url, params=data)
    return response.json()

def score_model(model_id, fields):
    url = f"{base_url}/model/{model_id}"
    data = {'fields': ','.join(map(str, fields))}
    response = requests.get(url, params=data)
    return response.text

def test_model(model_id, datasetid):
    url = f"{base_url}/model/{model_id}/test"
    data = {'dataset': ','.join(map(str, datasetid))}
    response = requests.get(url, params=data)
    return response.json()

def main():
    # Example usage
    dataset_id = upload_dataset('iris_extended_encoded.csv')
    model_id = create_model(dataset_id)
    history = retrain_model(model_id, dataset_id)
    r =  [161.8,0,5.16,3.41,1.64,0.26,17.5956,0.4264,1.5131964809384164,6.3076923076923075,3.1463414634146343,13.115384615384615,3.5200000000000005,3.1500000000000004,5.33,18.33,53.21,4.194710955477147,0.6529931086925803,41.265478424015015]
    the_score = score_model(model_id, r)
    the_test = test_model(model_id, dataset_id)
    
    print(f"Dataset ID: {dataset_id}")
    print(f"Model ID: {model_id}")
    print(f"Retrain History: {history}")
    print(f"Score: {the_score}")
    print(f"Test: {the_test}")

if __name__ == "__main__":
    main()
