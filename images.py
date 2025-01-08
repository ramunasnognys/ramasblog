import os
import re
import shutil

# Paths (using raw strings to handle Windows backslashes correctly)
posts_dir = r"C:\Users\Ramunas\AnthropicFun\ramasblog\content\posts"
attachments_dir = r"C:\Users\Ramunas\AnthropicFun\Second_Brain\posts\Attachments"
static_images_dir = r"C:\Users\Ramunas\AnthropicFun\ramasblog\static\images"

# Step 1: Process each markdown file in the posts directory
for filename in os.listdir(posts_dir):
    if filename.endswith(".md"):
        filepath = os.path.join(posts_dir, filename)
        
        with open(filepath, "r", encoding="utf-8") as file:
            content = file.read()
        
        # Step 2: Find all image links in the format ![[filename.png]]
        images = re.findall(r'!\[\[(.*?\.png)\]\]', content)
        
        # Step 3: Replace image links and ensure URLs are correctly formatted
        for image in images:
            # Convert URL-encoded filename back to normal for filesystem operations
            decoded_image = image.replace('%20', ' ')
            image_source = os.path.join(attachments_dir, decoded_image)
            
            if os.path.exists(image_source):
                # Copy the image to the static directory
                shutil.copy(image_source, static_images_dir)
                print(f"Copied {decoded_image} to {static_images_dir}")
            else:
                print(f"Warning: Image {decoded_image} not found in {attachments_dir}")
            
            # Prepare the Markdown-compatible link with %20 replacing spaces
            url_encoded_image = image.replace(' ', '%20')
            markdown_image = f"![{image}](/images/{url_encoded_image})"
            content = content.replace(f"![[{image}]]", markdown_image)
            
        # Step 5: Write the updated content back to the markdown file
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(content)

print("Markdown files processed and images copied successfully.")