import os

def create_directory_structure():
    """Create a clean directory structure for the project."""
    directories = [
        'figures',
        'tables',
        'papers',
        'presentations',
        'bibliography'
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created directory: {directory}")
    
    # Move files to appropriate directories (if they exist)
    file_moves = [
        # Format: (source, destination)
        ('paper_comparison.png', 'figures/paper_comparison.png'),
        ('degradation_comparison.png', 'figures/degradation_comparison.png'),
        ('oneformer_radar.png', 'figures/oneformer_radar.png'),
        ('sdcl_radar.png', 'figures/sdcl_radar.png'),
        # Add table files if they exist
        ('oneformer_ade20k.csv', 'tables/oneformer_ade20k.csv'),
        ('oneformer_cityscapes.csv', 'tables/oneformer_cityscapes.csv'),
        ('oneformer_coco.csv', 'tables/oneformer_coco.csv'),
        ('sdcl_prid.csv', 'tables/sdcl_prid.csv'),
        ('sdcl_ilids.csv', 'tables/sdcl_ilids.csv'),
    ]
    
    for source, destination in file_moves:
        if os.path.exists(source):
            if not os.path.exists(os.path.dirname(destination)):
                os.makedirs(os.path.dirname(destination))
            os.rename(source, destination)
            print(f"Moved: {source} → {destination}")

if __name__ == "__main__":
    create_directory_structure()
    print("Project organization complete!")
