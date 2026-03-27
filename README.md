# 🐋 VolumeKnuckle — Day 3, Soo hi chiggaaa😛
### Hand Tracking & Coordinate Mapping

**The Challenge:** Control system volume using a vertical fist gesture.

**Technical Achievement:**
- Integrated **MediaPipe** for 21-point hand landmarking.
- Mapped normalized Y-coordinates [0.15, 0.85] to Decibel levels [-65.0, 0.0] using **NumPy**.
- Implemented **Graceful Degradation**: Created a fail-safe mode to ensure the UI remains functional even if local audio drivers are locked.

**Reflection:**
Initially, the project faced "Not Responding" errors due to hardware constraints. I optimized the performance by lowering camera resolution and moving logic outside the main loop.
