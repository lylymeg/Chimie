import pygame
import random
import math
import sys

pygame.init()

# Dimensions de la fenêtre
WIDTH, HEIGHT = 900, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Particle Life Simulation (Artificial Chemistry)")
clock = pygame.time.Clock()

# Couleurs des types de particules
TYPES = 4
COLORS = [
    (255, 75, 75),   # Rouge (Type 0)
    (0, 255, 157),   # Vert (Type 1)
    (0, 162, 255),   # Bleu (Type 2)
    (255, 230, 0)    # Jaune (Type 3)
]

# Matrice des règles d'attraction/répulsion entre les types (-1.0 à 1.0)
rules = [[random.uniform(-1.0, 1.0) for _ in range(TYPES)] for _ in range(TYPES)]

class Particle:
    def __init__(self, x, y, p_type):
        self.x = x
        self.y = y
        self.vx = 0.0
        self.vy = 0.0
        self.type = p_type

particles = []

def spawn_ecosystem():
    global particles, rules
    # Générer de nouvelles lois chimiques aléatoires
    rules = [[random.uniform(-1.0, 1.0) for _ in range(TYPES)] for _ in range(TYPES)]
    
    particles = [
        Particle(
            random.randint(50, WIDTH - 50),
            random.randint(80, HEIGHT - 50),
            random.randint(0, TYPES - 1)
        )
        for _ in range(450)  # Nombre de particules
    ]

spawn_ecosystem()

# Polices
font_medium = pygame.font.SysFont("Arial", 20, bold=True)
font_small = pygame.font.SysFont("Arial", 15)

running = True
while running:
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                spawn_ecosystem()  # Régénérer un nouvel univers chimique

    # --- PHYSIQUE DE LA CHIMIE ARTIFICIELLE ---
    INTERACTION_RADIUS = 95
    
    for i, p1 in enumerate(particles):
        fx, fy = 0.0, 0.0
        for j, p2 in enumerate(particles):
            if i == j:
                continue
            
            dx = p2.x - p1.x
            dy = p2.y - p1.y
            dist = math.hypot(dx, dy)
            
            if 0 < dist < INTERACTION_RADIUS:
                f = rules[p1.type][p2.type]
                
                # Répulsion à très courte distance pour éviter qu'elles ne se superposent
                if dist < 22:
                    force = - (22 - dist) * 0.12
                else:
                    # Courbe d'attraction/répulsion selon la règle chimique
                    force = f * (1.0 - abs(dist - INTERACTION_RADIUS * 0.5) / (INTERACTION_RADIUS * 0.5))
                
                fx += (dx / dist) * force
                fy += (dy / dist) * force

        # Appliquer les forces avec frottement (amortissement)
        p1.vx = (p1.vx + fx) * 0.85
        p1.vy = (p1.vy + fy) * 0.85
        
        p1.x += p1.vx
        p1.y += p1.vy

        # Effet Tore (traverser les bords de l'écran)
        if p1.x < 0: p1.x = WIDTH
        elif p1.x > WIDTH: p1.x = 0
        if p1.y < 70: p1.y = HEIGHT
        elif p1.y > HEIGHT: p1.y = 70

    screen.fill((12, 15, 22))

    # 1. Dessiner les particules
    for p in particles:
        pygame.draw.circle(screen, COLORS[p.type], (int(p.x), int(p.y)), 4)

    # 2. En-tête HUD et Instructions
    title_txt = font_medium.render("PARTICLE LIFE — ÉMERGENCE & CHIMIE ARTIFICIELLE", True, (255, 255, 255))
    screen.blit(title_txt, (WIDTH // 2 - title_txt.get_width() // 2, 18))

    inst_txt = font_small.render("R : Générer un nouvel univers chimique avec de nouvelles lois d'attraction", True, (120, 130, 150))
    screen.blit(inst_txt, (WIDTH // 2 - inst_txt.get_width() // 2, 48))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()