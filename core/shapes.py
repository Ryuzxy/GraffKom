import cairo
import pygame
import math

def draw_bentuk(bentuk, warna, size=250):
    """Menggambar bentuk menggunakan Cairo"""
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, size, size)
    ctx = cairo.Context(surface)
    
    # Set warna
    r, g, b = warna
    ctx.set_source_rgb(r/255, g/255, b/255)
    color = (r, g, b, 255)
    
    pad = 25
    
    if bentuk == "persegi":
        ctx.rectangle(pad, pad, size - pad*2, size - pad*2)
        ctx.fill()
        
    elif bentuk == "lingkaran":
        ctx.arc(size/2, size/2, (size-pad*2)/2, 0, 2 * math.pi)
        ctx.fill()
        
    elif bentuk == "segitiga":
        ctx.move_to(size/2, pad)
        ctx.line_to(pad, size - pad)
        ctx.line_to(size-pad, size-pad)
        ctx.close_path()
        ctx.fill()
        
    elif bentuk == "bintang":
        # Gambar bintang 5 sudut
        center_x, center_y = size/2, size/2
        outer_radius = (size - pad*2)/2
        inner_radius = outer_radius * 0.4
        
        for i in range(10):
            radius = outer_radius if i % 2 == 0 else inner_radius
            angle = math.pi/2 + i * math.pi/5
            
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            
            if i == 0:
                ctx.move_to(x, y)
            else:
                ctx.line_to(x, y)
                
        ctx.close_path()
        ctx.fill()
        
    elif bentuk == "jajar_genjang":
        # Jajar genjang (parallelogram)
        skew = pad * 2  # Skew/jarak miring
        points = [
            (pad + skew, pad),                   # Kiri atas
            (size - pad, pad),                   # Kanan atas
            (size - pad - skew, size - pad),     # Kanan bawah
            (pad, size - pad)                    # Kiri bawah
        ]
        pygame.draw.polygon(surface, color, points)
    
    elif bentuk == "segi_enam":
        # Hexagon (segi enam)
        points = []
        for i in range(6):
            angle = math.pi/6 + i * math.pi/3  # Dimulai dari atas
            x = center_x + radius * 0.9 * math.cos(angle)
            y = center_y + radius * 0.9 * math.sin(angle)
            points.append((x, y))
        pygame.draw.polygon(surface, color, points)
        
    elif bentuk == "segi_lima":
        # Pentagon (segi lima)
        points = []
        for i in range(5):
            angle = math.pi/2 + i * 2 * math.pi/5  # Dimulai dari atas
            x = center_x + radius * 0.9 * math.cos(angle)
            y = center_y + radius * 0.9 * math.sin(angle)
            points.append((x, y))
        pygame.draw.polygon(surface, color, points)
    
    
    # Convert ke Pygame surface
    img = pygame.image.frombuffer(
        surface.get_data(), 
        (size, size), 
        "ARGB"
    )
    return img.convert_alpha()