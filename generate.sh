#!/bin/bash
# Runs the generate script preserving the build folder's .git repository and README.md

BUILD_DIR="build"
TEMP_DIR=".build_backup"

ensure_project_root() {
  if [ ! -d "site" ]; then
    echo "Error: This script must be run from the project root (missing ./site directory)." >&2
    exit 1
  fi
}

backup_build_artifacts() {
  if [ ! -d "$BUILD_DIR" ]; then
    return
  fi

  rm -rf "$TEMP_DIR"
  mkdir -p "$TEMP_DIR"

  [ -d "$BUILD_DIR/.git" ] && mv "$BUILD_DIR/.git" "$TEMP_DIR/"
  [ -f "$BUILD_DIR/README.md" ] && mv "$BUILD_DIR/README.md" "$TEMP_DIR/"
}

restore_build_artifacts() {
  if [ ! -d "$TEMP_DIR" ]; then
    return
  fi

  mkdir -p "$BUILD_DIR"

  [ -d "$TEMP_DIR/.git" ] && mv "$TEMP_DIR/.git" "$BUILD_DIR/"
  [ -f "$TEMP_DIR/README.md" ] && mv "$TEMP_DIR/README.md" "$BUILD_DIR/"

  rm -rf "$TEMP_DIR"
}

ensure_project_root
backup_build_artifacts
./.venv/bin/python3 ./site/generate.py
restore_build_artifacts

