import tensorflow as tf
from tensorflow.keras import layers
class BirdFusionModel:
    """
    Late Fusion: Combine predictions from both models
    This is more robust than early fusion for multimodal inputs
    """
    def __init__(self, audio_model, image_model, num_classes):
        self.audio_model = audio_model
        self.image_model = image_model
        self.num_classes = num_classes
    
    def build_late_fusion_model(self):
        # Audio branch
        audio_input = tf.keras.Input(shape=(128, 128, 3), name='audio_input')
        audio_features = self.audio_model(audio_input)  # (batch, num_classes)
        
        # Image branch
        image_input = tf.keras.Input(shape=(224, 224, 3), name='image_input')
        image_features = self.image_model(image_input)  # (batch, num_classes)
        
        # Weighted fusion layer — learn optimal weights
        fused = layers.Average()([audio_features, image_features])
        
        # Optional: learnable weighted fusion
        concat = layers.Concatenate()([audio_features, image_features])
        x = layers.Dense(256, activation='relu')(concat)
        x = layers.Dropout(0.3)(x)
        outputs = layers.Dense(self.num_classes, activation='softmax')(x)
        
        fusion_model = tf.keras.Model(
            inputs=[audio_input, image_input],
            outputs=outputs
        )
        return fusion_model
    
    def weighted_ensemble_predict(self, audio_probs, image_probs, audio_weight=0.6, image_weight=0.4):
        """
        Simple weighted ensemble at inference time
        Audio weight higher as bird sound is more discriminative
        """
        combined = (audio_weight * audio_probs) + (image_weight * image_probs)
        return combined