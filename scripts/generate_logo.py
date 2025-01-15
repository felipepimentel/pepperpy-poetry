from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# Configurações
OUTPUT_DIR = Path("docs/assets/images")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Cores
BACKGROUND_COLOR = (63, 81, 181)  # Indigo
TEXT_COLOR = (255, 255, 255)  # Branco

def create_logo(size=(512, 512), text="P", output_file="logo.png"):
    # Criar imagem com fundo transparente
    image = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # Desenhar círculo de fundo
    circle_bbox = [size[0]*0.1, size[1]*0.1, size[0]*0.9, size[1]*0.9]
    draw.ellipse(circle_bbox, fill=BACKGROUND_COLOR)
    
    # Adicionar texto
    font_size = int(size[0] * 0.6)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
    except OSError:
        font = ImageFont.load_default()
    
    # Centralizar texto
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    text_x = (size[0] - text_width) / 2
    text_y = (size[1] - text_height) / 2
    
    # Desenhar texto
    draw.text((text_x, text_y), text, font=font, fill=TEXT_COLOR)
    
    # Salvar
    output_path = OUTPUT_DIR / output_file
    image.save(output_path, "PNG")
    return output_path

def create_favicon(logo_path, size=(32, 32), output_file="favicon.png"):
    # Carregar e redimensionar logo
    image = Image.open(logo_path)
    image = image.resize(size, Image.Resampling.LANCZOS)
    
    # Salvar
    output_path = OUTPUT_DIR / output_file
    image.save(output_path, "PNG")
    return output_path

def main():
    # Criar logo
    logo_path = create_logo(text="P")
    print(f"Logo criado em: {logo_path}")
    
    # Criar favicon
    favicon_path = create_favicon(logo_path)
    print(f"Favicon criado em: {favicon_path}")

if __name__ == "__main__":
    main() 