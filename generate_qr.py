#!/usr/bin/env python3
import qrcode
import io
import base64

def generate_qr_code(url):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Save as file
    img.save("demo_qr_code.png")
    
    # Generate base64 for embedding
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    img_str = base64.b64encode(buffer.getvalue()).decode()
    
    return img_str

if __name__ == "__main__":
    # Replace with your deployed URL
    demo_url = "https://your-app.vercel.app"  # Update after deployment
    
    print("🔗 Generating QR Code for demo access...")
    qr_base64 = generate_qr_code(demo_url)
    
    print(f"✅ QR Code generated and saved as 'demo_qr_code.png'")
    print(f"📱 Demo URL: {demo_url}")
    print(f"🎯 Scan QR code to access the live demo!")
    
    # Generate HTML with embedded QR
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head><title>Supply Chain Optimizer - Demo Access</title></head>
    <body style="text-align: center; font-family: Arial;">
        <h1>🌱 Sustainable Supply Chain Optimizer</h1>
        <h2>📱 Scan to Access Live Demo</h2>
        <img src="data:image/png;base64,{qr_base64}" alt="QR Code" style="max-width: 300px;">
        <p><a href="{demo_url}" target="_blank">{demo_url}</a></p>
    </body>
    </html>
    """
    
    with open("demo_access.html", "w") as f:
        f.write(html_content)
    
    print("📄 Demo access page created: demo_access.html")