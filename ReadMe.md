# Interactive Webcam Stream

With this program you can quickly train a convolutional neural network on images obtained from your webcam stream, and use it to classify frames from your webcam stream live.

![](example.gif)

## How to start:
Enter labels in the textfield, and click "get training data" to gather training data for that label. Make sure to move around a bit so that the model does not just learn one static position.
Add a few more things, and click "train model". A small convolutional neural net will be trained on the data you just gathered.
After training is done, you can click "start predictions" to see the model in action.

Of course you can use this to gather and classify many different kinds of images, but my original plan is to eventually use this to overlay information in my video stream and use it in videoconferences.