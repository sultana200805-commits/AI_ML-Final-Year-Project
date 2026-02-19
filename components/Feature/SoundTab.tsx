import { Ionicons } from "@expo/vector-icons";
import React from "react";
import {
  Dimensions,
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
} from "react-native";
import { useAudioRecorder } from "../../hooks/useAudioRecorder";
import { colors, radii, spacing } from "../../lib/theme";
import { formatTime } from "../../utils/formatters";

const { height: SCREEN_HEIGHT } = Dimensions.get("window");
const COMPONENT_HEIGHT = SCREEN_HEIGHT * 0.8;

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
      }
    } else {
      await startRecording();
    }
  };

  const handleAddSound = async () => {
    const uri = await pickAudio();
    if (uri) {
      console.log("Audio file selected:", uri);
    }
  };

  return (
    <View style={styles.wrapper}>
      <View style={styles.container}>
        {/* Green top decorative area */}
        <View style={styles.greenArea} />

        {/* Controls */}
        <View style={styles.controls}>
          {/* Timer */}
          <Text style={styles.timerText}>{formatTime(recordingTime)}</Text>

          {/* Record Button */}
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

          {/* Instructions */}
          <Text style={styles.instructionsText}>
            Tap the button above to start recording or upload your sound
          </Text>

          {/* Add Sound Button */}
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
  wrapper: {
    height: COMPONENT_HEIGHT - 50,
    backgroundColor: colors.background,
  },
  container: {
    flex: 1,
    backgroundColor: colors.background,
  },
  greenArea: {
    flex: 7,
    backgroundColor: "#F0F4E8",
  },
  controls: {
    flex: 6,
    alignItems: "center",
    justifyContent: "space-evenly",
    paddingHorizontal: spacing.xxl,
    paddingVertical: spacing.md,
    backgroundColor: colors.background,
  },
  timerText: {
    fontSize: 24,
    fontWeight: "500",
    color: colors.text,
    letterSpacing: 2,
  },
  recordButton: {
    width: 70,
    height: 70,
    borderRadius: radii.round,
    borderWidth: 4,
    borderColor: colors.outline,
    backgroundColor: colors.background,
    justifyContent: "center",
    alignItems: "center",
  },
  recordButtonActive: {
    borderColor: "#FF5252",
  },
  recordButtonInner: {
    width: 50,
    height: 50,
    borderRadius: radii.round,
    backgroundColor: "#FF6B6B",
  },
  recordButtonInnerActive: {
    backgroundColor: "#FF5252",
  },
  instructionsText: {
    fontSize: 13,
    color: colors.textSecondary,
    textAlign: "center",
    lineHeight: 19,
  },
  addSoundButton: {
    backgroundColor: colors.primary,
    paddingVertical: spacing.md,
    paddingHorizontal: spacing.xxxl,
    borderRadius: radii.md,
    flexDirection: "row",
    alignItems: "center",
    gap: spacing.sm,
  },
  addSoundText: {
    fontSize: 15,
    fontWeight: "500",
    color: colors.textOnPrimary,
  },
});
