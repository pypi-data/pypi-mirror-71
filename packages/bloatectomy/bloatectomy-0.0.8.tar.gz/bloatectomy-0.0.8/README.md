# Bloatectomy
Bloatectomy: a method for the identification and removal of duplicate text in the bloated notes of electronic health records and other documents. Takes in a list of notes or a single file (.docx, .txt, .rtf, etc) or single string to be marked for duplicates. Marked output and tokens are output.

# Requirements
- Python>=3.7.x (in order for the regular expressions to work correctly)
- re
- sys
- pandas (optional, only necessary if using MIMIC III data)
- docx (optional, only necessary if input or output is a word/docx file)

# Installation
using pip via PyPI
```
pip install bloatectomy
```
using pip via github
```
pip install git+git://github.com/MIT-LCP/mimic-code
```
manual install by cloning the repository
```
git clone git://github.com/MIT-LCP/mimic-code
cd bloatectomy
python3 setup.py install
```

# Example
To run bloatectomy on the sample text provided in the `input` folder:

```
from bloatectomy import bloatectomy

bloatectomy('./input/sample_text.txt', style='highlight', display=False, filename='./output/sample_txt_highlight_output', output='html', output_numbered_tokens=True, output_original_tokens=True);
```

# Documentation
```
class bloatectomy(input_text,
                  path = '',
                  filename='bloatectomized_file',
                  display=False,
                  style='highlight',
                  output='html',
                  output_numbered_tokens=False,
                  output_original_tokens=False,
                  regex1=r"(.+?\.[\s\n]+)",
                  regex2=r"(?=\n\s*[A-Z1-9#-]+.*)",
                  postgres_engine=None,
                  postgres_table=None)
```
## Parameters  
**input_text**: file, str, list  
An input document (.txt, .rtf, .docx), a string of text, or list of hadm_ids for postgres mimiciii database or the raw text.

**style**: str, optional, default=`highlight`  
Method for denoting a duplicate. The following are allowed: `highlight`, `bold`, `remov`.

**filename**: str, optional, default=`bloatectomized_file`
A string to name output file of the bloat-ectomized document.

**path**: str, optional, default=`' '`  
The directory for output files.

**output_numbered_tokens**: bool, optional, default=`False`  
If set to `True`, a .txt file with each token enumerated and marked for duplication, is output as `[filename]_token_numbers.txt`. This is useful when diagnosing your own regular expression for tokenization or testing the `remov` option for **style**.

**output_original_tokens**: bool, optional, default=`False`  
If set to  `True`, a .txt file with each original (non-marked) token enumerated but not marked for duplication, is output as `[filename]_original_token_numbers.txt`.

**display**: bool, optional, default=`False`  
If set to `True`, the bloatectomized text will display in the console on completion.

**regex1**: str, optional, default=`r"(.+?\.[\s\n]+)"`  
The regular expression for the first tokenization. Split on a period (.) followed by one or more white space characters (space, tab, line breaks) or a line feed character (`\n`). This can be replaced with any valid regular expression to change the way tokens are created.

**regex2**: str, optional, default=`r"(?=\n\s*[A-Z1-9#-]+.*)"`  
The regular expression for the second tokenization. Split on any newline character (`\n`) followed by an uppercase letter, a number, or a dash. This can be replaced with any valid regular expression to change how sub-tokens are created.

**postgres_engine**: str, optional
The postgres connection. Only relevant for use with the MIMIC III dataset. See the jupyter notebook [mimic_bloatectomy_example](mimic_bloatectomy_example.ipynb) for the example code.

**postgres_table**: str, optional
The name of the postgres table containing the concatenated notes. Only relevant for use with the MIMIC III dataset. See the jupyter notebook [mimic_bloatectomy_example](mimic_bloatectomy_example.ipynb) for the example code.
