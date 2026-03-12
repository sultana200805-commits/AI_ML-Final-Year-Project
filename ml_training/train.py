# train.py
import os
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from pathlib import Path

from audio_preprocessor import AudioPreprocessor
from image_preprocessor import ImagePreprocessor
from dataset_builder import BirdDatasetBuilder
from audio_model import BirdAudioModel
from image_model import BirdImageModel
from trainer import ModelTrainer


def main():
    NUM_CLASSES = 132  # Update based on your dataset
    BATCH_SIZE = 16
    EPOCHS = 80
    
    os.makedirs('models', exist_ok=True)
    
    # ---- AUDIO MODEL TRAINING ----
    print("Building audio dataset...")
    dataset_builder = BirdDatasetBuilder('dataset/audio', 'dataset/images')
    X_audio, y_audio = dataset_builder.build_audio_dataset(augment=True)
    
    X_train, X_val, y_train, y_val = train_test_split(
        X_audio, y_audio, test_size=0.2, random_state=42, stratify=y_audio
    )
    
    train_ds = dataset_builder.build_tf_dataset(X_train, y_train, BATCH_SIZE)
    val_ds = dataset_builder.build_tf_dataset(X_val, y_val, BATCH_SIZE)
    
    print("Building audio model...")
    audio_model_builder = BirdAudioModel(NUM_CLASSES)
    audio_model, audio_base = audio_model_builder.build_efficientnet_model()
    audio_model.summary()
    
    trainer = ModelTrainer(audio_model, audio_base, NUM_CLASSES)
    trainer.train(train_ds, val_ds, EPOCHS)
    
    # Save final model
    audio_model.save('models/bird_audio_model.h5')
    print("Audio model saved!")
    
    # ---- IMAGE MODEL TRAINING ----
    # Similar process with ImageDataGenerator for images
    image_model_builder = BirdImageModel(NUM_CLASSES)
    image_model, image_base = image_model_builder.build_model()
    
    # Use flow_from_directory for image training
    img_preprocessor = ImagePreprocessor()
    datagen = img_preprocessor.get_augmentation_generator()
    
    train_gen = datagen.flow_from_directory(
        'dataset/images',
        target_size=(224, 224),
        batch_size=BATCH_SIZE,
        class_mode='sparse',
        subset='training'
    )
    val_gen = datagen.flow_from_directory(
        'dataset/images',
        target_size=(224, 224),
        batch_size=BATCH_SIZE,
        class_mode='sparse',
        subset='validation'
    )
    
    img_trainer = ModelTrainer(image_model, image_base, NUM_CLASSES)
    img_trainer.compile_model()
    image_model.fit(train_gen, validation_data=val_gen, epochs=EPOCHS,
                    callbacks=img_trainer.get_callbacks('image_model'))
    
    image_model.save('models/bird_image_model.h5')
    print("Image model saved!")

if __name__ == '__main__':
    main()
