# Federated_Learning_ChessAI

## Running the code
Run the Server.py followed by Client.py

## What is happening?
1. The server is initialized containing the global model - should see <b>global_model.h5</b>
2. The client is initialized where the training will take place

3. The client asks the server for the global model 
4. The server sends the global model to the client - should see <b>global_model</b> in Client folder

5. The client starts training based on the dataset it has collected - should see <b>client_weights</b> in Client folder
6. Client completes training and sends the weights to the server model - should see <b>client_weight1</b> in Server folder

7. The server aggregates the different model weights together to reform a new updated global weight - should see <b>updated_global_weights</b> in Client folder 
8. The global model is then sent back to the client to deploy/retrain - should see <b>global_weights</b> in Client folder 