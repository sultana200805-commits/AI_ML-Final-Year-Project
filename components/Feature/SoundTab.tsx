import { Ionicons } from "@expo/vector-icons";
import React from "react";
import { StyleSheet, Text, TouchableOpacity, View } from "react-native";
import { useAudioRecorder } from "../../hooks/useAudioRecorder";
import { colors, radii, spacing } from "../../lib/theme";
import { formatTime } from "../../utils/formatters";

export default function SoundTab() {
  const {
    isRecording,
    recordingTime,
    startRecording,
    stopRecording,
    pickAudio,
  } = useAudioRecorder();

  const handleRecordPress = async () => {
    if (isRecording) {
      const uri = await stopRecording();
      if (uri) {
        console.log("Recording saved:", uri);
        // Handle the recorded audio
      }
    } else {
      await startRecording();
    }
  };

  const handleAddSound = async () => {
    const uri = await pickAudio();
    if (uri) {
      console.log("Audio file selected:", uri);
      // Handle the selected audio
    }
  };
  // Bharatiya Pakshi Sahayak Phechan

  // Random Forest

  return (
    <View style={styles.container}>
      {/* Recording Area */}
      <View style={styles.recordingArea}>
        {/* Timer */}
        <View style={styles.timerContainer}>
          <Text style={styles.timerText}>{formatTime(recordingTime)}</Text>
        </View>

        {/* Record Button */}
        <View style={styles.recordButtonContainer}>
          <TouchableOpacity
            style={[
              styles.recordButton,
              isRecording && styles.recordButtonActive,
            ]}
            onPress={handleRecordPress}
          >
            <View
              style={[
                styles.recordButtonInner,
                isRecording && styles.recordButtonInnerActive,
              ]}
            />
          </TouchableOpacity>
        </View>

        {/* Instructions */}
        <View style={styles.instructionsContainer}>
          <Text style={styles.instructionsText}>
            Tap the button above to start recording or upload your sound
          </Text>
        </View>

        {/* Add Sound Button */}
        <View style={styles.addSoundContainer}>
          <TouchableOpacity
            style={styles.addSoundButton}
            onPress={handleAddSound}
          >
            <Text style={styles.addSoundText}>Add Sound</Text>
            <Ionicons name="add" size={20} color={colors.textOnPrimary} />
          </TouchableOpacity>
        </View>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#F0F4E8",
  },
  recordingArea: {
    flex: 1,
    justifyContent: "flex-end",
    paddingHorizontal: spacing.xxl,
    paddingBottom: spacing.xxxl,
  },
  timerContainer: {
    alignItems: "center",
    marginBottom: spacing.xxl,
  },
  timerText: {
    fontSize: 48,
    fontWeight: "400",
    color: colors.text,
    letterSpacing: 2,
  },
  recordButtonContainer: {
    alignItems: "center",
    marginBottom: spacing.xl,
  },
  recordButton: {
    width: 90,
    height: 90,
    borderRadius: radii.round,
    borderWidth: 5,
    borderColor: colors.outline,
    backgroundColor: colors.background,
    justifyContent: "center",
    alignItems: "center",
  },
  recordButtonActive: {
    borderColor: "#FF5252",
  },
  recordButtonInner: {
    width: 60,
    height: 60,
    borderRadius: radii.round,
    backgroundColor: "#FF6B6B",
  },
  recordButtonInnerActive: {
    backgroundColor: "#FF5252",
  },
  instructionsContainer: {
    alignItems: "center",
    marginBottom: spacing.xxl,
  },
  instructionsText: {
    fontSize: 14,
    color: colors.textSecondary,
    textAlign: "center",
    lineHeight: 20,
  },
  addSoundContainer: {
    alignItems: "center",
  },
  addSoundButton: {
    backgroundColor: colors.primary,
    paddingVertical: spacing.lg,
    paddingHorizontal: spacing.xxxl,
    borderRadius: radii.md,
    flexDirection: "row",
    alignItems: "center",
    gap: spacing.sm,
  },
  addSoundText: {
    fontSize: 16,
    fontWeight: "500",
    color: colors.textOnPrimary,
  },
});
