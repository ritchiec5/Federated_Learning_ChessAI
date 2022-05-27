# Test module FL

The test module FL utilizes tutorial from https://towardsdatascience.com/federated-learning-a-step-by-step-implementation-in-tensorflow-aac568283399.

<b>Description: </b>
The test module trains provides an understanding of how to utilize tensorflow for federated learning by:
1. Showing how to get the weights from the client - including the scaling factor
2. Showing how to aggregate the weights on the server 

<b>Note </b>
Although the tutorial runs the client and server on one python script - simulating the client and server together which does not make use of distributed learning. We can implement flask on top of this current architecture. 