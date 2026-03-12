import tensorflow as tf
from tensorflow.keras import layers, applications
class BirdImageModel:
    def __init__(self, num_classes, input_shape=(224, 224, 3)):
        self.num_classes = num_classes
        self.input_shape = input_shape
    
    def build_model(self):
        base_model = applications.EfficientNetB4(
            include_top=False,
            weights='imagenet',
            input_shape=self.input_shape
        )
        base_model.trainable = False
        
        inputs = tf.keras.Input(shape=self.input_shape)
        x = base_model(inputs, training=False)
        x = layers.GlobalAveragePooling2D()(x)
        x = layers.BatchNormalization()(x)
        x = layers.Dense(1024, activation='relu')(x)
        x = layers.Dropout(0.5)(x)
        x = layers.Dense(512, activation='relu')(x)
        x = layers.Dropout(0.3)(x)
        outputs = layers.Dense(self.num_classes, activation='softmax')(x)
        
        return tf.keras.Model(inputs, outputs), base_model