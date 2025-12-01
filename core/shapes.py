import cairo
import pygame
import math

def draw_bentuk(bentuk, warna, size=250):
    """Menggambar bentuk menggunakan Cairo"""
    try:
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, size, size)
        ctx = cairo.Context(surface)
        
        # Set background transparent
        ctx.set_source_rgba(0, 0, 0, 0)
        ctx.paint()
        
        # Set warna bentuk
        r, g, b = warna
        ctx.set_source_rgb(r/255, g/255, b/255)
        
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
            
        elif bentuk == "segi_enam":
            center_x, center_y = size/2, size/2
            radius = (size - pad*2) / 2
            
            for i in range(6):
                angle = i * math.pi / 3
                x = center_x + radius * math.cos(angle)
                y = center_y + radius * math.sin(angle)
                
                if i == 0:
                    ctx.move_to(x, y)
                else:
                    ctx.line_to(x, y)
            
            ctx.close_path()
            ctx.fill()
            
        elif bentuk == "segi_lima":
            center_x, center_y = size/2, size/2
            radius = (size - pad*2) / 2
            
            for i in range(5):
                angle = math.pi/2 + i * 2 * math.pi / 5
                x = center_x + radius * math.cos(angle)
                y = center_y + radius * math.sin(angle)
                
                if i == 0:
                    ctx.move_to(x, y)
                else:
                    ctx.line_to(x, y)
            
            ctx.close_path()
            ctx.fill()
            
        elif bentuk == "bintang":
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
            
        elif bentuk == "hati":
            center_x, center_y = size/2, size/2
            scale = (size - pad*2) / 100
            
            # Gambar hati dengan bezier curves
            t = 0
            while t <= 1:
                # Persamaan parametrik untuk hati
                x = 16 * math.sin(t * math.pi)**3
                y = 13 * math.cos(t * math.pi) - 5 * math.cos(2*t*math.pi) - 2*math.cos(3*t*math.pi) - math.cos(4*t*math.pi)
                
                px = center_x + x * scale * 0.5
                py = center_y - y * scale * 0.5
                
                if t == 0:
                    ctx.move_to(px, py)
                else:
                    ctx.line_to(px, py)
                
                t += 0.01
            
            ctx.close_path()
            ctx.fill()
            
        elif bentuk == "jajar_genjang":
            offset = 30
            ctx.move_to(pad + offset, pad)
            ctx.line_to(size - pad, pad)
            ctx.line_to(size - pad - offset, size - pad)
            ctx.line_to(pad, size - pad)
            ctx.close_path()
            ctx.fill()
        
        else:
            # Default: gambar persegi untuk bentuk tidak dikenal
            print(f"Warning: Bentuk '{bentuk}' tidak dikenal, menggunakan persegi")
            ctx.rectangle(pad, pad, size - pad*2, size - pad*2)
            ctx.fill()
        
        # Convert ke Pygame surface
        img = pygame.image.frombuffer(
            surface.get_data(), 
            (size, size), 
            "ARGB"
        )
        return img.convert_alpha()
    
    except Exception as e:
        print(f"Error drawing bentuk '{bentuk}': {e}")
        # Return blank surface jika error
        blank_surf = pygame.Surface((size, size), pygame.SRCALPHA)
        blank_surf.fill((0, 0, 0, 0))
        return blank_surf