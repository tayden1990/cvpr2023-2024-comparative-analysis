import matplotlib.pyplot as plt
import numpy as np
import os
from matplotlib.gridspec import GridSpec

def create_radar_chart(ax, attributes, values, title):
    """Create a radar chart for paper attributes."""
    # Number of variables
    N = len(attributes)
    
    # Repeat the first value to close the polygon
    values = np.concatenate((values, [values[0]]))
    
    # What will be the angle of each axis in the plot
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]
    
    # Draw one axe per variable and add labels
    plt.xticks(angles[:-1], attributes, size=10)
    
    # Draw ylabels
    ax.set_rlabel_position(0)
    plt.yticks([0.2, 0.4, 0.6, 0.8], ["0.2", "0.4", "0.6", "0.8"], color="grey", size=8)
    plt.ylim(0, 1)
    
    # Plot data
    ax.plot(angles, values, linewidth=2, linestyle='solid')
    
    # Fill area
    ax.fill(angles, values, alpha=0.25)
    
    # Add title
    plt.title(title, size=13, pad=20)

def create_bar_chart(ax, labels, values1, values2, title, ylabel):
    """Create a comparison bar chart."""
    x = np.arange(len(labels))
    width = 0.35
    
    ax.bar(x - width/2, values1, width, label='OneFormer')
    ax.bar(x + width/2, values2, width, label='SDCL')
    
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

def create_methodology_diagram(ax, title):
    """Create a methodology comparison diagram."""
    # Define text content
    oneformer_text = "• Transformer-based architecture\n• Task-conditioned joint training\n• Task input token\n• Query-text contrastive loss\n• Universal architecture for all segmentation tasks"
    sdcl_text = "• Deformable Spiking Neural Network\n• Cross-Feature Alignment Module\n• Pyramid Aggregation Module\n• RGB and event stream fusion\n• Sparse-Dense Complementary Learning"
    
    ax.axis('off')
    ax.set_title(title, fontsize=14)
    
    # Draw boxes
    oneformer_box = plt.Rectangle((0.05, 0.55), 0.4, 0.35, fill=True, alpha=0.1, color='blue')
    sdcl_box = plt.Rectangle((0.55, 0.55), 0.4, 0.35, fill=True, alpha=0.1, color='red')
    
    ax.add_patch(oneformer_box)
    ax.add_patch(sdcl_box)
    
    # Add titles and content
    ax.text(0.25, 0.93, "OneFormer", fontsize=12, ha='center', fontweight='bold')
    ax.text(0.75, 0.93, "SDCL", fontsize=12, ha='center', fontweight='bold')
    
    ax.text(0.07, 0.85, oneformer_text, fontsize=10, va='top', ha='left')
    ax.text(0.57, 0.85, sdcl_text, fontsize=10, va='top', ha='left')
    
    # Draw the performance section
    ax.text(0.5, 0.45, "Performance Highlights", fontsize=12, ha='center', fontweight='bold')
    
    oneformer_perf = "• State-of-the-art on ADE20K\n  (PQ: 51.5%, mIoU: 58.8%)\n• Single model for 3 segmentation tasks\n• 3x resource efficiency vs.\n  separate models"
    sdcl_perf = "• PRID-2011: 96.9% mAP, 96.5% Rank-1\n• iLIDS-VID: 93.2% mAP, 92.7% Rank-1\n• Outperforms RGB-only under\n  blur and occlusion"
    
    oneformer_box2 = plt.Rectangle((0.05, 0.05), 0.4, 0.35, fill=True, alpha=0.1, color='blue')
    sdcl_box2 = plt.Rectangle((0.55, 0.05), 0.4, 0.35, fill=True, alpha=0.1, color='red')
    
    ax.add_patch(oneformer_box2)
    ax.add_patch(sdcl_box2)
    
    ax.text(0.07, 0.35, oneformer_perf, fontsize=10, va='top', ha='left')
    ax.text(0.57, 0.35, sdcl_perf, fontsize=10, va='top', ha='left')

def main():
    # Create directory for figures if it doesn't exist
    output_dir = "figures"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Paper characteristics for radar chart
    attributes = ['Novelty', 'Technical Complexity', 'Performance Gain', 
                 'Resource Efficiency', 'Practical Applicability']
    oneformer_values = [0.85, 0.78, 0.9, 0.95, 0.82]  # Example values (0-1 scale)
    sdcl_values = [0.88, 0.85, 0.75, 0.7, 0.8]  # Example values (0-1 scale)
    
    # Performance comparison data
    datasets = ['ADE20K', 'Cityscapes', 'COCO/PRID-2011', 'iLIDS-VID']
    oneformer_perf = [0.515, 0.685, 0.580, 0]  # PQ scores
    sdcl_perf = [0, 0, 0.969, 0.932]  # mAP scores
    
    # Create the main figure with GridSpec
    plt.figure(figsize=(18, 14))
    gs = GridSpec(2, 2, width_ratios=[1, 1], height_ratios=[1, 1])
    
    # Radar charts
    ax1 = plt.subplot(gs[0, 0], polar=True)
    create_radar_chart(ax1, attributes, oneformer_values, 'OneFormer Characteristics')
    
    ax2 = plt.subplot(gs[0, 1], polar=True)
    create_radar_chart(ax2, attributes, sdcl_values, 'SDCL Characteristics')
    
    # Bar chart for performance comparison
    ax3 = plt.subplot(gs[1, 0])
    create_bar_chart(ax3, datasets, oneformer_perf, sdcl_perf, 
                    'Performance Comparison', 'Score (PQ/mAP)')
    
    # Methodology diagram
    ax4 = plt.subplot(gs[1, 1])
    create_methodology_diagram(ax4, 'Methodology & Performance Comparison')
    
    plt.tight_layout(pad=3.0)
    plt.savefig(os.path.join(output_dir, 'paper_comparison.png'), dpi=300, bbox_inches='tight')
    
    # Create individual charts for potential inclusion in the report
    plt.figure(figsize=(8, 6))
    ax = plt.subplot(111, polar=True)
    create_radar_chart(ax, attributes, oneformer_values, 'OneFormer Characteristics')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'oneformer_radar.png'), dpi=300, bbox_inches='tight')
    
    plt.figure(figsize=(8, 6))
    ax = plt.subplot(111, polar=True)
    create_radar_chart(ax, attributes, sdcl_values, 'SDCL Characteristics')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'sdcl_radar.png'), dpi=300, bbox_inches='tight')
    
    print(f"Visualizations saved to {output_dir} directory.")

if __name__ == "__main__":
    main()
