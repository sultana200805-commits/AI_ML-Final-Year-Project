import tensorflow as tf
from tensorflow.keras.callbacks import (
    ModelCheckpoint, EarlyStopping, ReduceLROnPlateau, TensorBoard
)

class ModelTrainer:
    def __init__(self, model, base_model, num_classes):
        self.model = model
        self.base_model = base_model
    
    def compile_model(self, learning_rate=1e-3):
        self.model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate),
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy', tf.keras.metrics.TopKCategoricalAccuracy(k=5, name='top5_acc')]
        )
    
    def get_callbacks(self, model_name):
        return [
            ModelCheckpoint(
                f'models/{model_name}_best.h5',
                monitor='val_accuracy',
                save_best_only=True,
                mode='max',
                verbose=1
            ),
            EarlyStopping(
                monitor='val_accuracy',
                patience=10,
                restore_best_weights=True
            ),
            ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=5,
                min_lr=1e-7
            ),
            TensorBoard(log_dir=f'logs/{model_name}')
        ]
    
    def train(self, train_dataset, val_dataset, epochs=50):
        # PHASE 1: Train only the head (base frozen)
        print("Phase 1: Training classification head...")
        self.compile_model(learning_rate=1e-3)
        history1 = self.model.fit(
            train_dataset,
            validation_data=val_dataset,
            epochs=20,
            callbacks=self.get_callbacks('audio_model_phase1')
        )
        
        # PHASE 2: Fine-tune top layers of base model
        print("Phase 2: Fine-tuning...")
        self.base_model.trainable = True
        
        # Freeze bottom 70%, unfreeze top 30%
        fine_tune_at = int(len(self.base_model.layers) * 0.7)
        for layer in self.base_model.layers[:fine_tune_at]:
            layer.trainable = False
        
        # Lower LR for fine-tuning to avoid destroying pretrained weights
        self.compile_model(learning_rate=1e-5)
        history2 = self.model.fit(
            train_dataset,
            validation_data=val_dataset,
            epochs=epochs,
            callbacks=self.get_callbacks('audio_model_phase2')
        )
        
        return history1, history2
    
    def evaluate_model(self, test_dataset, label_encoder):
        from sklearn.metrics import classification_report, confusion_matrix
        
        y_pred, y_true = [], []
        for X_batch, y_batch in test_dataset:
            preds = self.model.predict(X_batch)
            y_pred.extend(np.argmax(preds, axis=1))
            y_true.extend(y_batch.numpy())
        
        print("\n=== Classification Report ===")
        print(classification_report(
            y_true, y_pred,
            target_names=label_encoder.classes_
        ))
        
        return y_pred, y_true