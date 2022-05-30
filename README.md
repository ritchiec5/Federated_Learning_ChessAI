# Federated_Learning_ChessAI

## Overall implementation plan
Architecture: Client - Server

### Federated Learning:
1. The server is initialized - containing the global model
2. The client is initialized - where the training will take place

3. The client asks the server for the global model 
4. The server sends the global model to the client

5. The client starts training based on the dataset it has collected as well as the server model data
6. Client completes training and sends the weights to the server model

7. The server aggregates the different model weights together to reform a new global model
8. The global model is then sent back to the client to retrain  

9. Process repeats from 5 to 8

### Front-end:
1. Client enter website
2. Chess board is initialized

3. Players plays a move on the chess board
4. The position of the chess board is saved for dataset 
5. The position of the board is sent to the AI
6. The AI determines the best move to make
7. The best move is played on the chess board
8. The position of the chess board is saved for dataset

9. Process repeats until game over - 3 to 9

10. Once game over - users are able to click on train AI model button (Might be revised - might want to wait for sufficient dataset)
> The training will be run concurrently through threading
> Users will be able to play chess again

### Dockerize
1. Dockerize Client and Server
> Ensure Client and Server are able to communicate

### Evaluation
To evaluate the performance of the AI - we will have the AI play against a chess AI that was centrally trained
> The central AI will have to be provided similar amount of dataset
> Training - we could do it by a time basis or by epoch basis
1. Train centralized AI model - quite simple
2. Implement AI vs AI: To allow the central AI to compete against the FL AI
    - The score of the 10 matches will be kept for evaluation


## Code Deployment

### Installing Requirements
```pip install -r requirements.txt```

### Running Code
Run Server.py followed by Client.py in the complete code
- Don't cd into completed code or any other folder. The code is configured to run from Federated_Learning_ChessAI directory.

## How to go about the code

### Understanding FL & ML portion
1. Go through Tutorial code in ML Module (<b>Rmb to read the readme.md</b>)
- Test module_Chess_AI is a good place to start to understand how to train your own Chess_AI
- Test module_FL shows how to implement a FL code for classification model
- Test module_Flask show the general flask architecture for FL
- Actual FL_module combines all three test modules together

2. Go through Tutorial code in Web Interface
- Test module_Chess_board provides a good understanding of implementing chessboard on flask and implementing the chess AI (<b>optional</b> - can skip directly to the completed code to see web interface)