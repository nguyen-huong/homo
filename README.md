# homo
scam https://github.com/jarelllama/Scam-Blocklist/blob/main/data/parked_domains.txt https://easychair.org/publications/preprint/XvQH/open


1. Academic Research & Foundations
The GlyphNet Project:
Source Paper: "GlyphNet: Homoglyph Domains Dataset and Detection Using Attention-Based Convolutional Neural Networks" by Akshat Gupta, Laxman Tomar, and Ridhima Garg
.
Contributions: Provided the foundational concepts for attention-based convolutional neural networks (utilizing CBAM modules)
 and the 4-million domain image dataset designed to learn visual edge-strokes
.
Repository: Accessible at Akshat4112/Homoglyph
.
The ShamFinder Framework:
Source Paper: "ShamFinder: An Automated Framework for Detecting IDN Homographs" (published at ACM IMC 2019) by Hiroaki Suzuki, Daiki Chiba, Yoshiro Yoneya, Tatsuya Mori, and Shigeki Goto
.
Contributions: Designed the automated visual similarity pipeline to construct the SimChar database
, which extracts visual twins by calculating pixel differences in GNU Unifont bitmap images
.
Repository: Accessible at shamfinder/shamfinder
.
2. Official Technical Specifications
Unicode Technical Standard #39 (UTS #39):
Source Standard: "Unicode Security Mechanisms" edited by Mark Davis and Michel Suignard
.
Contributions: Contains the official, manually-vetted confusable mapping database (confusables.txt) used worldwide to generate base skeletal mappings
.
Data Directory: Hosted officially at unicode.org/Public/security/
.
Unicode Confusable Ruby Library:
Source Library: unicode-confusable gem by Jan Lelis
.
Contributions: Implements the transitive closure algorithm described in UTS #39 to check if strings are visually confusable
.
Repository: Accessible at janlelis/unicode-confusable
.
3. Permutation & Fuzzing Engines
dnstwist:
Source Tool: "dnstwist: Domain name permutation engine" by Marcin Ulikowski
.
Contributions: The industry-standard tool used by SOCs and threat intelligence platforms to automate the generation of brand typosquats, bitsquats, and registerable IDN homoglyphs
.
Repository: Accessible at elceef/dnstwist
.
4. Active Threat Intelligence Feeds
Jarelllama's Scam Blocklist:
Source Feed: "Scam-Blocklist" repository
.
Contributions: Serves daily-updated blocklists targeting malicious and parked domains
, alongside the regular expression phishing rules found in phishing_detection.csv
.
Repository: Accessible at jarelllama/Scam-Blocklist
.
"Into the thick of it!" Threat Blog:
Source Feed: "Generating and detecting phishing domains with IDN homograph attacks" by Varrick
.
Contributions: Outlined practical workflows for conducting reverse-lookup lookalike matching against newly registered domain lists obtained daily from WhoisDS
.
Repository: Accessible at varrickkoh/IDN-Homograph-Detector
.


https://github.com/Akshat4112/Glyphnet/tree/master
https://www.kaggle.com/datasets/alishan07/adversarial-homograph-detection

