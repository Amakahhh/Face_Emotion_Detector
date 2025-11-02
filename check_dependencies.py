"""
Quick script to check if all required dependencies are installed
"""

import sys

# Required packages
required_packages = {
    'flask': 'Flask',
    'tensorflow': 'TensorFlow',
    'numpy': 'NumPy',
    'pandas': 'Pandas',
    'cv2': 'OpenCV (opencv-python)',
    'PIL': 'Pillow',
    'gunicorn': 'Gunicorn'
}

print("=" * 60)
print("Checking Dependencies...")
print("=" * 60)

missing_packages = []
installed_packages = []

for package, name in required_packages.items():
    try:
        if package == 'cv2':
            import cv2
            print(f"[OK] {name} is installed")
            installed_packages.append(name)
        elif package == 'PIL':
            from PIL import Image
            print(f"[OK] {name} is installed")
            installed_packages.append(name)
        else:
            __import__(package)
            print(f"[OK] {name} is installed")
            installed_packages.append(name)
    except ImportError:
        print(f"[MISSING] {name} is NOT installed")
        missing_packages.append(name)

print("\n" + "=" * 60)
print("Summary:")
print("=" * 60)
print(f"Installed: {len(installed_packages)}/{len(required_packages)}")
print(f"Missing: {len(missing_packages)}/{len(required_packages)}")

if missing_packages:
    print("\n" + "=" * 60)
    print("Missing Packages:")
    print("=" * 60)
    for pkg in missing_packages:
        print(f"  - {pkg}")
    
    print("\n" + "=" * 60)
    print("To install all dependencies, run:")
    print("=" * 60)
    print("python -m pip install -r requirements.txt")
    sys.exit(1)
else:
    print("\n[SUCCESS] All dependencies are installed!")
    print("You can now run the app with: python app.py")
    sys.exit(0)

