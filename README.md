# BSL_Interpretor_preview
Here is where I show off my BSL interpreter project. The actual project is my Degree dissertation so I cant show it fully before its submitted without breaking academic rules. This is the early prototype I used to prove to my supervisor that I could do this ambitious project. For those interested in full demos of the full version contact me at christian.browning213@gmail.com. 

Because I made the model with BOBSL I will not include the model to be downloaded but have included a demo of the limited prototype. I would be happy to share and demonstrate the system over call however both academic integrety and BOBSL being a private dataset means I cannot share the models publicly.

The BSL model takes 13 frames of Mediapipe Pose and hand data giving 75 (x,y) coordinates and runs it through a LSTM to represent sequentiality of meaning to get the final sign. I will now go through the system from Dataset creation to final prototype and the planned design of the final system.

Dataset creation:

The dataset used was BOBSL which is a large multi terabyte dataset of BSL videos and specifc "spottings" of certain words, these spottings are what the AI is trained on.
Here is the original data:

[
“1”: {
		“Probs”: [
			______
			],
		“Global_times”: [
			______
			],
		“Video_Names”:[
			_____
			]
		},
]

I then processing these taking a limited number of specific signs for training the underpowered prototype. I formatted them as such:

Video,label,start,end

Then I used Wget to programatically get only the specific videos I needed from the dataset the ffmeg to split into individual 5 second clips.

This left me with a file structure looking like so:

BSL Data\Sign 1\____ , ____ , ____
BSL Data\Sign 2\____ , ____ , ____
BSL Data\Sign 3\____ , ____ , ____

The final dataset was then created by a python script which I have included called Dataset_creation.py which shows every video in every folder as seen above being passed through both mediapipe models and then stored in a large dataset file creating the final dataset to be passed into the model.

Prototype model:

this prototype was made to be lightweight and easy for my home pc to generate tests repeatably so its size was kept to a minimum.

it is a Lstm which was used to replicate the sequentiality needed to interprate BSL.

model = models.Sequential(
layers.LSTM(128, input_shape=(13, 150), return_sequences=True),
layers.BatchNormalization(),
layers.Dropout(0.4),
layers.LSTM(128, return_sequences=True),
layers.Dropout(0.4),
layers.LSTM(64),
layers.Dropout(0.4),
layers.BatchNormalization(),
layers.Dense(64, activation='relu'),
layers.Dense(23, activation='softmax')  
])

This model was effective getting a test accuracy of 0.75. This code can be found in "Model_Creation.py".

New model:

My new model is built of the old but with a much larger set of paramiters and dataset including many architectureal changes from what I learned from the original. 

Main architectural change was increased use of CNN's at the start as I realised that my model was digesting and inputting the data directly into LSTM cells which meant there wasnt a filter to learn what data wasnt important. This is especially important when trying to do BSL interpreting because the model leanring that the hands are way more important than any other specific pose data is something it would learn very quickly in a CNN but the sequentiality of a LSTM means this aspect is limited.

another change was use of tranformers and feed forward networks which has improved model effiencey and greatly.

if you want to see this model in action I am happy to do a demo and talk through the system with anyone interested. 



