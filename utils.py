import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
import os

def generate_performance_tables(output_dir="tables"):
    """Generate tables summarizing performance metrics for the papers."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # OneFormer performance data
    oneformer_ade20k = {
        "Model": ["OneFormer (Swin-L)", "Mask2Former (Swin-L)", "OneFormer (DiNAT-L)"],
        "PQ": [49.8, 48.7, 51.5],
        "AP": [35.9, 34.3, 37.8],
        "mIoU": [57.0, 56.3, 58.3]
    }
    
    oneformer_cityscapes = {
        "Model": ["OneFormer (Swin-L)", "Mask2Former (Swin-L)", "OneFormer (ConvNeXt-L)"],
        "PQ": [67.2, 66.6, 68.5],
        "AP": [45.6, 43.7, 46.5],
        "mIoU": [83.0, 82.9, 84.0]
    }
    
    oneformer_coco = {
        "Model": ["OneFormer (Swin-L)", "Mask2Former (Swin-L)", "OneFormer (DiNAT-L)"],
        "PQ": [57.9, 57.8, 58.0],
        "AP": [49.0, 48.6, 49.2],
        "mIoU": [67.4, 67.4, 68.1]
    }
    
    # SDCL performance data
    sdcl_prid = {
        "Method": ["Baseline (V)", "SDCL (V+E)", "Improvement"],
        "mAP": [85.3, 96.9, "+11.6"],
        "Rank-1": [78.7, 96.5, "+17.8"],
        "Rank-5": [92.3, 100.0, "+7.7"]
    }
    
    sdcl_ilids = {
        "Method": ["Baseline (V)", "SDCL (V+E)", "Improvement"],
        "mAP": [85.2, 93.2, "+8.0"],
        "Rank-1": [80.0, 92.7, "+12.7"],
        "Rank-5": [94.3, 97.7, "+3.4"]
    }
    
    # Create CSV files
    with open(os.path.join(output_dir, "oneformer_ade20k.csv"), "w") as f:
        header = ",".join(oneformer_ade20k.keys())
        f.write(header + "\n")
        for i in range(len(oneformer_ade20k["Model"])):
            row = [oneformer_ade20k["Model"][i], 
                   str(oneformer_ade20k["PQ"][i]),
                   str(oneformer_ade20k["AP"][i]), 
                   str(oneformer_ade20k["mIoU"][i])]
            f.write(",".join(row) + "\n")
    
    # Similar for other datasets
    datasets = [
        ("oneformer_cityscapes.csv", oneformer_cityscapes),
        ("oneformer_coco.csv", oneformer_coco),
        ("sdcl_prid.csv", sdcl_prid),
        ("sdcl_ilids.csv", sdcl_ilids)
    ]
    
    for filename, data in datasets:
        with open(os.path.join(output_dir, filename), "w") as f:
            header = ",".join(data.keys())
            f.write(header + "\n")
            for i in range(len(data[list(data.keys())[0]])):
                row = [str(data[key][i]) for key in data.keys()]
                f.write(",".join(row) + "\n")
    
    print(f"Performance tables saved to {output_dir} directory.")

def generate_degradation_comparison_chart(output_dir="figures"):
    """Generate chart showing performance under degraded conditions."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    conditions = ['Normal', 'Blurry', 'Occluded']
    
    # PRID-2011 dataset
    baseline_prid = [85.3, 65.1, 70.2]  # mAP for baseline (V)
    sdcl_prid = [96.9, 89.5, 88.9]      # mAP for SDCL (V+E)
    
    # iLIDS-VID dataset
    baseline_ilids = [85.2, 55.0, 68.8]  # mAP for baseline (V)
    sdcl_ilids = [93.2, 71.4, 80.7]      # mAP for SDCL (V+E)
    
    x = np.arange(len(conditions))
    width = 0.2
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # PRID-2011 plot
    ax1.bar(x - width/2, baseline_prid, width, label='Baseline (V)')
    ax1.bar(x + width/2, sdcl_prid, width, label='SDCL (V+E)')
    ax1.set_ylabel('mAP (%)')
    ax1.set_title('PRID-2011 Performance Under Degradation')
    ax1.set_xticks(x)
    ax1.set_xticklabels(conditions)
    ax1.legend()
    ax1.yaxis.set_major_formatter(PercentFormatter())
    
    # iLIDS-VID plot
    ax2.bar(x - width/2, baseline_ilids, width, label='Baseline (V)')
    ax2.bar(x + width/2, sdcl_ilids, width, label='SDCL (V+E)')
    ax2.set_ylabel('mAP (%)')
    ax2.set_title('iLIDS-VID Performance Under Degradation')
    ax2.set_xticks(x)
    ax2.set_xticklabels(conditions)
    ax2.legend()
    ax2.yaxis.set_major_formatter(PercentFormatter())
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'degradation_comparison.png'), dpi=300, bbox_inches='tight')
    print(f"Degradation comparison chart saved to {output_dir} directory.")

if __name__ == "__main__":
    generate_performance_tables()
    generate_degradation_comparison_chart()
