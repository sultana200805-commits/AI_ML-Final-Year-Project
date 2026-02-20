import tensorflow as tf
from tensorflow.keras import layers, models, applications

class BirdAudioModel:
    def __init__(self, num_classes, input_shape=(128, 128, 3)):
        self.num_classes = num_classes
        self.input_shape = input_shape
    
    def build_efficientnet_model(self):
        """
        Transfer Learning with EfficientNetB3
        Pretrained on ImageNet — works well even for spectrograms
        """
        # Load pretrained base
        base_model = applications.EfficientNetB3(
            include_top=False,
            weights='imagenet',
            input_shape=self.input_shape
        )
        
        # Freeze base initially for feature extraction
        base_model.trainable = False
        
        # Custom classification head
        inputs = tf.keras.Input(shape=self.input_shape)
        x = base_model(inputs, training=False)
        x = layers.GlobalAveragePooling2D()(x)
        x = layers.BatchNormalization()(x)
        x = layers.Dense(512, activation='relu')(x)
        x = layers.Dropout(0.4)(x)
        x = layers.Dense(256, activation='relu')(x)
        x = layers.Dropout(0.3)(x)
        outputs = layers.Dense(self.num_classes, activation='softmax')(x)
        
        model = tf.keras.Model(inputs, outputs)
        return model, base_model
    
    def build_custom_cnn(self):
        """
        Custom CNN from scratch — use if dataset is very domain-specific
        Multi-scale feature extraction for bird calls
        """
        inputs = tf.keras.Input(shape=self.input_shape)
        
        # Block 1 — capture fine-grained frequency patterns
        x = layers.Conv2D(32, (3, 3), padding='same', activation='relu')(inputs)
        x = layers.BatchNormalization()(x)
        x = layers.Conv2D(32, (3, 3), padding='same', activation='relu')(x)
        x = layers.MaxPooling2D((2, 2))(x)
        x = layers.Dropout(0.25)(x)
        
        # Block 2
        x = layers.Conv2D(64, (3, 3), padding='same', activation='relu')(x)
        x = layers.BatchNormalization()(x)
        x = layers.Conv2D(64, (3, 3), padding='same', activation='relu')(x)
        x = layers.MaxPooling2D((2, 2))(x)
        x = layers.Dropout(0.25)(x)
        
        # Block 3 — capture broader temporal patterns
        x = layers.Conv2D(128, (3, 3), padding='same', activation='relu')(x)
        x = layers.BatchNormalization()(x)
        x = layers.Conv2D(128, (3, 3), padding='same', activation='relu')(x)
        x = layers.MaxPooling2D((2, 2))(x)
        x = layers.Dropout(0.3)(x)
        
        # Block 4
        x = layers.Conv2D(256, (3, 3), padding='same', activation='relu')(x)
        x = layers.BatchNormalization()(x)
        x = layers.GlobalAveragePooling2D()(x)
        
        # Classification head
        x = layers.Dense(512, activation='relu')(x)
        x = layers.Dropout(0.4)(x)
        x = layers.Dense(256, activation='relu')(x)
        x = layers.Dropout(0.3)(x)
        outputs = layers.Dense(self.num_classes, activation='softmax')(x)
        
        return tf.keras.Model(inputs, outputs)