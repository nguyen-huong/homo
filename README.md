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


Dataset
The work by (Woodbridge et al. 2018) proposed their custom paired data set that comprises 
91
​
k
 real domains and 
900
​
k
 homoglyphs. Each real domain is used to generate its respective homoglyphs. Each point in this dataset is a three-element tuple denoting domain, homoglyph, and score. Here, if the value of the score is 
1.0
, then it is a valid homoglyph of the real domain. The real-world data limitation to Homoglpyh-based attacks is the lack of publicly available data sets.

Proposed dataset: GlyphNet
We have proposed a dataset consisting of real and homoglyph domains. To generate homoglyph domains, real domains are needed. We have obtained domains from the Domains Project(Turkynewych 2020). This repository is one of the largest collections of publicly available active domains. The entire repository comprises 500M domains, and we restricted our work to 2M domains due to hardware restrictions.

Homoglyph Creation Algorithm
Homoglyph Generation is an important task, as one needs to ensure enough randomness to make it appear real and keep the process simple enough to fool the target. Publicly available tools like dnstwist(Ulikowski 2015) replace every character in the real input domain with their respective glyphs. It generates poor homoglyphs for the large part because it relies on paired data which is not fit to serve the purpose practically. We created our novel algorithm for the generation of homoglyph domains to ensure that real homoglyphs are generated with randomness and closeness. To achieve this, we sample homoglyph noise characters using Gaussian sampling(Boor, Overmars, and Van Der Stappen 1999) from the glyph pool. We used 1M real domains to generate 
2
​
M
 homoglyphs with a single glyph character and introduce diversity in our dataset; we reran this algorithm on the remaining 1M real domains to generate homoglyph domains with two character glyphs. Finally, we have the 4M real and homoglyph domains.

Image Generation
Homoglyph attacks exploit the weakness of human vision to differentiate real from homoglyph domain names. From a visual perspective, we are interested in learning the visual characteristics of real and homoglyph domain names. To do so, we rendered images from the real and homoglyph strings generated via our algorithm. We have used ARIAL Typeface as our chosen font, a 
28
 font size, on a black background with white text from the middle left of the image; the image size is 
150
×
150
.
https://arxiv.org/html/2306.10392#Sx3

