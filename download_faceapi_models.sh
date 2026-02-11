#!/bin/bash
# Setup script for face-api.js models
# Run this to download required models for face recognition

mkdir -p static/face-api/models

echo "Downloading face-api.js library..."
curl -L -o static/face-api/face-api.min.js \
  "https://cdn.jsdelivr.net/npm/face-api.js@0.22.2/dist/face-api.min.js"

echo "Downloading face detection models..."
# Tiny face detector model (smaller, faster)
curl -L -o static/face-api/models/tiny_face_detector_model-shard1 \
  "https://raw.githubusercontent.com/justadudewhohacks/face-api.js/master/weights/tiny_face_detector_model-shard1"
curl -L -o static/face-api/models/tiny_face_detector_model-weights_manifest.json \
  "https://raw.githubusercontent.com/justadudewhohacks/face-api.js/master/weights/tiny_face_detector_model-weights_manifest.json"

# Face landmark 68 model
curl -L -o static/face-api/models/face_landmark_68_model-shard1 \
  "https://raw.githubusercontent.com/justadudewhohacks/face-api.js/master/weights/face_landmark_68_model-shard1"
curl -L -o static/face-api/models/face_landmark_68_model-weights_manifest.json \
  "https://raw.githubusercontent.com/justadudewhohacks/face-api.js/master/weights/face_landmark_68_model-weights_manifest.json"

# Face recognition model
curl -L -o static/face-api/models/face_recognition_model-shard1 \
  "https://raw.githubusercontent.com/justadudewhohacks/face-api.js/master/weights/face_recognition_model-shard1"
curl -L -o static/face-api/models/face_recognition_model-shard2 \
  "https://raw.githubusercontent.com/justadudewhohacks/face-api.js/master/weights/face_recognition_model-shard2"
curl -L -o static/face-api/models/face_recognition_model-weights_manifest.json \
  "https://raw.githubusercontent.com/justadudewhohacks/face-api.js/master/weights/face_recognition_model-weights_manifest.json"

echo "Download complete! Models saved to static/face-api/models/"
echo ""
echo "For cloud deployment (Render), models will be loaded from CDN."

