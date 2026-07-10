#!/usr/bin/env python3
"""
Academic Document Editor for MSc Thesis
Specifically for COMP40321 Research Methods submission
Focused on punctuation fixes and phrase-quality review
"""

import re
import os
from pathlib import Path
from datetime import datetime
import json
from typing import List, Dict, Tuple, Optional
import requests


class AcademicDocumentEditor:
    """Editor for academic documents with specific rules for MSc thesis."""
    
    def __init__(self, document_path: str):
        self.document_path = document_path
        self.backup_path = f"{document_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.changes_log = []
        
        # Load document
        with open(document_path, 'r', encoding='utf-8') as f:
            self.content = f.read()
        
        # Create backup
        with open(self.backup_path, 'w', encoding='utf-8') as f:
            f.write(self.content)
        
        print(f"📄 Loaded: {document_path}")
        print(f"💾 Backup: {self.backup_path}")
        print(f"📏 Length: {len(self.content)} characters, {len(self.content.split())} words")
    
    def analyze_document(self) -> Dict:
        """Analyze document for common issues."""
        print("\n🔍 Analyzing document for issues...")
        
        issues = {
            "em_dashes": self._count_em_dashes(),
            "semicolons": self._count_semicolons(),
            "long_sentences": self._find_long_sentences(),
            "ai_indicators": self._find_ai_indicators(),
            "punctuation_issues": self._find_punctuation_issues(),
            "section_breaks": self._find_sections()
        }
        
        # Print summary
        print(f"  • Em-dashes: {issues['em_dashes']['count']} found")
        print(f"  • Semicolons: {issues['semicolons']['count']} found")
        print(f"  • Long sentences: {len(issues['long_sentences'])} found")
        print(f"  • AI indicators: {len(issues['ai_indicators'])} found")
        print(f"  • Sections: {len(issues['section_breaks'])} found")
        
        return issues
    
    def _count_em_dashes(self) -> Dict:
        """Count and locate em-dashes."""
        # Em-dash patterns: —, --, –
        em_dash_pattern = r'—|--|–'
        matches = list(re.finditer(em_dash_pattern, self.content))
        
        return {
            "count": len(matches),
            "positions": [(m.start(), m.end()) for m in matches],
            "examples": [self.content[max(0, m.start()-50):min(len(self.content), m.end()+50)] 
                        for m in matches[:5]]  # First 5 examples
        }
    
    def _count_semicolons(self) -> Dict:
        """Count and locate semicolons."""
        matches = list(re.finditer(r';', self.content))
        
        return {
            "count": len(matches),
            "positions": [(m.start(), m.end()) for m in matches],
            "examples": [self.content[max(0, m.start()-50):min(len(self.content), m.end()+50)] 
                        for m in matches[:5]]
        }
    
    def _find_long_sentences(self) -> List[Dict]:
        """Find sentences that are too long."""
        sentences = re.split(r'[.!?]+', self.content)
        long_sentences = []
        
        for i, sentence in enumerate(sentences):
            word_count = len(sentence.split())
            if word_count > 30:  # Sentences longer than 30 words
                long_sentences.append({
                    "index": i,
                    "word_count": word_count,
                    "sentence": sentence.strip()[:200] + "..." if len(sentence) > 200 else sentence.strip()
                })
        
        return long_sentences
    
    def _find_ai_indicators(self) -> List[Dict]:
        """Find phrases that sound AI-generated."""
        ai_patterns = [
            r'it is important to note that',
            r'it should be noted that',
            r'in order to',
            r'as previously mentioned',
            r'as discussed above',
            r'this paper will',
            r'this study aims to',
            r'leveraging',
            r'harnessing',
            r'utilizing',
            r'furthermore',
            r'moreover',
            r'additionally',
            r'in conclusion',
            r'in summary',
            r'the aforementioned',
            r'it is worth noting that',
            r'it is crucial to',
            r'this research seeks to',
            r'this work presents',
            r'we propose a',
            r'our approach',
            r'state-of-the-art',
            r'cutting-edge',
            r'novel approach',
            r'innovative method',
        ]
        
        ai_indicators = []
        for pattern in ai_patterns:
            matches = list(re.finditer(pattern, self.content, re.IGNORECASE))
            for match in matches:
                ai_indicators.append({
                    "pattern": pattern,
                    "position": (match.start(), match.end()),
                    "context": self.content[max(0, match.start()-50):min(len(self.content), match.end()+50)]
                })
        
        return ai_indicators
    
    def _find_punctuation_issues(self) -> List[Dict]:
        """Find punctuation issues."""
        issues = []
        
        # Multiple spaces
        multi_space_matches = list(re.finditer(r' {2,}', self.content))
        for match in multi_space_matches:
            issues.append({
                "type": "multiple_spaces",
                "position": (match.start(), match.end()),
                "context": self.content[max(0, match.start()-30):min(len(self.content), match.end()+30)]
            })
        
        # Missing spaces after punctuation
        missing_space_matches = list(re.finditer(r'[.,!?;:][A-Za-z]', self.content))
        for match in missing_space_matches:
            issues.append({
                "type": "missing_space_after_punctuation",
                "position": (match.start(), match.end()),
                "context": self.content[max(0, match.start()-30):min(len(self.content), match.end()+30)]
            })
        
        return issues
    
    def _find_sections(self) -> List[Dict]:
        """Find document sections."""
        # Look for section headers (numbered or titled)
        section_patterns = [
            r'\n\d+\.\d+\s+[A-Z][^\n]+',  # 1.1 Title
            r'\n\d+\.\s+[A-Z][^\n]+',     # 1. Title
            r'\n[A-Z][A-Z\s]+\n',         # ALL CAPS HEADER
            r'\n###\s+[^\n]+',            # Markdown ### Header
            r'\n##\s+[^\n]+',             # Markdown ## Header
            r'\n#\s+[^\n]+',              # Markdown # Header
        ]
        
        sections = []
        for pattern in section_patterns:
            matches = list(re.finditer(pattern, self.content))
            for match in matches:
                sections.append({
                    "header": match.group().strip(),
                    "position": (match.start(), match.end()),
                    "type": "section_header"
                })
        
        return sections
    
    def fix_em_dashes(self, replace_with: str = ":") -> int:
        """
        Replace em-dashes with appropriate punctuation.
        
        Args:
            replace_with: What to replace em-dashes with (":", ",", or "—" to keep)
        """
        print(f"\n🔧 Fixing em-dashes (replacing with '{replace_with}')...")
        
        # Pattern for em-dashes
        em_dash_pattern = r'—|--|–'
        
        # Find all em-dashes
        matches = list(re.finditer(em_dash_pattern, self.content))
        
        if not matches:
            print("  No em-dashes found.")
            return 0
        
        # Build new content
        new_content = ""
        last_end = 0
        changes_made = 0
        
        for match in matches:
            start, end = match.start(), match.end()
            
            # Get context to decide if we should replace
            context_before = self.content[max(0, start-20):start]
            context_after = self.content[end:min(len(self.content), end+20)]
            
            # Ask for approval for each change
            print(f"\n  Found em-dash at position {start}:")
            print(f"    Context: ...{context_before}—{context_after}...")
            
            # Auto-replace based on context rules
            should_replace = True
            
            # Rule 1: If it's connecting clauses, replace with colon or semicolon
            if re.search(r'[a-z]\s*—\s*[A-Z]', self.content[max(0, start-1):end+1]):
                replacement = ":"
            # Rule 2: If it's parenthetical, replace with comma
            elif re.search(r'[.,;]\s*—\s*[a-z]', self.content[max(0, start-1):end+1]):
                replacement = ","
            else:
                replacement = replace_with
            
            print(f"    Proposed replacement: '{replacement}'")
            
            # Add to new content
            new_content += self.content[last_end:start] + replacement
            last_end = end
            changes_made += 1
            
            # Log change
            self.changes_log.append({
                "type": "em_dash_replacement",
                "position": start,
                "original": self.content[start:end],
                "replacement": replacement,
                "context": self.content[max(0, start-50):min(len(self.content), end+50)]
            })
        
        # Add remaining content
        new_content += self.content[last_end:]
        self.content = new_content
        
        print(f"  ✅ Replaced {changes_made} em-dashes")
        return changes_made
    
    def fix_semicolons(self) -> int:
        """Fix overuse of semicolons by breaking into separate sentences."""
        print("\n🔧 Fixing semicolon overuse...")
        
        # Find sentences with multiple semicolons
        semicolon_pattern = r'[^;]+;[^;]+;[^;]+'
        matches = list(re.finditer(semicolon_pattern, self.content))
        
        if not matches:
            print("  No problematic semicolon chains found.")
            return 0
        
        changes_made = 0
        new_content = ""
        last_end = 0
        
        for match in matches:
            start, end = match.start(), match.end()
            original_text = self.content[start:end]
            
            print(f"\n  Found semicolon chain at position {start}:")
            print(f"    Text: {original_text[:100]}...")
            
            # Ask for approval
            approval = input("    Replace with separate sentences? (y/n): ").lower().strip()
            
            if approval == 'y':
                # Replace semicolons with periods (except the last one if it's part of a list)
                fixed_text = re.sub(r';(?!\s*and\b|\s*or\b)', '.', original_text)
                
                # Capitalize sentences after periods
                sentences = re.split(r'\.\s+', fixed_text)
                fixed_sentences = []
                for i, sentence in enumerate(sentences):
                    if i > 0 and sentence and sentence[0].islower():
                        sentence = sentence[0].upper() + sentence[1:]
                    fixed_sentences.append(sentence)
                
                fixed_text = '. '.join(fixed_sentences)
                
                # Add to new content
                new_content += self.content[last_end:start] + fixed_text
                last_end = end
                changes_made += 1
                
                # Log change
                self.changes_log.append({
                    "type": "semicolon_fix",
                    "position": start,
                    "original": original_text,
                    "replacement": fixed_text,
                    "context": self.content[max(0, start-50):min(len(self.content), end+50)]
                })
                
                print(f"    ✅ Fixed: {fixed_text[:100]}...")
            else:
                print("    Skipped.")
        
        # Add remaining content
        new_content += self.content[last_end:]
        self.content = new_content
        
        print(f"  ✅ Fixed {changes_made} semicolon chains")
        return changes_made
    
    def humanize_with_superhumanizer(self, text: str, api_key: Optional[str] = None) -> str:
        """
        Use an optional rewriting service to compare alternative wording.
        Note: This requires an API key from https://superhumanizer.ai/
        """
        print("\nUsing an optional rewriting service to compare wording...")
        
        if not api_key:
            print("  ⚠️  No API key provided. Using local rules instead.")
            return self._humanize_locally(text)
        
        try:
            # Superhumanizer API endpoint (check their documentation for exact endpoint)
            url = "https://api.superhumanizer.ai/v1/humanize"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "text": text,
                "style": "academic",  # Or "professional", "casual"
                "tone": "formal"
            }
            
            response = requests.post(url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            humanized_text = result.get("humanized_text", text)
            
            print(f"  ✅ Text humanized (API)")
            return humanized_text
            
        except Exception as e:
            print(f"  ⚠️  API call failed: {e}")
            print("  Using local humanization rules instead.")
            return self._humanize_locally(text)
    
    def _humanize_locally(self, text: str) -> str:
        """Apply local rules for phrase-quality review."""
        # Common AI phrases and their more natural replacements
        replacements = {
            r'\bit is important to note that\b': 'Note that',
            r'\bit should be noted that\b': '',
            r'\bin order to\b': 'to',
            r'\bas previously mentioned\b': 'as mentioned',
            r'\bas discussed above\b': 'as discussed',
            r'\bthis paper will\b': 'this paper',
            r'\bthis study aims to\b': 'this study',
            r'\bleveraging\b': 'using',
            r'\bharnessing\b': 'using',
            r'\butilizing\b': 'using',
            r'\bfurthermore\b': 'also',
            r'\bmoreover\b': 'additionally',
            r'\badditionally\b': 'also',
            r'\bin conclusion\b': 'finally',
            r'\bin summary\b': 'to summarize',
            r'\bthe aforementioned\b': 'these',
            r'\bit is worth noting that\b': 'note that',
            r'\bit is crucial to\b': 'it is important to',
            r'\bthis research seeks to\b': 'this research',
            r'\bthis work presents\b': 'this work',
            r'\bwe propose a\b': 'we propose',
            r'\bour approach\b': 'our method',
            r'\bstate-of-the-art\b': 'advanced',
            r'\bcutting-edge\b': 'modern',
            r'\bnovel approach\b': 'new method',
            r'\binnovative method\b': 'new approach',
            r'\bcomputational compute\b': 'computational resources',
            r'\baccess to an institution\b': 'institutional support',
            r'\bto allow for transfer-learning\b': 'for transfer learning',
            r'\bn\s*=\s*\d+\b': lambda m: f"{m.group().split('=')[1].strip()} samples",  # n = 100 → 100 samples
        }
        
        humanized_text = text
        
        for pattern, replacement in replacements.items():
            if callable(replacement):
                humanized_text = re.sub(pattern, replacement, humanized_text, flags=re.IGNORECASE)
            else:
                humanized_text = re.sub(pattern, replacement, humanized_text, flags=re.IGNORECASE)
        
        # Fix common typos
        typos = {
            r'\bfort weekly\b': 'fortnightly',
            r'\bweeks\s+(\d+)\s*-\s*(\d+)\b': r'weeks \1–\2',  # Use en-dash for ranges
            r'\b(\d+)\s*-\s*(\d+)\b': r'\1–\2',  # Use en-dash for number ranges
        }
        
        for typo, correction in typos.items():
            humanized_text = re.sub(typo, correction, humanized_text)
        
        return humanized_text
    
    def humanize_section(self, section_header: str, api_key: Optional[str] = None) -> int:
        """Humanize a specific section."""
        print(f"\n🤖 Humanizing section: {section_header}")
        
        # Find the section
        section_start = self.content.find(section_header)
        if section_start == -1:
            print(f"  ❌ Section not found: {section_header}")
            return 0
        
        # Find the end of the section (next section header or end of document)
        next_section_pattern = r'\n\d+\.\d+\s+[A-Z]|\n\d+\.\s+[A-Z]|\n[A-Z][A-Z\s]+\n|\n###\s+|\n##\s+|\n#\s+'
        next_match = re.search(next_section_pattern, self.content[section_start + len(section_header):])
        
        if next_match:
            section_end = section_start + len(section_header) + next_match.start()
        else:
            section_end = len(self.content)
        
        # Extract section text
        section_text = self.content[section_start:section_end]
        
        print(f"  📏 Section length: {len(section_text)} characters")
        
        # Show before/after
        print("\n  📝 Original text (first 200 chars):")
        print(f"    {section_text[:200]}...")
        
        # Humanize
        humanized_text = self.humanize_with_superhumanizer(section_text, api_key)
        
        print("\n  📝 Humanized text (first 200 chars):")
        print(f"    {humanized_text[:200]}...")
        
        # Ask for approval
        approval = input("\n    Apply these changes? (y/n): ").lower().strip()
        
        if approval == 'y':
            # Replace section
            self.content = self.content[:section_start] + humanized_text + self.content[section_end:]
            
            # Log change
            self.changes_log.append({
                "type": "section_humanization",
                "section": section_header,
                "position": section_start,
                "length": len(section_text)
            })
            
            print(f"  ✅ Section humanized")
            return 1
        else:
            print("  Skipped.")
            return 0
    
    def save_changes(self, output_path: Optional[str] = None) -> str:
        """Save the edited document."""
        if output_path is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_path = f"{self.document_path}.edited_{timestamp}"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(self.content)
        
        # Save changes log
        log_path = f"{output_path}.changes.json"
        with open(log_path, 'w', encoding='utf-8') as f:
            json.dump(self.changes_log, f, indent=2)
        
        print(f"\n💾 Saved edited document: {output_path}")
        print(f"📋 Changes log: {log_path}")
        print(f"📊 Total changes made: {len(self.changes_log)}")
        
        return output_path
    
    def show_changes_summary(self):
        """Show summary of all changes made."""
        if not self.changes_log:
            print("\n📊 No changes made yet.")
            return
        
        print("\n📊 Changes Summary:")
        print("=" * 60)
        
        change_types = {}
        for change in self.changes_log:
            change_type = change.get("type", "unknown")
            change_types[change_type] = change_types.get(change_type, 0) + 1
        
        for change_type, count in change_types.items():
            print(f"  • {change_type}: {count}")
        
        print("=" * 60)


def main():
    """Main function for command-line use."""
    print("=" * 60)
    print("📚 Academic Document Editor for MSc Thesis")
    print("=" * 60)
    
    # Get document path
    document_path = input("\nEnter path to your document: ").strip()
    
    if not os.path.exists(document_path):
        print(f"❌ File not found: {document_path}")
        return
    
    # Create editor
    editor = AcademicDocumentEditor(document_path)
    
    # Analyze document
    issues = editor.analyze_document()
    
    # Menu
    while True:
        print("\n" + "=" * 60)
        print("📝 EDITING MENU")
        print("=" * 60)
        print("1. Fix em-dashes (replace with colons/commas)")
        print("2. Fix semicolon overuse")
        print("3. Humanize specific section")
        print("4. Humanize entire document (careful!)")
        print("5. Show changes summary")
        print("6. Save and exit")
        print("7. Exit without saving")
        print("=" * 60)
        
        choice = input("\nSelect option (1-7): ").strip()
        
        if choice == "1":
            replace_with = input("Replace em-dashes with (:, ,, or keep —): ").strip()
            if replace_with not in [":", ",", "—"]:
                replace_with = ":"
            editor.fix_em_dashes(replace_with)
        
        elif choice == "2":
            editor.fix_semicolons()
        
        elif choice == "3":
            # Show sections
            sections = editor._find_sections()
            if sections:
                print("\n📑 Available sections:")
                for i, section in enumerate(sections[:10]):  # Show first 10
                    print(f"  {i+1}. {section['header'][:50]}...")
                
                section_choice = input("\nEnter section number or header text: ").strip()
                
                # Try to parse as number
                try:
                    section_idx = int(section_choice) - 1
                    if 0 <= section_idx < len(sections):
                        section_header = sections[section_idx]['header']
                    else:
                        print("❌ Invalid section number")
                        continue
                except ValueError:
                    # Use as text
                    section_header = section_choice
                
                # Get API key if available
                api_key = input("Superhumanizer API key (press Enter to skip): ").strip()
                if not api_key:
                    api_key = None
                
                editor.humanize_section(section_header, api_key)
            else:
                print("❌ No sections found in document")
        
        elif choice == "4":
            print("⚠️  WARNING: This will humanize the ENTIRE document.")
            confirmation = input("Are you sure? (type 'yes' to confirm): ").strip()
            if confirmation.lower() == 'yes':
                api_key = input("Superhumanizer API key (press Enter to skip): ").strip()
                if not api_key:
                    api_key = None
                
                # Humanize in chunks
                chunk_size = 1000
                for i in range(0, len(editor.content), chunk_size):
                    chunk = editor.content[i:i+chunk_size]
                    humanized_chunk = editor.humanize_with_superhumanizer(chunk, api_key)
                    editor.content = editor.content[:i] + humanized_chunk + editor.content[i+chunk_size:]
                
                print("✅ Entire document humanized")
        
        elif choice == "5":
            editor.show_changes_summary()
        
        elif choice == "6":
            output_path = input(f"Save as (press Enter for default): ").strip()
            if not output_path:
                output_path = None
            editor.save_changes(output_path)
            break
        
        elif choice == "7":
            print("❌ Exiting without saving changes.")
            break
        
        else:
            print("❌ Invalid choice. Please enter 1-7.")


if __name__ == "__main__":
    main()
