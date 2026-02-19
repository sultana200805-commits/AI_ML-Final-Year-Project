import { usePathname, useRouter } from "expo-router";
import { StyleSheet, Text, TouchableOpacity, View } from "react-native";

import Svg, { Path } from "react-native-svg";

// Custom Tab Bar Component
export default function CustomTabBar({ state, descriptors, navigation }: any) {
  const router = useRouter();
  const pathname = usePathname();

  return (
    <View style={styles.tabBarContainer}>
      <View style={styles.tabBar}>
        {/* Home Tab */}
        <TouchableOpacity
          onPress={() => navigation.navigate("index")}
          style={styles.tabItem}
        >
          <View style={styles.iconContainer}>
            <Svg width="24" height="24" viewBox="0 0 24 24" fill="none">
              <Path
                d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"
                stroke={pathname === "/" ? "#6B8E4E" : "#9CA3AF"}
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
                fill={pathname === "/" ? "#E8F5E9" : "none"}
              />
              <Path
                d="M9 22V12h6v10"
                stroke={pathname === "/" ? "#6B8E4E" : "#9CA3AF"}
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </Svg>
          </View>
          <Text
            style={[styles.tabLabel, pathname === "/" && styles.activeTabLabel]}
          >
            Home
          </Text>
        </TouchableOpacity>

        {/* Center Scanner Button */}
        <View style={styles.centerButtonWrapper}>
          <TouchableOpacity
            onPress={() => router.push("/scan")}
            style={styles.centerButton}
            activeOpacity={0.8}
          >
            <Svg width="32" height="32" viewBox="0 0 32 32" fill="none">
              <Path
                d="M8 8V6a2 2 0 0 1 2-2h4M24 8V6a2 2 0 0 0-2-2h-4M8 24v2a2 2 0 0 0 2 2h4M24 24v2a2 2 0 0 1-2 2h-4"
                stroke="white"
                strokeWidth="2.5"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
              <Path
                d="M16 12v8M12 16h8"
                stroke="white"
                strokeWidth="2.5"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </Svg>
          </TouchableOpacity>
        </View>

        {/* Collections Tab */}
        <TouchableOpacity
          onPress={() => navigation.navigate("collection")}
          style={styles.tabItem}
        >
          <View style={styles.iconContainer}>
            <Svg width="24" height="24" viewBox="0 0 24 24" fill="none">
              <Path
                d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"
                stroke={pathname === "/collection" ? "#6B8E4E" : "#9CA3AF"}
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
                fill={pathname === "/collection" ? "#E8F5E9" : "none"}
              />
            </Svg>
          </View>
          <Text
            style={[
              styles.tabLabel,
              pathname === "/collection" && styles.activeTabLabel,
            ]}
          >
            Collections
          </Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  tabBarContainer: {
    position: "absolute",
    bottom: -10,
    left: 0,
    right: 0,
    backgroundColor: "transparent",
  },
  tabBar: {
    flexDirection: "row",
    backgroundColor: "white",
    height: 120,
    paddingBottom: 10,
    paddingTop: 10,
    borderTopWidth: 1,
    borderTopColor: "#E5E7EB",
    alignItems: "flex-start",
    justifyContent: "space-around",
    shadowColor: "#000",
    shadowOffset: {
      width: 0,
      height: -2,
    },
    shadowOpacity: 0.1,
    shadowRadius: 3,
    elevation: 5,
  },
  tabItem: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
  },
  iconContainer: {
    marginBottom: 4,
  },
  tabLabel: {
    fontSize: 12,
    color: "#9CA3AF",
    fontWeight: "500",
  },
  activeTabLabel: {
    color: "#6B8E4E",
    fontWeight: "600",
  },
  centerButtonWrapper: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
    marginTop: -30,
  },
  centerButton: {
    width: 70,
    height: 70,
    borderRadius: "50%",
    backgroundColor: "#7BA05B",
    alignItems: "center",
    justifyContent: "center",
    shadowColor: "#000",
    shadowOffset: {
      width: 0,
      height: 4,
    },
    shadowOpacity: 0.3,
    shadowRadius: 4.65,
    elevation: 8,
  },
});
