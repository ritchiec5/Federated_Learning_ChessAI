# Federated_Learning_ChessAI

## Running Application

1. Open command prompt and run ipconfig
2. Identify IPV4 address for the Wireless LAN adapter Wi-Fi. eg. 192.168.1.154
3. Replace all docker-compose.yml IPADDRESS env variables to your IPV4 address found in the previous step

```console
    server:
        build:
          dockerfile: Dockerfile
          context: ./Server
        ports:
          - '5000:5000'
        environment:
            - IPADDRESS=172.30.138.120 --- TO BE REPLACED

    client1:
        build: 
          dockerfile: Dockerfile
          context: ./Client 
        ports: 
          - '5003:5003'
        environment:
            - FLASKPORT=5003
            - STOCKFISHPORT=8082
            - IPADDRESS=172.30.138.120 --- TO BE REPLACED      

    client2:
        build: 
          dockerfile: Dockerfile
          context: ./Client 
        ports: 
          - '5004:5004'
        environment:
            - FLASKPORT=5004
            - STOCKFISHPORT=8083
            - IPADDRESS=172.30.138.120 --- TO BE REPLACED       
```

4. The docker compose has included both clients and server together for convience -- however you may choose to seperate them by running 
- eg. docker-compose up client1 stockfish1
- eg. docker-compose up server

5. Running the code

```console
cd '.\Completed Code\'

// build the docker compose up
docker-compose up --build

// run docker-compose
docker-compose up

// run detached
docker-compose up -d

// stop docker compose
docker-compose down

```

``` console
// Should there be any error
docker-compose up --build --remove-orphans --force-recreate
```


### You may adjust the docker compose file to add more clients 
- Simply by adding more client and stockfish to the docker-compose.yml while changing the ports to prevent overlaps
for eg. 

``` console
    client3:                                // Service name to be replaced
        build: 
          dockerfile: Dockerfile
          context: ./Client 
        ports: 
          - '5004:5004'                     // Port to be replaced
        environment:
            - FLASKPORT=5004                // Port to be replaced
            - STOCKFISHPORT=8083            // Port to be replaced
            - IPADDRESS=172.30.138.120      // IP to be replaced if applicable


    stockfish3:
        build: 
          dockerfile: Dockerfile
          context: ./Stockfish
        ports: 
          - '8083:8083'                     // To be replaced
        environment:
            - STOCKFISHPORT=8083            // To be replaced
```


6. Opening up the websites
- IF you are not using detached mode you should see multiple flask server starting up
- Find the client1 and client2 ipaddress and click on them to open them on your default browser
- For eg. 
    127.0.0.1:5003
    127.0.0.1:5004

7. Playing against the Chess AI
- Choose the depth you want to play on. The depth will improve the AI performance however increase the time required for the AI to move. 
- Depth 1: estimate 15s
- Depth 2: estimate 30s
- Depth 3: estimate 1min

- Play your first move by clicking and dragging the piece you want to move
- It might take a while for the tensorflow model to intialize, do be patient and not move any other pieces after the first move till a move is played by the AI.
- Currently the player is automatically white
- Play till you checkmate, draw, or lose

8. Game over - Check Docker logs for training
- Wait for a while for the docker logs show the model training epoches
- Stockfish will be printing out alot of logs in the mean time - this is because the dataset (y - output variable) is being created using stockfish

9. Should see logs 

Server:
"Aggregating client weights"
"Model Aggregated"
"Received updated server weights"

Client:
"Aggregation client weights"
"Received updated Global weights"


10. Extract global weights from server container

```console
// get server id
docker ps

// enter container
docker exec -t -i container_name /bin/bash

// extract file from container
// docker cp <containerId>:/file/path/within/container /host/path/target
docker cp completedcode_server_1:/model_data/Updated_global_weights '../Evaluation code/model_weight'
```


## Evaluating Global model weights
Additional you may evaluate the new global model weights

1. Run pip install
```console
// do ensure you are in the main folder cd.. if not
pip install -r requirement.txt

```

2. get dataset
- download https://drive.google.com/file/d/1YcFh-uBHflrRuQjh3rQ8CFfY2YKx7ytw/edit
- Extract the file after download for the npz - the file size is about 3GB.
- Place the dataset.npz within the Evaluation code folder

3. open Evaluate_model.ipynb

4. Run the first 4 code cells/ 7 cells to get the model loss


## Exploration of Results code
1. Evaluate_model.ipynb: Evaluate model accuracy between centralized and federated
2. Performance.ipynb: Observing for model accuracy improvement between initial and federated
3. AI_vs_AI.ipynb: Gameplay performance between AI and AI


## Kubernetes
Additionally kubernetes have been implemented

Required installation

Install Kubectl
https://kubernetes.io/docs/tasks/tools/

Install Minikube
https://minikube.sigs.k8s.io/docs/start/


bash terminal
```console

//build the docker images locally
eval $(minikube -p minikube docker-env)
docker compose build

//start cluster
minikube start

//start network gateway from host to the service
minikube tunnel

//create kubernetes resource
kubectl apply -f server.yaml

// additional no long need to run
kubectl apply -f client.yaml 
kubectl apply -f client1.yaml
kubectl apply -f stockfish.yaml
kubectl apply -f stockfish1.yaml

// creates a service exposing the port
kubectl expose deployment server --type=LoadBalancer --port=5000

//additional no longer need to run
kubectl expose deployment client --type=LoadBalancer --port=5003
kubectl expose deployment stockfish --type=LoadBalancer --port=8082
kubectl expose deployment client1 --type=LoadBalancer --port=5004
kubectl expose deployment stockfish1 --type=LoadBalancer --port=8083
// you may access 127.0.0.1:5003 to view the flask

// else you may access using 
minikube service server

// addittional no longer need to run
minikube service client
minikube service client1
minikube service stockfish
minikube service stockfish1

```


```console
// additional commands
kubectl get pods
kubectl get svc
kubectl delete pod,svc --all

// commands for ingress
minikube addons enable ingress
kubectl get ingress
kubectl describe ingress server-ingress

// views pods dashboard
minikube dashboard
```

1. Using cluser IP (everything is pods)
- Currently tested by changing the client.yaml environment IP address to server ip address
- client to server working - but server to client and client to stockfish not yet
- to get server IP address 
kubectl get pods -o wide


2. Server is pod - better as it makes more sense architecturaly
- server as pod
- client intialize docker compose
- client can reach server - change ip address to 127.0.0.1
- currently load balancing can open flask, but trying to use ingress to make it an endpoint doesnt work 


