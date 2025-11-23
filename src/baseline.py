"""
Baseline Module - Regex-based Extraction
Member 3: Data Scientist (Baseline)
File Ownership: src/baseline.py, src/evaluation.py

This file contains regex-based baseline for comparison with AI methods.
"""

import re
from typing import List, Dict


def get_regex_summary(text: str) -> Dict:
    """
    Extract summary using regex patterns (baseline approach)
    
    Args:
        text (str): Meeting transcription text
    
    Returns:
        dict: Summary data including action items found via regex
    
    TODO: Implement regex patterns for:
    - Action items (e.g., "TODO", "Action:", "@username will...")
    - Decisions (e.g., "We decided", "Agreed that")
    - Questions (e.g., "?", "Can we", "Should we")
    - Important phrases
    """
    
    action_items = extract_action_items_regex(text)
    decisions = extract_decisions_regex(text)
    questions = extract_questions_regex(text)
    
    return {
        'action_items': action_items,
        'decisions': decisions,
        'questions': questions,
        'method': 'regex_baseline'
    }


def extract_action_items_regex(text: str) -> List[str]:
    """
    Extract action items using regex patterns
    
    Args:
        text: Transcription text
    
    Returns:
        List of action items
    """
    # TODO: Implement regex patterns
    # Example patterns:
    # - "TODO: ..."
    # - "Action item: ..."
    # - "@person will ..."
    # - "We need to ..."
    
    patterns = [
        r'TODO:?\s*(.+?)(?:\n|$)',
        r'Action item:?\s*(.+?)(?:\n|$)',
        r'@\w+\s+will\s+(.+?)(?:\n|$)',
        r'We need to\s+(.+?)(?:\n|$)',
    ]
    
    action_items = []
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        action_items.extend(matches)
    
    return action_items


def extract_decisions_regex(text: str) -> List[str]:
    """Extract decisions using regex"""
    # TODO: Implement
    patterns = [
        r'We decided\s+(.+?)(?:\n|$)',
        r'Agreed that\s+(.+?)(?:\n|$)',
        r'Decision:?\s*(.+?)(?:\n|$)',
    ]
    
    decisions = []
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        decisions.extend(matches)
    
    return decisions


def extract_questions_regex(text: str) -> List[str]:
    """Extract questions using regex"""
    # TODO: Implement
    sentences = re.split(r'[.!?]\s+', text)
    questions = [s.strip() + '?' for s in sentences if '?' in s]
    
    return questions
