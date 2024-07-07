from PIL import Image

# Path to your image file
image_path = "/Users/thiennghiem/Documents/GitHub/agent-philip/diagrams/output.svg"

# Open the image
try:
    img = Image.open(image_path)
    
    # Display basic information about the image
    print(f"Image format: {img.format}")
    print(f"Image size: {img.size}")
    print(f"Image mode: {img.mode}")
    
    # Show the image (this will open the image in your default image viewer)
    img.show()
except IOError:
    print("Unable to open the image file.")