import os
import csv
import re
import sys
import unicodedata
import json

class HomoglyphDetector:
    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.single_char_mappings = {}
        self.composite_mappings = {}
        self.load_mappings()

    def load_mappings(self):
        if not os.path.exists(self.csv_path):
            raise FileNotFoundError(f"Mapping database not found at {self.csv_path}")
        
        with open(self.csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                category = row['Category']
                target = row['Target_Character_or_Sequence']
                lookalike = row['Lookalike_Character_or_Sequence']
                
                # Clean up lookalike text
                if "vs." in lookalike:
                    parts = [p.strip() for p in lookalike.split("vs.")]
                    lookalike = parts[0] if not parts[0].isascii() else parts[1]
                if lookalike == 'facébook.com':
                    lookalike = 'é'
                    target = 'e'
                
                if 'Composite' in category or 'Complex' in category:
                    self.composite_mappings[lookalike] = {
                        'target': target,
                        'category': category,
                        'desc': row['Description']
                    }
                else:
                    self.single_char_mappings[lookalike] = {
                        'target': target,
                        'category': category,
                        'desc': row['Description']
                    }

        # Add fallback mappings for very common visual twins not fully covered in the basic CSV
        fallbacks = {
            'а': 'a', 'с': 'c', 'е': 'e', 'і': 'i', 'ј': 'j', 'о': 'o', 'р': 'p', 'ѕ': 's', 'х': 'x', 'у': 'y',
            'А': 'A', 'С': 'C', 'Е': 'E', 'І': 'I', 'Ј': 'J', 'О': 'O', 'Р': 'P', 'Ѕ': 'S', 'Х': 'X', 'У': 'Y',
            'ı': 'i', 'í': 'i', 'ì': 'i', 'ï': 'i', 'ä': 'a', 'ö': 'o', 'ü': 'u'
        }
        for k, v in fallbacks.items():
            if k not in self.single_char_mappings:
                self.single_char_mappings[k] = {
                    'target': v,
                    'category': 'Single-Character (Twin)',
                    'desc': f"Visual lookalike mapping for '{v}' (diacritic or cross-script Cyrillic)"
                }

    def analyze_domain(self, domain):
        # We will scan the domain and look for homoglyphs
        skeleton = domain.lower()
        substitutions = []
        categories_triggered = set()
        
        # 1. Check composite/sequence mappings (e.g., 'rn' -> 'm')
        # We search them first since they represent multi-character sequences
        for lookalike, info in sorted(self.composite_mappings.items(), key=lambda x: len(x[0]), reverse=True):
            if lookalike in skeleton:
                # Find all occurrences
                for match in re.finditer(re.escape(lookalike), skeleton):
                    start, end = match.span()
                    substitutions.append({
                        'index': start,
                        'original_sequence': lookalike,
                        'target_sequence': info['target'],
                        'category': info['category'],
                        'description': info['desc'],
                        'lookalike_hex': ' '.join(f"U+{ord(c):04X}" for c in lookalike),
                        'target_hex': ' '.join(f"U+{ord(c):04X}" for c in info['target'])
                    })
                    categories_triggered.add(info['category'])
                # Perform substitution in skeleton
                skeleton = skeleton.replace(lookalike, info['target'])

        # 2. Scan character-by-character for single-character homoglyphs
        new_skeleton_chars = []
        for idx, char in enumerate(skeleton):
            if char in self.single_char_mappings:
                info = self.single_char_mappings[char]
                substitutions.append({
                    'index': idx,
                    'original_sequence': char,
                    'target_sequence': info['target'],
                    'category': info['category'],
                    'description': info['desc'],
                    'lookalike_hex': f"U+{ord(char):04X}",
                    'target_hex': f"U+{ord(info['target']):04X}"
                })
                categories_triggered.add(info['category'])
                new_skeleton_chars.append(info['target'])
            elif unicodedata.category(char) in ('Mn', 'Me'):
                substitutions.append({
                    'index': idx,
                    'original_sequence': char,
                    'target_sequence': '',
                    'category': 'Single-Character (Diacritics)',
                    'description': f"Combining diacritical mark: {unicodedata.name(char, 'Unknown')}",
                    'lookalike_hex': f"U+{ord(char):04X}",
                    'target_hex': ''
                })
                categories_triggered.add('Single-Character (Diacritics)')
            else:
                new_skeleton_chars.append(char)
                
        final_skeleton = "".join(new_skeleton_chars)
        
        # Decompose and normalize as a final ASCII safety filter
        decomp = unicodedata.normalize('NFKD', final_skeleton)
        final_skeleton_ascii = "".join([c for c in decomp if not unicodedata.combining(c) and c.isascii()])

        is_homoglyph = len(substitutions) > 0 or final_skeleton_ascii != domain.lower()
        
        return {
            'original_domain': domain,
            'is_homoglyph': is_homoglyph,
            'skeleton_domain': final_skeleton_ascii if is_homoglyph else domain,
            'substitutions': sorted(substitutions, key=lambda x: x['index']),
            'categories_triggered': list(categories_triggered)
        }

def run_demo():
    print("=" * 80)
    print("        GLYPHNET / SHAMFINDER AUTOMATED HOMOGLYPH DETECTION TOOL")
    print("=" * 80)
    
    csv_path = "/workspace/artifacts/comprehensive_homoglyphs.csv"
    detector = HomoglyphDetector(csv_path)
    
    test_domains = [
        "google.com",              # Legitimate
        "gmaıl.com",               # Turkish dotless i (U+0131)
        "facébook.com",            # Accent/Diacritic spoof (U+00E9)
        "rnicrosoft.com",          # ASCII composite (rn -> m)
        "арple.com",               # Cyrillic 'а' and 'р'
        "g໐໐gle.com",              # Lao Digit Zero (U+0ED0)
        "clown.com",               # Normal domain (Will trigger cl->d string replacement false positive)
        "cllntothethickof.com",    # cl -> d check
        "vviki.com"                # vv -> w typosquatting
    ]
    
    print(f"{'Test Domain':<25} | {'Is Homoglyph?':<12} | {'Original/Skeleton Target':<25}")
    print("-" * 80)
    for domain in test_domains:
        res = detector.analyze_domain(domain)
        status = "⚠️ YES" if res['is_homoglyph'] else "✅ NO"
        print(f"{res['original_domain']:<25} | {status:<12} | {res['skeleton_domain']:<25}")
        
    print("\n" + "=" * 80)
    print("               DETAILED ANALYSIS OF SUSPICIOUS DOMAINS")
    print("=" * 80)
    for domain in test_domains:
        res = detector.analyze_domain(domain)
        if res['is_homoglyph']:
            print(f"\n[!] Domain: {domain}")
            print(f"    Reconstructed Skeleton: {res['skeleton_domain']}")
            print(f"    Triggered Categories: {', '.join(res['categories_triggered'])}")
            
            # Theoretical Insight Highlight
            if domain == "clown.com":
                print("    💡 NOTE ON FALSE POSITIVES:")
                print("       Notice how standard string replacement naive scanners flag 'clown.com' as 'down.com'.")
                print("       This represents a major drawback of non-visual techniques described in the sources.")
                print("       GlyphNet overcomes this using an Attention-based CNN on rendered image grids.")
                
            print("    Substitutions Identified:")
            for sub in res['substitutions']:
                tgt_disp = f"'{sub['target_sequence']}'" if sub['target_sequence'] else "None (stripped)"
                print(f"      - Replacement: {sub['original_sequence']} ({sub['lookalike_hex']}) -> {tgt_disp} ({sub['target_hex']})")
                print(f"        Category: {sub['category']} | Reason: {sub['description']}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        csv_path = "/workspace/artifacts/comprehensive_homoglyphs.csv"
        detector = HomoglyphDetector(csv_path)
        for arg in sys.argv[1:]:
            if os.path.exists(arg):
                print(f"Scanning domain list file: {arg}")
                with open(arg, 'r', encoding='utf-8') as f:
                    domains = [line.strip() for line in f if line.strip()]
                detected_count = 0
                for d in domains:
                    res = detector.analyze_domain(d)
                    if res['is_homoglyph']:
                        detected_count += 1
                        print(f"⚠️ [HOMOGLYPH] {d} -> SKELETON: {res['skeleton_domain']} (Triggered: {', '.join(res['categories_triggered'])})")
                print(f"Scan complete. Detected {detected_count} homoglyphs out of {len(domains)} scanned.")
            else:
                res = detector.analyze_domain(arg)
                print(json.dumps(res, indent=2, ensure_ascii=False))
    else:
        run_demo()
