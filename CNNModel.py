def main():

    import numpy as np
    from keras.models import Sequential
    from keras.layers import Convolution2D
    from keras.layers import MaxPooling2D
    from keras.layers import Flatten
    from keras.layers import Dense, Dropout
    from tensorflow.keras import optimizers
    from sklearn.metrics import classification_report
    import matplotlib.pyplot as plt
    
    basepath = "E:/100% Code/24SS105-Disasterclassification"
    
    # Initializing the CNN
    classifier = Sequential()
    
    # Step 1 - Convolution Layer
    classifier.add(Convolution2D(32, 1, 1, input_shape=(64, 64, 3), activation='relu'))
    
    # Step 2 - Pooling
    classifier.add(MaxPooling2D(pool_size=(2, 2)))
    
    # Adding second convolution layer
    classifier.add(Convolution2D(32, 1, 1, activation='relu'))
    classifier.add(MaxPooling2D(pool_size=(2, 2)))
    
    # Adding 3rd Convolution Layer
    classifier.add(Convolution2D(64, 1, 1, activation='relu'))
    classifier.add(MaxPooling2D(pool_size=(2, 2)))
    
    # Step 3 - Flattening
    classifier.add(Flatten())
    
    # Step 4 - Full Connection
    classifier.add(Dense(256, activation='relu'))
    classifier.add(Dropout(0.8))
    classifier.add(Dense(6, activation='softmax'))  # change class no.
    
    # Compiling The CNN
    classifier.compile(
        optimizer=optimizers.SGD(lr=0.01),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    # Part 2: Fitting the CNN to the images
    from keras.preprocessing.image import ImageDataGenerator
    train_datagen = ImageDataGenerator(
        rescale=1. / 255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True
    )
    
    test_datagen = ImageDataGenerator(rescale=1. / 255)
    
    training_set = train_datagen.flow_from_directory(
        basepath + '/training',
        target_size=(64, 64),
        batch_size=32,
        class_mode='categorical'
    )
    
    test_set = test_datagen.flow_from_directory(
        basepath + '/testing',
        target_size=(64, 64),
        batch_size=32,
        class_mode='categorical'
    )
    
    steps_per_epoch = int(np.ceil(training_set.samples / 32))
    val_steps = int(np.ceil(test_set.samples / 32))
    
    model = classifier.fit(
        training_set,
        steps_per_epoch=steps_per_epoch,
        epochs=886,
        validation_data=test_set,
        validation_steps=val_steps
    )
    
    # Saving the model
    classifier.save(basepath + '/D_model.h5')
    
    # Evaluate on the test set
    scores = classifier.evaluate(test_set, verbose=1)
    B = "Testing Accuracy: %.2f%%" % (scores[1] * 100)
    print(B)
    
    # Evaluate on the training set
    scores = classifier.evaluate(training_set, verbose=1)
    C = "Training Accuracy: %.2f%%" % (scores[1] * 100)
    print(C)
    
    # Predicting the results
    test_set.reset()
    predictions = classifier.predict(test_set, steps=val_steps, verbose=1)
    
    # Get the predicted class labels
    predicted_classes = np.argmax(predictions, axis=1)
    
    # Get the true class labels
    true_classes = test_set.classes
    
    # Generate the classification report
    report = classification_report(true_classes, predicted_classes, target_names=test_set.class_indices.keys())
    print("Classification Report:\n", report)
    
    # Saving the report to a text file
    with open(basepath + '/classification_report.txt', 'w') as f:
        f.write(report)
    
    msg = B + '\n' + C + '\n' + "Classification Report:\n" + report
    
    # Plot accuracy
    plt.plot(model.history['accuracy'])
    plt.plot(model.history['val_accuracy'])
    plt.title('Model Accuracy')
    plt.ylabel('Accuracy')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Test'], loc='upper left')
    plt.savefig(basepath + "/accuracy.png", bbox_inches='tight')
    plt.show()
    
    # Plot loss
    plt.plot(model.history['loss'])
    plt.plot(model.history['val_loss'])
    plt.title('Model Loss')
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Test'], loc='upper left')
    plt.savefig(basepath + "/loss.png", bbox_inches='tight')
    plt.show()

    return msg
