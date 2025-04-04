import re
import os
from datetime import datetime

def extract_references_from_markdown(markdown_file):
    """Extract references from a markdown file containing links."""
    references = []
    with open(markdown_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to match markdown links: [title](url)
    pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    matches = re.findall(pattern, content)
    
    for title, url in matches:
        # Skip entries that are not valid URLs
        if not url.startswith(('http://', 'https://')):
            continue
            
        # Extract domain from URL
        domain_match = re.search(r'https?://(?:www\.)?([^/]+)', url)
        if domain_match:
            domain = domain_match.group(1)
        else:
            domain = "Unknown"
            
        references.append({
            'title': title,
            'url': url,
            'domain': domain,
            'accessed_date': datetime.now().strftime('%Y-%m-%d')
        })
    
    return references

def format_bibtex(references):
    """Format references in BibTeX format."""
    bibtex = []
    
    for i, ref in enumerate(references):
        # Create a key based on domain and index
        key = f"{ref['domain'].split('.')[0]}{i+1}"
        
        entry = f"""@online{{{key},
  title = {{{ref['title']}}},
  url = {{{ref['url']}}},
  urldate = {{{ref['accessed_date']}}},
  organization = {{{ref['domain']}}},
}}"""
        bibtex.append(entry)
    
    return '\n\n'.join(bibtex)

def format_csv(references):
    """Format references in CSV format."""
    header = "Title,URL,Domain,Accessed Date"
    rows = [f"\"{ref['title']}\",\"{ref['url']}\",\"{ref['domain']}\",\"{ref['accessed_date']}\"" 
            for ref in references]
    
    return header + '\n' + '\n'.join(rows)

def main():
    input_file = "additional_resources.md"
    output_dir = "bibliography"
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found.")
        return
    
    references = extract_references_from_markdown(input_file)
    print(f"Extracted {len(references)} references from {input_file}")
    
    # Generate BibTeX file
    bibtex_content = format_bibtex(references)
    with open(os.path.join(output_dir, "references.bib"), 'w', encoding='utf-8') as f:
        f.write(bibtex_content)
    
    # Generate CSV file
    csv_content = format_csv(references)
    with open(os.path.join(output_dir, "references.csv"), 'w', encoding='utf-8') as f:
        f.write(csv_content)
    
    print(f"Generated bibliography files in '{output_dir}' directory.")

if __name__ == "__main__":
    main()
