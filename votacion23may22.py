import pandas as pd
import matplotlib.pyplot as plt

# Datos oficiales ajustados
data = {
    'Partido': ['Morena', 'PAN', 'PRI', 'PVEM', 'PT', 'MC', 'PRD'],
    'A favor': [183, 99, 57, 36, 31, 1, 0],
    'En contra': [0, 0, 0, 0, 0, 0, 0],
    'Abstención': [0, 0, 0, 0, 0, 21, 14],
    'Ausente': [18, 14, 12, 4, 2, 6, 1]
}
df = pd.DataFrame(data)

# Colores por partido
partido_colors = {
    'Morena': '#800000',
    'PAN': '#0056A0',
    'PRI': '#E10600',
    'PVEM': '#3B9F3B',
    'PT': '#FF3300',
    'MC': '#FF7F00',
    'PRD': '#FFD700'
}

# Transparencias por tipo de voto
opacidades = {
    'A favor': 1.0,
    'Abstención': 0.5,
    'Ausente': 0.25
}

# Crear figura
fig, ax = plt.subplots(figsize=(12, 8))
bottoms = [0] * len(df)

# Orden de capas
voto_layers = ['A favor', 'Abstención', 'Ausente']

for voto in voto_layers:
    valores = df[voto]
    edgecolors = [
        'black' if not (p == 'MC' and voto == 'A favor') else '#4CAF50'
        for p in df['Partido']
    ]
    bars = ax.bar(
        df['Partido'],
        valores,
        bottom=bottoms,
        color=[partido_colors[p] for p in df['Partido']],
        edgecolor=edgecolors,
        linewidth=1.2 if voto == 'A favor' else 0.6,
        alpha=opacidades[voto],
        label=voto if voto not in ax.get_legend_handles_labels()[1] else ""
    )

    # Agregar etiquetas
    for bar in bars:
        height = bar.get_height()
        if height > 0:
            ypos = bar.get_y() + height / 2
            if height <= 3:
                ypos = bar.get_y() + height + 1.5  # subir etiqueta
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                ypos,
                f'{int(height)}',
                ha='center',
                va='bottom' if height <= 3 else 'center',
                fontsize=9,
                color='black' if voto != 'A favor' else 'white',
                weight='bold'
            )
    bottoms = [i + j for i, j in zip(bottoms, valores)]

# Anotación con flecha curva para destacar MC
ax.annotate(
    'MC: único voto a favor',
    xy=('MC', df.loc[5, 'A favor']),         # (MC, 1)
    xytext=('MC', 50),                      # texto arriba
    ha='center',
    va='bottom',
    arrowprops=dict(
        arrowstyle='->',
        lw=1.5,
        color='black',
        alpha=0.8,
        connectionstyle="arc3,rad=-0.3"  # curva hacia la izquierda
    ),
    fontsize=10,
    weight='bold'
)

# Título y ejes
ax.set_title('Votación por Partido - Reforma Ley del Equilibrio Ecológico (2022)', fontsize=15, weight='bold')
ax.set_ylabel('Número de Votos')
ax.set_xlabel('Partidos Políticos')
ax.set_ylim(0, max(df[['A favor', 'Abstención', 'Ausente']].sum(axis=1)) + 30)

# Leyenda y estética
ax.legend(title='Sentido del Voto', loc='upper right', frameon=False)
ax.grid(axis='y', linestyle='--', alpha=0.4)
plt.xticks(rotation=45)

# Firma y fuente
plt.figtext(0.5, 0.01, 'Autor: @el_laberintomx | Fuente: Gaceta Parlamentaria, Cámara de Diputados', 
            ha='center', fontsize=9, color='gray')

plt.tight_layout(rect=[0, 0.03, 1, 1])  # deja espacio para la firma
plt.show()
