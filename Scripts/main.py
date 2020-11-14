# from numpy import loadtxt
# from keras.models import Sequential
# from keras.layers import Dense
#
# #inputs:
# #1 fever
# #2 dry cough
# #3 fatigue
# #4 sore throat
# #5 difficulty breathing
# #6 new loss of taste or smell
# #7 headache
# #8 congestion
# #compile
# #output: no symptoms, observe, checked, emergency
#
# dataset = loadtxt('sample.cvs', delimiter=',')
#
# X = dataset[:,0:7]
# y = dataset[:,7]
#
# for i in range(len(y)):
#   y[i] *= 2
#
# model = Sequential()
# model.add(Dense(16, input_dim=7, activation='relu'))
# model.add(Dense(8, activation='softmax'))
# model.compile(loss="sparse_categorical_crossentropy", optimizer='adam', metrics=['accuracy'])
#
# model.fit(X, y, epochs=300, batch_size=30)
#
# _, accuracy = model.evaluate(X, y)
# print('Accuracy: %.2f' % (accuracy*100))
#
# model_json = model.to_json()
# with open("model.json", "w") as json_file:
#     json_file.write(model_json)
# # serialize weights to HDF5
# model.save_weights("model.h5")
# # model.save("model.h5")
#
# print("Saved model to disk")

from numpy import loadtxt
from keras.models import model_from_json
import operator
import collections

json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)

loaded_model.load_weights("model.h5")
loaded_model.compile(loss="sparse_categorical_crossentropy", optimizer='adam', metrics=['accuracy'])

print("This is a priority setter for doctors to deal with COVID patients effectively.\n"
      "Because there are millions of COVID patients, some take higher priorities then the rest, "
      "due to their symptoms")
text = ""
while text != "exit":
    while True:
        try:
            name = input("Please Type Your Name: ")
            fever = int(input("Rate Fever from 1-10: "))
            cough = int(input("Rate Your Dry Cough from 1-10: "))
            fatigue = int(input("Rate Fatigue from 1-10: "))
            throat = int(input("Rate Your Sore Throat from 1-10: "))
            breath = int(input("Rate Your Difficulty Breathing from 1-10: "))
            loss_of_taste = int(input("Rate Your Loss of Taste/Smell from 1-10: "))
            headache = int(input("Rate Your Headache from 1-10: "))
        except ValueError:
            print("Sorry, I didn't understand that.")
            continue
        else:
            # age was successfully parsed!
            # we're ready to exit the loop.
            break

    user_symptoms = [fever, cough, fatigue, throat, breath, loss_of_taste, headache]

    f = open("patients.txt", "a")
    m_string = str(user_symptoms)[1:-1]

    predictions = loaded_model.predict_classes([user_symptoms])

    f.write(name + ":" + m_string + ", " + str(predictions[0]) + "\n")
    f.close()

    f = open('patients.txt', 'r')
    patient_dict = {}

    while True:
        # Get next line from file
        line = f.readline()

        # if line is empty
        # end of file is reached
        if not line:
            break
        current_name = line.strip().split(":")[0]
        rating = line.strip().split(":")[1].split(',')[-1]

        patient_dict[current_name] = rating

    sorted_tuple = sorted(patient_dict.items(), key=operator.itemgetter(1), reverse=True)
    printing_dict = collections.OrderedDict(sorted_tuple)
    f.close()

    for keys in printing_dict.keys():
        print(keys + ": " + printing_dict[keys])
    text = input("If you would like to exit, spell 'exit'. If you would like to continue, press Enter:")
